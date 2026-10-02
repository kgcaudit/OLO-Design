#!/usr/bin/env python3
"""OLO menu glyphs -- the leading icons for an app's menu / dropdown rows.

A second, smaller glyph language beside the tile set. Where the tile glyphs are
white masses on a coloured square (picked by FileKind), these are **line**
marks for text menus: a 24dp viewport, a single stroke weight, round ends, one
colour the consumer tints to match the row's text. They keep a whole app's
overflow / sort / view menus in the OLO hand instead of a mix of Material icons.

Baseline (do not drift; a change here is a universe change, announced):
  * viewport 24 x 24 (matches the Material icons they replace);
  * stroke 1.9, round cap + round join, no fill (a few solid accents aside:
    the slider knobs and the note head);
  * one colour, `MENU_INK` -- a neutral the app overrides with a tint
    (`app:iconTint` on a MenuItem, `app:tint` / `android:tint` on an
    ImageView) so the glyph always matches its label colour. Nothing here is
    theme-hardcoded beyond that fallback.

The set (file -> meaning):
  sort keys   ic_menu_sort_name / _sort_date / _sort_size / _sort_type
  direction   ic_menu_sort_asc / _sort_desc
  scope       ic_menu_scope_folder  (apply to this folder only -- a pin)
  grouping    ic_menu_folders_first (folders to the top)
  toggle      ic_menu_hidden        (show hidden -- an eye)
  view        ic_menu_view_list / _view_grid
  actions     ic_menu_refresh / _search / _playlist / _settings

`ic_menu_view_list/_view_grid/_refresh/_search/_playlist/_settings` replace the
Material ViewList / GridView / Refresh / Search / QueueMusic / Settings so the
whole menu is one family.

Usage:
    python3 icons/menu_symbols.py                       # preview into icons/build/
    python3 icons/menu_symbols.py --out PATH/res/drawable  # straight into an app
"""
from __future__ import annotations

import argparse
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# One neutral ink; the consumer tints it to the row's text colour.
MENU_INK = "#FF574D45"
STROKE_W = 1.9


def circle(cx: float, cy: float, r: float) -> str:
    return (f"M{cx - r},{cy} A{r},{r} 0 1 0 {cx + r},{cy} "
            f"A{r},{r} 0 1 0 {cx - r},{cy} Z")


def rrect(x: float, y: float, w: float, h: float, r: float) -> str:
    return (f"M{x + r},{y} L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} "
            f"L{x + w},{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h} "
            f"L{x + r},{y + h} Q{x},{y + h} {x},{y + h - r} "
            f"L{x},{y + r} Q{x},{y} {x + r},{y} Z")


