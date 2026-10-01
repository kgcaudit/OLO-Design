#!/usr/bin/env python3
"""The OLO family's launcher icons: one clay ground, one white mark per app.

A row of the four OLO apps on a home screen should read as one family and still
be told apart at a glance. They share everything but the mark: the same clay
diagonal ground, the same ~56px margin, the same flat-white, no-stroke,
no-gradient silhouette language. Identity is the mark alone -- the way the
in-app tiles are told apart by hue and nothing else.

    explorer   a folder coming apart, its far corner torn into flying strips
    player     a play triangle
    cycle      a circular motion arrow -- cyclic activity
    ebook      an open book, two facing pages from a centre spine

Each app builds its own three launcher drawables from here:

    python3 appicons/launcher.py --app explorer --out PATH/res/drawable
    python3 appicons/launcher.py --app player   --out PATH/res/drawable
    python3 appicons/launcher.py --app cycle    --out PATH/res/drawable
    python3 appicons/launcher.py --app ebook    --out PATH/res/drawable

It writes ic_launcher_background.xml (shared, identical for every app),
ic_launcher_foreground.xml and ic_launcher_monochrome.xml (the app's mark).
The adaptive-icon wrappers that point at these three live in
appicons/mipmap/ and are copied as-is into each app's mipmap-anydpi-v26/.

Explorer's torn folder is cut with real polygon arithmetic, so it needs
shapely; the other three marks are plain path geometry and need nothing. The
shapely import is deferred into the folder so a Player or eBook build does not
require it.

    python3 appicons/launcher.py --app explorer     # preview into appicons/build/explorer/
"""
from __future__ import annotations

import argparse
import math
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent

# Claude's clay and the warm neutrals that go with it; see tokens/color.md.
WHITE = "#FFFFFF"

# The launcher's ground, which is a gradient rather than the flat clay the rest
# of the app uses. A home screen is thirty icons at 48px competing for one
# glance, and a flat mid-tone is what loses that competition; the app's own
# clay is the dark end of the ramp and a brighter one lights the corner the
# mark travels towards. Shared by every app in the family.
CLAY = "#C5613F"
CLAY_LIT = "#E07B55"


# ---------------------------------------------------------------------------
# Shared drawing primitives
# ---------------------------------------------------------------------------

def scaled(data: str, factor: float, about: float = 256.0) -> str:
    """Shrinks path data towards the middle of the viewport.

    An adaptive icon shows only the middle two thirds of its canvas, and a
    circular mask cuts a circle out of even that -- so artwork drawn to the
    full viewport loses its corners.

    Absolute coordinates move towards the centre; relative ones are only made
    smaller, because they are already distances rather than places. Treating
    the two alike is what sheared the arrows into ribbons the first time.
    """
    tokens = re.findall(r"[A-Za-z]|-?\d*\.?\d+", data)
    out: list[str] = []
    index = 0
    relative = False
    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            relative = token.islower()
            out.append(token)
            index += 1
            continue
        pair = []
        for value in (float(token), float(tokens[index + 1])):
            pair.append(value * factor if relative else about + (value - about) * factor)
        out.append(f"{pair[0]:g},{pair[1]:g}")
        index += 2
    return re.sub(r"([A-Za-z]) ", r"\1", " ".join(out)).strip()


def rounded_rect(x: float, y: float, w: float, h: float, r: float) -> str:
    """A rounded rectangle, as vector path data."""
    return (
        f"M{x + r},{y} L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} "
        f"L{x + w},{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h} "
        f"L{x + r},{y + h} Q{x},{y + h} {x},{y + h - r} "
        f"L{x},{y + r} Q{x},{y} {x + r},{y} Z"
    )


