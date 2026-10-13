# Maintainer notes

Notes for whoever maintains this repository. Students do not need this file.

## Layout

- `modules/NN-name/`: one lesson each. A `README.md` with the six-bullet shape below and, except for the text-only modules 00 and 11, one notebook. Files a notebook writes go to `work/` inside its module folder; `work/` is ignored by git.
- `projects/<name>/`: one research project each: background, recorded decisions, real example files, a capstone notebook.
- `paths/`: one file per student or project, giving the order of the modules and the weekly plan.
- `structures/`: small input structures the notebooks read by relative path (`../../structures/...`).
- `scripts/`: helper code shared by the notebooks (`onboarding_structures.py`), the script that fetches bulk structures from the Materials Project (`fetch_bulk.py`), the notebook linter (`check_notebook.py`), the verification script (`verify_all.sh`) and the two test files (`test_check_notebook.py`, `test_onboarding_structures.py`).
- `docs/`: this file, the design and plan, and one `verification-<date>.md` per full verification run.

## The verification environment

- Where it lives: `~/venv/onboarding-mace` on the maintainer's Mac. Every notebook in this repository was executed with it, and `scripts/verify_all.sh` uses it by default.
- How it was built: by following `modules/00-setup/README.md` literally, with two substitutions only: `~/venv/onboarding-mace` in place of `~/mlip/mlip-mace`, and `~/venv/onboarding-mace-src/` in place of `~/mlip` for the `mliprun` clone, so the clone lives at `~/venv/onboarding-mace-src/mliprun`. That is the standing location; do not move it. Every other command was run as written. The module text is the specification: if a command in it fails during a rebuild, fix the text first, then continue from that step.
- Editable install: `mliprun` is installed with `pip install -e`, so the venv reads the code from the cloned folder. `pip show mliprun` prints that folder under `Editable project location`. If the folder is deleted, `mlip` stops working. The venv does not need a rebuild for that: clone `mliprun` again into `~/venv/onboarding-mace-src/mliprun`, then run `~/venv/onboarding-mace/bin/pip install -e ".[neb]"` from inside that folder, and check with `~/venv/onboarding-mace/bin/pip show mliprun` and `~/venv/onboarding-mace/bin/mlip doctor`.
- When to rebuild: a change in `mliprun` that a module depends on, a new `mace-torch` or `torch` release you want the students to get, or a new Python version. Rebuild means: remove the folder (`rm -rf ~/venv/onboarding-mace`), follow module 00 again with the two substitutions, then re-verify everything (below). Record the date and the package versions in a new `docs/verification-<date>.md`.

## How to add a module

1. Create `modules/NN-name/` with `README.md` in this shape:

    ```markdown
    # NN. <Title>

    - Goal: <one line>
    - Before you start: <modules completed, files needed>
    - Time to run the notebook: <minutes, measured>
    - Time to work through it: <hours>
    - After this you can: <two or three bullets>
    - Files: `<name>.ipynb`, outputs go to `work/`
    ```

