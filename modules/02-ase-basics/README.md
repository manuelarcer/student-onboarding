# 02. ASE basics

- Goal: the `Atoms` object and everything the later modules do with it by hand, taught on the Pt crystal and a water molecule
- Before you start: module 00 and module 01 finished; the `mlip-mace` environment active; Jupyter Lab started from the repository root, as step 12 of module 00 says; the kernel at the top right of the notebook reads "Python 3 (ipykernel)"
- Time to run the notebook: under 1 minute (measured 6 s on a quiet machine, 5.6 s in the verification run of 2026-10-12, and 16 s once while the machine was busy, macOS on Apple Silicon)
- Time to work through it: about 3 hours, reading every cell, changing a value in it and running it again
- After this you can:
    - Read a structure file in any of the four formats of this course, change it and write it back in the format the next tool needs
    - Look at a structure before you calculate with it, in `ase gui` from a terminal or as a picture inside a notebook
    - Move atoms, turn a fragment, build a supercell that follows canon `S6`, fix atoms for a relaxation, and measure a distance with the minimum image convention
- Files: `ase_basics.ipynb`, outputs go to `work/`
- Needs `../../structures/Pt_bulk_fcc.vasp`; the water molecule comes from ASE itself
