# 07. Relaxation

- Goal: run a geometry relaxation from the terminal with `mliprun`, read every file it leaves behind, tell a run that reached its force target from one that ran out of steps, relax a folder of structures in one command, check a relaxed structure against the site name on its folder, and assemble an adsorption energy whose every term was relaxed at the same settings
- Before you start: modules 00 to 06 finished; the `mlip-mace` environment active; Jupyter Lab started from the repository root, as step 12 of module 00 says; the kernel at the top right of the notebook reads "Python 3 (ipykernel)"
- Time to run the notebook: under 2 minutes (measured 98.7 s and 99.9 s on a `work/` folder that was empty, and 107.5 s and 76.2 s on re-runs over an existing one (the 76.2 s is the verification run of 2026-10-12), macOS on Apple Silicon; the first run of a session is slower while the model weights and the package caches are cold)
    - Ten relaxations run in it, through seven `mlip` commands: eight on a 28-atom cell, the Pt(1 1 1) slab with one O on it, one on the 27-atom clean slab, and one on the two-atom O2 box
    - One of them, `bridge`, runs to its 200-step ceiling and takes about 13 to 25 s of that on its own, measured in two executions; it is meant to, and raising the ceiling is the wrong response
    - The MACE-MP-0 weights, about 45 MB, were downloaded by step 10 of module 00 and sit in `~/.cache/mace/`, so this notebook downloads nothing
- Time to work through it: about 3 hours, reading every cell, changing a setting and running it again
- After this you can:
    - Relax one structure with `mlip optimize run --structure <file> --mlip mace --device cpu --fmax 0.05 --optimizer bfgs --max-steps 200`, and say what each of those options decides (canon `C1`, `C2`)
    - Name every file a relaxation writes, say which of them take their name from `--logfile` and which do not, and find the `converged` label in `mliprun_run.json`, where it sits in the last stage's `results` and not at the top level
    - Tell a converged run from one that hit its step ceiling, and say why the command's return code does not tell you (canon `K1`)
    - Read `opt_convergence.csv` into pandas, plot the energy and the force against the step, and say why the force panel wants a logarithmic axis
    - Say what a tighter `--fmax` buys and what it costs, and why every term of one energy difference has to share one target (canon `C4`)
    - Relax a whole folder with `mlip optimize batch --parent <folder> --input-name POSCAR --mlip mace --device cpu --fmax 0.05 --optimizer bfgs --max-steps 200`, and read `batch_summary.csv`, including the `steps` column this version never fills and the `detail` column that stays empty only while nothing is skipped and nothing fails
    - Check a relaxed adsorbate against its own geometry and catch a structure that left the site it was placed on (canon `A1`)
    - Assemble `E_ads = E(slab+O) − E(slab) − ½ E(O2)` from relaxed energies, and say why a converged positive `E_ads` is a statement about one site and one reference rather than about whether the adsorbate binds
- Files: `relaxation.ipynb`; every command writes into `work/`, one folder per relaxation, and `work/` is not committed
- Needs `../../scripts/onboarding_structures.py`
