# OLO type & shape tokens

Seeded from OLO Explorer's shipping theme. These are the baseline for every
OLO app — change them here, never per app.

## Shape

Tight corners throughout — the family does not use pill or fully-rounded
shapes. Mapped onto Material3's `Shapes` roles so a component picks the right
radius by its own size:

| Role | Radius | Used by |
|------|--------|---------|
| extraSmall | `6.dp` | chips, small inline affordances |
| small | `10.dp` | tiles, list rows, buttons |
| medium | `14.dp` | cards |
| large | `18.dp` | sheets, larger cards |
| extraLarge | `20.dp` | dialogs, the biggest surfaces |

In Compose this is `Shapes(extraSmall = RoundedCornerShape(6.dp), …)` —
Explorer names it `OloShapes`.

### No pills: buttons take an explicit shape

Material3's buttons do **not** read their shape from the `Shapes` theme — a
`Button`, `OutlinedButton`, `TextButton`, `FilledTonalButton` and
`ElevatedButton` each default to `CornerFull`, a fully-rounded **pill/stadium**,
which the family does not use. Setting `OloShapes` alone does not fix this; left
untouched, every such button comes out a pill (this is why even Explorer shipped
pill buttons until it was corrected here).

So the family rule: **every pill-shaped button carries `shape =
MaterialTheme.shapes.small` (10.dp)** — the same corner as a tile or a list row.

```kotlin
Button(onClick = …, shape = MaterialTheme.shapes.small) { … }
OutlinedButton(onClick = …, shape = MaterialTheme.shapes.small) { … }
TextButton(onClick = …, shape = MaterialTheme.shapes.small) { … }
```

An app that has more than a couple of buttons should wrap this once rather than
repeat it — a small `OloButton`/`OloTextButton` that passes the shape, or (M3
1.2+) a `CompositionLocal`/`ButtonDefaults.shape` default — so a bare `Button`
can never slip back to a pill.

**Not pills, so left alone:** `FloatingActionButton` and
`ExtendedFloatingActionButton` keep their Material default (a ~16.dp rounded
rectangle, already between `medium` and `large`); `IconButton` is a circular hit
target, not a pill. Only the stadium buttons above tighten to 10.dp.

## Type

Built on Material3's default `Typography`, with only the headline and the
largest title roles pulled down in size — Material's defaults run large for a
dense file/media UI, and a dialog that titles itself nearly twice the size of
the pane behind it reads as a different app. Everything not listed keeps the
Material default.

| Role | Size | Line height |
|------|------|-------------|
| headlineLarge | `28.sp` | `34.sp` |
| headlineMedium | `24.sp` | `30.sp` |
| headlineSmall | `20.sp` | `26.sp` |
| titleLarge | `19.sp` | `25.sp` |

In Compose, Explorer names it `OloTypography` and builds it by `.copy()`-ing
these four roles off the base `Typography()`. No custom font family yet — the
family rides the platform default; a chosen face, when one lands, is set here
first.

## How an app adopts these

Copy the four shape radii and the four type overrides into the app's own
`theme/` (Explorer keeps both in `ui/theme/Theme.kt`). Keep the role→value
mapping exact; an app may *add* roles it needs but may not change these
baseline values in its own tree — a change goes here first, then flows out.

Also apply the **no-pill button rule** above: give every stadium button
`shape = MaterialTheme.shapes.small`, ideally through one shared wrapper so a
plain `Button` can't regress to a pill. This changes a button's look from
Material's default, so it is a real adoption step, not just a theme copy.
