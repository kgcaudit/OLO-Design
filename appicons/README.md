# OLO app-icon family

The four apps' launcher icons are siblings, not strangers: same silhouette
language, same clay ground, one distinct white mark each. A row of them on a
home screen should read as one family and still be told apart at a glance.
Seeded from OLO Explorer; the frame and all four marks are drawn from one script
here now.

## The shared frame

- **Adaptive icon** (`mipmap/ic_launcher.xml` + `ic_launcher_round.xml`): a
  `background`, a `foreground`, and a `monochrome` layer (for themed icons). These
  two wrappers are identical for every app and are copied as-is into the app's
  `mipmap-anydpi-v26/`.
- **Ground** — a clay diagonal gradient, top-left `#E07B55` to bottom-right
  `#C5613F`, on a 512 viewport (`ic_launcher_background.xml`). Shared by every
  app; a home screen is thirty icons competing for one glance, and a flat
  mid-tone loses it, so the ground is a ramp.
- **Mark** — a single flat **white** shape, centred inside the 512 grid with
  heavy margin so it sits safely within every OEM mask (circle, squircle,
  rounded square), no strokes, no inner gradients (`ic_launcher_foreground.xml`).
- **Monochrome** — the same mark as a single-colour silhouette for themed-icon
  mode (`ic_launcher_monochrome.xml`).

## What differs per app — the mark

Each app keeps the clay ground and changes only the white mark, so the apps are
told apart by *silhouette* the way the tiles are told apart by hue:

| App | Mark | Drawn as |
|-----|------|----------|
| **OLO Explorer** | a folder coming apart, its far corner torn into flying strips | polygon arithmetic (needs `shapely`) |
| **OLO Player** | a play triangle | rounded polygon |
| **OLO Cycle** | a circular motion arrow — cyclic activity | ring band + arrowhead |
| **OLO eBook** | an open book, two facing pages from a centre spine | two fanned page paths |

The Cycle mark reads the one idea the app's name and "activity" share — cyclic
motion — as a single bold loop rather than the two-arrow recycle symbol, which
turns to mud at 48px. The eBook mark lets the clay ground show through the spine
gap, the way the `comic` tile does.

## How icons are authored

Not hand-written XML. `launcher.py` draws all four launcher sets: a 512 viewport,
~56px margin, solid white marks, rounded ends, no strokes, no gradients on the
mark. Explorer's folder cut-outs are done with real polygon arithmetic (needs
`shapely`) so the drawable carries plain paths, not clip-paths (Android does not
antialias clip-paths); the shapely import is deferred into the folder so the
other three apps build with nothing extra. Palette constants (`CLAY`, `CLAY_LIT`)
sit at the top so the ground re-renders when the palette moves.

```sh
# each app builds its own three launcher drawables
python3 appicons/launcher.py --app explorer --out <app>/app/src/main/res/drawable
python3 appicons/launcher.py --app player   --out <app>/app/src/main/res/drawable
python3 appicons/launcher.py --app cycle    --out <app>/app/src/main/res/drawable
python3 appicons/launcher.py --app ebook    --out <app>/app/src/main/res/drawable

# plus the shared adaptive-icon wrappers, same for every app
cp appicons/mipmap/*.xml <app>/app/src/main/res/mipmap-anydpi-v26/
```

With no `--out`, the script writes to `appicons/build/<app>/` for preview.

## A baseline note: the launcher clay is `#C5613F`

The ground's dark end is `#C5613F`, the clay *before* the 5% darkening that took
the theme brand to `#B95B3B` for WCAG AA. A launcher ground carries no text, so
the lighter clay is fine and is Explorer's shipping baseline. Like any baseline
value it moves here first, deliberately, not per app.
