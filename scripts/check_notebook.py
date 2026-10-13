#!/usr/bin/env python3
"""Check an onboarding notebook against the house rules. Exit 1 on any failure."""
import re, sys
from pathlib import Path
import nbformat

CANON_DIRS = ("modules/06-", "modules/07-", "modules/08-", "modules/09-", "modules/10-", "capstone")
# Three spellings of "let the tool pick the model": the shell flag, the keyword argument,
# and the subprocess argument list (`"--mlip", "auto"`) that the contract uses.
AUTO = re.compile(r"""--mlip auto|mlip\s*=\s*["']auto["']|--mlip["']\s*,\s*["']auto["']""")
LABEL_VALUE = re.compile(r"""print\(f?["'][^"'\n]*:\s*\{""")
# A markdown line may be a heading, a bullet, a numbered item, a table row, a quote,
# an HTML tag, or a continuation of the line above (indented by two or more spaces).
LINE_OK = re.compile(r"^( {2,}|#|-|\*|\d+\.|\||>|<)")

def check(path: Path) -> list[str]:
    fails = []
    nb = nbformat.read(path, as_version=4)
    try:
        nbformat.validate(nb)
    except nbformat.ValidationError as e:
        fails.append(f"nbformat: {e}")
    if nb.metadata.get("kernelspec", {}).get("name") != "python3":
        fails.append("kernelspec: name must be python3")
    cells = nb.cells
    if not cells or cells[0].cell_type != "markdown" or not cells[0].source.startswith("# "):
        fails.append("first cell: must be a markdown title starting with '# '")
    for i, c in enumerate(cells):
        src = c.source
        m = AUTO.search(src)
        if m:
            fails.append(f"cell {i}: '--mlip auto' is banned, name the model (found {m.group(0)!r})")
        if c.cell_type == "markdown" and "$$" in src:
            fails.append(f"cell {i}: display math $$ is banned, use backticks")
        if c.cell_type == "code" and LABEL_VALUE.search(src):
            fails.append(f"cell {i}: label and value printed on one line, split them")
        if c.cell_type == "markdown":
            fenced = False
            for ln in src.splitlines():
                if ln.strip().startswith("```"):
                    fenced = not fenced
                    continue
                if fenced or not ln.strip():
                    continue
                if not LINE_OK.match(ln):
                    fails.append(f"cell {i}: prose line must be a heading or bullet: {ln[:60]!r}")
                    break
    p = str(path)
    if any(k in p for k in CANON_DIRS):
        if not any(c.cell_type == "markdown" and "### Before you run this for a project" in c.source for c in cells):
            fails.append("canon: missing '### Before you run this for a project' section")
    mds = [c for c in cells if c.cell_type == "markdown"]
    if not mds or "## Check yourself" not in mds[-1].source or "<details>" not in mds[-1].source:
        fails.append("ending: last markdown cell must be '## Check yourself' with a <details> answer block")
    return fails

def main(argv):
    bad = 0
    for arg in argv:
        fails = check(Path(arg))
        for f in fails:
            print(f"{arg}: {f}")
        bad += bool(fails)
    print(f"{len(argv) - bad} of {len(argv)} notebooks pass")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
