# OLO Design

The shared design universe for the **OLO** family of Android apps. One palette,
one symbol set, one type and shape language, one app-icon family — so the four
apps read as parts of a whole rather than four separate things.

## The family

| App | What it is | Repository |
|-----|------------|------------|
| **OLO Explorer** | FTP/FTPS/SFTP file manager + viewers | `kgcaudit/filezilla-client` |
| **OLO Player** | Media player (video/music) | `kgcaudit/OLO-Player` |
| **OLO Cycle** | (cycling / activity) | `kgcaudit/OLO-Cycle` |
| **OLO eBook** | e-book reader — "Crosspoint Reader" | `kgcaudit/Crosspoint-Reader` |
| **OLO Design** | **this repo** — the single source of truth | `kgcaudit/OLO-Design` |

## How it is shared

Sessions do not share live memory; **this repository is the shared point.**

```
            OLO-Design  (design session owns & evolves it)
                 |  tokens, symbols, app icons, rules
     +-----------+-----------+-----------+
  Explorer     Player      Cycle      Crosspoint-Reader
   (each app session pulls the tokens & icons it needs into
    its own theme/ and res/drawable/, and re-syncs on a new version)
```

- The **design session** defines and advances the universe here: palette,
  symbol (tile) icons, app icons, typography and shape tokens, and the rules for
  how an app keeps its own identity while staying in the family.
- Each **app session** consumes it: it reads this repo (`add_repo`), copies the
  tokens and generated drawables it needs into its project, and re-syncs when a
  new version lands. An app never edits the universe in its own tree — changes
  go here first, then flow out.

## The look, in one line

Clay orange on warm ivory, tight corners, and a set of rounded-square symbol
tiles coloured by *hue* (not lightness) so nine kinds stay scannable — seeded
from OLO Explorer, which is the most developed of the four.

See `tokens/` for the exact values, `icons/` for the symbol set and the
`FileKind` contract, `appicons/` for the app-icon family, `docs/CONSUMING.md`
for how an app pulls it all in, and `docs/DESIGN-BRIEF.md` for the design
session's charter.

## Status

Seeded from OLO Explorer's shipping design, and now self-contained:

- **Tokens** — colour, type and shape are captured in `tokens/`, verified
  against Explorer's shipping `Theme.kt`.
- **Symbols** — the SVG sources (`icons/svg/`), the tile/flat build
  (`icons/build_from_svg.py`), the authored glyphs (`icons/authored_symbols.py`)
  and the static tiles (`icons/static/`) all live here. The build
  reproduces Explorer's drawables exactly. `icons/FILEKIND.md` holds the shared
  kind set and maps.
- **App icons** — `appicons/launcher.py` draws the shared clay ground and all
  four per-app marks (Explorer folder-tear, Player play, Cycle motion-loop,
  eBook open-book) from one place; wrappers in `appicons/mipmap/`.
- **Consumption** — `docs/CONSUMING.md` says exactly what each app copies or
  builds and where it goes.

Apps now adopt from here; new work is a deliberate universe change made here and
announced to the app sessions.
