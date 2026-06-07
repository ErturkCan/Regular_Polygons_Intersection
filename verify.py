"""
verify.py
=========
Checks every formula in the paper
"The Maximum Number of Intersection Points of Overlapping Regular Polygons"
against a direct geometric computation.

For a given set of regular polygons it:
  1. computes all crossing points between edges of *different* polygons,
  2. removes duplicates,
  3. compares the count with the closed-form prediction,
  4. counts the bounded regions and compares with P + 1.

Run:
    python verify.py

No arguments. It prints a table of (predicted, computed) pairs and an
overall PASS/FAIL. Only depends on the standard library plus, optionally,
shapely for the region count (the script skips region checks if shapely
is not installed).
"""

import math
from itertools import combinations

# ---------------------------------------------------------------- geometry

def regular_polygon(k, radius=1.0, rotation=0.0, center=(0.0, 0.0)):
    """Return the k vertices of a regular k-gon as a list of (x, y)."""
    cx, cy = center
    return [
        (cx + radius * math.cos(rotation + 2 * math.pi * i / k),
         cy + radius * math.sin(rotation + 2 * math.pi * i / k))
        for i in range(k)
    ]


def edges(vertices):
    """The k closed edges of a polygon, as (p, q) segment pairs."""
    n = len(vertices)
    return [(vertices[i], vertices[(i + 1) % n]) for i in range(n)]


def segment_intersection(p1, p2, p3, p4, eps=1e-12):
    """Intersection point of segments p1p2 and p3p4, or None."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < eps:
        return None  # parallel or collinear
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom
    if -1e-9 <= t <= 1 + 1e-9 and -1e-9 <= u <= 1 + 1e-9:
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None


def dedupe(points, tol=1e-6):
    """Drop points that coincide within tol."""
    out = []
    for p in points:
        if not any(abs(p[0] - q[0]) < tol and abs(p[1] - q[1]) < tol for q in out):
            out.append(p)
    return out


def crossing_points(polygons):
    """All crossing points between edges of *different* polygons."""
    pts = []
    for a, b in combinations(range(len(polygons)), 2):
        for e1 in edges(polygons[a]):
            for e2 in edges(polygons[b]):
                ip = segment_intersection(e1[0], e1[1], e2[0], e2[1])
                if ip is not None:
                    pts.append(ip)
    return dedupe(pts)


def bounded_regions(polygons):
    """
    Number of bounded regions enclosed by the union of polygon outlines.
    Uses shapely if available; returns None otherwise.
    """
    try:
        from shapely.geometry import LineString
        from shapely.ops import unary_union, polygonize
    except ImportError:
        return None
    rings = [LineString(list(p) + [p[0]]) for p in polygons]
    return len(list(polygonize(unary_union(rings))))


# ------------------------------------------------------ general-position layout

def stacked(k, n):
    """
    n concentric regular k-gons, each turned by a small irrational-looking
    amount so that no three edges meet at one point (general position).
    """
    return [
        regular_polygon(k, rotation=i * 0.0531 + i * i * 0.00937)
        for i in range(n)
    ]


# ----------------------------------------------------------------- the checks

def check_single_type():
    """Theorem 2: n regular k-gons give kn^2 - kn crossings, and P + 1 regions."""
    print("Single-type polygons:  P = k n^2 - k n,   regions = P + 1")
    print(f"{'k':>2} {'n':>2} {'predicted P':>12} {'computed P':>11} "
          f"{'pred. R':>8} {'comp. R':>8}  result")
    ok = True
    for k in (3, 4, 5, 6):
        for n in (2, 3, 4, 5):
            polys = stacked(k, n)
            P_pred = k * n * n - k * n
            P_comp = len(crossing_points(polys))
            R_pred = P_pred + 1
            R_comp = bounded_regions(polys)
            line_ok = (P_pred == P_comp) and (R_comp is None or R_comp == R_pred)
            ok = ok and line_ok
            rc = "-" if R_comp is None else str(R_comp)
            print(f"{k:>2} {n:>2} {P_pred:>12} {P_comp:>11} "
                  f"{R_pred:>8} {rc:>8}  {'PASS' if line_ok else 'FAIL'}")
    return ok


def check_two_polygons():
    """Theorem 1: two regular k-gons cross in at most 2k points."""
    print("\nTwo equal polygons, scanning the rotation angle:  max should be 2k")
    print(f"{'k':>2} {'2k':>4} {'found max':>10}  result")
    ok = True
    for k in (3, 4, 5, 6, 7, 8):
        best = 0
        steps = 400
        for s in range(1, steps):
            ang = (2 * math.pi / k) * s / steps
            polys = [regular_polygon(k, rotation=0.0),
                     regular_polygon(k, rotation=ang)]
            best = max(best, len(crossing_points(polys)))
        line_ok = best == 2 * k
        ok = ok and line_ok
        print(f"{k:>2} {2*k:>4} {best:>10}  {'PASS' if line_ok else 'FAIL'}")
    return ok


def check_mixed():
    """Special mixed cases: 2 n-gons + 1 k-gon = 2n + 4k, etc. (k < n)."""
    print("\nMixed cases (smaller polygon has k sides, k < n)")
    print(f"{'case':>26} {'predicted':>10} {'computed':>9}  result")
    ok = True
    cases = []
    for n in (4, 5, 6):
        for k in (3,):  # triangle as the small polygon, k < n
            # two n-gons + one k-gon -> 2n + 4k
            polys = ([regular_polygon(n, rotation=0.0),
                      regular_polygon(n, rotation=0.21)]
                     + [regular_polygon(k, rotation=0.07)])
            cases.append((f"2x{n}-gon + 1x{k}-gon", 2 * n + 4 * k, polys))
            # three n-gons + one k-gon -> 6(n + k)
            polys3 = ([regular_polygon(n, rotation=0.0),
                       regular_polygon(n, rotation=0.21),
                       regular_polygon(n, rotation=0.41)]
                      + [regular_polygon(k, rotation=0.07)])
            cases.append((f"3x{n}-gon + 1x{k}-gon", 6 * (n + k), polys3))
    for name, pred, polys in cases:
        comp = len(crossing_points(polys))
        line_ok = comp == pred
        ok = ok and line_ok
        print(f"{name:>26} {pred:>10} {comp:>9}  {'PASS' if line_ok else 'FAIL'}")
    return ok


def main():
    print("=" * 60)
    print("Verifying the regular-polygon intersection formulas")
    print("=" * 60)
    a = check_single_type()
    b = check_two_polygons()
    c = check_mixed()
    print("\n" + "=" * 60)
    print("OVERALL:", "ALL CHECKS PASSED" if (a and b and c) else "SOME CHECKS FAILED")
    print("=" * 60)


if __name__ == "__main__":
    main()
