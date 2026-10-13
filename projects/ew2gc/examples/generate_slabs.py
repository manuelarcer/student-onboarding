"""Stand-in written for the onboarding repository. This is NOT a project file.

Why it exists
-------------
`gen_slabs.py` begins with `import generate_slabs as gs`, a module of the group's
`compcatalysis-skills` repository that `gen_slabs.py` looks for at a fixed folder on
the supervisor's computer. On any other computer that import fails before anything
else runs, and `gen_rs_slabs.py` imports `gen_slabs.py`.

What it does
------------
`gen_slabs.py` uses two functions of the real module: `gs.filter_unique_top_surfaces`,
in `slabs_for_target`, and `gs.apply_selective_dynamics`, in `write_slab_with_constraints`,
which `gen_rs_slabs.py` does not import. Only the first is reachable from
`gen_rs_slabs.py`, and only through `slabs_for_target`. `gen_rs_slabs.py` calls `slabs_for_target` only when it is run
without `--skip-prod-map` (it maps the new faces to the labels of the earlier
production slabs). With `--skip-prod-map`, as the capstone runs it, the function below
is never called. If it is called, it stops with an error and does not guess.

To map faces to production labels, use the real module from the group's
`compcatalysis-skills` repository instead of this file.
"""


def filter_unique_top_surfaces(slabs):
    raise NotImplementedError(
        "This is the stand-in generate_slabs.py of the onboarding repository. "
        "Run gen_rs_slabs.py with --skip-prod-map, or use the real module from "
        "compcatalysis-skills.")
