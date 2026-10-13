# Decisions of the EW2GC project, and the master canon behind them

- This file is a dated copy and not the source
    - The project's own file is `CANON.md` in the EWaste2GreenCat project folder, and the group's master is `CANON.md` in your supervisor's `~/.claude` folder; the files on your supervisor's computer are authoritative
    - Snapshot time: 2026-10-12, 19:12 (Singapore time)
    - The project file as read then was last modified on 2026-10-12 at 18:04, and the master file on 2026-10-09 at 12:53
    - This file copies what those two files record and nothing from `CANON-EVIDENCE.md`, which holds the project's measurements and rejected alternatives
- If the two files change after the snapshot, this one is out of date
    - The project's `CANON.md` was still changing on the day of the snapshot, and the entry for `S1` carries sub-decisions dated 2026-10-12
    - Ask Juan for the current file before a project calculation, as the last section says
- An item that is `PENDING` in the project file is shown as pending here and is never to be read as settled

## How to read the table

- The group's master canon lists the methodological decisions that belong to your supervisor and are never assumed by a person or a tool
    - `OPEN` means the master has no default, so a project must record a decision before a calculation that touches the item is run
    - `SETTLED` means the master carries a standing default with its date, and it applies unless the project's file overrides it
    - Precedence: a project decision first, then the master default, and with neither recorded the question is blocking
- The column "this project" says what the project file records for the item
    - "Recorded" points to the entry copied under the table
    - "Not recorded, ask Juan before running" is the answer for every `OPEN` item the project file does not mention
    - "Not recorded in the project file, so the master default applies" is the answer for a `SETTLED` item the project file does not mention
- VASP parameter items, prefix `CV`, live in a separate file of the master canon and are not listed; you do not run VASP

## The master items, 25 of them

| ID | master status | what the item decides | this project |
|---|---|---|---|
| B1 | OPEN | source of the bulk structure when no file is given | not recorded, ask Juan before running |
| B2 | OPEN | bulk relaxation degrees of freedom: cell and atoms, or atoms only, and whether symmetry is enforced | not recorded, ask Juan before running |
| B3 | OPEN | building a complex bulk from a template, such as an alloy | not recorded, ask Juan before running |
| S1 | OPEN | surface cleavage procedure, tool and settings | recorded, entry `S1` below |
| S2 | OPEN | slab thickness, and what counts as a layer | not recorded, ask Juan before running; the minimum thickness rule of `E-p3` is `PENDING` |
| S3 | OPEN | stoichiometry and top and bottom symmetry on cleaving | recorded, entry `S3` below |
| S4 | OPEN | which terminations to generate | recorded, entry `S4` below |
| S5 | OPEN | thickness of the vacuum region | recorded, entry `S5` below |
| S6 | SETTLED 2026-07-16 | smallest in-plane lattice vector about 7.5 Å for surface and adsorption cells | not recorded in the project file, so the master default applies |
| S7 | SETTLED 2026-07-11 | never cleave slabs from idealized or conventional-cell coordinates; use the bulk optimized at the project's level of theory | not recorded in the project file, so the master default applies; entry `S1` refers to it |
| S8 | OPEN | frozen-layer scheme for slab calculations | not recorded, ask Juan before running; `E-p3` records all atoms free for the project's symmetric slabs, which is a separate item |
| S9 | SETTLED 2026-07-13 | slab cells are never relaxed, no `--relax-cell` on a slab unless Juan instructs it | not recorded in the project file, so the master default applies |
| A1 | OPEN | adsorption-site selection | not recorded, ask Juan before running |
| A2 | OPEN | binding mode and orientation of the adsorbate | not recorded, ask Juan before running |
| C1 | OPEN | MLIP model and head or task | recorded, entry `C1` below |
| C2 | OPEN | force convergence criterion for MLIP relaxations | recorded, entry `C2` below |
| C3 | SETTLED 2026-07-13 | one head per energy formula, never mixed within one γ, adsorption energy or ΔE | not recorded in the project file, so the master default applies |
| C4 | SETTLED 2026-07-13 | the same `fmax` and optimizer across one energy diagram, NEB endpoints and standalone relaxations alike | not recorded in the project file, so the master default applies |
| C5 | OPEN | MD run decisions: ensemble, temperature, timestep, total steps | recorded, entry `C5` below |
| C6 | OPEN | NEB parameters: images, spring constant, climbing image | not recorded, ask Juan before running |
| C7 | SETTLED 2026-08-25 | NEB band integrity: force convergence alone never certifies a band | not recorded in the project file, so the master default applies |
| K1 | SETTLED 2026-07-13 | convergence status is part of the result, labelled converged or not converged wherever it is reported | not recorded in the project file, so the master default applies |
| K2 | SETTLED 2026-07-14 | calculations outside the group's database are recorded in the provenance ledger before their numbers are used | not recorded in the project file, so the master default applies |
| K3 | SETTLED 2026-08-19 | ASPIRE2A jobs are charged to a project number that each project records | not recorded, ask Juan before running; the master says no recorded number is a blocking question |
| K4 | SETTLED 2026-09-18 | a catplat database holds two rows per structure, so a row count is never a count of structures | not recorded in the project file, so the master default applies |

