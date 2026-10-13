# Starting structures

Every file here is a starting point for the notebooks, nothing more. The symmetry, atom
count and cell lengths below were read from the files with pymatgen on the date shown.

| file | source | date fetched | space group | atoms | cell lengths (Å) |
|---|---|---|---|---|---|
| `Pt_bulk_fcc.vasp` | ASE `bulk("Pt", "fcc", a=3.92, cubic=True)` | 2026-09-17 | Fm-3m (#225) | 4 | a = b = c = 3.9200, cubic |
| `Co3O4_mp-18748.vasp` | Materials Project `mp-18748`, conventional cell | 2026-09-17 | Fd-3m (#227) | 56 | a = b = c = 8.0459, cubic |
| `CoOOH_mp-27913.vasp` | Materials Project `mp-27913`, primitive cell as served | 2026-09-17 | R-3m (#166) | 4 | a = b = c = 4.6148, α = β = γ = 35.96° |
| `H2O.xyz` | ASE `molecule("H2O")` | 2026-09-17 | point group C2v | 3 | none; `molecule_in_box` puts it in a 12 Å box |
| `O2.xyz` | ASE `molecule("O2")`, triplet, carries initial magnetic moments | 2026-09-17 | point group D∞h | 2 | none; `molecule_in_box` puts it in a 12 Å box |
| `H2.xyz` | ASE `molecule("H2")` | 2026-09-17 | point group D∞h | 2 | none; `molecule_in_box` puts it in a 12 Å box |

- These are starting structures only, never relaxed. Every notebook that needs a relaxed
  structure relaxes it with the model it uses (canon S7).

## Notes on the choices

- Co3O4: `mp-18748` is the normal spinel the project uses. It was fetched with
  `--conventional`, so the file holds the 56-atom cubic cell, the one the capstone relaxes
  directly.
- CoOOH: `scripts/fetch_bulk.py --formula CoOOH --list-polymorphs` returned eight entries
  on 2026-09-17. Two are R-3m (rhombohedral, β-CoOOH, the mineral heterogenite):
  `mp-27913` at 0.0000 eV/atom above the hull and `mp-1280464` at 0.0985 eV/atom. The
  file holds `mp-27913`, the one on the hull, as the 4-atom primitive cell Materials
  Project serves by default. Its hydrogen sits midway between the two oxygens
  (fractional 0.5, 0.5, 0.5), a symmetric O–H···O position that a relaxation is expected
  to break.
- Pt: the ASE reference lattice constant 3.92 Å, the same value `scripts/onboarding_structures.py`
  uses for the Pt(111) slabs.

## How they were made

- `Pt_bulk_fcc.vasp` and the three `.xyz` files: `ase.build.bulk` and `ase.build.molecule`,
  written with `ase.io.write`.
- `Co3O4_mp-18748.vasp`:
  `python scripts/fetch_bulk.py --mp-id mp-18748 --conventional --output structures/Co3O4_mp-18748.vasp`
- `CoOOH_mp-27913.vasp`:
  `python scripts/fetch_bulk.py --mp-id mp-27913 --output structures/CoOOH_mp-27913.vasp`
- Both fetch commands need the environment variable `MP_API_KEY` exported in the shell
  (`export MP_API_KEY=...`); a variable that is set but not exported is invisible to Python.
