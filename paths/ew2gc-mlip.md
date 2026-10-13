# Learning path: EW2GC work package 4, MLIP calculations

This file tells you which modules to do in which week, what to read with each, what to bring to the weekly meeting, and how to write down a result.

## Who this is for

- You are a student helping with work package 4 of the EW2GC project
    - This path is planned for about 10 hours per week; if you have more or less time, agree the pace with your supervisor
- This path assumes no Python and no terminal experience, and you do not use VASP
    - You cannot use VASP. You will most likely not be added to the group's ASPIRE2A projects.
    - Every calculation of this path, except module 11, is a machine-learning interatomic potential (MLIP) calculation run on your own computer
- A free personal ASPIRE2A account is possible, and only then module 11 applies to you
    - Module 11 is optional; if you do not get a free account, skip it

## The week table

- Weeks are counted from the day you start
- The notebook time is what the author measured on one Mac; your computer may be slower, and the first run of a session is slower again
- "Hours" is the time to read a module, change a value in it and run it again; it is not the notebook time
- The full measured numbers are in the README of each module; if a number here differs from that README, the README is right

| weeks | module | title | notebook time | hours |
|---|---|---|---|---|
| 1 to 3 | 00 | Setup | no notebook | about 2 |
| 1 to 3 | 01 | Python for atoms | under 1 minute | about 3 |
| 1 to 3 | 02 | ASE basics | under 1 minute | about 3 |
| 1 to 3 | 03 | Bulk structures and the Materials Project | under 1 minute | about 2 |
| 1 to 3 | 04 | Slabs | under 1 minute | about 4 |
| 1 to 3 | 05 | Adsorbates | under 1 minute | about 3 |
| 4 to 6 | 06 | Single point | under 1 minute | about 2 |
| 4 to 6 | 07 | Relaxation | under 2 minutes | about 3 |
| 4 to 6 | 08 | Frequencies | under 1 minute | about 2 |
| 4 to 6 | 09 | NEB | under 1.5 minutes (39 to 83 s) | about 2 |
| 4 to 6 | 10 | Molecular dynamics | about 2.5 minutes (136 to 146 s) | about 3 |
| 7 to 8 | capstone | `projects/ew2gc/capstone.ipynb` | about 2.5 minutes (146 to 166 s) | about 4 |
| 7 to 8 | 11 (optional) | ASPIRE2A: run the same calculation on a supercomputer | no notebook | about 3 plus the first login, which you do together with your supervisor; an estimate, not timed on ASPIRE2A |
| 9 onwards | | project work with your supervisor | | |

- Weeks 1 to 3: modules 00 to 05 add up to about 17 hours, and the three weeks hold about 30 hours; the rest is for reading and for repeating what you did not understand
- Weeks 4 to 6: modules 06 to 10 add up to about 12 hours, and the three weeks hold about 30 hours; use the rest for the reading in the next section, for repeating the exercises you did not understand, and for the weekly meeting
- Weeks 7 to 8: the capstone is about 4 hours, and module 11 adds about 3 hours if you take it, and the two weeks hold about 20 hours; use the rest as in weeks 4 to 6
- From week 9: you work on the project with your supervisor
- If your programme sets a report or another deadline, tell your supervisor its date in your first week, so that the weeks above can be planned around it
- Do the modules in order, and do not start module 06 before module 05 is finished

## Reading that pairs with each module

- The entries come from the reading list of the project, the file `EW2GC_WP4_Onboarding_Reading_List.docx`; it is not in this repository, so ask Juan for a copy
- The reading list sets its own rule for when to read
    - Part A: "Part A is seven items, and it is the whole of what you are expected to read up front", and it "is roughly two to three weeks at a comfortable pace"
    - Part B: each entry carries a trigger, and the list says "Wait for the trigger."
- The table below does not replace that rule; for a Part A entry the module in the left column is the latest point by which to have read it, and for a Part B entry it is the module where the trigger usually arrives
    - Read the Part A entries in the first weeks, as the list says, and have each one read before the module named for it
    - A Part B entry is read at its trigger and not before; the two Part B5 entries have triggers that fall at modules 03 and 04, and the Part B4 entry is read only if and when you join the nanoparticle-shape work
- Read an entry to learn the idea; you do not need to follow every equation

