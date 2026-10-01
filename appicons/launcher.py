#!/usr/bin/env python3
"""The OLO family's launcher icons: ink-brush marks on a value-graded clay ground.

A row of the four OLO apps on a home screen should read as one family and still
be told apart at a glance. They share the finish and differ only in the mark.

Two references set the finish:
  * an ink-brush painting on paper -- the *stroke-width variation* (a stroke
    swelling then drying to a thin tail) and the mix of solid ink masses with
    fine brushed lines;
  * a calligraphy wash -- the *value gradation*, one colour carried from light
    to deep rather than several colours.

So the family uses ONE hue (clay) graded by brightness, plus white. That keeps
to the three-colour rule: clay-as-a-value-family counts as one colour, white is
the second, and a per-app accent (unused today) would be the third.

  ground   clay, lit upper-left into depth lower-right -- a value gradation, with
           a soft sheen. Shared, identical for every app.
  mark     white, in the sumi manner: solid ink masses (folder, book, play) with
           variable-width brushed lines (the rays, the spine, and Cycle's ensō).

  explorer   a folder with files flying off as tapered brush strokes
  cycle      an ensō -- a brushed open circle, a cycle told calmly; with a marker
  ebook      an open book, two pages and a brushed spine
  player     a play triangle with tapered sound strokes

No sunburst: the radial burst is Anthropic's mark, not ours. We borrow the clay
depth and the brush hand, and keep our own metaphors.

Everything is plain path geometry (no external deps), kept inside the adaptive
safe circle (radius 156.4 of 512) so no mark clips under a round mask. Paper
*texture* itself is not baked in -- it does not survive a 48px vector icon and is
not cleanly vector; the "ink on paper" feeling is carried by the stroke-width
variation and the value gradation instead.

    python3 appicons/launcher.py --app explorer --out PATH/res/drawable
    python3 appicons/launcher.py --app cycle    --out PATH/res/drawable
    python3 appicons/launcher.py --app ebook    --out PATH/res/drawable
    python3 appicons/launcher.py --app player   --out PATH/res/drawable

It writes ic_launcher_background.xml (shared), ic_launcher_foreground.xml and
ic_launcher_monochrome.xml (the app's mark). The adaptive-icon wrappers live in
appicons/mipmap/ and are copied as-is into each app's mipmap-anydpi-v26/.
"""
from __future__ import annotations

import argparse
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
WHITE = "#FFFFFF"
CX = CY = 256.0
SAFE = 33.0 / 108.0 * 512.0  # 156.44 -- adaptive safe-circle radius

# The clay value ladder (light -> deep) and the ground geometry are shared.
CLAY_LIGHT = "#F0A684"
CLAY_LIT = "#E8855F"
CLAY = "#C5613F"
CLAY_DEEP = "#A64D30"


# ---------------------------------------------------------------------------
# Brush geometry -- a variable-width stroke is a filled polygon whose half-width
# swells along a centreline and dries to a thin tail, the mark of a real brush.
# ---------------------------------------------------------------------------

