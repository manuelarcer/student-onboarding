# Verification run of 2026-10-12

This page records one full execution of every notebook in the repository, in the verification environment, by `scripts/verify_all.sh`. How to repeat it is in `docs/maintainers.md`, "How to re-verify everything".

## What was run

- Command: `VENV=~/venv/onboarding-mace bash scripts/verify_all.sh`, from the repository root, with `MPLCONFIGDIR` set to a scratch folder
- The script first lints the 11 notebooks (`scripts/check_notebook.py`, 11 of 11 pass), then executes each one in its own folder with `jupyter nbconvert --to notebook --execute --inplace`, in the order of the table, and stops at the first failure; it did not stop
- Start 19:48:33, end 19:56:16 (+08), so 463 s of wall time for the script; the sum of the `real` times below is 462.2 s
- Load average (1, 5 and 15 minutes) at the start: 3.12, 3.65, 4.31; at the end: 6.37, 5.78, 5.02. The Mac was shared with other sessions, so read the times as an upper range
- Two executions were repeated after the script, and the table shows both
    - Module 03: `MP_API_KEY` was not exported in the shell that ran the script, so the script's execution took the no-key path of the notebook (3.70 s). `scripts/verify_all.sh` now stops before any execution when `MP_API_KEY` is not set, with the message "export MP_API_KEY first; module 03 needs it", so this cannot happen silently again. The notebook was executed again by itself with the key exported, which took the database path (19.86 s), and that is the execution whose outputs are in the repository
    - Capstone: one code cell (the figure of the slab with `*OH`) was changed after the script's execution, so the notebook was executed again by itself (158.97 s), and that is the execution whose outputs are in the repository
- Every notebook before this run had been executed on its own during the build; this is the first run of all of them in one go on the final text

## Result

| notebook | wall time (s) | passed |
|---|---|---|
| `modules/01-python-for-atoms/python_for_atoms.ipynb` | 3.26 | yes |
| `modules/02-ase-basics/ase_basics.ipynb` | 5.62 | yes |
| `modules/03-bulk-and-mp/bulk_and_mp.ipynb` | 3.70 in the script, no key; 19.86 on the repeat, with a key | yes, both |
| `modules/04-slabs/slabs.ipynb` | 5.37 | yes |
| `modules/05-adsorbates/adsorbates.ipynb` | 4.84 | yes |
| `modules/06-single-point/single_point.ipynb` | 12.09 | yes |
| `modules/07-relaxation/relaxation.ipynb` | 76.23 | yes |
| `modules/08-frequencies/frequencies.ipynb` | 27.44 | yes |
| `modules/09-neb/neb.ipynb` | 39.25 | yes |
| `modules/10-md/md.ipynb` | 135.63 | yes |
| `projects/ew2gc/capstone.ipynb` | 148.76 in the script; 158.97 on the repeat | yes, both |

- Notebooks passed: 11 of 11
- Load average at the start and end of the two repeats: module 03 with the key 4.47 to 4.06; capstone 3.83 to 4.40

## What changed in the text because of the run

- Markdown that quotes a number was compared with the new outputs, notebook by notebook, and edited where the two no longer matched: modules 07 and 10 and the capstone (the `fix:` commit before this one); module 03 and the other notebooks printed the same quoted values
- Qualitative results are the same as before: the main MD run still heats from about 300 K to above 500 K, all four 2.0 fs runs still blow up, the bridge site of module 07 still does not converge with `bfgs`, and every capstone term still converged
- Two numbers vary from run to run and are expected to: the MD temperatures (no seed is given to the command) and the final energy of the slab with `*OH` (45, 48 and 50 steps; the three energies differ in the third decimal)

## Versions

From `~/venv/onboarding-mace/bin/pip list`:

| package | version |
|---|---|
| torch | 2.14.0 |
| mace-torch | 0.3.16 |
| ase | 3.29.0 |
| pymatgen | 2026.5.4 |
| pymatgen-core | 2026.8.30 (the package that provides `pymatgen.core`, so `pymatgen.core.__version__` prints this number, and the capstone quotes it) |
| mp-api | 0.46.5 |
| mliprun | 0.4.0 (editable install from `~/venv/onboarding-mace-src/mliprun`) |
| jupyterlab | 4.6.3 |
| nbconvert | 7.17.1 |
| ipykernel | 7.3.0 |
| numpy | 2.4.6 |
| pandas | 3.0.5 |
| matplotlib | 3.11.2 |

- Python 3.11.10
- Export: Quarto 1.7.31 and pandoc 3.9 (`docs/export.md`)

## Machine

- macOS 27.0.1 (build 26A434), from `sw_vers`
- Chip: Apple M3, 8 cores, 16 GB of memory (`sysctl -n machdep.cpu.brand_string`, `hw.ncpu`, `hw.memsize`)
- Device used by every calculation: `cpu`; the MACE-MP-0 weights were already in `~/.cache/mace/`

## Not executed

- Windows: the Windows variants of module 00
- Linux: the Linux variants of module 00
- ASPIRE2A: module 11 and its files (`job_cpu.pbs`, `job_gpu.pbs`, `setup_env_aspire2a.sh`); the login host and the Python module name there are marked "confirm" in the text
- Module 00 on macOS was executed on 2026-09-17 by rebuilding the environment from its text, not in this run
- No GPU execution of any notebook
