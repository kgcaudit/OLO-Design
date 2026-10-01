# OLO symbol set

The in-app symbols — the coloured rounded-square **tiles** that stand in front
of a folder, a file kind, or a place — plus the flat single-colour glyphs used
in toolbars. Seeded from OLO Explorer.

## The tile

A tile is a rounded square (`small`, `10.dp`) filled with the kind's hue (see
`tokens/color.md`, `MaterialTheme.tiles`) carrying a **white glyph**. Kinds are
told apart by *hue*, not by lightness — so a wall of tiles stays scannable
before any glyph is read. Dark-theme hues are deliberately lighter than light
ones, because the glyph stays white on both.

### Two-tone white glyphs

Some glyphs are drawn two-tone (a solid white shape plus a semi-transparent
white detail) rather than a single flat white. These are authored with their
own opacity baked in and **must be drawn with `tint = Unspecified`** — tinting
them would collapse the two tones into one and lose the detail. A plain
single-colour glyph is tinted white as usual.

## The set

The tiles that ship in Explorer (`res/drawable/ic_tile_*.xml`), by meaning:

- **File/content kinds** — `folder`, `archive`, `comic` (open-book glyph on the
  archive hue), `document`, `image`, `video`, `audio`, `code`, `app`.
- **Places & actions** — `server`, `sdcard`, `recents`, `transfers`,
  `bookmark`, `search`, `trash`, `locked`, `phone`, `alert`.

Flat toolbar glyphs are the `ic_flat_*` set (`folder`, `server`, `transfers`,
`search`, `secure`, `log`, `warning`) — single-colour, tinted at use.

## FileKind → tile mapping

Each app maps a file (by extension) to a `FileKind`, and each kind to a tile +
its hue. The canonical kinds are the nine content hues above; COMIC is a
variant of ARCHIVE (same hue, open-book glyph). The extension→kind table lives
with each app's browse/list code; keep the *kind set* and the *kind→hue* map
identical across apps so the same file type wears the same colour everywhere.

## The build pipeline

Tiles are generated from SVG sources, not hand-edited:

- Sources: `tools/icons/svg/*.svg` in **OLO Explorer** (`kgcaudit/filezilla-client`).
- Generator: `tools/icons/build_from_svg.py` — crosses each SVG path over to an
  Android vector drawable verbatim, recolouring the pack's palette to OLO's via
  an explicit `RECOLOUR` map (written out, not computed — distance metrics
  misfiled hues quietly), flattening what Android needs extra machinery for,
  and dropping no-op clips. Nothing is redrawn.

The design session owns migrating these sources + generator into this repo so
every app builds its tiles from one place. Until then, the SVGs and the script
live in Explorer's tree and are pulled from there.
