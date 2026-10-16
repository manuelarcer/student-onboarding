# Student onboarding: MLIP calculations with the group's tools

This repository is a practical course for a student who joins one of the group's
projects and will run calculations with machine-learning interatomic potentials (MLIPs) using the group's
tools. It assumes no Python and no terminal experience. Each module is a folder with a
short README and, in most cases, one Jupyter notebook that you run and edit yourself.
By the end you can build a surface, place an adsorbate on it, relax it with the MACE
model through the `mliprun` command line, compute a reaction barrier, run a short
molecular dynamics simulation, and, if you get a free account, submit the same kind of
job to the ASPIRE2A supercomputer.

## Status of this course

- This is a first version, and it will change while you use it
    - Tell your supervisor where a step is unclear or does not work, and the repository is updated
- The aim is hands-on practice with the tools: building structures, running `mliprun`, and reading the files it writes
- The science in it is not checked to the standard of a paper, and some of it may be wrong
    - This covers the scientific statements, the numbers, and what a result is said to mean for a material
    - Do not quote them in a report, and do not use them as a reference
    - The science is settled with your supervisor, in your one-to-one meetings, and not by this repository

## What is in this repository

- `modules/`: the numbered lessons, 00 to 11, each a folder with a README and usually one notebook; do them in order.
- `projects/`: one folder per research project, with the project background, the recorded decisions, and a capstone notebook that applies the modules to the project's own material.
- `paths/`: one file per student profile, saying which modules to do in which week and what to bring to the weekly meeting.

Two more folders hold shared files: `structures/` (small input structures the
notebooks read) and `scripts/` (helper code the notebooks import). `docs/` holds notes
for the people who maintain this repository; you do not need it.

## Start here

1. Open `paths/ew2gc-mlip.md`. It gives the order of the modules, the weekly plan, the reading that goes with each module, and what to bring to the weekly meeting.
2. Do `modules/00-setup/` first. It installs everything. Nothing else works before it.
3. Each module README says what you need before starting and how long it takes.

## The modules

- Do them in order; module 11 is optional and only for a student who gets a free personal ASPIRE2A account
- "Notebook time" is the time to run the notebook, measured on one Mac; "hours" is the time to read the module, change a value in it and run it again
- The full measured numbers are in each module's README, and if a number here differs from it, the README is right

| module | title | notebook time | hours |
|---|---|---|---|
| `modules/00-setup/` | Setup: install the tools on your own computer | no notebook | about 2 |
| `modules/01-python-for-atoms/` | Python for atoms | under 1 minute | about 3 |
| `modules/02-ase-basics/` | ASE basics | under 1 minute | about 3 |
| `modules/03-bulk-and-mp/` | Bulk structures and the Materials Project | under 1 minute | about 2 |
| `modules/04-slabs/` | Slabs | under 1 minute | about 4 |
| `modules/05-adsorbates/` | Adsorbates | under 1 minute | about 3 |
| `modules/06-single-point/` | Single point | under 1 minute | about 2 |
| `modules/07-relaxation/` | Relaxation | under 2 minutes | about 3 |
| `modules/08-frequencies/` | Frequencies | about 1 minute | about 2 |
| `modules/09-neb/` | NEB | under 1.5 minutes | about 2 |
| `modules/10-md/` | Molecular dynamics | about 2.5 minutes | about 3 |
| `projects/ew2gc/` | Capstone: `capstone.ipynb` | about 2.5 minutes | about 4 |
| `modules/11-hpc-aspire2a/` | ASPIRE2A: run the same calculation on a supercomputer (optional) | no notebook | about 3 plus the first login, which you do together with your supervisor; an estimate |

## How to get help

- Ask on GitHub: open the repository page, go to the "Issues" tab, click "New issue", and pick one of the two forms
    - "Question about a module": a step, a cell or a result you do not understand
    - "Something does not work": a command fails, a cell raises an error, or the output is not what the module says
    - Search the closed issues first; another student may have asked the same thing, and the answer is there
    - One question per issue, so that each answer can be found again
- Do not spend more than one hour stuck on an installation problem: open an issue and also tell your supervisor directly
- The forms ask for what your supervisor needs to answer, and the same items apply when you ask in person
    - The exact command you typed, copied from the terminal, not retyped from memory
    - The last 20 lines of the output, including the error message
    - What you expected to happen and what happened instead
    - For a notebook, which cell (the number in brackets on its left), and the error text pasted as text
- You can also ask in an issue what a result means for the science; your supervisor may then answer it in your next one-to-one meeting instead of in the issue

## Tested on

On 2026-10-12 the author executed every notebook of modules 01 to 10 and the capstone,
from top to bottom, on macOS 27.0.1 (Apple M3, Python 3.11.10); the versions and the
times are in `docs/verification-2026-10-12.md`. Module 00 was executed end to end on
macOS 26.6 (Apple Silicon, Python 3.11.10) on 2026-09-17: every command in
`modules/00-setup/README.md`, from a fresh virtual environment to a loaded MACE model.
On 2026-10-16 modules 06 to 10 and the capstone were executed again on a Linux laptop
against mliprun 0.5.0, and modules 06 and 08 were rewritten for its new `singlepoint` and
`freq` commands; that run, and what it did not cover, is in `docs/verification-2026-10-16.md`.
The Windows and Linux instructions in module 00 are taken from mliprun's tested install
guides and were not executed here, and neither was module 11 (ASPIRE2A), which the
author has not run on the cluster. If a Windows, Linux or ASPIRE2A step fails, tell your
supervisor; the step will be corrected in this repository.
