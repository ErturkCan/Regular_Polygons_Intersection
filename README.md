# Intersection Points of Overlapping Regular Polygons

How many points appear when you draw several regular polygons on top of one
another? This repository contains a short research note answering that
question, together with the Python script that checks every formula in it.

The work is an award-winning MOSTRATEC project, carried out at Halil İnalcık
Bilim ve Sanat Merkezi (BİLSEM) in Bursa, Türkiye. This version adds proofs,
fixes an index error in the original general rule, and proves a new result
about the number of regions the figure is cut into.

## The main results

Let several regular polygons sit in *general position*: every pair overlaps,
and no point is shared by three or more polygons at once.

| Situation | Most intersection points |
|---|---|
| Two regular k-gons | 2k |
| n copies of a regular k-gon | kn² − kn |
| Triangles (k = 3) | 3n² − 3n |
| Squares (k = 4) | 4n² − 4n |
| Pentagons (k = 5) | 5n² − 5n |
| Two n-gons and one k-gon (k < n) | 2n + 4k |
| Three n-gons and one k-gon (k < n) | 6(n + k) |

The single key fact is that a regular polygon is convex, so a straight line
crosses its outline at most twice. Each of the k edges of one polygon therefore
meets another polygon in at most two points, which gives the bound 2k for a
pair. Everything else follows by adding up over all pairs.

**New result.** The same arrangement encloses exactly

```
kn² − kn + 1
```

bounded regions, which is one more than the number of intersection points. This
comes straight from Euler's formula for planar graphs and is proved in the note.

## What's in this repository

```
regular-polygon-intersections/
├── README.md          this file
├── verify.py          checks every formula by direct computation
├── requirements.txt   optional dependency (shapely, for region counts)
├── paper.pdf          the research note
└── figures/           the figures used in the note
```

## Running the check

```bash
python verify.py
```

`verify.py` builds the polygons, finds every crossing point between edges of
different polygons, removes duplicates, and compares the count with the formula.
It also scans the rotation angle for a pair of polygons to confirm that 2k is
actually reached, and checks the mixed cases. With `shapely` installed it counts
the bounded regions too.

Sample output:

```
 k  n  predicted P  computed P  pred. R  comp. R  result
 3  2            6           6        7        7  PASS
 4  3           24          24       25       25  PASS
 5  4           60          60       61       61  PASS
 ...
OVERALL: ALL CHECKS PASSED
```

Only the region check needs a third-party library. The rest runs on a plain
Python install.

```bash
pip install -r requirements.txt   # optional, only for region counts
```

## Author

Can Ertürk. Award-winning MOSTRATEC project, carried out at Halil İnalcık
Bilim ve Sanat Merkezi (BİLSEM), Bursa. Currently a BSc student at Eindhoven
University of Technology (TU/e). The university is named only to describe the
author and was not involved in the research.

## License

Released under the MIT License. See `LICENSE`.
