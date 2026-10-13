# Student onboarding repository — design

Date: 2026-09-17. Approved by Juan in chat the same day (option "core modules plus
project tracks plus learning paths", with one change: the HPC module is written for a
person at a terminal, not for an AI agent).

## Purpose

A reusable, hands-on guide that brings a new student from "no Python" to running
machine-learning interatomic potential (MLIP) calculations with the group's tools, and
then into a specific project. The first users are students helping with EW2GC WP4, at
about 10 h/week. Students cannot run VASP (licence), so the guide is MLIP-only.

Future students on other projects, with more or less prior knowledge, must be served by
adding files, never by restructuring.

## Principles

1. **Core is project-agnostic.** Numbered modules teach tools and concepts on a simple
   system. Nothing in `modules/` names a project decision as if it were general.
2. **Projects add, they do not fork.** A project folder carries its recorded decisions,
   its worked examples, and one capstone that reuses the core modules on the project's
   own material.
3. **A learning path is a one-page file.** It lists which modules, in what order, with
   hours. A new student profile is a new path file.
4. **Canon awareness is built in.** Every calculation module opens with the list of canon
   items it touches and the sentence that those are decided per project by the
   supervisor, never by the tool default. Teaching values are labelled as teaching values.
5. **The model is always explicit.** No `--mlip auto` anywhere. MACE-MP-0 (`--mlip mace`)
   for every exercise; it needs no access request and runs on a laptop CPU.
6. **Everything runs on a laptop.** Each calculation notebook completes on CPU in under
   ten minutes. Cluster use is a separate module, not a prerequisite.
7. **Readable before Python exists.** Install instructions are Markdown, not notebooks.
8. **Plain international English.** Short sentences, common words, every term defined at
   first use. The reader is fluent in materials science, not in English idiom or in
   software conventions.

## Layout

```
student-onboarding/
  README.md                    what this is, how to pick a path, how to get help
  paths/
    ew2gc-mlip.md              the EW2GC WP4 path
  modules/
    00-setup/                  Markdown: Python, venv, git, mliprun, MACE, Jupyter, mlip doctor
    01-python-for-atoms/       notebook: the Python the later modules use
    02-ase-basics/             notebook + CLI: read, write, view, move, rotate, supercell
    03-bulk-and-mp/            notebook: CIF/POSCAR in; Materials Project fetch with own key
    04-slabs/                  notebook: pymatgen SlabGenerator; Miller index, layers, vacuum, freezing
    05-adsorbates/             notebook: add O/OH/OOH; move, rotate; sites
    06-single-point/           notebook: energies and forces via the mliprun Python API
    07-relaxation/             notebook + CLI: optimize run; fmax, optimizer, max steps; convergence CSV
    08-frequencies/            notebook: ASE Vibrations on the MACE calculator; ZPE
    09-neb/                    notebook + CLI: neb run; O diffusion on Pt(111); images, k, climb
    10-md/                     notebook + CLI: md run; NVT; timestep; md_energy.csv
    11-hpc-aspire2a/           Markdown: login, PBS, venv on scratch, job template, login-node rules
  projects/
    ew2gc/
      README.md                WP4 in one page; links to the onboarding deck and reading list
      DECISIONS.md             dated snapshot of the recorded project canon; unrecorded items marked "ask Juan"
      examples/                gen_slabs_sharable.py, one queue YAML, one PBS script, with provenance notes
      capstone.ipynb           Co oxide: relax bulk with MACE, cleave, add *OH, relax
  structures/                  small inputs the notebooks read
  scripts/                     helpers shared by notebooks
  docs/                        maintainer notes; this design
```

Each module folder holds one `README.md` (goal, prerequisites, time, what you will be
able to do) and, where applicable, one notebook. Structures a module needs are read from
`structures/` by relative path.

## Module specifications

Common to every notebook: follows the group's notebook style (heading plus nested
bullets carrying the reasoning; printed output as a label line and a bare value with the
unit in the label) and plot style. Ends with "check yourself" questions; answers sit in a
collapsed cell.

Common to modules 06 to 10: opening box "Before you run this for a project" listing the
canon IDs touched. Mapping:

