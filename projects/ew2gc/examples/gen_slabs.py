#!/usr/bin/env python3
# PROVENANCE, added when this file was copied into the onboarding repository.
# Everything below the next blank line is the project's file, unchanged.
#   Source:        calculations/explicit_solvation/scripts/phase2_surface/gen_slabs.py
#                  (path relative to the EWaste2GreenCat project folder)
#   Copied on:     2026-10-12
#   File modified: 2026-07-07 14:17
#   SHA-256 of the original: c26d03a8cd3be574e9a3f33ef308df8eeb96aaf5f125680bc61033aa2e5e3121
# This is a dated snapshot. gen_rs_slabs.py imports four functions from it. The project's
# own file is the authoritative one.

"""Phase 2 slab generator with two frameworks (PLAN §1):

  - **sym_stoich** (CoOOH default): keep terminations that are both symmetric
    and stoichiometric. Single slab per termination, simple γ formula.

  - **tasker_flip** (Co3O4 default): the spinel has no naturally cleaved
    symmetric+stoichiometric slab on any facet. Each stoichiometric
    cleavage is relaxed twice — once with the bottom half fixed (member
    A) and once with the top half fixed (member B). The two relaxations
    sample the two surface terminations of the same cleavage; their
    energies enter γ via γ = (E_A + E_B − 2·n·E_bulk) / (4·A), with no
    need for shift-pair period detection. Supersedes the older
    tasker_pair scheme (retired 2026-05-15): pair A and pair B are
    spatial mirror images of one another, so a single cleavage plus two
    masks captures the same thermodynamics with half the cleavages
    enumerated.

Outputs (per surviving slab):
    <output_base>/<material>/<mlip>/<miller>_<term_label>/POSCAR
where `term_label` is `t<i>` for sym_stoich and `f<cleavage_id><A|B>` for
tasker_flip (e.g. `f0A`, `f0B`), and `<NaxNb>` is the in-plane supercell
multiplier picked to satisfy ``--min-lateral-A`` (e.g. ``2x2``, ``2x1``,
``1x1``). Pass ``--allow-lateral-A`` to relax the threshold for the
(1 1 0)-style judgement-call facets where a strict 10 Å would force a
4× atom inflation.

Metadata CSV at `<output_base>/slabs_index.csv` with columns including
`framework`, `pair_id`, `pair_member`, `partner_shift`, plus
`lateral_label`, `lateral_a_A`, `lateral_b_A` for the tiled cell.

Usage
-----
    # Co3O4 (100) — auto-selects tasker_flip (one cleavage, two masks)
    python scripts/gen_slabs.py \
        --bulk 00_mlip_validation/Co3O4_bulk/uma-s/opt_final.vasp \
        --material Co3O4 --mlip uma-s --miller 1 0 0 \
        --thicknesses 6 8 10 12 --ftol 0.05

    # CoOOH (001) — auto-selects sym_stoich
    python scripts/gen_slabs.py \
        --bulk 00_mlip_validation/CoOOH_bulk/uma-s/opt_final.vasp \
        --material CoOOH --mlip uma-s --miller 0 0 1 \
        --thicknesses 6 8 10 12 --ftol 0.05
"""
from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

import numpy as np
from pymatgen.core import Composition, Structure
from pymatgen.core.surface import SlabGenerator

_COMPCAT = Path("/Users/juar/github/work/compcatalysis-skills/"
                "surface-generation/scripts")
if _COMPCAT.is_dir():
    sys.path.insert(0, str(_COMPCAT))
import generate_slabs as gs  # noqa: E402


DEFAULT_FRAMEWORK = {"CoOOH": "sym_stoich", "Co3O4": "tasker_flip"}

CSV_COLUMNS = [
    "material", "mlip", "miller", "framework",
    "term_label", "pair_id", "pair_member", "shift", "partner_shift",
    "target_A", "actual_A", "thick_label",
    "lateral_label", "lateral_a_A", "lateral_b_A",
    "n_atoms", "formula",
    "cell_a", "cell_b", "area_A2", "n_fixed",
    "is_symmetric", "is_stoichiometric",
]