| module | reading |
|---|---|
| 00, 01 | none |
| 02 | Part A, entry 7: Hjorth Larsen, A.; Jørgen Mortensen, J.; Blomqvist, J.; et al. The atomic simulation environment — a Python library for working with atoms. *Journal of Physics: Condensed Matter* 2017, 29, 273002. doi.org/10.1088/1361-648X/aa680e |
| 03 | Part B5: Jain, A.; Ong, S. P.; Hautier, G.; et al. Commentary: The Materials Project. *APL Materials* 2013, 1, 011002. doi.org/10.1063/1.4812323 |
| 04 | Part B5: Ong, S. P.; Richards, W. D.; Jain, A.; et al. Python Materials Genomics (pymatgen). *Computational Materials Science* 2013, 68, 314–319. doi.org/10.1016/j.commatsci.2012.10.028 |
| 04 | Part B4 (the list's trigger is "Read when: you join the nanoparticle-shape work."; read it only if and when that happens; module 04 is where cutting a surface is first done, so the topic becomes relevant there, but that is not a deadline): Tran, R.; Xu, Z.; Radhakrishnan, B.; Winston, D.; Sun, W.; Persson, K. A.; Ong, S. P. Surface energies of elemental crystals. *Scientific Data* 2016, 3, 160080. doi.org/10.1038/sdata.2016.80 |
| 05 | none |
| 06 and 07 | Part A, entry 1: Nørskov, J. K.; Bligaard, T.; Rossmeisl, J.; Christensen, C. H. Towards the computational design of solid catalysts. *Nature Chemistry* 2009, 1, 37–46. doi.org/10.1038/nchem.121 |
| 06 and 07 | Part A, entry 5: Deringer, V. L.; Caro, M. A.; Csányi, G. Machine learning interatomic potentials as emerging tools for materials science. *Advanced Materials* 2019, 31, 1902765. doi.org/10.1002/adma.201902765 |
| 08 | Part A, entry 2: Nørskov, J. K.; Rossmeisl, J.; Logadottir, A.; Lindqvist, L.; Kitchin, J. R.; Bligaard, T.; Jónsson, H. Origin of the overpotential for oxygen reduction at a fuel-cell cathode. *Journal of Physical Chemistry B* 2004, 108, 17886–17892. doi.org/10.1021/jp047349j |
| 09 | none required |
| 10 | Part A, entry 6: Unke, O. T.; Chmiela, S.; Sauceda, H. E.; Gastegger, M.; Poltavsky, I.; Schütt, K. T.; Tkatchenko, A.; Müller, K.-R. Machine learning force fields. *Chemical Reviews* 2021, 121, 10142–10186. doi.org/10.1021/acs.chemrev.0c01111 |
| capstone | Part A, entry 4: Bajdich, M.; García-Mota, M.; Vojvodic, A.; Nørskov, J. K.; Bell, A. T. Theoretical investigation of the activity of cobalt oxides for the electrochemical oxidation of water. *Journal of the American Chemical Society* 2013, 135, 13521–13530. doi.org/10.1021/ja405997s |
| capstone | Part A, entry 3: Man, I. C.; Su, H.-Y.; Calle-Vallejo, F.; Hansen, H. A.; Martínez, J. I.; Inoglu, N. G.; Kitchin, J.; Jaramillo, T. F.; Nørskov, J. K.; Rossmeisl, J. Universality in oxygen evolution electrocatalysis on oxide surfaces. *ChemCatChem* 2011, 3, 1159–1165. doi.org/10.1002/cctc.201000397 |
| 11 | none |

- For the capstone, also read `projects/ew2gc/README.md` and `projects/ew2gc/DECISIONS.md` first
- Two habits from the reading list apply to every paper you read
    - When a paper reports an energy, find what it was referenced against before you compare it with any number of ours
    - When an MLIP and DFT disagree, that disagreement is a result to record, not a problem to tidy away

## What to bring to the weekly meeting

- The notebook you ran this week, with its outputs, so that your supervisor can see the cells and not a description of them
- One number you do not trust, with the reason: for example a value that is far from what the paper gives, or one that changed when you ran the cell again
- One question, written down before the meeting, that you could not answer from the module or the paper

## How to report a result

Every energy or other calculated value you report carries these five items, in this order. A value without them cannot be compared with anything.

1. Model and head: the model name, and the head or task if the model has one (for example `mace` here, and in the project the three models of canon item `C1`)
2. `fmax`: the force convergence criterion of the relaxation, in eV/Å (canon item `C2`)
3. Converged or not converged: say which, every time you quote the number (canon item `K1`); a relaxation that ran out of steps is reported as not converged
4. The reference state: what the energy is measured against, for example the clean slab and a water and hydrogen reference for an adsorption energy
5. The value with its unit

- Example form: "ΔE(*OH) = 0.42 eV; model `mace`; fmax 0.05 eV/Å; converged; referenced to the clean slab and H2O and H2; teaching value, not a project number" (the numbers in this line are made up to show the form)
- The values the project has recorded for its own calculations, and the items it has not recorded, are in `projects/ew2gc/DECISIONS.md`
    - A number from the exercises of this repository is a teaching number, never a project number, and you say so when you report it
    - If an item is not recorded there, ask Juan before you run
