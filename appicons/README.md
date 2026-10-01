# OLO app-icon family

The four apps' launcher icons are siblings: one finish, one mark each. A row of
them on a home screen reads as one family and is still told apart at a glance.
Drawn from one script, `launcher.py`.

## The finish (shared)

Two references set it: an **ink-brush painting** (stroke-width variation — a
stroke that swells then dries to a thin tail — and solid ink masses beside fine
brushed lines) and a **calligraphy wash** (value gradation — one colour carried
light to deep, not several colours).

- **Ground** — clay, lit upper-left into depth lower-right: a **value
  gradation** (`#F0A684 → #E8855F → #C5613F → #A64D30`) with a soft sheen. One
  hue, brightness-graded. Shared, identical for every app
  (`ic_launcher_background.xml`).
- **Mark** — **white**, in the sumi manner: solid ink masses (folder, book,
  play) together with **variable-width brushed lines** (the rays, the book
  spine, and Cycle's ensō). Kept inside the adaptive safe circle (radius 156.4
  of 512) so nothing clips under a round mask (`ic_launcher_foreground.xml`).
- **Monochrome** — the same white mark for themed-icon mode
  (`ic_launcher_monochrome.xml`); the launcher flattens it to one tint.

**Three-colour rule.** Clay-as-a-value-family counts as one colour, white is the
second; a per-app accent (unused today) would be the third. The gradation is
brightness, not extra colours.

**The OS adds its own drop shadow**, and themed mode drops the gradient/sheen —
both expected. Paper *texture* is deliberately not baked in: it does not survive
a 48px vector icon and is not cleanly vector, so the "ink on paper" feeling is
carried by the stroke-width variation and the value gradation instead.

## The marks (per app)

| App | Mark |
|-----|------|
| **OLO Explorer** | a folder with files flying off as tapered brush strokes |
| **OLO Cycle** | an **ensō** — a brushed open circle, a cycle told calmly and discreetly, with a marker (period tracking; no pink, no flower, no drop) |
| **OLO eBook** | an open book — two pages and a brushed spine |
| **OLO Player** | a play triangle with tapered sound strokes (video + music) |

**No sunburst.** The radial burst is Anthropic's / Claude's brand mark, not
ours; we borrow the clay depth and the brush hand, and keep our own metaphors so
each icon says what its app *is* and no icon is mistaken for Claude.

## How icons are authored

`launcher.py` draws all four from plain path geometry — no external
dependencies. A variable-width brush stroke is a filled polygon whose half-width
swells along a centreline and dries to a thin tail. The clay value constants sit
at the top so the ground re-renders when the palette moves. Every build checks
the mark stays inside the safe circle and refuses otherwise.

```sh
# each app builds its own three launcher drawables
python3 appicons/launcher.py --app explorer --out <app>/app/src/main/res/drawable
python3 appicons/launcher.py --app cycle    --out <app>/app/src/main/res/drawable
python3 appicons/launcher.py --app ebook    --out <app>/app/src/main/res/drawable
python3 appicons/launcher.py --app player   --out <app>/app/src/main/res/drawable

# plus the shared adaptive-icon wrappers, same for every app
cp appicons/mipmap/*.xml <app>/app/src/main/res/mipmap-anydpi-v26/
```

With no `--out`, the script writes to `appicons/build/<app>/` for preview.

## Preview (optional)

`cairosvg` + `pillow` render a flat preview; the real icon is the vector
drawable above. Only needed if you want a PNG to look at.