def rounded_polygon(points: list[tuple[float, float]], r: float) -> str:
    """A closed polygon with its corners rounded off by radius r.

    Each corner is cut back by r along both of its edges and the two cut ends
    joined by a quadratic through the original vertex -- so a triangle or a
    kite comes out with the same soft corners the rest of the set carries,
    without any strokes.
    """
    n = len(points)
    segs: list[str] = []
    for i in range(n):
        prev = points[(i - 1) % n]
        cur = points[i]
        nxt = points[(i + 1) % n]

        def unit(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            d = math.hypot(dx, dy) or 1.0
            return dx / d, dy / d

        ux, uy = unit(cur, prev)
        vx, vy = unit(cur, nxt)
        # Do not cut back further than half of the shorter adjoining edge.
        back = min(r, math.hypot(prev[0] - cur[0], prev[1] - cur[1]) / 2,
                   math.hypot(nxt[0] - cur[0], nxt[1] - cur[1]) / 2)
        p_in = (cur[0] + ux * back, cur[1] + uy * back)
        p_out = (cur[0] + vx * back, cur[1] + vy * back)
        if i == 0:
            segs.append(f"M{p_in[0]:.1f},{p_in[1]:.1f}")
        else:
            segs.append(f"L{p_in[0]:.1f},{p_in[1]:.1f}")
        segs.append(f"Q{cur[0]:.1f},{cur[1]:.1f} {p_out[0]:.1f},{p_out[1]:.1f}")
    segs.append("Z")
    return " ".join(segs)


def vector(paths: list[tuple[str, str]], size: int = 24) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<!-- Generated by appicons/launcher.py. Do not edit by hand. -->",
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"',
        '    xmlns:aapt="http://schemas.android.com/aapt"',
        f'    android:width="{size}dp"',
        f'    android:height="{size}dp"',
        '    android:viewportWidth="512"',
        '    android:viewportHeight="512">',
    ]
    for fill, data in paths:
        if ":" in fill:
            # A gradient, written the long way round: a vector drawable can
            # only take one as a nested attribute, not as a colour string.
            start, end = fill.split(":")
            lines += [
                "    <path",
                f'        android:pathData="{data}">',
                '        <aapt:attr name="android:fillColor">',
                '            <gradient',
                '                android:type="linear"',
                '                android:startX="0" android:startY="0"',
                '                android:endX="512" android:endY="512"',
                f'                android:startColor="{start}"',
                f'                android:endColor="{end}" />',
                "        </aapt:attr>",
                "    </path>",
            ]
        else:
            lines += ["    <path", f'        android:fillColor="{fill}"',
                      f'        android:pathData="{data}" />']
    lines += ["</vector>", ""]
    return "\n".join(lines)


def _as_path(poly) -> str:
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in poly) + " Z"


# ---------------------------------------------------------------------------
# Explorer -- a folder coming apart
# ---------------------------------------------------------------------------
#
# The body intact and readable on the left, the far corner torn away into
# strips that fly up and to the right.
#
# The brief was a file explorer that takes the eye, drawn with the swing of
# weight a brush gives a stroke rather than the even width a vector does. The
# swing here is in the pieces: a wide body, then a strip, then a thinner one,
# then a sliver -- four weights along one tear instead of four shapes of the
# same thickness.
#
# The folder had to survive it. Earlier attempts put the energy outside the
# form -- rays spraying from an open folder, strips bowing away like wheat, a
# radial burst -- and each one read as weather happening near a folder rather
# than to it. Tearing the folder itself keeps the silhouette, which is the only
# part anybody identifies at 48px, and spends the drama on what happens to it.
TRAVEL = -34.0                          # the line the tear runs along
CUTS = (52.0, 92.0, 114.0, 126.0)       # where along it the folder gives way
PUSHES = (0.0, 14.0, 30.0, 48.0, 70.0)  # how far each piece has got
DRIFTS = (0.0, 7.0, -5.0, 9.0, -13.0)   # and how far it has wandered across
SPINS = (0.0, 4.0, -5.0, 8.0, -11.0)    # each piece turning as it goes
RAGGED = (9.0, -7.0, 11.0, -5.0, 8.0, -10.0, 6.0)   # the zigzag of a tear
REACH = 152.0                           # the adaptive circle is 156


def _folder_outline(x, y, w, h, tab_w, tab_h, r, steps=14):
    """The folder as a closed polyline, corners sampled rather than arced."""
    pts: list[tuple[float, float]] = []

    def corner(cx, cy, a0, a1):
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    corner(x + r, y + tab_h + r, 180, 270)          # top of the tab
    pts.append((x + tab_w - 16, y + tab_h))
    pts.append((x + tab_w + 6, y))                  # the slanted shoulder
    corner(x + w - r, y + r, 270, 360)
    corner(x + w - r, y + h - r, 0, 90)
    corner(x + r, y + h - r, 90, 180)
    return pts


def _band(travel, d0, d1, ragged=None, reach=900.0):
    """The slab of the plane between d0 and d1, measured along `travel`."""
    a = math.radians(travel)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux

    def at(d, s):
        return (256.0 + ux * d + nx * s, 256.0 + uy * d + ny * s)

    lead = []
    if ragged:
        n = len(ragged)
        lead.append(at(d0 + ragged[0], -reach))
        for i, jog in enumerate(ragged):
            lead.append(at(d0 + jog, -reach + 2 * reach * (i + 0.5) / n))
        lead.append(at(d0 + ragged[-1], reach))
    else:
        lead = [at(d0, -reach), at(d0, reach)]
    return lead + [at(d1, reach), at(d1, -reach)]


