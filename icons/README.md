# OLO symbol set

The in-app symbols — the coloured rounded-square **tiles** that stand in front
of a folder, a file kind, or a place — plus the flat single-colour glyphs used
in toolbars. Seeded from OLO Explorer; the sources and the build live here now,
so every app builds the same symbols from this one place.

## The tile

A tile is a rounded square (`small`, `10.dp`) filled with the kind's hue (see
`../tokens/color.md`, `MaterialTheme.tiles`) carrying a **white glyph**. Kinds are
told apart by *hue*, not by lightness — so a wall of tiles stays scannable
before any glyph is read. Dark-theme hues are deliberately lighter than light
ones, because the glyph stays white on both.

The glyph XML is only the white shape; the coloured square behind it is drawn
by the app in Compose from the `tiles` token. So the same `ic_tile_folder.xml`
sits on a clay square in a file list and the colour, not the file, is picked at
the point of use.

### Two-tone white glyphs

Some glyphs are drawn two-tone (a solid white shape plus a semi-transparent
white detail, `#8CFFFFFF`) rather than a single flat white. These are authored
with their own opacity baked in and **must be drawn with `tint = Unspecified`** —
tinting them would collapse the two tones into one and lose the detail. A plain
single-colour glyph is tinted white as usual.

## The set

| Group | Tiles |
|-------|-------|
| **File/content kinds** | `folder`, `archive`, `comic` (open-book glyph on the archive hue), `book` (plain open-book glyph on the document hue, for epub), `document`, `image`, `video`, `audio`, `code`, `app` |
| **Places & actions** | `server`, `sdcard`, `recents`, `transfers`, `bookmark`, `search`, `trash`, `locked`, `phone`, `alert` |

Flat toolbar glyphs are the `ic_flat_*` set (`folder`, `server`, `transfers`,
`search`, `secure`, `log`, `warning`) — single-colour, tinted at use.

See `FILEKIND.md` for the canonical `FileKind` set, the extension→kind table,
and the kind→hue / kind→glyph maps that every app must mirror exactly.

## Menu glyphs (`ic_menu_*`)

A second, smaller glyph language for **menu / dropdown rows** (sort, view,
overflow). Where tiles are white masses on a coloured square, these are **line**
marks: a `24dp` viewport, one stroke weight (`1.9`, round cap + join), no fill
(bar a couple of solid accents — the slider knobs, the note head), and **one
colour the app tints** to match the row's text (`app:iconTint` on a `MenuItem`,
`app:tint` / `android:tint` on an `ImageView`). This keeps an app's menus in the
OLO hand instead of a mix of Material icons.

| Group | Glyphs |
|-------|--------|
| **Sort keys** | `sort_name` (A·Z), `sort_date` (clock), `sort_size` (bars), `sort_type` (tag) |
| **Direction** | `sort_asc` (↑), `sort_desc` (↓) |
| **Scope / grouping / toggle** | `scope_folder` (pin — apply to this folder only), `folders_first` (folder + ▲), `hidden` (eye — show hidden) |
| **View** | `view_list`, `view_grid` |
| **Actions** | `refresh`, `search`, `playlist`, `settings` (sliders) |

The view/refresh/search/playlist/settings five replace the Material ViewList /
GridView / Refresh / Search / QueueMusic / Settings so a whole menu is one
family. Authored in `menu_symbols.py` (24 viewport, line, tint-ready) — a
different language from the tiles on purpose; its baseline is stated at the top
of that file and a change to it is a universe change, announced.

## What is here

| Path | Holds |
|------|-------|
| `svg/` | the icon pack's SVG sources (126 drawings); only a subset is mapped to symbols |
| `build_from_svg.py` | SVG → vector-drawable builder for the pack-derived tiles and flat glyphs, recolouring as it goes |
| `authored_symbols.py` | the in-app glyphs the pack has no drawing for — `transfers`, `log`, `alert` |
| `menu_symbols.py` | the `ic_menu_*` line glyphs for menu / dropdown rows (24dp, tint-ready) |
| `static/` | the hand-authored tiles that no script generates — `comic`, `book`, `bookmark`, `recents`, `trash` |

(The launcher / app-icon marks are their own thing and live in `../appicons/`.)

## The build pipeline

Tiles and flat glyphs are generated from the SVG sources, not hand-edited:

- **`build_from_svg.py`** crosses each mapped SVG path over to an Android vector
  drawable verbatim (nothing is redrawn), recolouring the pack's palette to
  OLO's via an explicit `RECOLOUR` map (written out, not computed — distance
  metrics misfile hues quietly), flattening gradients Android would need extra
  machinery for, and dropping no-op clips. For a tile it re-reads each fill as
  figure or ground by lightness and emits white (solid or `#8CFFFFFF`); three
  knockout drawings are listed in `INVERTED` because the rule reads them
  backwards. An unmapped colour **stops the build** rather than being guessed.
- **`authored_symbols.py`** draws the three glyphs the pack does not contain, in
  the same language (512 viewport, ~56px margin, solid fills, no strokes, no
  gradients on a mark).
- **`static/`** holds the tiles that are themselves the source of truth —
  plain hand-written XML, copied as-is, regenerated by nothing.

```sh
pip install cairosvg pillow        # only needed for the preview scripts
python3 icons/build_from_svg.py    --out <app>/app/src/main/res/drawable
python3 icons/authored_symbols.py  --out <app>/app/src/main/res/drawable
cp icons/static/*.xml              <app>/app/src/main/res/drawable/
```

With no `--out`, each script writes to `icons/build/` for preview. The generated
drawables carry a `Do not edit by hand` header naming the script — a change goes
into the script (or the SVG, or `static/`), never into the emitted XML.

## A baseline note: the flat-glyph clay is `#C5613F`

`RECOLOUR` sends the pack's primary blue to `#C5613F`, the clay *before* the 5%
darkening that took the theme brand to `#B95B3B` for WCAG AA (see
`../tokens/color.md`). So a pack-derived flat glyph like `ic_flat_folder` carries
the lighter clay, while the theme's `primary` and the folder **tile hue** are the
darkened `#B95B3B`. This is Explorer's shipping baseline, kept as-is. It is a
candidate for a future deliberate unification — which, like any baseline change,
happens here first and is announced to the app sessions, never edited silently.

## How an app adopts these

An app pulls `OLO-Design` and runs the two scripts with `--out` pointed at its
own `res/drawable`, then copies `static/`. It does **not** fork the SVG sources
or the recolour table into its own tree; those stay here so every app's symbols
move together. See `../docs/CONSUMING.md` for the exact per-app steps.
