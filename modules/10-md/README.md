# 10. Molecular dynamics

- Goal: run a short molecular dynamics run, MD, from the terminal with `mliprun` on a Pt(1 1 1) slab with six water molecules above it, read the two files it writes, tell a run whose temperature stays bounded from a run that blows up, continue a run with `--resume`, and say which settings of an MD are decisions of the project and not defaults
- Before you start: modules 00 to 09 finished; the `mlip-mace` environment active; Jupyter Lab started from the repository root, as step 12 of module 00 says; the kernel at the top right of the notebook reads "Python 3 (ipykernel)"
- Time to run the notebook: about 2.5 minutes, 136 to 146 s over five executions of the notebook (measured 143.0, 145.8, 138.8, 139.5 and 135.6 s, the last in the verification run of 2026-10-12, macOS on Apple Silicon, with the model weights and the package caches already warm; a first run on a cold machine is slower, an effect module 06's README measures on its own notebook)
    - Seven `mlip` commands run in it, all of them `mlip md run` on a 45-atom structure: the main run of 400 steps of 0.5 fs, 43.7 to 48.5 s over the five executions; four runs of 100 steps of 2.0 fs, of which the notebook times the first, 14.2 to 15.0 s; one resume of 200 steps, 24.1 to 27.2 s; and one resume of 20 steps on a copy, 6.7 to 7.2 s
    - The machine was shared with other sessions during these executions, with a load average of 3.1 to 7 at the start and the end of each of the five executions, so read the times as an upper range and not as what an idle laptop gives
    - The MACE-MP-0 weights, about 45 MB, were downloaded by step 10 of module 00 and sit in `~/.cache/mace/`, so this notebook downloads nothing
- Time to work through it: about 3 hours, reading every cell, changing a setting and running it again
- After this you can:
    - Build a Pt(1 1 1) slab with water molecules above it at random orientations from a fixed seed, check that no two molecules overlap, and write it as a `POSCAR`
    - Run `mlip md run --structure work/md/POSCAR --mlip mace --ensemble nvt --thermostat langevin --temperature 300 --friction 0.01 --timestep 0.5 --steps 400 --log-interval 10 --traj-interval 20 --device cpu` and say where its files go, which is next to the structure and not into the folder the command is started from (canon `C1`, `C5`)
    - Read `md_energy.csv` and `md.traj`, take block means of the temperature and the potential energy, and say why a run whose block means drift, as the block means of the temperature do in the saved run, from 368.5 K to 553.5 K, has not settled
    - Run the same system at `--timestep 2.0`, and say why a return code of 0 and a `status` of `converged` in `mliprun_run.json` say nothing about whether an MD run is usable
    - Continue a run with `--resume --steps 200`, say that `--steps` is additional on top of the earlier run, and say that every other flag takes its default when it is left out, which includes a timestep of 1.0 fs
    - Say which settings canon `C5` leaves to the project, and that the project's recorded protocol is 175 ps in total, 50 ps of equilibration and 125 ps of production, which is 875 times the 0.2 ps of this notebook
- Files: `md.ipynb`; the runs write into `work/md/`, `work/md_dt2/`, `work/md_dt2_b/`, `work/md_dt2_c/`, `work/md_dt2_d/` and `work/md_resume_check/`, and `work/` is not committed
- Needs `../../scripts/onboarding_structures.py`