2. Write the notebook with a builder script: a short Python script that assembles the cells with `nbformat` and writes `name.ipynb`. The builders live in `.superpowers/sdd/2026-09-17-onboarding-repo/builders/` inside the checkout. That folder is ignored by git, so the builders exist only on the maintainer's Mac, and `git clean -fdx` destroys them. Modules 01, 04 to 10 and the capstone have a builder; modules 02 and 03 have none and are edited directly in the notebook. Run a builder with `~/venv/onboarding-mace/bin/python`. Building from a script keeps every cell as plain text you can edit and compare between versions; the notebook file is the product, not the source. After a text-only change, merge the new markdown cells into the executed notebook instead of re-executing it, and check that every code cell is unchanged.
3. Follow the notebook rules. Markdown cells are a heading plus nested bullets, never prose paragraphs, and no `$$` maths. Printed output is a label line and then the bare value, with the unit in the label (`print("Cell vector a (Å)")` then `print(round(a, 3))`), never `print(f"a: {a}")`. Every `mlip` command and every `setup_calculator` call names the model explicitly (`--mlip mace`, `mlip="mace"`). Calculation notebooks (modules 06 to 10 and every capstone) open with a section `### Before you run this for a project` listing the canon IDs they touch, with "if a value is not recorded, ask before running". The last markdown cell is `## Check yourself` with the answers in a `<details>` block. The kernel name is `python3`. Figures follow the group's plot style.
4. Lint it: `~/venv/onboarding-mace/bin/python scripts/check_notebook.py modules/NN-name/name.ipynb`. Exit code 0 means every rule passes; otherwise it prints one line per failure as `<file>: <rule>: <detail>`. The rules are the ones in step 3 plus notebook validity; they are listed at the top of `scripts/check_notebook.py`.
5. Execute it headless, from the module folder so that `work/` and `../../structures` resolve:

    ```bash
    cd modules/NN-name
    MPLCONFIGDIR=${TMPDIR:-/tmp}/mpl /usr/bin/time -p ~/venv/onboarding-mace/bin/jupyter nbconvert \
      --to notebook --execute --inplace \
      --ExecutePreprocessor.timeout=1800 \
      --ExecutePreprocessor.kernel_name=python3 name.ipynb
    ```

    `/usr/bin/time -p` prints `real <seconds>` at the end. Write that number into the README under "Time to run the notebook" in seconds, with a rounded headline in minutes in front of it, and when the notebook was run several times give the range over those runs, as the existing READMEs do. A notebook that takes more than 10 minutes on CPU is too large: reduce the system size, the number of steps or the number of model calls.
6. Commit the executed notebook (with its text outputs and figures, so the reader sees what to expect), the README, and any new file in `structures/` or `scripts/`. Never commit `work/`, `.traj` files, model weights (`.model`) or `.ipynb_checkpoints/`; all four are in `.gitignore`.
7. Add the module to the table in the top `README.md` and to the week table of the relevant file in `paths/`.

## How to add a project track

Create `projects/<name>/` with four items:

- `README.md`: the project in one page: what it studies, which work package, where the onboarding deck and the reading list are.
- `DECISIONS.md`: a dated copy of the decisions recorded in the project's `CANON.md`, one entry per canon ID. Copy only what is recorded there. Every other canon ID is written as "not recorded, ask <supervisor> before running". Never fill a gap with a tool default or with a value from another project; a wrong default changes the level of theory silently.
- `examples/`: real input files from the project (a structure generator, a queue file, a job script), each with a short note saying where it came from and on which date.
- `capstone.ipynb`: one notebook that applies the modules to the project's own material. Build, lint and execute it exactly like a module (steps 2 to 6 above), including the canon section.

## How to add a path

Create `paths/<student-or-project>.md` with: who the path is for (course code, duration, hours per week, what the student is not expected to know); a week table (weeks, modules, hours, using the measured times from the module READMEs); the reading-list items that pair with each module; what to bring to the weekly meeting (the notebook that was run, one number the student does not trust, one question); how to report a result (model and head, `fmax`, converged or not, reference used, value with unit); report deadlines and format.

## How to re-verify everything

From the repository root, with the verification venv built and the Materials Project key exported (module 03 needs it; the script stops before running anything if `MP_API_KEY` is not set):

```bash
cd ~/github/work/student-onboarding
export MP_API_KEY=<your Materials Project key>    # export MP_API_KEY first; module 03 needs it
VENV=~/venv/onboarding-mace bash scripts/verify_all.sh
```

The script lints every notebook, then executes each one in order inside its own folder, and stops at the first failure. It prints `real <seconds>` after each notebook. Record the times and the package versions (`~/venv/onboarding-mace/bin/pip list`, the rows for torch, mace-torch, ase, mliprun, pymatgen, mp-api and jupyterlab) in a new `docs/verification-<date>.md`, and update "Time to run the notebook" in every README whose time changed.

Re-verify after any of these: a venv rebuild, a change to `scripts/onboarding_structures.py`, a change to any notebook, a new `mliprun` version.

Two things the script does not cover. Module 00 is verified by rebuilding the venv from its text (section above). The Windows and Linux variants of module 00, and module 11 (ASPIRE2A), have never been executed by the author; the top README says so, and a student's report of a failing step there is the only test they get.
