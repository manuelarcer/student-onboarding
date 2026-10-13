"""Small builders used by the onboarding notebooks from module 05 onward.

They package what modules 02, 04 and 05 teach by hand, so later notebooks start from a
known structure in one line. Teaching values throughout: three layers, one frozen,
10 Å vacuum, adsorbate heights per species and per site. A project decides its own
(canon S2, S5, S8), and the heights are starting guesses only, meant to be relaxed.
"""
from ase import Atoms
from ase.build import fcc111, add_adsorbate, molecule
from ase.constraints import FixAtoms

A_PT = 3.92   # Å, ASE's reference lattice constant for fcc Pt


def pt111_slab(size=(3, 3, 3), vacuum=10.0, fix_bottom_layers=1) -> Atoms:
    slab = fcc111("Pt", size=size, a=A_PT, vacuum=vacuum)
    tags = slab.get_tags()                     # 1 = top layer, increasing downward
    n_layers = size[2]
    fixed = [i for i, t in enumerate(tags) if t > n_layers - fix_bottom_layers]
    slab.set_constraint(FixAtoms(indices=fixed))
    slab.pbc = (True, True, False)
    return slab


_ADS = {
    "O":   (Atoms("O"), 0),
    "OH":  (Atoms("OH", positions=[[0, 0, 0], [0, 0, 0.97]]), 0),
    "OOH": (Atoms("OOH", positions=[[0, 0, 0], [0.9, 0, 1.1], [1.75, 0, 0.63]]), 0),
}

# Å above the top layer, per species and per site. A hollow site sits the adsorbate
# lower than an ontop site because it already gains distance from each Pt sideways.
# Starting guesses only — relax them.
_HEIGHT = {
    "O":   {"ontop": 1.85, "bridge": 1.45, "fcc": 1.30, "hcp": 1.30},
    "OH":  {"ontop": 1.95, "bridge": 1.55, "fcc": 1.45, "hcp": 1.45},
    "OOH": {"ontop": 2.00, "bridge": 1.65, "fcc": 1.55, "hcp": 1.55},
}


def pt111_with_adsorbate(species: str, site: str, size=(3, 3, 3), vacuum=10.0, height=None) -> Atoms:
    slab = pt111_slab(size=size, vacuum=vacuum)
    # copy: ASE's add_adsorbate moves the object it is given, template included
    ads = _ADS[species][0].copy()
    anchor = _ADS[species][1]
    h = _HEIGHT[species][site] if height is None else height
    add_adsorbate(slab, ads, height=h, position=site, mol_index=anchor)
    return slab


def molecule_in_box(name: str, box=12.0) -> Atoms:
    m = molecule(name)
    m.set_cell([box, box, box])
    m.center()
    m.pbc = True
    return m
