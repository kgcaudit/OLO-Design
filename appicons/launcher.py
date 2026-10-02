#!/usr/bin/env python3
"""The OLO family's launcher icons: ink-brush marks on a value-graded clay ground.

A row of the four OLO apps on a home screen should read as one family and still
be told apart at a glance. They share the finish and differ only in the mark.

Two references set the finish:
  * an ink-brush painting on paper -- the *stroke-width variation* (thick and
    thin coexisting within one stroke) and the mix of solid ink masses with fine
    brushed lines, strokes layered so overlaps deepen on an object's structure;
  * a calligraphy wash -- the *value gradation*, one colour carried from light
    to deep rather than several colours.

So the family uses ONE hue (clay) graded by brightness, plus white. That keeps
to the three-colour rule: clay-as-a-value-family counts as one colour, white is
the second, and a per-app accent (unused today) would be the third.

  ground   clay, lit upper-left into depth lower-right -- a value gradation, with
           a soft sheen. Shared, identical for every app.
  mark     white, in the sumi manner: solid ink masses (folder, book cover, play
           triangle) beside variable-width brushed lines; each stroke is its own
           translucent layer, so where strokes cross -- a fold, a contour, a
           spine -- the white deepens on the object's defining structure.

  explorer   a filled folder with a small lined document sheet above it
  cycle      an ensō (a brushed open circle) with a free-form water-drop whose
             tail touches the ring -- period tracking, told calmly (no pink, no
             flower)
  ebook      an open book -- a filled cover, two brushed pages, a deep spine fold
  player     a filled play triangle inside a brushed double ring

No sunburst: the radial burst is Anthropic's mark, not ours. We borrow the clay
depth and the brush hand, and keep our own metaphors.

Everything is plain path geometry (no external deps). Each mark is auto-fitted
to the adaptive safe circle (radius 156.4 of 512) so no stroke clips under a
round mask. Paper *texture* itself is not baked in -- it does not survive a 48px
vector icon and is not cleanly vector; the "ink on paper" feeling is carried by
the stroke-width variation and the value gradation instead.

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
import re

HERE = pathlib.Path(__file__).resolve().parent
WHITE = "#FFFFFF"
CX = CY = 256.0
SAFE = 33.0 / 108.0 * 512.0  # 156.44 -- adaptive safe-circle radius

# The clay value ladder (light -> deep); the ground geometry is shared.
CLAY_LIGHT = "#F0A684"
CLAY_LIT = "#E8855F"
CLAY = "#C5613F"
CLAY_DEEP = "#A64D30"

# Per-stroke ink weights (alpha): translucent layers stack so overlaps deepen.
CT = 0.82    # ordinary contour stroke
FOLD = 0.96  # the defining fold/edge -- strongest
FINE = 0.52  # fine detail lines (text, hatching highlights)
FILL = 0.50  # a solid ink mass (folder body, book cover, play triangle, drop)
GH = 0.40    # the faintest depth / shadow side


# ---------------------------------------------------------------------------
# Brush geometry -- a variable-width stroke is a filled polygon whose half-width
# swells and dries along a centreline, the mark of a real brush. Strokes are
# emitted as separate translucent paths so crossings deepen the ink.
# ---------------------------------------------------------------------------

Pt = tuple
Stroke = tuple  # (pathData: str, alpha: float)


def _normals(pts):
    n = len(pts)
    out = []
    for i in range(n):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1.0
        out.append((-dy / d, dx / d))
    return out


def strk(pts, hw):
    """A filled variable-width stroke down centreline `pts` with half-widths `hw`."""
    nm = _normals(pts)
    L = [(pts[i][0] + nm[i][0] * hw[i], pts[i][1] + nm[i][1] * hw[i]) for i in range(len(pts))]
    R = [(pts[i][0] - nm[i][0] * hw[i], pts[i][1] - nm[i][1] * hw[i]) for i in range(len(pts))]
    d = "M%.1f,%.1f " % L[0]
    for p in L[1:]:
        d += "L%.1f,%.1f " % p
    for p in reversed(R):
        d += "L%.1f,%.1f " % p
    return d + "Z"


def quad(p0, c, p1, n=18):
    o = []
    for i in range(n):
        t = i / (n - 1)
        m = 1 - t
        o.append((m * m * p0[0] + 2 * m * t * c[0] + t * t * p1[0],
                  m * m * p0[1] + 2 * m * t * c[1] + t * t * p1[1]))
    return o


def wmod(n, lo, hi, bumps=1.5, phase=0.3):
    """Width profile: thick and thin coexist along one stroke (brush press/lift)."""
    return [lo + (hi - lo) * (0.15 + 0.85 * max(0.0, math.sin((i / (n - 1)) * math.pi * bumps + phase)) ** 0.7)
            for i in range(n)]


def seg(p0, c, p1, hi, lo=1.3, n=18, bumps=1.0, ph=0.0):
    return strk(quad(p0, c, p1, n), wmod(n, lo, hi, bumps, ph))


def dbl(p0, c, p1, hi, op, n=18, j=3.0, bumps=1.0):
    """A sketchy double stroke -- two offset passes -- for a hand-drawn contour."""
    a = seg(p0, c, p1, hi, 1.3, n, bumps, 0.2)
    b = seg((p0[0] + j, p0[1] + j * 0.6), (c[0] - j, c[1] + j),
            (p1[0] + j * 0.5, p1[1] - j * 0.6), hi * 0.75, 1.1, n, bumps, 1.1)
    return [(a, op), (b, op * 0.75)]


def fillpoly(corners, bow=5, seg_=6, jit=2.0):
    """A solid ink mass with slightly bowed, hand-wobbled edges."""
    pts = []
    n = len(corners)
    cx = sum(c[0] for c in corners) / n
    cy = sum(c[1] for c in corners) / n
    for i in range(n):
        a = corners[i]
        b = corners[(i + 1) % n]
        for s in range(seg_):
            t = s / seg_
            x = a[0] + (b[0] - a[0]) * t
            y = a[1] + (b[1] - a[1]) * t
            ox, oy = ((a[0] + b[0]) / 2 - cx), ((a[1] + b[1]) / 2 - cy)
            d = math.hypot(ox, oy) or 1.0
            bw = bow * math.sin(t * math.pi)
            x += ox / d * bw + jit * math.sin(t * 3 + i)
            y += oy / d * bw + jit * math.cos(t * 3 + i)
            pts.append((x, y))
    return "M" + " L".join("%.1f,%.1f" % p for p in pts) + " Z"


def arc(a0, a1, R, n=48, wob=4, ph=0, cx=CX, cy=CY):
    return [(cx + (R + wob * math.sin(i / (n - 1) * math.pi * 3 + ph)) * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))),
             cy + (R + wob * math.sin(i / (n - 1) * math.pi * 3 + ph)) * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1))))
            for i in range(n)]


def ring_band(pts, hw):
    """A CLOSED variable-width ring as two concentric contours + even-odd, so the
    hole is cut on every renderer. A single out-and-back `strk` contour relies on
    non-zero winding and fills as a solid disk under Android's VectorDrawable
    renderer -- this does not. Emitted with >1 'Z' so mark_vector sets evenOdd."""
    nm = _normals(pts)
    outer = [(pts[i][0] + nm[i][0] * hw[i], pts[i][1] + nm[i][1] * hw[i]) for i in range(len(pts))]
    inner = [(pts[i][0] - nm[i][0] * hw[i], pts[i][1] - nm[i][1] * hw[i]) for i in range(len(pts))]
    d = "M%.1f,%.1f " % outer[0] + "".join("L%.1f,%.1f " % p for p in outer[1:]) + "Z "
    d += "M%.1f,%.1f " % inner[0] + "".join("L%.1f,%.1f " % p for p in inner[1:]) + "Z"
    return d


def wline(p0, p1, hi, op, n=14):
    return (strk(quad(p0, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 2), p1, n),
                 wmod(n, 0.8, hi, 1, 0.2)), op)


def teardrop(cx, cy, rb, th, n=16):
    T = (cx, cy - th)
    pts = []
    for i in range(n):
        t = i / (n - 1)
        m = 1 - t
        pts.append((m * m * T[0] + 2 * m * t * (cx + rb * 0.98) + t * t * (cx + rb),
                    m * m * T[1] + 2 * m * t * (cy - th * 0.28) + t * t * cy))
    for i in range(1, n):
        a = math.radians(0 + 180 * i / (n - 1))
        pts.append((cx + rb * math.cos(a), cy + rb * math.sin(a)))
    for i in range(1, n):
        t = i / (n - 1)
        m = 1 - t
        pts.append((m * m * (cx - rb) + 2 * m * t * (cx - rb * 0.98) + t * t * T[0],
                    m * m * cy + 2 * m * t * (cy - th * 0.28) + t * t * T[1]))
    return pts


def drop_free(T, axdeg, L, rb, asym=1.3, n=12):
    """A free, asymmetric water-drop: tip at T, bulb hanging along axis `axdeg`."""
    a = math.radians(axdeg)
    u = (math.cos(a), math.sin(a))
    w = (-u[1], u[0])

    def M(lx, ly):
        return (T[0] + ly * u[0] + lx * w[0], T[1] + ly * u[1] + lx * w[1])

    def q(l0, c, l1):
        o = []
        for i in range(n):
            t = i / (n - 1)
            m = 1 - t
            o.append(M(m * m * l0[0] + 2 * m * t * c[0] + t * t * l1[0],
                       m * m * l0[1] + 2 * m * t * c[1] + t * t * l1[1]))
        return o

    P0 = (0, 0)
    P1 = (rb * asym, L - rb)
    P2 = (0, L)
    P3 = (-rb, L - rb)
    pts = q(P0, (rb * 0.95 * asym, (L - rb) * 0.42), P1)
    pts += q(P1, (rb * asym * 0.72, L + rb * 0.18), P2)[1:]
    pts += q(P2, (-rb * 0.66, L + rb * 0.12), P3)[1:]
    pts += q(P3, (-rb * 0.9, (L - rb) * 0.36), P0)[1:]
    return pts


def _polygon(pts):
    return "M" + " L".join("%.1f,%.1f" % p for p in pts) + " Z"


def scale_path(d, k, cx=CX, cy=CY):
    """Scale every coordinate pair in `d` by k about (cx, cy). Marks are M/L/Z
    only, so a coordinate-pair substitution is exact (no arc radii to mangle)."""
    def f(m):
        x = float(m.group(1))
        y = float(m.group(2))
        return f"{cx + (x - cx) * k:.1f},{cy + (y - cy) * k:.1f}"
    return re.sub(r"(-?\d+\.?\d*),(-?\d+\.?\d*)", f, d)


# ---------------------------------------------------------------------------
# The four marks -- each returns a list of (pathData, alpha) translucent strokes
# ---------------------------------------------------------------------------

def mark_explorer():
    s = []
    # back document sheet (small), lined
    doc = [(272, 154), (342, 146), (350, 232), (282, 242)]
    s.append((fillpoly(doc, bow=2.5, jit=1.3), 0.42))
    for a, b in zip(doc, doc[1:] + doc[:1]):
        s.append((seg(a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b, 3.4, 1.2), CT))
    for y in (172, 192, 212):
        s.append(wline((288, y), (342, y - 4), 2.6, FINE))
    # folder body, filled (the dominant mass)
    C = [(158, 374), (158, 236), (232, 236), (258, 266), (358, 266), (358, 374)]
    s.append((fillpoly(C, bow=4, jit=2), FILL))
    es = [(C[0], C[1]), (C[1], C[2]), (C[3], C[4]), (C[4], C[5]), (C[5], C[0])]
    for a, b in es:
        s += dbl(a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b, 5.5, CT, j=2.6)
    s.append((seg(C[2], (245, 251), C[3], 6.5, 1.6), FOLD))          # lid fold strongest
    s.append((seg((160, 330), (256, 326), (358, 330), 5, 1.4), CT))  # front crease
    s.append((seg((358, 266), (370, 281), (370, 374), 3.6, 1.2), GH))  # side depth
    return s


def mark_cycle():
    s = []
    R = 122.0
    # ensō ring (slightly lighter so the drop reads as the subject)
    s.append((strk(arc(28, 28 + 330, R, 60, 5), wmod(60, 2.2, 7)), 0.70))
    s.append((strk(arc(20, 20 + 160, R, 30, 6, 1.2), wmod(30, 2, 6)), 0.86))  # lap deepens
    # water-drop (period): asymmetric/free, tail touching the ring (upper-right)
    td = -58.0
    T = (CX + R * math.cos(math.radians(td)), CY + R * math.sin(math.radians(td)))
    dp = drop_free(T, 122, 84, 24, asym=1.32)
    s.append((_polygon(dp), 0.42))                                   # soft fill (강조 대상)
    s.append((strk(dp + [dp[0]], wmod(len(dp) + 1, 1.2, 4.2, 1.0)), FOLD))  # brush outline
    s.append((seg((272, 198), (266, 214), (273, 232), 1.6, 0.7), 0.50))     # inner highlight
    return s


def mark_ebook():
    s = []
    # cover block (filled, strong) -> anchors the book
    s.append((fillpoly([(170, 322), (256, 336), (342, 322), (346, 348), (256, 360), (166, 348)], bow=3, jit=1.5), FILL))
    # taller, slightly narrower pages
    s += dbl((252, 186), (208, 174), (166, 188), 8, CT)   # L top
    s += dbl((166, 188), (160, 258), (170, 324), 7, CT)   # L outer
    s += dbl((170, 324), (214, 330), (252, 328), 6, CT)   # L bottom
    s += dbl((260, 186), (304, 174), (346, 188), 8, CT)   # R top
    s += dbl((346, 188), (352, 258), (342, 324), 7, CT)   # R outer
    s += dbl((342, 324), (298, 330), (260, 328), 6, CT)   # R bottom
    # spine valley (fold) strongest + hatch
    s.append((seg((256, 330), (252, 260), (252, 186), 9, 2), FOLD))
    s.append((seg((256, 330), (260, 260), (260, 186), 9, 2), FOLD))
    for k in range(8):
        t = k / 7
        y = 198 + t * 120
        s.append((strk([(252 - 7 - 5 * math.sin(t * 6), y), (253, y + 6)], wmod(6, 1.3, 3.4)), 0.55))
        s.append((strk([(259, y + 6), (260 + 7 + 5 * math.sin(t * 6), y)], wmod(6, 1.3, 3.4)), 0.55))
    # text rows
    for y in (210, 232, 254, 276, 298):
        s.append(wline((178, y), (240, y - 2), 3, FINE))
        s.append(wline((272, y - 2), (334, y), 3, FINE))
    # page corner curl
    s.append((seg((346, 188), (330, 198), (340, 220), 4, 1.2), CT))
    return [(scale_path(p, 1.1), op) for p, op in s]


def mark_player():
    s = []
    # closed ring: two concentric contours + even-odd so the hole is cut on
    # Android (a single out-and-back contour fills as a disk there).
    s.append((ring_band(arc(0, 360, 152, 72, 4), wmod(72, 2.5, 6)), CT))     # ring
    s.append((strk(arc(14, 352, 144, 66, 5, 1.2), wmod(66, 2, 4.5)), 0.55))  # open second pass overlaps
    s.append((fillpoly([(214, 182), (342, 256), (214, 330)], bow=4, jit=2), 0.72))  # play triangle
    s += dbl((214, 182), (300, 214), (342, 256), 5, FOLD, j=2.2)
    s += dbl((342, 256), (300, 298), (214, 330), 5, FOLD, j=2.2)
    s.append((seg((214, 330), (210, 256), (214, 182), 6, 1.5), FOLD))
    return s


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
                android:startX="41" android:startY="20"
                android:endX="481" android:endY="502">
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
                <item android:offset="0" android:color="#26FFFFFF" />
                <item android:offset="1" android:color="#00FFFFFF" />
            </gradient>
        </aapt:attr>
    </path>
</vector>
"""


