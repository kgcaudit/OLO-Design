# OLO app-icon family

The four apps' launcher icons are siblings, not strangers: same silhouette
language, same clay ground, one distinct white mark each. A row of them on a
home screen should read as one family.

## The shared frame

Seeded from OLO Explorer's launcher:

- **Adaptive icon** (`mipmap-anydpi-v26/ic_launcher.xml` +
  `ic_launcher_round.xml`): a `background`, a `foreground`, and a `monochrome`
  layer (for themed icons).
- **Ground** — a clay diagonal gradient, top-left `#E07B55` to bottom-right
  `#C5613F`, on a 512 viewport (`ic_launcher_background.xml`).
- **Mark** — a single flat **white** shape, centred with roughly 56px of margin
  inside the 512 grid, no strokes, no inner gradients
  (`ic_launcher_foreground.xml`). Keep the heavy inner padding so the mark sits
  safely inside every OEM mask (circle, squircle, rounded square).
- **Monochrome** — the same mark as a single-colour silhouette for themed-icon
  mode (`ic_launcher_monochrome.xml`).

## What differs per app — the mark

Each app keeps the clay ground and changes only the white mark, so the apps are
told apart by *silhouette* the way the tiles are told apart by hue:

| App | Mark (the idea) |
|-----|-----------------|
| **OLO Explorer** | a folder cut by a transfer arrow — files moving |
| **OLO Player** | a play triangle |
| **OLO Cycle** | (activity mark — the design session settles it) |
| **OLO eBook** | an open book / page |

The exact geometry of each mark is the design session's to draw; the frame
above is fixed.

## How icons are authored

Not hand-written XML. Explorer draws its launcher pieces in
`tools/icons/authored.py` — a 512 viewport, ~56px margin, solid palette fills,
rounded ends, no strokes, no gradients on the mark; the folder's cut-outs are
done with real polygon arithmetic (needs `shapely`) so the drawable carries
plain paths, not clip-paths (Android does not antialias clip-paths). Palette
constants (`CLAY`, `CLAY_SOFT`, …) sit at the top so the whole set re-renders
when the palette moves.

The design session owns bringing this authoring script into the repo and
drawing the four marks from one place.