| module | canon items named |
|---|---|
| 04 slabs | S1, S2, S3, S4, S5, S6, S7, S8, S9 |
| 05 adsorbates | A1, A2 |
| 06 single point | C1, C3 |
| 07 relaxation | C1, C2, C4, K1 |
| 08 frequencies | C1 |
| 09 NEB | C1, C4, C6, C7 |
| 10 MD | C1, C5 |
| 11 HPC | K2, K3 |

**00-setup** (Markdown, ~2 h). Windows, macOS, Linux in parallel columns or sections.
Python 3.11 or 3.12 install; a terminal; `python -m venv`; activation on each OS; git
install and `git clone` of mliprun; `pip install -e .`; `pip install mace-torch`;
`pip install jupyterlab pymatgen mp-api`; `mlip doctor` as the acceptance test; a
first-run note that MACE downloads its weights once. Sources: mliprun `AGENTS.md`,
`docs/install/mace.md`, `docs/windows_setup_guide.md`. States that only macOS was executed
end to end by the author.

**01-python-for-atoms** (notebook, ~3 h). Variables, lists, dicts, loops, functions,
imports, NumPy arrays, reading a CSV with pandas, one matplotlib plot. Every example uses
atoms or energies as the data so nothing is abstract.

**02-ase-basics** (notebook + CLI, ~3 h). `Atoms`, `read`/`write` across formats
(POSCAR, CIF, xyz, traj), `ase gui`, `ase convert`, `ase info`; positions, cell, pbc;
translate, rotate a fragment about an axis, `repeat` for supercells; constraints
(`FixAtoms`) as the freezing mechanism the later modules rely on.

**03-bulk-and-mp** (notebook, ~2 h). Load a CIF and a POSCAR; primitive versus
conventional cell with pymatgen; Materials Project: get a personal API key, store it as an
environment variable, query by formula, energy above hull, pick an entry, save POSCAR.
Uses the group's `fetch_bulk.py` as the worked script. B1 is named as the project
decision.

**04-slabs** (notebook, ~4 h). `SlabGenerator` on Pt bulk: Miller index, minimum slab
size, vacuum, centering; count layers and define what a layer is; terminations on a
second material; orthogonalize; in-plane repeat against the S6 minimum; freeze bottom
layers with selective dynamics; write POSCAR; view. The project's
`gen_slabs_sharable.py` is pointed to as "the way one project does it".

**05-adsorbates** (notebook, ~3 h). Build O, OH, OOH; place on top, bridge, hollow of
Pt(111) with `ase.build.add_adsorbate`; move and rotate an adsorbate about its anchor
atom; a small site enumeration; keep the frozen layers intact; write structures for
module 07.

**06-single-point** (notebook, ~1.5 h). `setup_calculator(atoms, mlip="mace")` from the
mliprun Python API; `get_potential_energy`, `get_forces`; max force; energy differences
(clean slab, slab + O, O2 reference) and why references must match (C3). Boxed note that
a mliprun CLI single-point command is planned and this cell will be replaced when it
lands.

**07-relaxation** (notebook + CLI, ~3 h). `optimize run` on a slab + O from module 05:
`--mlip mace`, `--fmax`, `--optimizer`, `--max-steps`; read `opt_convergence.csv`, plot
max force versus step; converged versus not converged as a label (K1); compare two fmax
values; `optimize batch` over the site set. Adsorption energy from the relaxed results.

**08-frequencies** (notebook, ~2 h). ASE `Vibrations` on the adsorbate atoms with the
MACE calculator; harmonic frequencies; imaginary modes as a diagnostic; zero-point energy
and why it enters free-energy diagrams. Boxed note that a CLI command is planned.

**09-neb** (notebook + CLI, ~3 h). O on Pt(111) from fcc hollow to hcp hollow: relax
both endpoints, `neb run --initial --final --mlip mace --num-images --k --climb`,
read `neb_data.csv`, plot the band, barrier; what C6 and C7 ask for.

**10-md** (notebook + CLI, ~2 h). `md run` NVT Langevin on a small Pt slab with water
molecules above it, a few hundred steps; read `md_energy.csv`, temperature versus time,
why the timestep depends on hydrogen; `--resume` semantics. C5 named.

**11-hpc-aspire2a** (Markdown, ~3 h plus first login with Juan). Written for a person at
a terminal. Getting an account; `ssh`; home versus scratch and the home quota; where a
venv and model caches go; a PBS job script template for a CPU job and a GPU job with the
project charging code as a placeholder that must come from the supervisor (K3); `qsub`,
`qstat`, `qdel`; what never to run on a login node and why (the August account block);
`rsync` to and from a laptop; recording a run in the provenance ledger (K2) as a pointer
to the supervisor. No agent-side mechanics of any kind: no connection sharing recipes, no
"ask the assistant to connect", no dispatch agents. Marked "verify on first login with
Juan" because it cannot be executed by the author for the student's account.

