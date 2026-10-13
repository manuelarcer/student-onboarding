import pytest
from ase.constraints import FixAtoms
from onboarding_structures import pt111_slab, pt111_with_adsorbate, molecule_in_box


def test_slab_size_and_fixed_layer():
    s = pt111_slab(size=(3, 3, 3), vacuum=10.0, fix_bottom_layers=1)
    assert len(s) == 27
    fixed = [c for c in s.constraints if isinstance(c, FixAtoms)]
    assert fixed and len(fixed[0].index) == 9
    assert s.cell.lengths()[0] > 7.5      # canon S6 minimum in-plane length
    # the frozen atoms must be the bottom layer, not the top one
    z = s.positions[:, 2]
    fixed_idx = set(fixed[0].index)
    free_idx = [i for i in range(len(s)) if i not in fixed_idx]
    assert z[list(fixed_idx)].max() < z[free_idx].min()


def test_adsorbate_added_above_surface():
    s = pt111_with_adsorbate("OH", "fcc")
    assert s.get_chemical_symbols()[-2:] == ["O", "H"]
    z_top = max(a.position[2] for a in s if a.symbol == "Pt")
    assert s[-2].position[2] > z_top + 1.0


@pytest.mark.parametrize("site", ["ontop", "fcc"])
def test_adsorbate_heights_per_site(site):
    # the height is per site, so the Pt-O bond stays near its equilibrium length
    s = pt111_with_adsorbate("O", site)
    i_O = [i for i, a in enumerate(s) if a.symbol == "O"][0]
    pt_indices = [i for i, a in enumerate(s) if a.symbol == "Pt"]
    d = s.get_distances(i_O, pt_indices, mic=True).min()
    assert 1.8 < d < 2.1, f"{site}: nearest Pt-O is {d:.2f} A"


def test_ooh_template_oh_bond():
    s = pt111_with_adsorbate("OOH", "ontop")
    assert s.get_chemical_symbols()[-3:] == ["O", "O", "H"]
    d_OH = s.get_distance(len(s) - 2, len(s) - 1, mic=True)
    assert 0.95 < d_OH < 1.00, f"O-H is {d_OH:.3f} A"


def test_molecule_box():
    m = molecule_in_box("H2O")
    assert len(m) == 3 and abs(m.cell.lengths()[0] - 12.0) < 1e-6
