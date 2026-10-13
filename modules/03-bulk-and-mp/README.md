# 03. Bulk structures and the Materials Project

- Goal: where the bulk crystal at the start of every surface calculation comes from, how to read its symmetry, and how to choose among the entries a database offers
- Before you start: modules 00, 01 and 02 finished; the `mlip-mace` environment active; Jupyter Lab started from the repository root, as step 12 of module 00 says; the kernel at the top right of the notebook reads "Python 3 (ipykernel)"
    - A Materials Project key is optional for running the notebook: it runs from top to bottom without one, on the files already in `structures/`
    - The key is what makes the two database sections do anything live; without it they fall back to `../../structures/Co3O4_mp-18748.vasp` and print the command you would have run
    - The notebook section "Get your own Materials Project key" tells you how to get one and where to store it, for macOS, Linux and Windows
- Time to run the notebook: under 1 minute (measured 21 s and 19.9 s with a key and 5 s and 3.7 s without one, the second number of each pair from the verification run of 2026-10-12, macOS on Apple Silicon; the difference is the three queries to the database)
- Time to work through it: about 2 hours, reading every cell, changing a value in it and running it again
- After this you can:
    - Read a bulk structure file, report its formula, space group and lattice parameters, and move it between ASE and pymatgen
    - Choose between the primitive and the conventional cell, and say which one a slab is cut from and why
    - Query the Materials Project with your own key, read an energy above hull, and say why the lowest entry is not automatically the right one
    - Check whether two entries with different space-group symbols are really two different structures, before you treat them as two phases
- Files: `bulk_and_mp.ipynb`, outputs go to `work/`
- Needs `../../structures/Co3O4_mp-18748.vasp` and `../../scripts/fetch_bulk.py`