# Each glyph is a list of (mode, pathData): "s" stroked, "f" filled (solid accent).
GLYPHS: dict[str, list[tuple[str, str]]] = {
    # --- sort keys ---
    "ic_menu_sort_name": [            # letters A / Z + a down arrow
        ("s", "M3.4,11 L6,4.2 L8.6,11"),
        ("s", "M4.5,8.6 L7.5,8.6"),
        ("s", "M3.4,14 L8.6,14 L3.4,20 L8.6,20"),
        ("s", "M17.5,5 L17.5,18"),
        ("s", "M15,15.5 L17.5,18.3 L20,15.5"),
    ],
    "ic_menu_sort_date": [            # a clock
        ("s", circle(12, 12, 7.6)),
        ("s", "M12,12 L12,7.3"),
        ("s", "M12,12 L15.6,13.4"),
    ],
    "ic_menu_sort_size": [           # bars, small -> large
        ("s", "M4,19.5 L20,19.5"),
        ("s", "M6.5,19.5 L6.5,14"),
        ("s", "M12,19.5 L12,10"),
        ("s", "M17.5,19.5 L17.5,5.5"),
    ],
    "ic_menu_sort_type": [           # a tag (kind / format)
        ("s", "M12,2.9 L21.1,2.9 L21.1,12 L12,21.1 L2.9,12 Z"),
        ("s", circle(17.1, 7.3, 1.35)),
    ],
    # --- direction ---
    "ic_menu_sort_asc": [
        ("s", "M12,19 L12,5"),
        ("s", "M7.6,9.6 L12,5.2 L16.4,9.6"),
    ],
    "ic_menu_sort_desc": [
        ("s", "M12,5 L12,19"),
        ("s", "M7.6,14.4 L12,18.8 L16.4,14.4"),
    ],
    # --- scope / grouping / toggle ---
    "ic_menu_scope_folder": [        # a pin: apply to this folder only
        ("s", "M12,21.2 C12,21.2 5.2,14.4 5.2,9.3 A6.8,6.8 0 1 1 18.8,9.3 "
              "C18.8,14.4 12,21.2 12,21.2 Z"),
        ("s", circle(12, 9.2, 2.5)),
    ],
    "ic_menu_folders_first": [       # folder + up chevron
        ("s", "M3.6,7.2 L9,7.2 L10.8,9 L19.6,9 Q20.6,9 20.6,10 L20.6,17.8 "
              "Q20.6,18.8 19.6,18.8 L4.6,18.8 Q3.6,18.8 3.6,17.8 Z"),
        ("s", "M9.2,15.6 L12,12.8 L14.8,15.6"),
    ],
    "ic_menu_hidden": [              # an eye (show hidden)
        ("s", "M3,12 Q12,4.6 21,12 Q12,19.4 3,12 Z"),
        ("s", circle(12, 12, 2.6)),
    ],
    # --- view ---
    "ic_menu_view_list": [
        ("s", rrect(4, 5.5, 2.6, 2.6, 0.6)), ("s", "M9,6.8 L20,6.8"),
        ("s", rrect(4, 10.7, 2.6, 2.6, 0.6)), ("s", "M9,12 L20,12"),
        ("s", rrect(4, 15.9, 2.6, 2.6, 0.6)), ("s", "M9,17.2 L20,17.2"),
    ],
    "ic_menu_view_grid": [
        ("s", rrect(4, 4, 7, 7, 1.4)), ("s", rrect(13, 4, 7, 7, 1.4)),
        ("s", rrect(4, 13, 7, 7, 1.4)), ("s", rrect(13, 13, 7, 7, 1.4)),
    ],
    # --- actions ---
    "ic_menu_refresh": [
        ("s", "M18.4,8.2 A7,7 0 1 0 19,12"),
        ("s", "M15.6,8.1 L18.5,8.4 L18.9,5.5"),
    ],
    "ic_menu_search": [
        ("s", circle(10.2, 10.2, 6.1)),
        ("s", "M14.6,14.6 L20,20"),
    ],
    "ic_menu_playlist": [           # list lines + a note (solid head)
        ("s", "M4,7 L15,7"), ("s", "M4,12 L15,12"), ("s", "M4,17 L11,17"),
        ("s", "M19.2,16 L19.2,7.6"), ("s", "M19.2,7.6 L21.2,9"),
        ("f", circle(17.4, 16.2, 1.9)),
    ],
    "ic_menu_settings": [           # sliders (tune): rails + solid knobs
        ("s", "M3,7 L21,7"), ("f", circle(8, 7, 2)),
        ("s", "M3,12 L21,12"), ("f", circle(15, 12, 2)),
        ("s", "M3,17 L21,17"), ("f", circle(10, 17, 2)),
    ],
}


def vector(paths: list[tuple[str, str]]) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<!-- Generated by icons/menu_symbols.py. Do not edit by hand. -->",
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"',
        '    android:width="24dp"',
        '    android:height="24dp"',
        '    android:viewportWidth="24"',
        '    android:viewportHeight="24">',
    ]
    for mode, data in paths:
        lines.append("    <path")
        if mode == "f":
            lines.append(f'        android:fillColor="{MENU_INK}"')
        else:
            lines.append('        android:fillColor="#00000000"')
            lines.append(f'        android:strokeColor="{MENU_INK}"')
            lines.append(f'        android:strokeWidth="{STROKE_W}"')
            lines.append('        android:strokeLineCap="round"')
            lines.append('        android:strokeLineJoin="round"')
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
    for name, paths in GLYPHS.items():
        (out / f"{name}.xml").write_text(vector(paths), encoding="utf-8")
        print(f"{name}.xml")
    print(f"{len(GLYPHS)} menu glyphs -> {out}")


if __name__ == "__main__":
    main()
