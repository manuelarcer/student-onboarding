# Verification run of 2026-10-16

This page records a check of the calculation notebooks against mliprun 0.5.0, and the rewrite of modules 06 and 08 that followed it. It was not run in the verification environment of `docs/maintainers.md`, and it does not replace a full re-verification on the Mac; what is missing is listed at the end.

## Why

- Since the run of 2026-10-12, mliprun gained `mlip singlepoint run` and `mlip freq run` and was released as 0.5.0 (`manuelarcer/mliprun` PR #63)
- The course had been built against mliprun commit `9d2e3db` of 2026-09-09: its line citations of mliprun's source match that commit
- Modules 06 and 08 said the two commands did not exist, and told the student to compare their version with 0.4.0 to find out, which a clone of `main` before the release defeated, because it still reported 0.4.0

## What was run

- Machine: Linux laptop, Intel Core i5-8250U, 8 threads, CPU only
- Python environment: mliprun's own development venv (`~/github/mliprun/.venv`), editable install of mliprun, with `nbclient`, `ipykernel` and `pymatgen` installed into a scratch folder on `PYTHONPATH`; not built from module 00
- Every notebook was executed with `nbclient` on a copy of the repository, never in the checkout itself
- First pass, the notebooks as they stood, against mliprun `main` at `95750f2` (code of 0.5.0, still labelled 0.4.0): modules 06 to 10 and the capstone
- Second pass, modules 06 and 08 after the rewrite, against the release branch at `f544aca` (labelled 0.5.0), each on a `work/` folder that did not exist yet

## Result of the first pass

| notebook | wall time (s) | passed | outputs against the committed ones |
|---|---|---|---|
| `modules/06-single-point/single_point.ipynb` | 9.9 | yes | identical, timings aside |
| `modules/07-relaxation/relaxation.ipynb` | 170.7 | yes | identical to the third or fourth decimal; the non-converged bridge run ends 0.00002 eV lower |
| `modules/08-frequencies/frequencies.ipynb` | 52.0 | yes | identical to 0.1 cm⁻¹; the `mlip --help` panel now lists `webapp`, `singlepoint` and `freq` |
| `modules/09-neb/neb.ipynb` | 89.2 | yes | identical, timings and the date in the backup folder name aside |
| `modules/10-md/md.ipynb` | 385.1 | yes | different, as expected without a seed; the columns and the files are unchanged |
| `projects/ew2gc/capstone.ipynb` | 439.9 | yes | same E_ads(*OH), 1.35 eV, every term converged; pymatgen-core 2026.10.2 found the same 16 cuts and 4 faces |

- No mliprun change since `9d2e3db` breaks a notebook: the required `--mace-head` and `--uma-task` (#45) apply only to multi-head models and the course uses plain `mace`, and the MD changes (#53, #55) are NPT only, where the course runs NVT
- In module 10, run 1 of the four 2.0 fs runs did not blow up this time (highest temperature 727 K); the text says all four blow up, which holds only for some seeds

## Found while rewriting module 08

- ASE 3.29.0 gives wrong frequencies when `Vibrations` is handed an unsorted list of two or more atoms: the Hessian is built in the order of the list, but `VibrationsData` takes the masses, and places the mode patterns, in increasing atom order (`ase/vibrations/data.py`, `self._atoms[self.get_mask()]`)
- Module 08 passed `[i_o, i_h]` = `[1, 0]` for OH, so its committed OH results were wrong: 90.4i, 218.1, 1080.4 and 3841.7 cm⁻¹, against the correct 288.9i, 223.0, 338.2 and 3758.7 cm⁻¹
- Checked three ways: an independent finite-difference Hessian with the right masses gives the correct numbers; the same Hessian with the masses swapped reproduces the wrong ones exactly; `mlip freq run`, which sorts the list (`core/vibrations.py`), gives the correct ones whichever order is typed
- The single-atom sections of module 08 are not affected, and no other notebook uses `Vibrations`

## Result of the second pass

| notebook | wall time (s) | passed | lint |
|---|---|---|---|
| `modules/06-single-point/single_point.ipynb` | 12.7 | yes | passes |
| `modules/08-frequencies/frequencies.ipynb` | 74.7 | yes | passes |

- The committed outputs of these two notebooks are from this pass, so their kernel metadata says Python 3.14.7
- Every number quoted in the new or changed markdown was checked against these outputs

## Versions

| package | version |
|---|---|
| mliprun | 0.5.0 (release branch, `f544aca`) |
| mace-torch | 0.3.16 |
| torch | 2.14.1+cpu |
| ase | 3.29.0 |
| numpy | 2.5.4 |
| pandas | 3.0.6 |
| scipy | 1.18.1 |
| matplotlib | 3.11.2 |
| pymatgen-core | 2026.10.2 (capstone only) |
| nbclient | 0.11.0 |
| ipykernel | 7.4.0 |

- Python 3.14.7

## Not done

- No execution on the Mac or in `~/venv/onboarding-mace`: rebuild it from module 00 against mliprun 0.5.0, run `scripts/verify_all.sh`, and record the times in a new verification page; the times of modules 06 and 08 in their READMEs are from this Linux laptop until then
- The builders of modules 06 and 08 on the Mac are now out of date: the two notebooks were edited directly, by script, and running the old builders would bring back the old sections and the unsorted `indices`
- Module 00's expected `mlip doctor` output now says 0.5.0, but module 00 was not re-executed
- The capstone still cites `cli/commands/optimize.py` lines 259 to 303 and `core/optimize.py` lines 531 to 533 of `9d2e3db`; in 0.5.0 those are lines 62 to 106 and 540 to 542
- The committed outputs of modules 07, 09 and 10 and of the capstone still print mliprun 0.4.0, from the run of 2026-10-12