## The project's own items

- The master carries no energetics items by design, because energetics conventions are reporting choices of one project (Juan, 2026-09-11); the project records its own under the ID prefix `E-p`
- One entry carries a `PENDING` flag, and it is kept
    - `E-p3` is `PENDING`: its minimum thickness rule is not decided, and a three-rung sweep on the (100), (311) and (321) faces is to decide it
    - `E-p1` was rewritten on 2026-10-09 and has no flag; the entry below is the text as it stands at the snapshot

**Parsimony** (2026-10-09, master law 10): among methods that meet the accuracy gate, use the
one with the fewest steps, parameters and assumptions; add a step only for a measured error.

- **E-p1** (2026-10-09): γ_SL uses a **symmetric R&S slab wetted on both faces, full PBC, no vacuum**:
  γ_SL(μ_O) = [⟨E_slab+water⟩ − (N_Co/3)·E_bulk_fu + ((4/3)·N_Co − N_O)·μ_O − N·μ_H2O]/(2A). Water
  volume is fixed by the packing guess (`pack_water_on_slab.py`: 1.0 g/cm³ over t_water, 1.0 Å gap
  per face), then one NVT run (C5); no NPT stage, no calibration. Why: E-p3 makes both faces
  identical, and the guess is one MD instead of two at a few % density cost (parsimony).

- **E-p2** (2026-09-03): Vacuum surface energies for Co3O4 use the **Reuter-Scheffler
  framework on symmetric, non-stoichiometric slabs**, γ(μ_O) = [E_slab − (N_Co/3)·E_bulk_fu
  + ((4/3)·N_Co − N_O)·μ_O]/(2A), replacing tasker_flip as the canonical vacuum γ for both the
  Wulff construction and the γ_vac term of E-p1. γ per termination is a line in μ_O, so the
  equilibrium crystal shape is a function of μ_O and the exposed termination is set by
  thermodynamics, not by a selection rule. Why: Co3O4 is Tasker class III, so only the
  symmetric (non-stoichiometric) route resolves the single-face γ that E-p1 requires.

- **E-p3** (2026-09-03): Symmetric R&S slabs relax with **all atoms free — no frozen region** —
  plus a mandatory validator flagging any slab whose central interlayer spacings are not
  bulk-like. Why: frozen atoms are the 0.05–0.19 J/m² artifact we are leaving tasker_flip to
  escape, and full relaxation adds no facet-dependent relaxation-depth parameter.
  **PENDING**: the minimum thickness rule, decided by a three-rung sweep on (100)/(311)/(321).

- **E-p4** (2026-09-03): μ_O carries **two anchors**. O-poor (synthesis/vacuum):
  μ_O_min = [E_bulk_fu − 3·E_Co(hcp)]/4 per MLIP, bulk hcp Co only, no O2 (2026-08-25).
  Electrochemical (OER marker): μ_O(U) = μ_H2O − μ_H2 + 2eU on the RHE scale, pH-independent,
  with **μ_H2 computed per MLIP in the gas phase**; μ_O2 is computed as a **diagnostic only**,
  gated against the experimental 2.46 eV/O. **O2 reference** (2026-10-09): H2 is taken as
  correct and E_O2 = 2·(μ_H2O,liq − E_H2 + 2.46 eV) per MLIP (`PRODUCTION/00_molecules/o2_derived.csv`);
  the MLIP O2 is not used. Why: all three MLIPs fail the O2 gate by +0.5 to +1.4 eV (spinless
  triplet), while H2 and gas H2O are well described. Why (anchor choice): one MLIP molecular
  reference is unavoidable, and H2 (closed shell) is the far smaller risk than O2 (spin
  triplet). Affects the marker position only, never the γ(μ_O) lines.

- **E-p5** (2026-10-10): CoOOH γ is evaluated **on the electrochemical axis only**. With Co as
  reference, γ = [E_slab − n_fu·E_CoOOH − ΔO·μ_O − ΔH·μ_H]/(2A), with μ_H = ½μ_H2 − eU_RHE and
  μ_O = μ_H2O − μ_H2 + 2eU_RHE (computational hydrogen electrode, E-p4 references), so γ is a
  line in U_RHE with slope set by (ΔH − 2ΔO). No synthesis (O-poor) anchor. Why: CoOOH forms only
  under electrochemical conditions; experimentalists synthesize Co3O4, not CoOOH.

## The master items the project records

- These are the entries of the project file for `S1`, `S3`, `S4`, `S5`, `C1`, `C2` and `C5`, copied as they stand at the snapshot
    - `S1` carries sub-decisions dated 2026-10-12 inside its text: the `ftol` value of each of the two materials, and the rule that no cut of CoOOH may break an O–H bond
    - The pinned pymatgen version of `S1` is 2025.6.14 or older, and the environment of this course has a newer one, so a slab built here may not match the project's labels; the capstone shows the script's warning about it

