# 05. Adsorbates

- Goal: put O, OH and OOH on a Pt(1 1 1) surface, move them, turn them and keep the frozen layers, with the two canon items that decide every choice named as you meet them
- Before you start: modules 00 to 04 finished; the `mlip-mace` environment active; Jupyter Lab started from the repository root, as step 12 of module 00 says; the kernel at the top right of the notebook reads "Python 3 (ipykernel)"
- Time to run the notebook: under 1 minute (measured 5.0 to 6.1 s over three runs on a quiet machine and 4.8 s in the verification run of 2026-10-12, macOS on Apple Silicon; the first run of a session is slower while the package caches are cold, measured 20 s, and a busy machine can stretch it to a couple of minutes)
- Time to work through it: about 3 hours, reading every cell, changing a value in it and running it again
- After this you can:
    - Build the three adsorbates of this course by hand, and say which atom of each one is the anchor that binds to the surface
    - Place an adsorbate on any of the four sites of a close-packed metal face with `add_adsorbate`, and check the site you got from the adsorbate to metal distances instead of trusting the line that built it
    - Move an adsorbate by hand and turn it about its anchor, and use the symmetry of a close-packed metal site to tell which turns give back the structure you started from and which give a new one, warned that an oxide site has lower symmetry and needs more orientations to be tried (canon `A2`)
    - Let pymatgen's `AdsorbateSiteFinder` enumerate the sites of a surface, and say when a geometric enumeration stops being the right tool and scan-relax site discovery takes over (canon `A1`)
    - Keep the frozen bottom layer through a placement and through a file write, and build any of these structures in one line with `pt111_with_adsorbate`
- Files: `adsorbates.ipynb`, outputs go to `work/`
- Needs `../../scripts/onboarding_structures.py`
