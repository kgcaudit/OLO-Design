# Consuming OLO Design

How an app session pulls the universe into its own tree. The rule throughout:
**an app pulls; it never edits the world here.** A change to any shared value is
made in `OLO-Design` first, then the apps re-sync. The design session announces
such a change; an app that notices drift should raise it here, not patch locally.

Explorer's own locations are given as the worked example (it is the seed); the
other three apps place the same things in the same kind of file.

## 0. Get the repo

```sh
# in the app session
add_repo kgcaudit/OLO-Design        # read
# then clone/pull it beside the app checkout, and re-pull on a new version
```

Nothing below is committed into OLO-Design by an app. The scripts write into the
app's tree via `--out`; the app commits the generated output in its own repo.

## 1. Colour, type, shape → the app's theme

**Source:** `tokens/color.md`, `tokens/type-shape.md`
**Explorer keeps it in:** `app/src/main/kotlin/org/filezilla/android/ui/theme/Theme.kt`

Copy, as Compose values, keeping every name and hex/dp/sp exact:

- the brand constants (`Clay #B95B3B`, `ClayLight`, `Stone`, `StoneLight`);
- the **full** light and dark `ColorScheme` — *every* role, including the surface
  ladder and containers. An unset role is not an omission; Material fills it from
  its own purple baseline (this is why dialogs once came up lavender). No
  Material-You / dynamic colour anywhere.
- `TileColors` (the nine tile hues, light + dark) exposed as `MaterialTheme.tiles`;
- `StatusColors` (`running, waiting, paused, done, failed, progressTrack`, light +
  dark) exposed as `MaterialTheme.status`;
- `OloShapes` — `6 / 10 / 14 / 18 / 20 dp`;
- `OloTypography` — the four pulled-down roles (`headlineLarge 28`,
  `headlineMedium 24`, `headlineSmall 20`, `titleLarge 19`), `.copy()`-ed off the
  base `Typography()`; everything else stays Material default.

An app may *add* roles it needs; it may not change these baseline values locally.

**No-pill buttons.** `OloShapes` alone does not fix button corners: Material3's
`Button`/`OutlinedButton`/`TextButton`/`FilledTonalButton`/`ElevatedButton`
default to a fully-rounded pill, independent of the theme. Give every such button
`shape = MaterialTheme.shapes.small` (10.dp) — ideally via one shared
`OloButton` wrapper so a bare `Button` can't regress. `FloatingActionButton`,
`ExtendedFloatingActionButton` and `IconButton` are not pills and are left as-is.
See `../tokens/type-shape.md`.

## 2. Tiles and flat glyphs → the app's drawables

**Source:** `icons/svg/` + `icons/build_from_svg.py` + `icons/authored_symbols.py`
+ `icons/static/`
**Explorer keeps it in:** `app/src/main/res/drawable/ic_tile_*.xml`,
`ic_flat_*.xml`

Build straight into the app's drawable folder, then copy the static tiles:

```sh
python3 icons/build_from_svg.py    --out <app>/app/src/main/res/drawable
python3 icons/authored_symbols.py  --out <app>/app/src/main/res/drawable
cp icons/static/*.xml              <app>/app/src/main/res/drawable/
```

This produces the full set: content-kind tiles, place/action tiles, and the
`ic_flat_*` toolbar glyphs. An app that needs only some of them can delete the
drawables it does not reference after the build; it does **not** fork the SVG
sources or the `RECOLOUR` table into its own tree.

Two rules the rendering code must honour (see `icons/README.md`):

- the tile glyph XML is only the **white** shape — the coloured square behind it
  is drawn in Compose from the matching `tiles` hue, picked by `FileKind`;
- two-tone glyphs (solid white + `#8CFFFFFF`) render with **`tint = Unspecified`**.

## 3. FileKind → the app's browse/list code

**Source:** `icons/FILEKIND.md`
**Explorer keeps it in:** `ui/FileKind.kt` (kinds + extension table) and the
`colourFor(kind)` function in `ui/FlatIcon.kt` (kind → hue).

Copy the kind set, the extension→kind table, and the kind→hue / kind→glyph maps
verbatim. Keep them identical across apps so the same file type wears the same
colour and glyph everywhere. An app may key its own behaviour off a kind; it may
not change the set or the maps locally.

## 4. Launcher icon → the app's mipmap + drawables

**Source:** `appicons/launcher.py` + `appicons/mipmap/`
**Explorer keeps it in:** `app/src/main/res/drawable/ic_launcher_*.xml` +
`app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml`, `ic_launcher_round.xml`

Each app builds **its own** mark and copies the shared wrappers:

```sh
python3 appicons/launcher.py --app <explorer|player|cycle|ebook> \
    --out <app>/app/src/main/res/drawable
cp appicons/mipmap/*.xml <app>/app/src/main/res/mipmap-anydpi-v26/
```

That writes `ic_launcher_background.xml` (shared ground, identical for every
app), `ic_launcher_foreground.xml` and `ic_launcher_monochrome.xml` (the app's
mark). The wrappers point at those three by name, so no rename is needed.

`shapely` is required only for `--app explorer` (the torn folder); the other
three build with the standard library alone.

## Re-syncing on a new version

When OLO-Design advances, an app re-pulls and re-runs whichever of the four steps
changed:

| What moved here | App re-does |
|-----------------|-------------|
| a hex / radius / type size / tile hue | step 1 (Theme.kt) — and step 2 if a tile hue moved behind a white glyph that must stay readable |
| an SVG source, the recolour table, or an authored/static glyph | step 2 |
| the FileKind set, extension table, or a map | step 3 (and step 2 if a glyph was added) |
| the launcher frame or a mark | step 4 |

Because the generated drawables carry a `Do not edit by hand` header, re-running
a script overwrites cleanly; an app reviews the diff and commits it in its own
repo.
