# OLO Design — session charter

This repo is owned by a dedicated **design session**. Its job is to define and
advance one visual world for the four OLO apps, and to keep this repo as the
single source of truth the apps pull from. This file is that session's standing
brief.

## The world, in a sentence

Clay orange on warm ivory; tight corners; no Material-You; file/symbol kinds
told apart by **hue** (a set of coloured rounded-square tiles); each app its own
sibling in one family — same tile language, same clay-ground launcher, one
white mark apiece.

## What lives here

| Path | Holds |
|------|-------|
| `tokens/color.md` | the canonical palette — brand, light/dark roles, status, tiles |
| `tokens/type-shape.md` | the four shape radii and the type overrides |
| `icons/` | the tile symbol set + the two-tone-white rule + the `FileKind` contract (`FILEKIND.md`); the SVG sources (`svg/`), the tile/flat build (`build_from_svg.py`), the authored glyphs (`authored_symbols.py`) and the static tiles (`static/`) |
| `appicons/` | the shared launcher frame + the per-app marks, drawn from `launcher.py`; the adaptive-icon wrappers in `mipmap/` |
| `docs/CONSUMING.md` | what each app copies or builds, and where it goes |
| `docs/` | this charter and any design notes |

Everything is seeded from **OLO Explorer** (`kgcaudit/filezilla-client`), the
most developed of the four. The seed values are the baseline, not a draft:
treat Explorer's shipping numbers as correct unless there is a reason on the
record to move them.

## How the session works

1. **Read the seed first.** Start from the files already here. Then
   `add_repo kgcaudit/filezilla-client` (read) and pull the real artefacts the
   token files point at — `ui/theme/Theme.kt`, `tools/icons/svg/*`,
   `tools/icons/build_from_svg.py`, `tools/icons/authored.py`,
   `res/drawable/ic_tile_*.xml`, the launcher drawables — so the canonical files
   here are built from what actually ships, not from memory.
2. **Make this repo self-contained.** Migrate the SVG sources, the tile build
   script, and the icon-authoring script into this repo so every app builds its
   symbols and icons from one place rather than from Explorer's tree.
3. **Draw the family out.** Settle the per-app launcher marks (Explorer=folder+
   document, Player=play triangle in a ring, Cycle=ensō + water-drop for period
   tracking, eBook=open book). The icons are white **ink-brush** marks (sumi:
   solid masses + variable-width brushed lines, each stroke a translucent layer
   so overlaps deepen on an object's structure) on a shared clay
   **value-gradation** ground — one hue graded by brightness, plus white (a
   per-app accent would be the third colour, unused today). No sunburst
   (Anthropic's mark); identity is the metaphor, never a second palette. See
   `../appicons/README.md`.
4. **Document consumption.** For each token/icon group, say exactly what an app
   copies and where it goes (Explorer keeps colour+type+shape in
   `ui/theme/Theme.kt`, tiles in `res/drawable/`). An app pulls; it does not
   edit the world in its own tree.

## Hard constraints

- **Do not break Explorer's baseline.** The seeded hex values, radii, type
  sizes, and tile hues are what ships; a change to any of them is a deliberate
  universe change made here, announced to the app sessions, not a silent edit.
- **No Material-You / dynamic colour** anywhere in the family.
- Tiles are told apart by **hue, not lightness**; dark hues stay lighter than
  light ones because the glyph is always white.
- Two-tone white glyphs render with `tint = Unspecified`.
- Keep the FileKind set and the kind→hue map identical across all apps.

## The flow, once more

```
  design session  →  evolves this repo  →  app sessions pull on a new version
```

The design session never commits into an app's repo; an app session never
edits the world here. Changes land here first, then flow out.
