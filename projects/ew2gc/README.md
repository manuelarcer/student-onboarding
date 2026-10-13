# EW2GC, work package 4: Co oxides for the oxygen evolution reaction

This folder is the project track of the course. It says what the project is, what your work in it is, which decisions the project has recorded, and ends in a capstone notebook that applies modules 00 to 10 to the project's own material.

As the top README's "Status of this course" says, this is a first version for practice with the tools: its science, the capstone's results included, is not checked to the standard of a paper and may be wrong, and it is settled with your supervisor in your one-to-one meetings.

## The project in one page

- E-Waste-to-Green-Catalysis, EW2GC, is a publicly funded research project that recovers cobalt, nickel and manganese from spent lithium-ion batteries and converts them into oxide electrocatalysts
    - It has four work packages (WP, source: slide 2 of the onboarding deck named below)
    - WP1: recovery of metals from spent cathodes by leaching in deep-eutectic solvents, precipitation and thermal annealing
    - WP2: structural and compositional characterisation by SEM, XRD and TEM
    - WP3: electrochemical testing for hydrogen evolution, oxygen evolution and oxygen reduction
    - WP4, the one this repository is for: atomistic simulation of the surface, to identify the active sites and to quantify the effect of defects, impurities and dopants
- The first reaction is oxygen evolution, OER, the anode half-reaction of water electrolysis (slide 3)
    - Two water molecules are oxidised to one O2 molecule in four steps, each leaving an intermediate bound to the surface: `2H2O → *OH → *O → *OOH → O2`
    - The asterisk marks a species adsorbed on the surface, and each step releases one proton and one electron, four in all per O2 molecule
    - Activity is set by how strongly the intermediates bind: too weak limits the early steps, too strong limits the later ones
- What WP4 computes (slides 3 to 5)
    - The adsorption energies of `*OH`, `*O` and `*OOH` on each surface, the energy of each step, and from them the overpotential, the voltage above the thermodynamic minimum of 1.23 V that the largest step needs; a lower overpotential is a better catalyst
    - The platform that automates the sequence is CATPLAT, the group's own: bulk crystal from the Materials Project, relaxed; facets and terminations, each relaxed; adsorbates placed on each distinct site; then the energetics
    - Co3O4 and CoOOH are the two cobalt oxides whose surface energies and equilibrium shapes the project computes (slide 6), and they are the two materials of the capstone
- Two directions are open (slide 6), and both ask what the catalyst is like in contact with the electrolyte and not as a surface in vacuum
    - Equilibrium nanoparticle shape: surface energies of each facet give the shape, and the open question is whether explicit water changes the distribution of facets found in vacuum
    - OER energetics under solvation: the adsorption energies computed with explicit water present and not on a bare slab, and the open question is how large the correction is against the vacuum result

## Where the onboarding material is

- The onboarding deck is the file `EW2GC_WP4_-_Student_Onboarding.pptx` and the reading list is the file `EW2GC_WP4_Onboarding_Reading_List.docx`; they are not in this repository, so ask Juan for copies
- The reading list is seven items to read first (Part A) and a longer list grouped by topic (Part B), each with a trigger for when to read it; this track cites its entries as "Part A, entry N"
    - Part A, entry 2 is the computational hydrogen electrode, which the capstone uses for the form of its adsorption energy
    - Part A, entry 6 is the review of how machine-learning force fields fail, which section 1 of the capstone is a small practice of

## How you will compute

- Juan's note of 2026-10-12: you will most likely work on your own computer, or on a free personal ASPIRE2A account as module 11 sets up
    - You will most likely not be added to the group's ASPIRE2A projects, and you cannot use VASP, so every calculation of this track is a machine-learning potential calculation
- The models the project runs, canon `C1` in `DECISIONS.md`: `uma-s-1p2` with `--uma-task oc25`, `mace-mh-1`, and `chgnet`
- The course uses MACE-MP-0 instead, and it is not one of those three
    - Module 00 installs one model only, because the packages of the different models need different versions of `torch` and break each other when installed together, and MACE-MP-0 is the one it installs
    - The project itself used MACE-MP-0 in its first phase and then left it for `mace-mh-1`; the reason it records is in line 17 of `calculations/explicit_solvation/PLAN.md` of the project folder, and section 1 of the capstone sets its own CoOOH result beside that note
    - So a number from these exercises is a teaching number and never a project number

## What is in this folder

- `DECISIONS.md`: a dated copy of the project's recorded decisions and of the group's master canon, and what to do about an item that is not recorded
- `examples/`: files copied from the project, with a README that says what each one is and what to look at in it
- `capstone.ipynb`: the capstone; it needs modules 00 to 10, `../../structures/` and `../../scripts/onboarding_structures.py`, and its outputs go to `work/`, which is not committed
    - Time to run: about 2.5 minutes, 146 to 166 s over five executions of the notebook (measured 146.5, 165.7, 147.9, 148.8 and 159.0 s, the last two in the verification run of 2026-10-12, macOS on Apple Silicon, with the model weights and the package caches already warm; a first run on a cold machine is slower, an effect module 06's README measures on its own notebook)
    - Ten commands run in it, nine of them `mlip optimize run` and one the project's slab script, and the times below are the lowest and the highest of the five executions
    - The three bulk relaxations take 8.2 to 8.8 s for the 56-atom Co3O4 cell, 4.3 to 5.6 s for CoOOH from the file as served and 5.6 to 6.1 s for CoOOH with the H moved; the slab script takes 3.7 to 4.3 s
    - The relaxation of the clean 166-atom slab takes 9.7 to 10.8 s, and the three relaxations of the slab with `*OH` in each execution, fifteen in all, take 30.6 to 50.7 s each; H2O takes 4.5 to 7.9 s and H2 takes 3.8 to 15.5 s, the upper end of each coming from the last of the five executions, whose cause this page did not look into
    - The machine was shared with other sessions during these executions, with a load average of 3.1 to 6.4 at the start and the end of each one, so read the times as an upper range and not as what an idle laptop gives
    - The MACE-MP-0 weights, about 45 MB, were downloaded by step 10 of module 00 and sit in `~/.cache/mace/`, so this notebook downloads nothing
    - Time to work through it: about 4 hours, reading every cell and changing a setting and running it again
