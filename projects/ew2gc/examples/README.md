# Examples copied from the project

- These files are copies of the project's own working files, with a provenance header added to the top of each one: where it came from, the date it was copied, the date the original was last changed and the SHA-256 of the original
    - SHA-256 is a fingerprint of a file: if the original changes by one character, its fingerprint changes
    - They are dated snapshots, and the project's file is always the authoritative one; ask Juan for the current one before a project calculation
    - The files were copied on 2026-10-12
- They are for reading, and the capstone runs one script, `gen_rs_slabs.py`, which imports `gen_slabs.py` and, through it, the stand-in `generate_slabs.py`
    - Paths such as `/scratchb/juar/...` inside them are the project's own folders on its GPU computer and they will not exist on your computer; they are part of the copied text and were not changed
    - `gen_slabs_sharable.py`, an earlier script of the project, is not copied, because the route it belongs to, `tasker_flip`, has been replaced by the symmetric slabs of `E-p2` in `DECISIONS.md`

## `gen_rs_slabs.py`

- What it is: the project's script that cleaves a surface into symmetric slabs, one slab for every distinct face, and writes an audit table with one row per face
    - It was last changed on 2026-10-12 and it is under active development; this copy is the file as it stood at 18:22 that day
- What to look at
    - The docstring at the top: why the unit is the face and not the cleavage, and the five steps of the algorithm
    - `MATERIAL_DEFAULTS` and `PMG_MAX_VERSION`: the settings per material that the script takes from the project's canon `S1`, and the pymatgen version above which it prints the warning that the capstone shows
    - `AUDIT_COLUMNS` and the `main` function: the columns of the audit table, and the return code, which is 0 when every face it built is ok, or in a dry run, and 1 otherwise
    - The capstone runs it from this folder with `--skip-prod-map`, which leaves out a comparison with the labels of the project's earlier production slabs

## `gen_slabs.py`

- What it is: the project's earlier slab script, which `gen_rs_slabs.py` imports four functions from: `compute_supercell_mult`, `measure_z_extent`, `orthogonalize_structure` and `slabs_for_target`
    - Most of the file is the `tasker_flip` route that `E-p2` replaced, and it is kept here only because the script above needs it to run
- What to look at
    - `compute_supercell_mult` and its docstring: how the in-plane cell is repeated until it meets the smallest vector of canon `S6` and the area asked for
    - The first lines of the `tasker_flip` description in its docstring, to see what the project did before `E-p2`

## `generate_slabs.py`

- What it is: a stand-in that was written for this repository and is not a project file
    - `gen_slabs.py` begins with `import generate_slabs`, a module of the group's `compcatalysis-skills` repository that the script looks for at a fixed folder on the supervisor's computer, so on any other computer the import fails before anything runs
    - The stand-in has the one function that `gen_rs_slabs.py` can reach through `gen_slabs.py`, `filter_unique_top_surfaces`, and that function stops with an error if it is called; `gen_slabs.py` also uses `apply_selective_dynamics` from the real module, in `write_slab_with_constraints`, which `gen_rs_slabs.py` does not import
- What to look at
    - The docstring: `gen_rs_slabs.py` calls that function only without `--skip-prod-map`, and the capstone uses `--skip-prod-map`, so the stand-in is never called there
    - To map faces to the project's production labels, use the real module from `compcatalysis-skills`, not this file

## `queue_optimize_excerpt.yaml`

- What it is: the first part of a queue file of the project, a list of jobs for the project's job runner, which asks for a GPU (`gpu_required: true`), and the jobs are relaxations of vacuum slabs of Co3O4 of the earlier `tasker_flip` production
    - It holds the `defaults` block, the first two jobs of the original, both with `chgnet`, and then the first job of the original that carries `--uma-task oc25`, which is the third job here; the header of the file says so
    - It teaches the format of a queue file, and not the way the project builds slabs now: `f0A` and `f0B` are the two members of one cleavage in the `tasker_flip` pairs
- What to look at
    - Every model is named: `--mlip chgnet` in the first two jobs and `--mlip uma-s-1p2 --uma-task oc25` in the third, canon `C1`, with nothing left to a default
    - `--fmax '0.05'`, `--optimizer bfgs` and `--max-steps '300'` are written out in each job, canon `C2`
    - The first item of `cmd` is the full path of the `mlip` of one environment, and the two models use two different environments (`.venv/chgnet` and `.venv/uma`), which is the one-model-per-environment rule of module 00 in practice
    - `completion_check` names a file, here `opt_final.vasp`, and `output_dir` is the folder the job writes into, which is the folder of its structure file, as module 07 showed

## `queue_md_excerpt.yaml`

- What it is: the head of the project's queue for the slab-plus-water stage, with its first job, an MD run of a Co3O4 slab with water, written in the same style as the other queue
    - It was last changed on 2026-07-25, before the symmetric slabs of `E-p2`, and the structure it runs is in a folder of the project that is not copied
- What to look at
    - The MD flags that match canon `C5`: `nvt`, `langevin`, `--temperature 300`, `--friction 0.01`, `--timestep 0.5`, and `--steps 350000`, which is 175 ps at 0.5 fs and is the total of `C5`
    - `--mlip uma-s-1p2 --uma-task oc25` is written out here too, canon `C1`
    - `completion_check` of the type `md_steps_reached` with a target of 350000 steps, and `resumable_md: true`: the job runner that reads these keys is not in this repository, so what it does with them is the project's; compare module 10, where continuing a run takes the flag `--resume`