def _normals(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    n = len(pts)
    out = []
    for i in range(n):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1.0
        out.append((-dy / d, dx / d))
    return out


def brush(pts: list[tuple[float, float]], hw: list[float]) -> str:
    """A filled variable-width stroke down the centreline `pts` with half-widths `hw`."""
    nm = _normals(pts)
    left = [(pts[i][0] + nm[i][0] * hw[i], pts[i][1] + nm[i][1] * hw[i]) for i in range(len(pts))]
    right = [(pts[i][0] - nm[i][0] * hw[i], pts[i][1] - nm[i][1] * hw[i]) for i in range(len(pts))]
    d = "M%.1f,%.1f " % left[0]
    for p in left[1:]:
        d += "L%.1f,%.1f " % p
    for p in reversed(right):
        d += "L%.1f,%.1f " % p
    return d + "Z"


def circle(cx: float, cy: float, r: float) -> str:
    return (f"M{cx - r:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 1 0 {cx + r:.1f},{cy:.1f} "
            f"A{r:.1f},{r:.1f} 0 1 0 {cx - r:.1f},{cy:.1f} Z")


def enso(R: float = 116.0, a0: float = 18.0, sweep: float = 326.0,
         n: int = 60, wmax: float = 24.0, wmin: float = 4.0) -> str:
    """A brushed open circle: swells through the sweep, dries to a thin tail."""
    pts, hw = [], []
    for i in range(n):
        t = i / (n - 1)
        ang = math.radians(a0 + sweep * t)
        r = R + 5.0 * math.sin(t * math.pi * 2.0)  # a little hand-wobble
        pts.append((CX + r * math.cos(ang), CY + r * math.sin(ang)))
        prof = math.sin(min(1.0, t * 1.15) * math.pi) ** 0.7
        hw.append(wmin + (wmax - wmin) * prof)
    return brush(pts, hw)


def ray(angle_deg: float, r0: float, r1: float, wmax: float) -> str:
    """A tapered brush stroke from r0 (thin point) to r1 (round, full)."""
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    pts = [(CX + ux * r0, CY + uy * r0),
           (CX + ux * (r0 + r1) / 2, CY + uy * (r0 + r1) / 2),
           (CX + ux * r1, CY + uy * r1)]
    return brush(pts, [2.5, wmax * 0.7, wmax])


def rounded_tri(cx: float, cy: float, size: float, r: float = 24.0) -> str:
    pts = [(cx - size * 0.78, cy - size), (cx + size * 1.02, cy), (cx - size * 0.78, cy + size)]
    seg: list[str] = []
    for i in range(3):
        p0, p1, p2 = pts[(i - 1) % 3], pts[i], pts[(i + 1) % 3]

        def unit(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            d = math.hypot(dx, dy) or 1.0
            return dx / d, dy / d

        ux, uy = unit(p1, p0)
        vx, vy = unit(p1, p2)
        bk = min(r, math.hypot(p0[0] - p1[0], p0[1] - p1[1]) / 2,
                 math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / 2)
        a = (p1[0] + ux * bk, p1[1] + uy * bk)
        b = (p1[0] + vx * bk, p1[1] + vy * bk)
        seg.append((f"M{a[0]:.1f},{a[1]:.1f}" if i == 0 else f"L{a[0]:.1f},{a[1]:.1f}")
                   + f" Q{p1[0]:.1f},{p1[1]:.1f} {b[0]:.1f},{b[1]:.1f}")
    return " ".join(seg) + " Z"


def _book_page(sign: float) -> str:
    g = 8.0
    it = (CX + sign * g, 196.0)
    ot = (CX + sign * 122.0, 216.0)
    ob = (CX + sign * 122.0, 320.0)
    ib = (CX + sign * g, 336.0)
    tc = (CX + sign * 70.0, 200.0)
    bc = (CX + sign * 70.0, 332.0)
    return (f"M{it[0]:.1f},{it[1]:.1f} Q{tc[0]:.1f},{tc[1]:.1f} {ot[0]:.1f},{ot[1]:.1f} "
            f"L{ob[0]:.1f},{ob[1]:.1f} Q{bc[0]:.1f},{bc[1]:.1f} {ib[0]:.1f},{ib[1]:.1f} Z")


# ---------------------------------------------------------------------------
# The four marks (white path data, inside the safe circle)
# ---------------------------------------------------------------------------

def mark_explorer() -> list[str]:
    folder = ("M150,212 q0,-16 16,-16 h62 q10,0 16,8 l16,20 h94 q16,0 16,16 "
              "v92 q0,16 -16,16 h-188 q-16,0 -16,-16 Z")
    return [folder, ray(-58, 118, 150, 24), ray(-43, 114, 146, 19), ray(-28, 110, 140, 15)]


def mark_cycle() -> list[str]:
    # An ensō -- a brushed circle, read as a cycle, calm and discreet (no pink,
    # no flower, no drop). The marker sits where the stroke begins again.
    return [enso(), circle(CX, CY - 116, 15)]


def mark_ebook() -> list[str]:
    spine = brush([(CX, 196.0), (CX, 336.0)], [3.0, 9.0])
    return [_book_page(-1.0), _book_page(1.0), spine]


def mark_player() -> list[str]:
    tri = rounded_tri(212, 256, 92)
    return [tri, ray(-26, 120, 150, 22), ray(0, 124, 152, 26), ray(26, 120, 150, 22)]


MARKS = {
    "explorer": mark_explorer,
    "cycle": mark_cycle,
    "ebook": mark_ebook,
    "player": mark_player,
}


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

# The shared ground: a clay value gradation (light upper-left -> deep lower-right)
# plus a soft sheen. One hue, brightness-graded.
BACKGROUND_XML = f"""<?xml version="1.0" encoding="utf-8"?>
<!-- Generated by appicons/launcher.py. Do not edit by hand. -->
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="512"
    android:viewportHeight="512">
    <path android:pathData="M0,0 L512,0 L512,512 L0,512 Z">
        <aapt:attr name="android:fillColor">
            <gradient
                android:type="linear"
                android:startX="40" android:startY="20"
                android:endX="480" android:endY="500">
                <item android:offset="0" android:color="{CLAY_LIGHT}" />
                <item android:offset="0.35" android:color="{CLAY_LIT}" />
                <item android:offset="0.72" android:color="{CLAY}" />
                <item android:offset="1" android:color="{CLAY_DEEP}" />
            </gradient>
        </aapt:attr>
    </path>
    <path android:pathData="M0,0 L512,0 L512,512 L0,512 Z">
        <aapt:attr name="android:fillColor">
            <gradient
                android:type="radial"
                android:centerX="154" android:centerY="123"
                android:gradientRadius="300">
                <item android:offset="0" android:color="#33FFFFFF" />
                <item android:offset="1" android:color="#00FFFFFF" />
            </gradient>
        </aapt:attr>
    </path>
</vector>
"""


def mark_vector(paths: list[str]) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<!-- Generated by appicons/launcher.py. Do not edit by hand. -->",
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"',
        '    android:width="108dp"',
        '    android:height="108dp"',
        '    android:viewportWidth="512"',
        '    android:viewportHeight="512">',
    ]
    for data in paths:
        lines.append("    <path")
        lines.append(f'        android:fillColor="{WHITE}"')
        if data.count("Z") > 1:
            lines.append('        android:fillType="evenOdd"')
        lines.append(f'        android:pathData="{data}" />')
    lines.append("</vector>")
    return "\n".join(lines) + "\n"


def _path_points(d: str) -> list[tuple[float, float]]:
    """Every on-path point of SVG path data, tracking the pen through absolute
    and relative commands (arc radii/flags are skipped; the arc endpoint is
    kept). Control points of Q/C are included, which only over-estimates the
    reach -- fine for a conservative safe-zone bound."""
    import re
    toks = re.findall(r"[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?", d)
    params = {"M": 2, "L": 2, "T": 2, "H": 1, "V": 1, "Q": 4, "S": 4, "C": 6, "A": 7, "Z": 0}
    pts: list[tuple[float, float]] = []
    i = 0
    cx = cy = 0.0
    cmd = ""
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in ("Z", "z"):
                continue
        up = cmd.upper()
        rel = cmd.islower()
        k = params[up]
        vals = [float(v) for v in toks[i:i + k]]
        i += k
        if up == "H":
            cx = (cx + vals[0]) if rel else vals[0]
        elif up == "V":
            cy = (cy + vals[0]) if rel else vals[0]
        elif up == "A":
            ex, ey = vals[5], vals[6]
            cx, cy = (cx + ex, cy + ey) if rel else (ex, ey)
        else:
            coords = [(vals[j], vals[j + 1]) for j in range(0, k, 2)]
            for (px, py) in coords:
                ax, ay = (cx + px, cy + py) if rel else (px, py)
                pts.append((ax, ay))
            cx, cy = (cx + coords[-1][0], cy + coords[-1][1]) if rel else coords[-1]
        pts.append((cx, cy))
    return pts


def max_radius(paths: list[str]) -> float:
    worst = 0.0
    for d in paths:
        for (x, y) in _path_points(d):
            worst = max(worst, math.hypot(x - CX, y - CY))
    return worst


def build(app: str, out: pathlib.Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    paths = MARKS[app]()
    r = max_radius(paths)
    if r > SAFE + 0.5:
        raise SystemExit(f"{app}: mark reaches radius {r:.1f} > safe {SAFE:.1f}")
    (out / "ic_launcher_background.xml").write_text(BACKGROUND_XML, encoding="utf-8")
    (out / "ic_launcher_foreground.xml").write_text(mark_vector(paths), encoding="utf-8")
    (out / "ic_launcher_monochrome.xml").write_text(mark_vector(paths), encoding="utf-8")
    print(f"{app}: background + foreground + monochrome  (maxR {r:.1f} / safe {SAFE:.1f})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", choices=sorted(MARKS), required=True)
    parser.add_argument("--out", type=pathlib.Path, default=None,
                        help="drawable directory (default: appicons/build/<app>/ for preview)")
    args = parser.parse_args()
    out = args.out if args.out is not None else HERE / "build" / args.app
    build(args.app, out)


if __name__ == "__main__":
    main()
