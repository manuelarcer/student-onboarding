# Export: PDF copies of the notebooks and the Markdown modules

This page says how to turn the notebooks and the Markdown modules into PDF files, for a student who wants to read offline or print. The files go to `export/` in the repository root. That folder is ignored by git, so it is never committed, and you can delete it and make it again at any time.

## Which route worked

- Route used: `quarto render <notebook> --to typst`, which writes a PDF through Typst, a document typesetting program that comes inside Quarto
    - It needs no separate Typst or LaTeX installation: Quarto 1.7.31 carries its own Typst, and `typst` was not on the `PATH` of the maintainer's Mac
    - It does not run the notebook; it takes the outputs already stored in the `.ipynb` file, so a notebook has to be executed first (`docs/maintainers.md`, "How to re-verify everything")
- Fallback, not needed on 2026-10-12: `jupyter nbconvert --to html <notebook> --output-dir export/<name>` makes one HTML file per notebook
- All 14 PDF files below were made on 2026-10-12 with Quarto 1.7.31 and pandoc 3.9, on the maintainer's Mac; all exited with code 0
- Quarto also leaves a folder `.quarto/` and a `.gitignore` next to each notebook it renders; the repository `.gitignore` ignores `.quarto/`, and the small `.gitignore` files quarto writes are not part of the repository

## The commands

Run from the repository root. `--output-dir` is relative to the notebook's own folder, which is why it starts with `../../`.

```bash
cd ~/github/work/student-onboarding
mkdir -p export

quarto render modules/01-python-for-atoms/python_for_atoms.ipynb --to typst --output-dir ../../export/01
quarto render modules/02-ase-basics/ase_basics.ipynb             --to typst --output-dir ../../export/02
quarto render modules/03-bulk-and-mp/bulk_and_mp.ipynb           --to typst --output-dir ../../export/03
quarto render modules/04-slabs/slabs.ipynb                       --to typst --output-dir ../../export/04
quarto render modules/05-adsorbates/adsorbates.ipynb             --to typst --output-dir ../../export/05
quarto render modules/06-single-point/single_point.ipynb         --to typst --output-dir ../../export/06
quarto render modules/07-relaxation/relaxation.ipynb             --to typst --output-dir ../../export/07
quarto render modules/08-frequencies/frequencies.ipynb           --to typst --output-dir ../../export/08
quarto render modules/09-neb/neb.ipynb                           --to typst --output-dir ../../export/09
quarto render modules/10-md/md.ipynb                             --to typst --output-dir ../../export/10
quarto render projects/ew2gc/capstone.ipynb                      --to typst --output-dir ../../export/ew2gc
```

The Markdown files (module 00, module 11 and the project README) have no stored outputs, so they go through pandoc to a Typst file and then to PDF:

```bash
mkdir -p export/00 export/11 export/ew2gc

pandoc modules/00-setup/README.md -f gfm -t typst -s -o export/00/00-setup.typ
quarto typst compile export/00/00-setup.typ export/00/00-setup.pdf

pandoc modules/11-hpc-aspire2a/README.md -f gfm -t typst -s -o export/11/11-hpc-aspire2a.typ
quarto typst compile export/11/11-hpc-aspire2a.typ export/11/11-hpc-aspire2a.pdf

pandoc projects/ew2gc/README.md -f gfm -t typst -s -o export/ew2gc/ew2gc-README.typ
quarto typst compile export/ew2gc/ew2gc-README.typ export/ew2gc/ew2gc-README.pdf
```

- `-f gfm` reads the file as GitHub-flavoured Markdown, the dialect the READMEs are written in
- `-t typst -s` writes a complete (standalone) Typst document
- `quarto typst compile <in.typ> <out.pdf>` is the Typst compiler inside Quarto

## What is in `export/` afterwards

- `export/00/00-setup.pdf`, `export/11/11-hpc-aspire2a.pdf`
- `export/01/` to `export/10/`: one PDF per notebook, named like the notebook
- `export/ew2gc/`: `capstone.pdf` and `ew2gc-README.pdf`
- The PDFs were checked for existence and size only, with exit code 0 from every command; no page-by-page reading was done
