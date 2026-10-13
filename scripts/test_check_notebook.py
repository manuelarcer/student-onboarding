# scripts/test_check_notebook.py
import subprocess, sys
from pathlib import Path
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

HERE = Path(__file__).parent
CHECK = HERE / "check_notebook.py"
META = {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}

def write(path, cells):
    nb = new_notebook(cells=cells, metadata=META)
    nbformat.write(nb, path)

def run(path):
    return subprocess.run([sys.executable, str(CHECK), str(path)], capture_output=True, text=True)

GOOD_END = new_markdown_cell("## Check yourself\n\n1. Why?\n\n<details>\n<summary>Answers</summary>\n\n- Because\n\n</details>")

def test_good_notebook_passes(tmp_path):
    p = tmp_path / "modules" / "02-x" / "ok.ipynb"
    p.parent.mkdir(parents=True)
    write(p, [new_markdown_cell("# Title\n\n- one clause"),
              new_code_cell("print('Number of atoms')\nprint(3)"), GOOD_END])
    r = run(p)
    assert r.returncode == 0, r.stdout + r.stderr

def test_mlip_auto_fails(tmp_path):
    p = tmp_path / "bad.ipynb"
    write(p, [new_markdown_cell("# T"), new_code_cell("cmd = ['mlip', '--mlip', 'auto']  # --mlip auto"), GOOD_END])
    r = run(p)
    assert r.returncode == 1 and "mlip auto" in r.stdout

# Rule 3, argument-list spelling: the contract runs mliprun from a Python list, so the
# likely real violation is `"--mlip", "auto"` with no `--mlip auto` substring anywhere.
def test_mlip_auto_in_argument_list_fails(tmp_path):
    p = tmp_path / "bad.ipynb"
    write(p, [new_markdown_cell("# T"),
              new_code_cell('cmd = [str(MLIP), "optimize", "run", "--mlip", "auto"]'), GOOD_END])
    r = run(p)
    assert r.returncode == 1 and "auto" in r.stdout

def test_mlip_mace_in_argument_list_passes(tmp_path):
    p = tmp_path / "ok.ipynb"
    write(p, [new_markdown_cell("# T"),
              new_code_cell('cmd = [str(MLIP), "optimize", "run", "--mlip", "mace"]'), GOOD_END])
    r = run(p)
    assert r.returncode == 0, r.stdout + r.stderr

def test_missing_canon_box_fails(tmp_path):
    p = tmp_path / "modules" / "07-relaxation" / "relaxation.ipynb"
    p.parent.mkdir(parents=True)
    write(p, [new_markdown_cell("# T"), new_code_cell("pass"), GOOD_END])
    r = run(p)
    assert r.returncode == 1 and "Before you run this for a project" in r.stdout

def test_inline_label_value_print_fails(tmp_path):
    p = tmp_path / "bad.ipynb"
    write(p, [new_markdown_cell("# T"), new_code_cell('print(f"Atoms: {n}")'), GOOD_END])
    r = run(p)
    assert r.returncode == 1 and "label" in r.stdout.lower()

def test_prose_paragraph_fails(tmp_path):
    p = tmp_path / "bad.ipynb"
    write(p, [new_markdown_cell("# T\n\nThis is a paragraph of prose."), new_code_cell("pass"), GOOD_END])
    r = run(p)
    assert r.returncode == 1 and "bullet" in r.stdout.lower()

# Rule 8, fenced code: a prose line inside a fenced block is not checked.
# The opener carries a language tag and the closer does not, so both spellings
# must toggle the fence.
def test_prose_line_inside_fenced_block_passes(tmp_path):
    p = tmp_path / "ok.ipynb"
    write(p, [new_markdown_cell("# T\n\n- run this in a terminal\n\n```python\n"
                                "this line looks like prose but sits inside a fence\n```"),
              new_code_cell("pass"), GOOD_END])
    r = run(p)
    assert r.returncode == 0, r.stdout + r.stderr

# Rule 8, continuation: a bullet wrapped onto a second line indented by two spaces
# is a continuation, not a prose paragraph (ruling: option 1).
def test_two_space_continuation_line_passes(tmp_path):
    p = tmp_path / "ok.ipynb"
    write(p, [new_markdown_cell("# T\n\n- In a project, the items below are decided by your supervisor and written in the\n"
                                "  project's `CANON.md`; they are never taken from a tool default"),
              new_code_cell("pass"), GOOD_END])
    r = run(p)
    assert r.returncode == 0, r.stdout + r.stderr

# Smoke test: the contract's two verbatim shapes, in a notebook under a canon directory.
CONTRACT_CANON = """### Before you run this for a project

- The values in this notebook are teaching values, chosen so it runs on a laptop in minutes
- In a project, the items below are decided by your supervisor and written in the
  project's `CANON.md`; they are never taken from a tool default
    - `C1` MLIP model and head: this notebook uses `mace` (MACE-MP-0); the project may use another
    - `C2` force convergence `fmax`: this notebook uses 0.05 eV/Å
    - ...one sub-bullet per ID in the spec's table for this module...
- If a value is not recorded, ask before running; the tool will not stop you"""

CONTRACT_CHECK_YOURSELF = """## Check yourself

1. <question>
2. <question>
3. <question>

<details>
<summary>Answers</summary>

- <answer 1>
- <answer 2>
- <answer 3>

</details>"""

def test_contract_shapes_pass_under_canon_dir(tmp_path):
    p = tmp_path / "modules" / "07-relaxation" / "relaxation.ipynb"
    p.parent.mkdir(parents=True)
    write(p, [new_markdown_cell("# Title\n\n- one clause"),
              new_markdown_cell(CONTRACT_CANON),
              new_code_cell("pass"),
              new_markdown_cell(CONTRACT_CHECK_YOURSELF)])
    r = run(p)
    assert r.returncode == 0, r.stdout + r.stderr