def thick_label_for(slab) -> str:
    """Single source of truth for the slab directory name.

    Measured on the *orthogonalized* slab so the z-extent is the true
    perpendicular thickness (the surface normal along +z), not the inflated
    z-projection of a tilted high-Miller cell. Rounds the raw float, not its
    CSV-stringified form, so downstream consumers read this column rather
    than re-rounding.
    """
    return f"thick{int(round(measure_z_extent(orthogonalize_structure(slab)))):02d}A"


def measure_z_extent(struct) -> float:
    z = np.array([site.coords[2] for site in struct])
    return float(z.max() - z.min())


def upsert_csv(csv_path: Path, new_rows: list[dict]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    pk = ("material", "mlip", "miller", "framework",
          "term_label", "target_A", "lateral_label")
    new_keys = {tuple(r[k] for k in pk) for r in new_rows}
    existing: list[dict] = []
    if csv_path.exists():
        with csv_path.open(newline="") as f:
            existing = [row for row in csv.DictReader(f)
                        if tuple(row.get(k, "") for k in pk) not in new_keys]
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        for r in existing:
            w.writerow(r)
        for r in new_rows:
            w.writerow(r)


def slabs_for_target(bulk: Structure, miller, target_A: float,
                     vacuum: float, ftol: float) -> list:
    gen = SlabGenerator(bulk, miller_index=miller,
                        min_slab_size=target_A, min_vacuum_size=vacuum,
                        center_slab=True, lll_reduce=True, primitive=True)
    slabs = gen.get_slabs(ftol=ftol, filter_out_sym_slabs=False,
                           symmetrize=False)
    slabs = gs.filter_unique_top_surfaces(slabs)
    slabs.sort(key=lambda s: float(s.shift))
    return slabs


def orthogonalize_structure(struct: Structure, tol_deg: float = 1e-3) -> Structure:
    """Return a copy of ``struct`` with a, b in xy and c along +z.

    Rigid rotation aligning (a × b) with +z, followed by a tiny snap that
    drops residual in-plane components of c. The snap is energy-preserving
    for a slab with vacuum along c (no atom near the c-faces): atom
    Cartesian coordinates are untouched; only the periodic image across c
    shifts laterally, and the vacuum gap absorbs that shift. Site
    properties (incl. selective_dynamics) are carried through unchanged.
    """
    L = np.array(struct.lattice.matrix)
    a, b, c = L[0], L[1], L[2]
    normal = np.cross(a, b)
    n_norm = float(np.linalg.norm(normal))
    if n_norm < 1e-12:
        raise ValueError("Degenerate cell: a × b is zero.")
    n_hat = normal / n_norm
    cos_ang = float(np.clip(n_hat[2], -1.0, 1.0))
    ang_deg = float(np.degrees(np.arccos(cos_ang)))

    coords = np.array([site.coords for site in struct])

    if ang_deg > tol_deg:
        axis = np.array([n_hat[1], -n_hat[0], 0.0])  # n_hat × ẑ
        ax_norm = float(np.linalg.norm(axis))
        if ax_norm < 1e-12:
            axis = np.array([1.0, 0.0, 0.0])
        else:
            axis = axis / ax_norm
        theta = np.radians(ang_deg)
        K = np.array([[0.0, -axis[2], axis[1]],
                      [axis[2], 0.0, -axis[0]],
                      [-axis[1], axis[0], 0.0]])
        R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
        L = L @ R.T
        coords = coords @ R.T

    # Snap residual numerical components and rebuild the structure
    L[0] = [L[0, 0], L[0, 1], 0.0]
    L[1] = [L[1, 0], L[1, 1], 0.0]
    L[2] = [0.0, 0.0, abs(L[2, 2])]

    new_struct = Structure(
        lattice=L,
        species=[site.specie for site in struct],
        coords=coords,
        coords_are_cartesian=True,
        site_properties=dict(struct.site_properties),
        to_unit_cell=True,
    )
    return new_struct


def compute_supercell_mult(slab, min_axis_A: float = 7.5,
                           min_area_A2: float = 100.0,
                           edge_tol_A: float = 0.4) -> tuple[int, int, list]:
    """Pick (na, nb) for the in-plane supercell, robust across MLIPs.

    Two criteria: every tiled axis ``na·|a|`` / ``nb·|b|`` must reach
    ``min_axis_A`` (a deliberately loose ~7.5 Å floor), and the tiled area
    must reach ``min_area_A2`` (~100 Å²). The loose floor is the fix for the
    cross-MLIP inconsistency (e.g. (2 1 0): uma-s' b sat just under a strict
    10 Å and got doubled while mace/chgnet did not) — a ~7.5 Å floor is far
    from the ~10 Å lattice lengths, so the ±0.1 Å differences between MLIPs
    can no longer flip the tiling. The area target then tops up thin cells.

    Returns ``(na, nb, edge_notes)``. ``edge_notes`` lists any axis sitting
    within ``edge_tol_A`` of a tiling flip, or a final area within ~8 Å² of
    the target — i.e. the borderline cases where a slightly different MLIP
    lattice *could* still diverge. The caller surfaces these for a human
    decision (leave it, or tile up). ``min_axis_A <= 0`` keeps the primitive
    cell.
    """
    av = np.asarray(slab.lattice.matrix[0])
    bv = np.asarray(slab.lattice.matrix[1])
    a = float(np.linalg.norm(av))
    b = float(np.linalg.norm(bv))

    def area(na, nb):
        return float(np.linalg.norm(np.cross(na * av, nb * bv)))

    if min_axis_A <= 0 and min_area_A2 <= 0:
        return 1, 1, []

    na = max(1, int(np.ceil(min_axis_A / a - 1e-9))) if min_axis_A > 0 else 1
    nb = max(1, int(np.ceil(min_axis_A / b - 1e-9))) if min_axis_A > 0 else 1
    # top up the shorter tiled axis until the area target is met
    guard = 0
    while area(na, nb) < min_area_A2 and guard < 50:
        if na * a <= nb * b:
            na += 1
        else:
            nb += 1
        guard += 1

    notes = []
    for name, length, n in (("a", a, na), ("b", b, nb)):
        # length at which ceil(min_axis/length) would drop n by one
        if min_axis_A > 0:
            boundary = min_axis_A / n            # length just below -> n+1
            if abs(length - boundary) < edge_tol_A:
                notes.append(f"{name}={length:.2f} Å sits within "
                             f"{edge_tol_A} Å of a tiling flip (n{name}={n})")
    if abs(area(na, nb) - min_area_A2) < 8.0:
        notes.append(f"area={area(na, nb):.0f} Å² is within 8 Å² of the "
                     f"{min_area_A2:.0f} Å² target")
    return na, nb, notes


def write_slab_with_constraints(slab, out_dir: Path, fix_bottom: float,
                                fix_top: bool = False,
                                na: int = 1, nb: int = 1):
    """Write a POSCAR with a FixAtoms-style selective_dynamics mask.

    ``fix_top=False`` (default) fixes the bottom ``fix_bottom`` fraction.
    ``fix_top=True`` inverts the mask — fixes the top ``fix_bottom`` fraction
    instead. Used by tasker_flip to emit a complementary partner per cleavage.

    Order matters: the slab is **orthogonalized first** (a, b in xy; c along
    +z) so that +z is the surface normal, and only *then* is the freeze mask
    selected by Cartesian z. Applying the mask before orthogonalization would
    select along the tilted-cell z, which for a high-Miller facet is not the
    surface normal — scrambling the frozen region after rotation. If ``na`` or
    ``nb`` exceed 1 the cell is tiled afterward; selective-dynamics flags
    propagate through the supercell, so the fixed fraction is preserved.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out = orthogonalize_structure(slab.copy())
    if fix_bottom > 0:
        out, _ = gs.apply_selective_dynamics(out, fix_bottom)
        if fix_top:
            sd = out.site_properties["selective_dynamics"]
            inverted = [[not v for v in row] for row in sd]
            out.add_site_property("selective_dynamics", inverted)
    if na > 1 or nb > 1:
        out.make_supercell([na, nb, 1])
    sd = out.site_properties.get("selective_dynamics",
                                  [[True, True, True]] * out.num_sites)
    n_fixed = sum(1 for row in sd if not any(row))
    poscar = out_dir / "POSCAR"
    out.to(filename=str(poscar), fmt="poscar")
    return poscar, n_fixed


def slab_row(slab, *, material, mlip, miller_str, framework, term_label,
             pair_id, pair_member, partner_shift, target_A, n_fixed,
             bulk_formula, na: int = 1, nb: int = 1):
    a_prim = float(slab.lattice.a)
    b_prim = float(slab.lattice.b)
    area_prim = float(np.linalg.norm(np.cross(slab.lattice.matrix[0],
                                               slab.lattice.matrix[1])))
    a_super = a_prim * na
    b_super = b_prim * nb
    area_super = area_prim * na * nb
    n_atoms_super = slab.num_sites * na * nb
    return {
        "material": material,
        "mlip": mlip,
        "miller": miller_str,
        "framework": framework,
        "term_label": term_label,
        "pair_id": pair_id if pair_id is not None else "",
        "pair_member": pair_member,
        "shift": f"{float(slab.shift):.4f}",
        "partner_shift": (f"{partner_shift:.4f}"
                          if partner_shift is not None else ""),
        "target_A": f"{target_A:.1f}",
        "actual_A": f"{measure_z_extent(orthogonalize_structure(slab)):.3f}",
        "thick_label": thick_label_for(slab),
        "lateral_label": f"{na}x{nb}",
        "lateral_a_A": f"{a_super:.4f}",
        "lateral_b_A": f"{b_super:.4f}",
        "n_atoms": n_atoms_super,
        "formula": Composition(slab.composition).reduced_formula,
        "cell_a": f"{a_super:.4f}",
        "cell_b": f"{b_super:.4f}",
        "area_A2": f"{area_super:.3f}",
        "n_fixed": n_fixed,
        "is_symmetric": slab.is_symmetric(),
        "is_stoichiometric": (Composition(slab.composition).reduced_formula
                              == bulk_formula),
    }


def write_facet_readme(csv_path: Path, output_base: Path, material: str,
                       miller_str: str):
    """Write ``<material>/<miller>/README.md``: average thickness on top, then a
    per-termination table. Aggregated from ``slabs_index.csv`` so it reflects
    every MLIP generated for the facet — the thickness lives in the CSV (and
    this README), not in the folder name anymore."""
    if not csv_path.exists():
        return None
    with csv_path.open(newline="") as f:
        rows = [r for r in csv.DictReader(f)
                if r["material"] == material and r["miller"] == miller_str]
    if not rows:
        return None
    thicks = [float(r["actual_A"]) for r in rows if r.get("actual_A")]
    avg, lo, hi = statistics.mean(thicks), min(thicks), max(thicks)
    spread = f"{lo:.1f}–{hi:.1f}" if (hi - lo) > 0.15 else f"{avg:.1f}"
    lats = sorted({r["lateral_label"] for r in rows})
    by_term: dict[str, list] = {}
    for r in rows:
        by_term.setdefault(r["term_label"], []).append(r)

    out = [f"# {material} ({' '.join(miller_str)}) slabs", ""]
    out.append(f"**Average slab thickness: {avg:.1f} Å** "
               f"(range {spread} Å; lateral {', '.join(lats)}).")
    out.append("")
    out.append("Thickness = relaxed-cell atomic z-extent perpendicular to the "
               "surface. It is no longer encoded in the path; this table is the "
               "record. Layout: one subfolder per termination, one per MLIP "
               "inside (`<term>/<mlip>/`).")
    out.append("")
    out.append("| termination | thickness (Å) | lateral | area (Å²) | n_atoms | MLIPs |")
    out.append("|---|---|---|---|---|---|")
    for term in sorted(by_term):
        rs = by_term[term]
        t = statistics.mean(float(r["actual_A"]) for r in rs)
        lat = ",".join(sorted({r["lateral_label"] for r in rs}))
        area = ",".join(sorted({str(round(float(r["area_A2"]))) for r in rs}))
        nat = ",".join(sorted({str(r["n_atoms"]) for r in rs}))
        mlips = ",".join(sorted({r["mlip"] for r in rs}))
        out.append(f"| {term} | {t:.1f} | {lat} | {area} | {nat} | {mlips} |")
    readme = output_base / material / f"README_{miller_str}.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text("\n".join(out) + "\n")
    return readme


def run_sym_stoich(bulk, miller, miller_str, args, target_A) -> list[dict]:
    bulk_formula = Composition(bulk.composition).reduced_formula
    slabs = slabs_for_target(bulk, miller, target_A, args.vacuum, args.ftol)
    rows = []
    for term_id, s in enumerate(slabs):
        if not s.is_symmetric():
            continue
        if Composition(s.composition).reduced_formula != bulk_formula:
            continue
        na, nb, edge_notes = compute_supercell_mult(
            s, args.min_axis_A, args.min_area_A2)
        for note in edge_notes:
            print(f"  [EDGE] ({miller_str}) t{term_id} {na}x{nb}: {note}")
        term_label = f"t{term_id}"
        out_dir = (args.output_base / args.material / args.mlip /
                   f"{miller_str}_{term_label}")
        poscar, n_fixed = write_slab_with_constraints(s, out_dir,
                                                       args.fix_bottom,
                                                       na=na, nb=nb)
        rows.append(slab_row(
            s, material=args.material, mlip=args.mlip, miller_str=miller_str,
            framework="sym_stoich", term_label=term_label,
            pair_id=None, pair_member="solo", partner_shift=None,
            target_A=target_A, n_fixed=n_fixed, bulk_formula=bulk_formula,
            na=na, nb=nb,
        ))
        print(f"  [target {target_A:5.1f} Å] {term_label} (shift "
              f"{float(s.shift):.4f}) sym+stoich {na}x{nb} -> {poscar}")
    return rows


def run_tasker_flip(bulk, miller, miller_str, args, target_A) -> list[dict]:
    """Flip-pair Tasker III γ: one cleavage, two relaxations with
    complementary FixAtoms masks (bot-fixed + top-fixed). Avoids the period
    detector entirely. γ = (E_bot + E_top − 2·n·E_bulk) / (4·A).
    """
    bulk_formula = Composition(bulk.composition).reduced_formula
    slabs = slabs_for_target(bulk, miller, target_A, args.vacuum, args.ftol)
    stoich = [s for s in slabs
              if Composition(s.composition).reduced_formula == bulk_formula]
    print(f"  [target {target_A:5.1f} Å] {len(stoich)} stoich terms — "
          f"flip-pair (bot-fixed + top-fixed per cleavage)")

    rows = []
    for term_id, s in enumerate(stoich):
        na, nb, edge_notes = compute_supercell_mult(
            s, args.min_axis_A, args.min_area_A2)
        for note in edge_notes:
            print(f"      [EDGE] ({miller_str}) f{term_id} {na}x{nb}: {note}")
        for member, fix_top in (("A", False), ("B", True)):
            term_label = f"f{term_id}{member}"
            out_dir = (args.output_base / args.material / args.mlip /
                       f"{miller_str}_{term_label}")
            poscar, n_fixed = write_slab_with_constraints(
                s, out_dir, args.fix_bottom, fix_top=fix_top,
                na=na, nb=nb)
            rows.append(slab_row(
                s, material=args.material, mlip=args.mlip,
                miller_str=miller_str, framework="tasker_flip",
                term_label=term_label, pair_id=term_id, pair_member=member,
                partner_shift=None, target_A=target_A,
                n_fixed=n_fixed, bulk_formula=bulk_formula,
                na=na, nb=nb,
            ))
            face = "top-fixed" if fix_top else "bot-fixed"
            print(f"      {term_label} (shift {float(s.shift):.4f}, "
                  f"{face}, {na}x{nb}) -> {poscar}")
    return rows


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bulk", type=Path, required=True)
    p.add_argument("--material", required=True, choices=["Co3O4", "CoOOH"])
    p.add_argument("--mlip", required=True,
                   choices=["uma-s", "uma-s-oc20", "uma-m",
                            "mace-mh-1", "chgnet"])
    p.add_argument("--miller", nargs=3, type=int, required=True,
                   metavar=("H", "K", "L"))
    p.add_argument("--thicknesses", nargs="+", type=float, required=True,
                   help="Target thicknesses in Å (atomic z-extent).")
    p.add_argument("--vacuum", type=float, default=15.0)
    p.add_argument("--ftol", type=float, default=0.05)
    p.add_argument("--fix-bottom", type=float, default=0.5)
    p.add_argument("--output-base", type=Path, default=Path("02_vacuum_slabs"))
    p.add_argument("--csv", type=Path, default=None)
    p.add_argument("--framework", choices=["auto", "sym_stoich",
                                            "tasker_flip"],
                   default="auto",
                   help=("Override the per-material default framework. "
                         "tasker_flip handles Tasker III polar surfaces; "
                         "the older tasker_pair scheme was retired 2026-05-15."))
    p.add_argument("--min-axis-A", dest="min_axis_A", type=float, default=7.5,
                   help=("Minimum length (Å) of each tiled in-plane axis. "
                         "Default 7.5 — a deliberately loose floor so the "
                         "~0.1 Å lattice differences between MLIPs cannot "
                         "flip the supercell tiling (the (2 1 0) bug). "
                         "Pass 0 to disable the axis floor."))
    p.add_argument("--min-area-A2", dest="min_area_A2", type=float,
                   default=100.0,
                   help=("Minimum tiled in-plane area (Å²). Default 100. The "
                         "shorter tiled axis is grown until this is met."))
    args = p.parse_args()

    framework = (DEFAULT_FRAMEWORK[args.material]
                 if args.framework == "auto" else args.framework)
    miller = tuple(args.miller)
    miller_str = "".join(str(x) for x in miller)
    csv_path = args.csv or (args.output_base / "slabs_index.csv")

    bulk = Structure.from_file(str(args.bulk))
    print(f"Bulk: {bulk.composition.reduced_formula} "
          f"({bulk.num_sites} atoms) | facet ({miller_str}) | "
          f"framework {framework} | targets {args.thicknesses} | "
          f"min axis {args.min_axis_A:.1f} Å | min area {args.min_area_A2:.0f} Å²")

    rows = []
    for target_A in args.thicknesses:
        if framework == "sym_stoich":
            rows.extend(run_sym_stoich(bulk, miller, miller_str, args,
                                        target_A))
        elif framework == "tasker_flip":
            rows.extend(run_tasker_flip(bulk, miller, miller_str, args,
                                         target_A))
        else:
            raise ValueError(f"Unknown framework {framework}")

    if len(args.thicknesses) > 1:
        print("  [WARN] multiple --thicknesses with the flat layout collide "
              "(no <thick> dir level); generate one target per facet for "
              "production, or use a separate --output-base per thickness.")

    if rows:
        upsert_csv(csv_path, rows)
        readme = write_facet_readme(csv_path, args.output_base, args.material,
                                    miller_str)
        print(f"\nWrote {len(rows)} slabs. CSV: {csv_path}")
        if readme:
            print(f"Facet README: {readme}")
    else:
        print("\nNo slabs survived for any target.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
