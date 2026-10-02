#!/usr/bin/env python3
"""OLO control glyphs -- menu / dropdown / in-app action icons, in the pack hand.

A third glyph layer beside the tiles and the flat toolbar glyphs. Where a tile
says what a thing IS (a file kind on a coloured square), a control glyph names a
MENU ACTION or an IN-APP ACTION: sort, view, refresh, rotate, delete, and so on.

The rule the family follows -- symbols come from the one source art pack -- holds
here too. Every control glyph the pack already draws is taken FROM the pack and
flattened to a single ink (its own geometry, verbatim); only the controls the
pack has no drawing for are hand-authored, drawn to the pack's weight so the two
read as one hand.

  pack-derived   refresh, search, settings(gear), sort_date(clock),
                 sort_type(tag), scope_folder(pin), hidden(lock), delete(trash);
                 folders_first and location_off build on the pack's folder / pin.
  hand-authored  sort_name(A·Z), sort_size(bars), sort_asc, sort_desc,
                 view_list, view_grid, playlist, rotate_left, rotate_right, map.

Finish (one hue, tint-ready):
  * 24 x 24 viewport (matches the Material icons these replace);
  * a single ink -- the pack figure solid (`INK`), the pale body at ~40%
    (`BODY`), the pack's white detail dropped; hand strokes at `SW`, round
    cap + join. The RGB is a neutral fallback; the consumer TINTS the glyph to
    its row's text colour (`app:iconTint` on a MenuItem, `app:tint` on an
    ImageView, `tint =` on a Compose Icon), and the baked alphas survive the
    tint so the two-tone reading is kept.

Names: `ic_menu_*` for the menu layer, `ic_action_*` for the in-app action layer
(registered one-glyph-one-action in an app's IconMeaningTest).

Usage:
    python3 icons/control_symbols.py                       # preview into icons/build/
    python3 icons/control_symbols.py --out PATH/res/drawable   # straight into an app
"""
from __future__ import annotations

import argparse
import pathlib
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
SVG = HERE / "svg"
NS = "{http://www.w3.org/2000/svg}"

INK = "#FF574D45"          # pack figure, and all hand strokes/fills
BODY = "#66574D45"         # pack pale body, ~40% so figure still leads
SW = 2.0                   # hand-stroke weight, tuned to the pack
FIGURE_BELOW = 0.62        # same split as build_from_svg
WHITE_ABOVE = 0.90         # pack white detail / knock-out -> dropped