## Project track: `projects/ew2gc/`

- `README.md`: WP4 in one page; the OER steps; pointers to the onboarding deck and the
  reading list (file names, where to get them); which MLIPs the project runs and why
  the exercises used a different one.
- `DECISIONS.md`: a dated table of every canon ID in the master file, with the project's
  recorded decision where one exists (C1, C5, E-p1 as of 2026-07-25) and "not recorded,
  ask Juan before running" where none does. Header states that the file on Juan's machine
  is authoritative and this is a snapshot.
- `examples/`: `gen_slabs_sharable.py` (verbatim, with a provenance header), one
  `optimize` queue YAML and one MD queue YAML excerpt from `explicit_solvation`, one PBS
  GPU script skeleton. Each with a short note on what to look at.
- `capstone.ipynb`, two parts:
  - Part A, bulk validation gate: relax both Co3O4 and CoOOH bulk (positions and cell)
    with MACE-MP-0 and compare lattice parameters and volume against the values the
    project recorded with its production models. CoOOH is expected to fail the check
    (the project documented a +18 % volume expansion and a stretched hydrogen bond with
    MACE-MP-0, which is why it moved to MACE-MH-1). The lesson is the one the reading
    list's Unke 2021 entry sets up: a smooth, converged relaxation can still be wrong,
    and a validation gate against a trusted reference is how the project catches it.
  - Part B, slab and adsorbate on the oxide that passed: cleave Co3O4(100) with the
    project's `gen_slabs_sharable.py` in `tasker_flip` mode, so the student sees why a
    polar surface needs complementary pairs; take one member; state that the thickness,
    vacuum and freezing used are teaching values; add *OH; relax; adsorption energy
    against the clean slab and a water/hydrogen reference; write a one-paragraph result
    in the style of a lab note. Explicitly contrasts with the project's production
    models. If MACE-MP-0 also fails the Co3O4 gate during the build, the slab leg keeps
    Co3O4 but the notebook says so and the adsorption energy is labelled accordingly.

## Learning path: `paths/ew2gc-mlip.md`

| weeks | modules | hours |
|---|---|---|
| 1 to 3 | 00 to 05 | ~17 |
| 4 to 6 | 06 to 10 | ~12 |
| 7 to 8 | capstone, 11 | ~10 |
| 9 onwards | project work | — |

Plus: what to bring to the weekly meeting, how to report a result (converged or not,
model and head, reference used), and the reading-list items that pair with each module.

## Build and verification

1. Build a fresh venv on this Mac by following `modules/00-setup/README.md` literally.
   Any step that fails is a bug in the text, fixed before proceeding.
2. Execute every notebook headless (`jupyter nbconvert --execute`) in that venv. All
   must pass. Record wall time per notebook in its README; any over ten minutes is
   resized.
3. Module 03 is executed with the author's Materials Project key; the notebook reads the
   key from the environment and fails with a clear message if absent.
4. Windows and Linux install text is taken from mliprun's tested guides and is not
   executed here. The README says so.
5. Export the whole guide to PDF with nbconvert at the end, HTML if the PDF toolchain is
   missing on this machine.
6. Git: gitignore from the group template. Notebooks are committed executed, with their
   text outputs and figures, so the reader sees what to expect and the PDF export has
   content. Files a notebook writes to disk go to a `work/` folder inside its module,
   which is ignored. No model weights, no trajectories, no `.traj` in git.

## Out of scope

- Running anything on ASPIRE2A for the student, or testing module 11 there.
- Copying any canon value into `DECISIONS.md` that is not already in the project file.
- A documentation site (MkDocs). The layout allows it later.
- UMA, SevenNet or CHGNet installs. Named, linked to mliprun's recipes, not taught.

## Open items for Juan

- The ASPIRE2A project code the student will charge to (K3): placeholder until given.
- Whether a student also gets a cos-cluster account (module 11 covers ASPIRE2A only).
- The mliprun single-point and frequency CLI commands, when they land, replace the
  Python-API cells in modules 06 and 08.