- **S1** (2026-10-09): Slabs are cleaved from each MLIP's own relaxed bulk (S7) with pymatgen
  `SlabGenerator` (`lll_reduce`, `primitive`, `center_slab`; no symmetry filtering, no
  symmetrize), then rigidly rotated so the surface normal is +z. Symmetric slabs are built once
  per face class (S4) by the `nonstoichiometric_symmetrized_slab` trimming loop. `ftol` **0.005**
  (Co3O4, 2026-10-12; tasker_flip production used 0.05), **0.02** (CoOOH, 2026-10-12, cut in the
  1×2×1 alt-H cell; tasker_flip used 0.007). CoOOH: **no cut may break an O–H bond**
  (`--keep-bonds O-H:1.2`, checked on every slab; 2026-10-12). pymatgen ≤ 2025.6.14. Scripts
  `gen_slabs.py` (stoichiometric cleavages), `gen_rs_slabs.py` (symmetric slabs; updated
  2026-10-10, replaces the pilot `gen_symmetric_slabs.py`). Why: how every production slab was
  made; pymatgen 2026.x changes the cut set and the `f<N>` numbering. Why ftol 0.005: the only
  tested value giving the same number of cuts and faces for all 3 MLIPs on all 13 facets. Why
  CoOOH 0.02: uma-s and mace-mh-1 give identical cuts and faces on all 9 facets; chgnet keeps
  its own face set (differs on 6/9 facets, accepted per S7). Why O–H rule: a bare proton or an
  O stripped of its H is not a physical termination.

- **S3** (2026-10-09): Both materials use symmetric slabs in the R&S framework (E-p2).
  A cleavage that is already symmetric and stoichiometric is valid as is (its γ has zero
  slope in μ_O). Stoichiometric asymmetric cleavages serve only as parents. Why: one
  consistent framework; Co3O4 is Tasker class III, so symmetry forces non-stoichiometry.

- **S4** (2026-10-10): **One symmetric slab per distinct face.** All raw stoichiometric cuts
  (no top-face filter) are enumerated, both faces of each cut are fingerprinted on the
  orthogonalized slab (per-layer (element, coordination number) per area plus layer depths,
  4 Å deep), and each face class `r<k>` is symmetrized once from one carrier cut. Each MLIP
  enumerates from its own bulk (S7); faces are compared across MLIPs in a report, not forced to
  one set. Script `gen_rs_slabs.py`. Why: an R&S γ belongs to one face, so the face is the unit;
  per-cleavage enumeration duplicates faces (uma-s (311): 24 cleavages, 8 faces).

- **S5** (2026-10-09): Vacuum 15 Å along z for vacuum slabs. Why: standard in vacuum slab
  modelling; MLIPs have no SCF or dipole correction, so the gap only has to exceed the
  model's interaction range.

- **C1** (recorded 2026-07-25, decided earlier in PHASE5_SPEC): MLIP models/heads for
  explicit_solvation = uma-s-1p2 with `--uma-task oc25` (fully self-consistent, 2026-07-02),
  mace-mh-1, chgnet (single head). Why: UMA heads have independent energy zeros, so one head
  per formula (master C3) binds the whole uma-s pipeline including μ_H2O and γ_LV.

- **C2** (2026-09-03): Force convergence for all MLIP geometry relaxations = **fmax
  0.05 eV/Å** (BFGS, max 300 steps), bulk and slabs and references alike. Why: it is what
  every relaxation in the project has already used, and recording it closes master C2, which
  warns that the platform default otherwise executes silently.

- **C5** (2026-07-25): Phase 5 slab+water production MDs run NVT Langevin, 300 K, friction
  0.01 fs⁻¹, 0.5 fs timestep, **175 ps total = 50 ps equilibration discarded + 125 ps
  production**, with a mandatory block-trend check and `--resume` extension before any γ
  enters a table. Why: the transient dies by ~20–30 ps and γ noise at 125 ps (~0.012–0.015
  J/m²) sits well under the 0.05 J/m² decision gate. Supersedes the 250 ps protocol
  (2026-05-18) for slab+water runs; water-reference and film MDs keep their as-run lengths.

## What "ask" means

- When a calculation touches an `OPEN` item with nothing recorded for it, stop and ask Juan before you run it, because the tool will not stop you
- Send one message with three things in it
    - The calculation you intend to run, in one line, with the structure and the model
    - The value you propose for the item, and where you took it from
    - Why you think that value is right for this calculation
- Do not write the answer into the project's `CANON.md` yourself: Juan records it, with its ID, its date and a one-line reason
- A value from a tool default, from an old job script or from this course's notebooks is never an answer, because the notebooks use teaching values chosen so that they run on a laptop