def _lightness(c: str) -> float:
    c = c.strip()
    if c in ("white",):
        return 1.0
    v = c.lstrip("#")
    if len(v) == 3:
        v = "".join(x * 2 for x in v)
    try:
        r, g, b = (int(v[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return 0.5
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def _ink_for(light: float, mode: str):
    """Pick the ink for one pack fill, by lightness and the glyph's recipe.

    A pack control drawing is a main shape plus a white knock-out detail (a
    clock's hands, a pin's centre, a tag's hole). A blind lightness split turns
    the main shape into a solid blob and throws the detail away, so each pack
    glyph names how it should read:

      twotone     figure(<.62)->INK, mid->BODY, white(>.90)->drop  (default)
      silhouette  every non-white -> INK, white -> drop            (solid mark)
      marker      every non-white -> INK, white -> BODY            (keep inset)
      invert      white -> INK, everything else -> BODY            (hands on face)
    """
    near_white = light > WHITE_ABOVE
    if mode == "invert":
        return INK if near_white else BODY
    if mode == "marker":
        return BODY if near_white else INK
    if near_white:
        return None                                         # drop
    if mode == "silhouette":
        return INK
    return INK if light < FIGURE_BELOW else BODY            # twotone


def mono(stem: str, mode: str = "twotone") -> list[tuple]:
    """A pack SVG flattened to one ink: (pathData, colour, None, evenOdd)."""
    root = ET.parse(SVG / f"{stem}.svg").getroot()
    out: list[tuple] = []

    def walk(node: ET.Element) -> None:
        for el in node:
            if el.tag == f"{NS}g":
                walk(el)
                continue
            if el.tag == f"{NS}defs":
                continue
            fill = el.get("fill")
            if not fill or fill == "none":
                continue
            light = 0.30 if fill.startswith("url(") else _lightness(fill)
            colour = _ink_for(light, mode)
            if colour is None:
                continue
            eo = el.get("fill-rule") == "evenodd"
            if el.tag == f"{NS}path":
                out.append((el.get("d", ""), colour, None, eo))
            elif el.tag == f"{NS}rect":
                x, y, w, h = (float(el.get(k, 0)) for k in ("x", "y", "width", "height"))
                out.append((f"M{x},{y} h{w} v{h} h{-w} Z", colour, None, eo))
    walk(root)
    return out


def S(d: str, w: float = SW) -> tuple:      # a hand stroke
    return (d, None, w, False)


def F(d: str) -> tuple:                      # a hand solid fill
    return (d, INK, None, False)


def C(cx: float, cy: float, r: float) -> tuple:   # a hand solid dot / disc
    return F(f"M{cx - r},{cy} A{r},{r} 0 1 0 {cx + r},{cy} "
             f"A{r},{r} 0 1 0 {cx - r},{cy} Z")


# ---- hand-authored gaps (pack has no drawing), drawn to the pack weight -----
GAPS = {
    "ic_menu_sort_name": [
        S("M3.4,11 L6,4.2 L8.6,11"), S("M4.5,8.6 L7.5,8.6"),
        S("M3.4,14 L8.6,14 L3.4,20 L8.6,20"),
        S("M17.5,5 L17.5,18"), S("M15,15.5 L17.5,18.3 L20,15.5"),
    ],
    "ic_menu_sort_size": [
        F("M4.5,13 h3 v6.5 h-3 Z"), F("M10.5,9 h3 v10.5 h-3 Z"),
        F("M16.5,5 h3 v14.5 h-3 Z"),
    ],
    "ic_menu_sort_asc": [F("M12,4.5 L17,10.5 L13.5,10.5 L13.5,19.5 L10.5,19.5 L10.5,10.5 L7,10.5 Z")],
    "ic_menu_sort_desc": [F("M12,19.5 L7,13.5 L10.5,13.5 L10.5,4.5 L13.5,4.5 L13.5,13.5 L17,13.5 Z")],
    "ic_menu_view_list": [
        F("M4,5.5 h2.8 v2.8 h-2.8 Z"), F("M4,10.6 h2.8 v2.8 h-2.8 Z"), F("M4,15.7 h2.8 v2.8 h-2.8 Z"),
        S("M9,6.9 L20,6.9", 2.4), S("M9,12 L20,12", 2.4), S("M9,17.1 L20,17.1", 2.4),
    ],
    "ic_menu_view_grid": [
        S("M5.6,4.2 L9.6,4.2 Q11,4.2 11,5.6 L11,9.6 Q11,11 9.6,11 L5.6,11 Q4.2,11 4.2,9.6 L4.2,5.6 Q4.2,4.2 5.6,4.2 Z"),
        S("M14.4,4.2 L18.4,4.2 Q19.8,4.2 19.8,5.6 L19.8,9.6 Q19.8,11 18.4,11 L14.4,11 Q13,11 13,9.6 L13,5.6 Q13,4.2 14.4,4.2 Z"),
        S("M5.6,13 L9.6,13 Q11,13 11,14.4 L11,18.4 Q11,19.8 9.6,19.8 L5.6,19.8 Q4.2,19.8 4.2,18.4 L4.2,14.4 Q4.2,13 5.6,13 Z"),
        S("M14.4,13 L18.4,13 Q19.8,13 19.8,14.4 L19.8,18.4 Q19.8,19.8 18.4,19.8 L14.4,19.8 Q13,19.8 13,18.4 L13,14.4 Q13,13 14.4,13 Z"),
    ],
    "ic_menu_view_gallery": [       # stacked photo + mountain/sun (photo grid)
        S("M9.1,4.5 L17.9,4.5 Q19.5,4.5 19.5,6.1 L19.5,12.4 Q19.5,14 17.9,14 L9.1,14 Q7.5,14 7.5,12.4 L7.5,6.1 Q7.5,4.5 9.1,4.5 Z"),
        S("M6.1,8 L14.9,8 Q16.5,8 16.5,9.6 L16.5,17.4 Q16.5,19 14.9,19 L6.1,19 Q4.5,19 4.5,17.4 L4.5,9.6 Q4.5,8 6.1,8 Z"),
        S("M5.4,18 L9,13.5 L11.2,16 L13.2,13 L15.6,18"),
        S("M6.7,11.2 A1.3,1.3 0 1 0 9.3,11.2 A1.3,1.3 0 1 0 6.7,11.2 Z"),
    ],
    "ic_menu_view_compact": [       # dense horizontal rows, no bullets
        S("M4,6.2 L20,6.2"), S("M4,9.6 L20,9.6"), S("M4,13 L20,13"),
        S("M4,16.4 L20,16.4"), S("M4,19.8 L14,19.8"),
    ],
    "ic_menu_playlist": [
        S("M4,7 L15,7"), S("M4,12 L15,12"), S("M4,17 L11,17"),
        S("M19.2,16 L19.2,7.6"), S("M19.2,7.6 L21.2,9"),
        F("M17.4,14.3 a1.9,1.9 0 1 0 0.01,0 Z"),
    ],
    "ic_action_rotate_left": [
        S("M6.5,10 L16,10 L16,19.5 L6.5,19.5 Z"),
        S("M13,6.2 A6.2,6.2 0 0 0 4.6,9.2"), S("M4.2,6.3 L4.4,9.4 L7.3,9.1"),
    ],
    "ic_action_rotate_right": [
        S("M8,10 L17.5,10 L17.5,19.5 L8,19.5 Z"),
        S("M11,6.2 A6.2,6.2 0 0 1 19.4,9.2"), S("M19.8,6.3 L19.6,9.4 L16.7,9.1"),
    ],
    "ic_action_map": [
        S("M3.5,6.5 L9,4.5 L15,6.5 L20.5,4.5 L20.5,17.5 L15,19.5 L9,17.5 L3.5,19.5 Z"),
        S("M9,4.5 L9,17.5"), S("M15,6.5 L15,19.5"),
    ],
    # --- overflow / app-wide actions (pack has no drawing; drawn to its weight) ---
    "ic_menu_more": [C(12, 5.6, 1.6), C(12, 12, 1.6), C(12, 18.4, 1.6)],
    "ic_menu_upload": [
        S("M4,15 L4,19 Q4,20 5,20 L19,20 Q20,20 20,19 L20,15"),
        S("M12,16.5 L12,5"), S("M8,9 L12,5 L16,9"),
    ],
    "ic_menu_sync": [
        S("M5,11 A7,7 0 0 1 16.8,6.9"), S("M14.2,6.2 L17.2,6.8 L16.6,9.9"),
        S("M19,13 A7,7 0 0 1 7.2,17.1"), S("M9.8,17.8 L6.8,17.2 L7.4,14.1"),
    ],
    "ic_menu_select_all": [
        S("M2.5,12 L6,15.5 L11.5,9"), S("M9.5,12.5 L13,16 L21.5,6.5"),
    ],
    "ic_menu_view_options": [       # tune / sliders
        S("M4,7 L20,7"), S("M4,12 L20,12"), S("M4,17 L20,17"),
        C(8, 7, 2), C(15, 12, 2), C(10, 17, 2),
    ],
    "ic_menu_associations": [       # an app square + an "open out" arrow
        S("M5.5,7 Q5.5,5.5 7,5.5 L13,5.5 Q14.5,5.5 14.5,7 L14.5,13 "
          "Q14.5,14.5 13,14.5 L7,14.5 Q5.5,14.5 5.5,13 Z"),
        S("M12,18.5 L19,18.5 L19,11.5"), S("M16,15.5 L19,18.5"),
    ],
}

# ---- pack-derived (verbatim pack geometry, flattened to one ink) ------------
# (name, source stem, mode) -- mode chosen so the knock-out detail reads right.
PACK = {
    "ic_menu_refresh": ("122.최신화,새로고침", "twotone"),
    "ic_menu_search": ("025.검색", "twotone"),
    "ic_menu_settings": ("027.설정,관리", "marker"),      # gear teeth solid, centre inset
    "ic_menu_sort_date": ("120.시간,기록", "invert"),     # pale face, solid hands
    "ic_menu_sort_type": ("036.태그", "silhouette"),      # solid tag
    "ic_menu_scope_folder": ("055.위치,GPS", "invert"),   # pale pin, solid centre dot
    "ic_menu_hidden": ("070.잠금,숨김", "twotone"),       # padlock
    "ic_action_delete": ("030.휴지통,삭제", "twotone"),   # bin + ribs
    "ic_menu_select": ("113.승인,완료", "invert"),        # pale disc, solid check
}

# ---- composed: a pack glyph plus a hand mark -------------------------------
def _composed() -> dict:
    return {
        # folder (pack) + an up-chevron: folders to the top
        "ic_menu_folders_first": mono("012.폴더,저장소", "silhouette") + [S("M9.2,15 L12,12.2 L14.8,15", 2.2)],
        # location pin (pack) + a slash: remove location
        "ic_action_location_off": mono("055.위치,GPS", "invert") + [S("M4,4 L20,20", 2.2)],
        # box (pack) + an up-arrow out: unarchive (marker keeps the pale body)
        "ic_menu_unarchive": mono("045.상자", "marker") + [
            S("M12,9 L12,2.5"), S("M9,5 L12,2.2 L15,5")],
        # folder (pack) + a plus: new folder
        "ic_menu_new_folder": mono("012.폴더,저장소", "silhouette") + [
            S("M16.5,15 L21,15"), S("M18.75,12.75 L18.75,17.25")],
    }


def all_glyphs() -> dict:
    out = {name: mono(stem, mode) for name, (stem, mode) in PACK.items()}
    out.update(_composed())
    out.update(GAPS)
    return out


def vector(paths: list[tuple]) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<!-- Generated by icons/control_symbols.py. Do not edit by hand. -->",
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"',
        '    android:width="24dp"',
        '    android:height="24dp"',
        '    android:viewportWidth="24"',
        '    android:viewportHeight="24">',
    ]
    for data, fill, stroke_w, even_odd in paths:
        lines.append("    <path")
        if stroke_w is not None:
            lines.append('        android:fillColor="#00000000"')
            lines.append(f'        android:strokeColor="{INK}"')
            lines.append(f'        android:strokeWidth="{stroke_w}"')
            lines.append('        android:strokeLineCap="round"')
            lines.append('        android:strokeLineJoin="round"')
        else:
            lines.append(f'        android:fillColor="{fill}"')
            if even_odd:
                lines.append('        android:fillType="evenOdd"')
        lines.append(f'        android:pathData="{data}" />')
    lines.append("</vector>")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=pathlib.Path, default=HERE / "build",
                        help="drawable directory (default: icons/build/ for preview)")
    args = parser.parse_args()
    out: pathlib.Path = args.out
    out.mkdir(parents=True, exist_ok=True)
    glyphs = all_glyphs()
    for name, paths in glyphs.items():
        (out / f"{name}.xml").write_text(vector(paths), encoding="utf-8")
        print(f"{name}.xml")
    print(f"{len(glyphs)} control glyphs -> {out}")


if __name__ == "__main__":
    main()
