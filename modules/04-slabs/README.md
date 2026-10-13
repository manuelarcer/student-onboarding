# 04. Slabs

- Goal: what a slab is and how to build one, with the nine canon items that decide every choice named as you meet them
- Before you start: modules 00 to 03 finished; the `mlip-mace` environment active; Jupyter Lab started from the repository root, as step 12 of module 00 says; the kernel at the top right of the notebook reads "Python 3 (ipykernel)"
- Time to run the notebook: under 1 minute (measured 7 s on a quiet machine and 5.4 s in the verification run of 2026-10-12, macOS on Apple Silicon; the first run of a session is slower while the package caches are cold, and a busy machine can stretch it to a couple of minutes)
- Time to work through it: about 4 hours, reading every cell, changing a value in it and running it again
- After this you can:
    - Build a metal slab with `ase.build.fcc111`, and cut any Miller index out of any crystal with pymatgen's `SlabGenerator`
    - Count the layers of a slab from its coordinates instead of trusting the argument you gave the builder, and say why the count needs a definition (canon `S2`)
    - List the terminations of an oxide surface, read `is_symmetric()` and `is_polar()` correctly, and say what a polar surface costs you
    - Size a cell in plane so that it clears the 7.5 Å minimum of canon `S6`, freeze the bottom layers for a relaxation, and check the frozen set in the file that was written
- Files: `slabs.ipynb`, outputs go to `work/`
- Needs `../../structures/Pt_bulk_fcc.vasp` and `../../structures/Co3O4_mp-18748.vasp`