def mark_vector(strokes):
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<!-- Generated by appicons/launcher.py. Do not edit by hand. -->",
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"',
        '    android:width="108dp"',
        '    android:height="108dp"',
        '    android:viewportWidth="512"',
        '    android:viewportHeight="512">',
    ]
    for data, alpha in strokes:
        lines.append("    <path")
        lines.append(f'        android:fillColor="{WHITE}"')
        lines.append(f'        android:fillAlpha="{alpha:.2f}"')
        if data.count("Z") > 1:  # a compound (multi-contour) path -> cut holes
            lines.append('        android:fillType="evenOdd"')
        lines.append(f'        android:pathData="{data}" />')
    lines.append("</vector>")
    return "\n".join(lines) + "\n"


def _path_points(d):
    """On-path points of M/L/Z path data (the marks use nothing else)."""
    toks = re.findall(r"[A-Za-z]|-?\d*\.?\d+", d)
    params = {"M": 2, "L": 2, "Z": 0}
    pts = []
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
        coords = [(vals[j], vals[j + 1]) for j in range(0, k, 2)]
        for (px, py) in coords:
            ax, ay = (cx + px, cy + py) if rel else (px, py)
            pts.append((ax, ay))
        if coords:
            cx, cy = (cx + coords[-1][0], cy + coords[-1][1]) if rel else coords[-1]
    return pts