def _placed(poly, spin, pivot, shift):
    """One piece, turned about where it tore away and moved along its travel."""
    out = []
    c, s = math.cos(math.radians(spin)), math.sin(math.radians(spin))
    px, py = pivot
    for x, y in poly:
        rx, ry = x - px, y - py
        out.append((px + rx * c - ry * s + shift[0], py + rx * s + ry * c + shift[1]))
    return out


def torn_folder() -> list[list[tuple[float, float]]]:
    """The Explorer mark, as polygons already in their final positions."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union

    whole = Polygon(_folder_outline(96, 148, 320, 216, 164, 58, 22))
    a = math.radians(TRAVEL)
    edges = (-400.0,) + CUTS + (400.0,)

    pieces = []
    for i in range(len(edges) - 1):
        slab = Polygon(_band(TRAVEL, edges[i], edges[i + 1],
                             ragged=None if i == 0 else RAGGED))
        cut = whole.intersection(slab)
        if cut.is_empty:
            continue
        pivot = (256.0 + edges[i] * math.cos(a), 256.0 + edges[i] * math.sin(a))
        shift = (PUSHES[i] * math.cos(a) - DRIFTS[i] * math.sin(a),
                 PUSHES[i] * math.sin(a) + DRIFTS[i] * math.cos(a))
        parts = cut.geoms if cut.geom_type == "MultiPolygon" else [cut]
        for part in parts:
            ring = list(part.exterior.coords)[:-1]
            if len(ring) > 2:
                pieces.append(_placed(ring, SPINS[i], pivot, shift))

    # Centred and sized from what is actually drawn: the pieces fly by
    # different amounts and the envelope is nothing the numbers above state.
    bounds = unary_union([Polygon(p) for p in pieces]).bounds
    cx, cy = (bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2
    half = math.hypot(bounds[2] - bounds[0], bounds[3] - bounds[1]) / 2
    k = REACH / half
    return [[(256.0 + (x - cx) * k, 256.0 + (y - cy) * k) for x, y in p] for p in pieces]


def mark_explorer() -> list[str]:
    return [_as_path(p) for p in torn_folder()]


# ---------------------------------------------------------------------------
# Player -- a play triangle
# ---------------------------------------------------------------------------
#
# One rounded right-pointing triangle, the plainest mark in the family and the
# one that can be plainest: a play glyph is read whole, so it asks for weight
# and balance rather than drama. Nudged a hair left of centre because a
# right-pointing triangle's visual centre sits ahead of its centroid, and set
# inside the same ~56px margin so it survives every mask.
def mark_player() -> list[str]:
    tri = [
        (196.0, 150.0),   # top-left
        (372.0, 256.0),   # the tip, on the centre line
        (196.0, 362.0),   # bottom-left
    ]
    return [rounded_polygon(tri, 26.0)]


# ---------------------------------------------------------------------------
# Cycle -- a circular motion arrow
# ---------------------------------------------------------------------------
#
# A thick ring broken near the top, with an arrowhead carrying it on round:
# cyclic motion, which is the one idea the app's name and "activity" share. A
# single bold loop rather than the two-arrow recycle symbol, because two arrows
# at 48px turn to mud and one reads as motion cleanly. The gap and the head are
# what keep it from reading as a plain ring.
def _ring_band(cx, cy, ro, ri, a0, a1, steps=48) -> list[tuple[float, float]]:
    outer = [(cx + ro * math.cos(a0 + (a1 - a0) * i / steps),
              cy + ro * math.sin(a0 + (a1 - a0) * i / steps)) for i in range(steps + 1)]
    inner = [(cx + ri * math.cos(a1 + (a0 - a1) * i / steps),
              cy + ri * math.sin(a1 + (a0 - a1) * i / steps)) for i in range(steps + 1)]
    return outer + inner


def mark_cycle() -> list[str]:
    cx = cy = 256.0
    # Pulled in from ro=136/ri=94/head_ext=20, which put the arrowhead's outer
    # corner at radius 156 -- right on the 156.4 safe-zone edge, the heaviest
    # mark in the row. These give a ~10px margin inside the circular mask and
    # bring the loop's visual weight closer to the folder and the book.
    ro, ri = 128.0, 88.0
    rmid = (ro + ri) / 2.0
    # Screen y is down, so angles run clockwise on screen. Sweep from the top
    # gap round almost the whole way; the arrowhead sits at the leading end.
    a0 = math.radians(-60.0)     # just right of top
    a1 = math.radians(205.0)     # round past the bottom to upper-left
    band = _ring_band(cx, cy, ro, ri, a0, a1)
    ring = _as_path(band)

    # The arrowhead: a triangle wider than the band, its tip carried a little
    # further along the sweep so the loop looks like it is still turning.
    head_ext = 16.0
    head_adv = math.radians(26.0)
    base_out = (cx + (ro + head_ext) * math.cos(a1), cy + (ro + head_ext) * math.sin(a1))
    base_in = (cx + (ri - head_ext) * math.cos(a1), cy + (ri - head_ext) * math.sin(a1))
    tip = (cx + rmid * math.cos(a1 + head_adv), cy + rmid * math.sin(a1 + head_adv))
    head = _as_path([base_out, tip, base_in])
    return [ring, head]


# ---------------------------------------------------------------------------
# eBook -- an open book
# ---------------------------------------------------------------------------
#
# Two facing pages rising from a centre spine, the clay ground showing through
# the spine gap the way it shows through the comic tile's. Fuller and bolder
# than that little tile, because here the book is the whole identity. Symmetric
# about the spine; the page tops fan with a gentle curve so it reads as paper
# rather than as two slabs.
def _page(sign: float) -> str:
    """One page. sign=-1 draws the left page, sign=+1 the right (mirrored).

    Tall at the spine and shorter at the outer edge, so the two page tops slope
    down and away from the centre -- the line an open book makes. The spine edge
    is vertical, the outer edge vertical, and the top and bottom carry a gentle
    fan curve so it reads as paper rather than as a leaning slab.
    """
    cx = 256.0
    spine_gap = 9.0            # half the clay spine showing between the pages
    inner_top = (cx + sign * spine_gap, 172.0)
    outer_top = (cx + sign * 150.0, 202.0)
    outer_bot = (cx + sign * 150.0, 332.0)
    inner_bot = (cx + sign * spine_gap, 352.0)
    # The fan: the top bowed up a touch in the middle, the bottom bowed down a
    # touch, both subtle so the outer edge still reads as straight.
    top_ctrl = (cx + sign * 82.0, 176.0)
    bot_ctrl = (cx + sign * 82.0, 350.0)
    return (
        f"M{inner_top[0]:.1f},{inner_top[1]:.1f} "
        f"Q{top_ctrl[0]:.1f},{top_ctrl[1]:.1f} {outer_top[0]:.1f},{outer_top[1]:.1f} "
        f"L{outer_bot[0]:.1f},{outer_bot[1]:.1f} "
        f"Q{bot_ctrl[0]:.1f},{bot_ctrl[1]:.1f} {inner_bot[0]:.1f},{inner_bot[1]:.1f} "
        f"L{inner_top[0]:.1f},{inner_top[1]:.1f} Z"
    )


# The whole book, scaled in towards the centre. At full size the page corners
# reached radius ~168 -- past the 156.4 safe circle -- so the outer edges were
# clipped under a round mask and the book sat heavier than its siblings. 0.82
# brings the width to ~48% (the folder's) and the corners well inside the mask;
# the spine gap and the page curves are unchanged, only the size.
EBOOK_SCALE = 0.82


def mark_ebook() -> list[str]:
    return [scaled(_page(-1.0), EBOOK_SCALE), scaled(_page(1.0), EBOOK_SCALE)]


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

MARKS = {
    "explorer": mark_explorer,
    "player": mark_player,
    "cycle": mark_cycle,
    "ebook": mark_ebook,
}

LAUNCHER_BACKGROUND = [(f"{CLAY_LIT}:{CLAY}", rounded_rect(0, 0, 512, 512, 0))]


def launcher_layers(app: str) -> tuple[list, list]:
    """The foreground and the themed-icon layer, which are the same shapes."""
    shapes = [(WHITE, data) for data in MARKS[app]()]
    return shapes, list(shapes)


def build(app: str, out: pathlib.Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    foreground, monochrome = launcher_layers(app)
    for name, paths in (
        ("ic_launcher_background", LAUNCHER_BACKGROUND),
        ("ic_launcher_foreground", foreground),
        ("ic_launcher_monochrome", monochrome),
    ):
        (out / f"{name}.xml").write_text(vector(paths, size=108))
        print(f"{name}.xml  ({app})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", choices=sorted(MARKS), required=True,
                        help="which app's mark to draw")
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=None,
        help="drawable directory to write into "
        "(an app points this at its own app/src/main/res/drawable; "
        "default: appicons/build/<app>/ for preview)",
    )
    args = parser.parse_args()
    out = args.out if args.out is not None else HERE / "build" / args.app
    build(args.app, out)


if __name__ == "__main__":
    main()
