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
| `icons/` | the tile symbol set + the two-tone-white rule + FileKind mapping; eventually the SVG sources and `build_from_svg.py` |
| `appicons/` | the shared launcher frame + the per-app mark; eventually the authoring script |
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
   arrow, Player=play, Cycle=activity, eBook=open book) and any per-app accent
   within the shared palette. Each app keeps the clay ground and the tile
   language; identity is the mark and, where needed, one accent — never a second
   palette.
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