def max_radius(strokes):
    worst = 0.0
    for data, _ in strokes:
        for (x, y) in _path_points(data):
            worst = max(worst, math.hypot(x - CX, y - CY))
    return worst


def fit_to_safe(strokes, margin=2.0):
    """Uniformly scale the whole mark about centre so it sits inside the safe
    circle -- preserving every proportion the design locked, never clipping."""
    r = max_radius(strokes)
    k = min(1.0, (SAFE - margin) / r) if r > 0 else 1.0
    if k < 1.0:
        strokes = [(scale_path(d, k), a) for d, a in strokes]
    return strokes, r, k


def build(app, out):
    out.mkdir(parents=True, exist_ok=True)
    strokes, r0, k = fit_to_safe(MARKS[app]())
    r = max_radius(strokes)
    if r > SAFE + 0.5:
        raise SystemExit(f"{app}: mark reaches radius {r:.1f} > safe {SAFE:.1f}")
    (out / "ic_launcher_background.xml").write_text(BACKGROUND_XML, encoding="utf-8")
    (out / "ic_launcher_foreground.xml").write_text(mark_vector(strokes), encoding="utf-8")
    (out / "ic_launcher_monochrome.xml").write_text(mark_vector(strokes), encoding="utf-8")
    fit = "" if k >= 1.0 else f", fit x{k:.3f} from {r0:.1f}"
    print(f"{app}: background + foreground + monochrome  (maxR {r:.1f} / safe {SAFE:.1f}{fit})")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", choices=sorted(MARKS), required=True)
    parser.add_argument("--out", type=pathlib.Path, default=None,
                        help="drawable directory (default: appicons/build/<app>/ for preview)")
    args = parser.parse_args()
    out = args.out if args.out is not None else HERE / "build" / args.app
    build(args.app, out)


if __name__ == "__main__":
    main()
