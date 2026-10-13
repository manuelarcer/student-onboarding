#!/usr/bin/env python3
# PROVENANCE, added when this file was copied into the onboarding repository.
# Everything below the next blank line is the project's file, unchanged.
#   Source:        calculations/explicit_solvation/scripts/phase2_surface/gen_rs_slabs.py
#                  (path relative to the EWaste2GreenCat project folder)
#   Copied on:     2026-10-12
#   File modified: 2026-10-12 18:22
#   SHA-256 of the original: fadea57790cb33170993db55c01bd52348041f16060630761ac2b6360f76129c
# This is a dated snapshot of a file under active development. The project's own
# file is the authoritative one.

"""Symmetric slab generator for Reuter-Scheffler surface energies, one slab per FACE.

Canon: S1 (cleavage settings), S3 (symmetric slabs, R&S), S4 (one symmetric slab
per distinct face, each MLIP enumerated from its own bulk), E-p2/E-p3.

Why faces, not cleavages
------------------------
A symmetric slab exposes one face on both sides, so its gamma belongs to that face
alone. The unit to enumerate is therefore the distinct face. Every stoichiometric
cut has a top face and a bottom face; both are collected, grouped into face classes,
and each class is built exactly once. Collecting both sides keeps the enumeration
complete even for a bulk without an inversion centre.

Algorithm (per material, MLIP, facet)
-------------------------------------
1. Enumerate ALL raw cuts with the S1 SlabGenerator settings (no top-face filter),
   keep the bulk-stoichiometric ones.
2. Orthogonalize each cut (surface normal along +z) and fingerprint its top and its
   bottom face: per layer, the atoms per unit area of each (element, coordination
   number) pair, plus the layer depths, down to ``--face-depth-A``. Faces with
   equal fingerprints form one class ``r<k>``.
3. For each class, take one cut carrying that face (prefer the top side, then the
   lowest shift) and trim atoms one at a
   time from the OTHER side until the slab is symmetric. This is pymatgen's
   ``nonstoichiometric_symmetrized_slab`` loop, run for the one side needed. The
   untouched side is never modified, so the doubled face is the target face. A cut
   that is already symmetric is used as is (S3: a symmetric stoichiometric slab is
   valid, slope zero in mu).
4. If trimming fails (pymatgen "too many sites removed"), re-cut at
   ``--sym-target-A + n*--sym-step-A`` up to ``--sym-max-A``.
5. Validate: pymatgen symmetry, top and bottom fingerprints equal, and the doubled
   face equal to the target face. The fingerprint includes each atom's
   coordination number, so faces with equal layer compositions but a different
   in-plane arrangement are kept apart.

Chemistry (general, any bulk)
-----------------------------
With a reference element R (default: the least electronegative element of the
bulk), n_fu = N_R / nu_R and, for every other element X, the excess
Delta_X = N_X - n_fu * nu_X. Then

    gamma(mu) = [E_slab - n_fu * E_bulk_fu - sum_X Delta_X * mu_X] / (2A)

For Co3O4 (R = Co) this is E-p2. For CoOOH (R = Co) the excesses are Delta_O and
Delta_H, so gamma depends on mu_O and mu_H.

Output
------
    <output_base>/<material>/<mlip>/<miller>_r<k>/POSCAR   (all atoms free, E-p3)
    <audit>  one row per face class, including faces that failed (status column)

pymatgen must be <= 2025.6.14 (S1); the version is recorded in every audit row.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import pymatgen.core as pmg_core
from pymatgen.core import Composition, Element, Structure
from pymatgen.core.surface import SlabGenerator

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from gen_slabs import (  # noqa: E402
    compute_supercell_mult,
    measure_z_extent,
    orthogonalize_structure,
    slabs_for_target,
)

PMG_MAX_VERSION = (2025, 6, 14)

# Canon S1 settings per material (2026-10-12). Keys are path labels; aliases map the
# bulk reduced formula to a label. A material without an entry must get --ftol on the
# command line: there is no silent fallback.
MATERIAL_DEFAULTS = {
    "Co3O4": {"ftol": 0.005, "keep_bonds": [], "prod_ftol": 0.05},
    "CoOOH": {"ftol": 0.02, "keep_bonds": ["O-H:1.2"], "prod_ftol": 0.007},
}
MATERIAL_ALIASES = {"CoHO2": "CoOOH"}

AUDIT_COLUMNS = [
    "material", "mlip", "miller", "face_label", "status", "face_key",
    "n_cuts_with_face", "carriers", "prod_carriers", "source_shift", "source_side",
    "sym_target_A", "n_trimmed",
    "n_atoms", "composition", "ref_element", "n_fu", "excess",
    "excess_per_nm2_per_face", "area_A2", "lateral_label", "actual_A",
    "is_symmetric_pmg", "faces_match", "doubled_face_ok", "is_stoichiometric",
    "target_A", "vacuum_A", "ftol", "prod_ftol", "face_depth_A", "cn_cutoff_A",
    "layer_tol_A", "keep_bonds", "bonds_ok",
    "bulk_file", "pymatgen",
]


# ---------------------------------------------------------------- fingerprints
def _layers_from_top(struct: Structure, depth: float, layer_tol: float):
    """Layers within ``depth`` of the top face: list of (depth_A, site indices)."""
    z = struct.cart_coords[:, 2]
    order = np.argsort(-z)
    ztop = z[order[0]]
    layers, cur, cur_z = [], [], ztop
    for i in order:
        zi = z[i]
        if ztop - zi > depth:
            break
        if cur_z - zi > layer_tol:
            layers.append((ztop - cur_z, cur))
            cur = []
        cur.append(int(i))
        cur_z = zi
    if cur:
        layers.append((ztop - cur_z, cur))
    return layers


def _flip(struct: Structure) -> Structure:
    """180 deg rotation about x (proper rotation): bottom face becomes top."""
    rot = np.diag([1.0, -1.0, -1.0])
    lat = struct.lattice.matrix @ rot.T
    lat[2] = -lat[2]                     # keep c pointing up (+z)
    lat[1] = -lat[1]                     # keep a right-handed (a, b, c) set
    return Structure(lat, struct.species, struct.cart_coords @ rot.T,
                     coords_are_cartesian=True, to_unit_cell=True)


def face_fingerprint(struct: Structure, side: str, depth: float,
                     cn_cutoff: float = 2.2, layer_tol: float = 0.2):
    """Return (key, depths) for one face of an orthogonalized slab.

    key    : per layer, the atoms per 100 A^2 (rounded to 0.01) of each
             (element, coordination number) pair. The coordination number counts
             neighbours within ``cn_cutoff`` (A), any species, with in-plane
             periodicity. Per-area counts let cuts with different in-plane
             primitive cells compare.
    depths : layer depths below the outermost atom (A), compared separately with a
             tolerance so numerical noise cannot split one face into two.
    """
    s = struct if side == "top" else _flip(struct)
    area = float(np.linalg.norm(np.cross(s.lattice.matrix[0], s.lattice.matrix[1])))
    centers = s.get_neighbor_list(cn_cutoff)[0]
    cn = np.bincount(centers, minlength=len(s))
    key, depths = [], []
    for d, idx in _layers_from_top(s, depth, layer_tol):
        labels = [(s[i].specie.symbol, int(cn[i])) for i in idx]
        comp = tuple(sorted((el, c, round(labels.count((el, c)) * 100.0 / area, 2))
                            for el, c in set(labels)))
        key.append(comp)
        depths.append(d)
    return tuple(key), np.array(depths)


def key_to_str(key) -> str:
    return "|".join("_".join(f"{el}{x:g}[{c}]" for el, c, x in layer) for layer in key)


def same_face(fa, fb, depth_tol: float) -> bool:
    (ka, da), (kb, db) = fa, fb
    return ka == kb and len(da) == len(db) and bool(np.all(np.abs(da - db) < depth_tol))


# ---------------------------------------------------------------- enumeration
def parse_bonds(specs) -> dict:
    """['O-H:1.2', ...] -> {('O', 'H'): 1.2, ...} for SlabGenerator.get_slabs."""
    out = {}
    for spec in specs or []:
        pair, dist = spec.split(":")
        a, b = pair.split("-")
        out[(a, b)] = float(dist)
    return out


def bonds_intact(struct: Structure, bonds: dict) -> bool:
    """True when, for every (A, B): d rule, each B atom has an A neighbour within d.

    Written for rules like O-H:1.2 (every H keeps its O). Checks the final slab, so
    it also covers atoms removed by the symmetrizing trim.
    """
    for (a, b), d in bonds.items():
        for site in struct:
            if site.specie.symbol != b:
                continue
            if not any(nn.specie.symbol == a for nn in struct.get_neighbors(site, d)):
                return False
    return True


def raw_stoich_cuts(bulk: Structure, miller, target_A: float, vacuum: float,
                    ftol: float, bonds: dict | None = None) -> list:
    """All stoichiometric cuts. With ``bonds``, cut planes that would break any
    listed bond are discarded (pymatgen ``max_broken_bonds=0``)."""
    gen = SlabGenerator(bulk, miller_index=miller, min_slab_size=target_A,
                        min_vacuum_size=vacuum, center_slab=True,
                        lll_reduce=True, primitive=True)
    raw = gen.get_slabs(bonds=bonds or None, max_broken_bonds=0, ftol=ftol,
                        filter_out_sym_slabs=False, symmetrize=False)
    bf = bulk.composition.reduced_formula
    cuts = [s for s in raw if Composition(s.composition).reduced_formula == bf]
    cuts.sort(key=lambda s: float(s.shift))
    # pymatgen's trimming stops once the slab has no more sites than the bulk
    # structure it was built from (len(self.parent)); mirror that limit.
    return cuts, len(bulk)


def classify_faces(cuts, depth: float, depth_tol: float, cn_cutoff: float,
                   layer_tol: float = 0.2):
    """Group the two faces of every cut into classes.

    Returns list of classes; each class is a dict with the reference fingerprint
    and a list of carriers (cut_index, side).
    """
    classes: list[dict] = []
    for ci, cut in enumerate(cuts):
        o = orthogonalize_structure(cut.copy())
        for side in ("top", "bottom"):
            fp = face_fingerprint(o, side, depth, cn_cutoff, layer_tol)
            for c in classes:
                if same_face(c["fp"], fp, depth_tol):
                    c["carriers"].append((ci, side))
                    break
            else:
                classes.append({"fp": fp, "carriers": [(ci, side)]})
    return classes


def trim_to_symmetric(cut, keep: str, n_bulk_cell: int):
    """pymatgen nonstoichiometric_symmetrized_slab, one side only.

    keep='top' removes the lowest site (fractional c) until symmetric, so the top
    face survives untouched and is doubled. Returns (slab, n_removed) or (None, n).
    """
    if cut.is_symmetric():
        return cut.copy(), 0
    slab = cut.copy()
    n_removed = 0
    while True:
        fz = [site.frac_coords[2] for site in slab]
        idx = int(np.argmin(fz)) if keep == "top" else int(np.argmax(fz))
        slab.remove_sites([idx])
        n_removed += 1
        if len(slab) <= n_bulk_cell:
            return None, n_removed
        if slab.is_symmetric():
            return slab, n_removed


# ---------------------------------------------------------------- chemistry
def chemistry(comp: Composition, bulk_comp: Composition, ref: str):
    nu = bulk_comp.reduced_composition.as_dict()
    n = comp.as_dict()
    n_fu = n.get(ref, 0.0) / nu[ref]
    excess = {el: n.get(el, 0.0) - n_fu * nu[el] for el in sorted(nu) if el != ref}
    return n_fu, excess


def default_ref_element(bulk_comp: Composition) -> str:
    return min((Element(el) for el in bulk_comp.as_dict()),
               key=lambda e: e.X).symbol


def pmg_version_ok(v: str) -> bool:
    try:
        parts = tuple(int(x) for x in v.split(".")[:3])
    except ValueError:
        return False
    return parts <= PMG_MAX_VERSION


# ---------------------------------------------------------------- main
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bulk", type=Path, required=True,
                   help="This MLIP's relaxed bulk (S7).")
    p.add_argument("--mlip", required=True)
    p.add_argument("--miller", nargs=3, type=int, required=True,
                   metavar=("H", "K", "L"))
    p.add_argument("--material", default=None,
                   help="Label used in paths (default: bulk reduced formula).")
    p.add_argument("--ref-element", default=None,
                   help="Element that fixes n_fu (default: least electronegative).")
    p.add_argument("--target-A", type=float, default=13.0,
                   help="Production cut target, used only to map production f<N> faces.")
    p.add_argument("--sym-target-A", type=float, default=26.0,
                   help="Cut thickness fed to the trimming (A). E-p3 sets the rule.")
    p.add_argument("--sym-step-A", type=float, default=4.0)
    p.add_argument("--sym-max-A", type=float, default=50.0)
    p.add_argument("--vacuum", type=float, default=15.0)
    p.add_argument("--ftol", type=float, default=None,
                   help="Layer clustering tolerance (A) for the cut enumeration. Default: "
                        "the canon S1 value for the material (MATERIAL_DEFAULTS: Co3O4 "
                        "0.005, CoOOH 0.02). Required for any other material.")
    p.add_argument("--prod-ftol", type=float, default=None,
                   help="ftol of the tasker_flip production slabs, used only to map "
                        "faces to their f<N> labels (provenance).")
    p.add_argument("--face-depth-A", type=float, default=4.0,
                   help="Fingerprint depth below the outermost atom (A).")
    p.add_argument("--depth-tol-A", type=float, default=0.15,
                   help="Tolerance on layer depths when comparing faces (A).")
    p.add_argument("--min-axis-A", type=float, default=7.5)
    p.add_argument("--min-area-A2", type=float, default=100.0)
    p.add_argument("--output-base", type=Path, required=True)
    p.add_argument("--audit", type=Path, default=None,
                   help="Audit CSV (default: <output_base>/rs_slabs_audit.csv).")
    p.add_argument("--skip-prod-map", action="store_true",
                   help="Do not map faces to production f<N> ids (saves one "
                        "enumeration; use for tests with a non-production ftol).")
    p.add_argument("--dry-run", action="store_true",
                   help="Enumerate and classify faces only; no trimming, no POSCARs.")
    p.add_argument("--layer-tol-A", type=float, default=0.2,
                   help="Atoms closer than this along the normal (A) form one layer "
                        "in the face fingerprint.")
    p.add_argument("--keep-bonds", nargs="*", default=None, metavar="A-B:DIST",
                   help="Bonds no cut may break, e.g. O-H:1.2 (every H keeps its O). "
                        "Each output slab is checked for it. Default: the canon S1 rule "
                        "for the material (CoOOH: O-H:1.2; Co3O4: none). Pass the flag "
                        "with no value to switch the rule off.")
    p.add_argument("--cn-cutoff-A", type=float, default=2.2,
                   help="Neighbour cutoff for the coordination numbers in the face "
                        "fingerprint (A). Must sit in a gap of the pair-distance "
                        "distribution: above every first-shell bond, clearly below the "
                        "next shell. 2.2 fits Co3O4 (Co-O <= 1.94, O-O >= 2.64) and CoOOH "
                        "(H...O <= 1.51, O-O >= 2.45). 2.5 split CoOOH faces (2026-10-12).")
    args = p.parse_args()

    pmg_v = pmg_core.__version__
    if not pmg_version_ok(pmg_v):
        print(f"[WARN] pymatgen {pmg_v} > 2025.6.14: cut set and f<N> numbering "
              f"may differ from production (S1).")

    bulk = Structure.from_file(str(args.bulk))
    bulk_comp = bulk.composition
    material = args.material or bulk_comp.reduced_formula
    material = MATERIAL_ALIASES.get(material, material)
    preset = MATERIAL_DEFAULTS.get(material, {})
    src = []
    keys = ("ftol", "keep_bonds") + (() if args.skip_prod_map else ("prod_ftol",))
    for key in keys:
        if getattr(args, key) is None:
            if key not in preset:
                p.error(f"--{key.replace('_', '-')} is required: no canon default for "
                        f"material '{material}' (MATERIAL_DEFAULTS)")
            setattr(args, key, preset[key])
            src.append(f"{key}={getattr(args, key)} (canon default)")
        else:
            src.append(f"{key}={getattr(args, key)} (command line)")
    print("Settings: " + ", ".join(src))
    keep_bonds = parse_bonds(args.keep_bonds)
    ref = args.ref_element or default_ref_element(bulk_comp)
    miller = tuple(args.miller)
    mstr = "".join(str(x) for x in miller)
    audit_path = args.audit or (args.output_base / "rs_slabs_audit.csv")

    # Production f<N> faces (provenance only): same filter and order as gen_slabs.py,
    # at the production ftol. Matched to face classes by fingerprint, because cut
    # shifts change with ftol.
    if args.skip_prod_map:
        prod = []
    else:
        prod = slabs_for_target(bulk, miller, args.target_A, args.vacuum,
                                args.prod_ftol)
    prod = [s for s in prod
            if Composition(s.composition).reduced_formula == bulk_comp.reduced_formula]
    prod_faces = []
    for i, s in enumerate(prod):
        o = orthogonalize_structure(s.copy())
        for side, tag in (("top", "T"), ("bottom", "B")):
            prod_faces.append((f"f{i}{tag}", face_fingerprint(
                o, side, args.face_depth_A, args.cn_cutoff_A, args.layer_tol_A)))

    # Faces are enumerated at the first sym target. Shifts do not depend on the
    # cut thickness, so the classes are the same at every target.
    cache: dict[float, tuple] = {}

    def cuts_at(t):
        if t not in cache:
            cuts, n_cell = raw_stoich_cuts(bulk, miller, t, args.vacuum, args.ftol,
                                           keep_bonds)
            cache[t] = (cuts, n_cell, classify_faces(cuts, args.face_depth_A,
                                                     args.depth_tol_A,
                                                     args.cn_cutoff_A,
                                                     args.layer_tol_A))
        return cache[t]

    cuts0, _, classes0 = cuts_at(args.sym_target_A)
    print(f"{material} {args.mlip} ({mstr}): {len(cuts0)} stoichiometric cuts, "
          f"{len(prod)} production f<N>, {len(classes0)} distinct faces "
          f"(depth {args.face_depth_A} A), ref element {ref}, pymatgen {pmg_v}")

    rows, built = [], []
    for k, cls in enumerate(classes0):
        label = f"r{k}"
        carriers = cls["carriers"]
        carrier_str = " ".join(
            f"s{float(cuts0[ci].shift):.4f}{'T' if side == 'top' else 'B'}"
            for ci, side in carriers)
        prod_str = " ".join(lab for lab, fp in prod_faces
                            if same_face(fp, cls["fp"], args.depth_tol_A))
        row = {"material": material, "mlip": args.mlip, "miller": mstr,
               "face_label": label, "face_key": key_to_str(cls["fp"][0]),
               "n_cuts_with_face": len({ci for ci, _ in carriers}),
               "carriers": carrier_str, "prod_carriers": prod_str,
               "ref_element": ref,
               "target_A": args.target_A, "vacuum_A": args.vacuum,
               "ftol": args.ftol, "prod_ftol": args.prod_ftol,
               "face_depth_A": args.face_depth_A,
               "cn_cutoff_A": args.cn_cutoff_A, "layer_tol_A": args.layer_tol_A,
               "keep_bonds": " ".join(args.keep_bonds),
               "bulk_file": str(args.bulk), "pymatgen": pmg_v}
        print(f"  {label}: {row['face_key']}  production faces: {prod_str or '-'}")
        if args.dry_run:
            row["status"] = "dry_run"
            rows.append(row)
            continue

        child = None
        t = args.sym_target_A
        while t <= args.sym_max_A + 1e-9:
            cuts, n_cell, classes = cuts_at(t)
            match = [c for c in classes if same_face(c["fp"], cls["fp"],
                                                     args.depth_tol_A)]
            if not match:
                print(f"    [WARN] face not found at cut target {t:.0f} A")
                t += args.sym_step_A
                continue
            cand = sorted(match[0]["carriers"],
                          key=lambda cs: (cs[1] != "top",
                                          float(cuts[cs[0]].shift)))
            ci, side = cand[0]
            child, n_trim = trim_to_symmetric(cuts[ci], side, n_cell)
            if child is not None:
                src = cuts[ci]
                break
            print(f"    trimming failed at cut target {t:.0f} A; thicker cut")
            t += args.sym_step_A

        if child is None:
            row["status"] = f"failed_up_to_{args.sym_max_A:.0f}A"
            rows.append(row)
            print(f"    [FAIL] {label}: no symmetric slab up to {args.sym_max_A} A")
            continue

        child_o = orthogonalize_structure(child.copy())
        fp_top = face_fingerprint(child_o, "top", args.face_depth_A, args.cn_cutoff_A,
                                  args.layer_tol_A)
        fp_bot = face_fingerprint(child_o, "bottom", args.face_depth_A, args.cn_cutoff_A,
                                  args.layer_tol_A)
        faces_match = same_face(fp_top, fp_bot, args.depth_tol_A)
        doubled_ok = same_face(fp_top, cls["fp"], args.depth_tol_A)

        na, nb, notes = compute_supercell_mult(child_o, args.min_axis_A,
                                               args.min_area_A2)
        for note in notes:
            print(f"    [EDGE] {label} {na}x{nb}: {note}")
        tiled = child_o.copy()
        if na > 1 or nb > 1:
            tiled.make_supercell([na, nb, 1])
        area = float(np.linalg.norm(np.cross(tiled.lattice.matrix[0],
                                             tiled.lattice.matrix[1])))
        n_fu, excess = chemistry(tiled.composition, bulk_comp, ref)
        b_ok = bonds_intact(child_o, keep_bonds) if keep_bonds else True
        ok = child.is_symmetric() and faces_match and doubled_ok and b_ok
        row.update({
            "status": "ok" if ok else "check",
            "source_shift": f"{float(src.shift):.4f}", "source_side": side,
            "sym_target_A": t,
            "n_trimmed": n_trim, "n_atoms": tiled.num_sites,
            "composition": tiled.composition.formula.replace(" ", ""),
            "n_fu": f"{n_fu:.4f}",
            "excess": ";".join(f"{el}={v:+.3f}" for el, v in excess.items()),
            "excess_per_nm2_per_face": ";".join(
                f"{el}={v / (2 * area) * 100:+.3f}" for el, v in excess.items()),
            "area_A2": f"{area:.3f}", "lateral_label": f"{na}x{nb}",
            "actual_A": f"{measure_z_extent(child_o):.3f}",
            "is_symmetric_pmg": child.is_symmetric(), "faces_match": faces_match,
            "doubled_face_ok": doubled_ok, "bonds_ok": b_ok,
            "is_stoichiometric": (tiled.composition.reduced_formula
                                  == bulk_comp.reduced_formula),
        })
        out_dir = args.output_base / material / args.mlip / f"{mstr}_{label}"
        out_dir.mkdir(parents=True, exist_ok=True)
        tiled.to(filename=str(out_dir / "POSCAR"), fmt="poscar")
        built.append(label)
        rows.append(row)
        print(f"    -> {row['composition']} {na}x{nb}, {row['actual_A']} A, "
              f"excess {row['excess']}, trimmed {n_trim}, status {row['status']}")

    # Upsert audit rows for this (material, mlip, miller).
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if audit_path.exists():
        with audit_path.open(newline="") as f:
            existing = [r for r in csv.DictReader(f)
                        if (r["material"], r["mlip"], r["miller"])
                        != (material, args.mlip, mstr)]
    with audit_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=AUDIT_COLUMNS)
        w.writeheader()
        for r in existing + rows:
            w.writerow({c: r.get(c, "") for c in AUDIT_COLUMNS})
    n_ok = sum(r.get("status") == "ok" for r in rows)
    if args.dry_run:
        print(f"\nDry run: {len(rows)} faces listed; audit: {audit_path}")
    else:
        print(f"\n{n_ok}/{len(rows)} faces ok; audit: {audit_path}")
    return 0 if args.dry_run or n_ok == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
