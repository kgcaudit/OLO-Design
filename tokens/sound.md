# OLO sound & motion tokens

The family's rule for **where a sound comes from**: a sound starts on the side
the movement started, and sweeps along with it, so hand, eye, and ear all tell
one story.

Decided 2026-10-05; first shipped in **OLO eBook 0.48.1** (the page-turn sound).
It governs **every** OLO sound effect from here on, not only the reader — change
it here, never per app.

## The principle

When something moves across the screen from one side, its sound begins there and
is carried along the motion. The pan follows the **moving thing**, not the point
the finger touched.

- **Page turn.** Left→right reading: the *next* page is the right-hand leaf
  folding over, so its sound comes from the **right**; the *previous* page comes
  from the **left**. A right→left comic is mirrored.
- **Other motions.** A side panel that opens from the right sounds from the
  right; a row swiped away to the left sweeps **left**.

## The sweep

The pan is not fixed — it travels with the motion:

| Point | Pan | Meaning |
|-------|-----|---------|
| start | **+0.7**, on the motion-origin side | where the movement begins |
| end | **−0.3** (just past centre) | carried through and a little beyond |

`−1` is hard left, `+1` is hard right; the sign of `start` is the origin side,
so a **left**-origin motion mirrors to `−0.7 → +0.3`. The sweep crosses slightly
past centre rather than pinning to one side — a sound heard many times a day
tires one ear if it always lands in the same place.

## The strength (loudness per channel)

Take the family's existing equal-power pan law (`cos`/`sin` across the two
channels), multiply it by **√2**, then clamp each channel at **1.0**:

- at **centre** the two channels are `0.707 × √2 = 1.0` — the sound stays its
  original size, not quieter;
- at a **full side** the louder channel would be `1.0 × √2 = √2`, so the clamp
  holds it at `1.0` — it stops there instead of clipping.

## When to place it left/right — and when not

Spatialise **only when left and right are really left and right**:

- wired/Bluetooth **earphones**, **landscape** orientation, or width **≥ 600dp**
  (an unfolded foldable or a tablet).

Otherwise play it **centred**. A phone held upright has its speakers at the top
and the bottom, so a left/right split comes out as a top/bottom split — the wrong
axis. When in doubt, centre it.

## Two rules that keep it simple

- **No in-app setting.** Someone who needs mono gets it from the phone's
  accessibility **"Mono audio"**, which folds the channels for the whole system;
  the app does not add a toggle of its own.
- **One mono source only.** Ship a single mono clip per effect. The swept
  (stereo) versions are generated on first use and **cached** — the APK does not
  grow, and there is one file to change when the sound changes.

## Reference implementation

Seeded from OLO eBook — `kgcaudit/Crosspoint-Reader`,
`android/ui-design/.../PageTurnFx.kt`:

| Symbol | Does |
|--------|------|
| `turnSide` | which side the motion starts (origin → sign of the pan) |
| `spatialTurnSound` | the gate: earphones / landscape / ≥ 600dp, else centre |
| `turnSweep` | the `+0.7 → −0.3` travel |
| `sweepStereo` | the `cos`/`sin × √2`, clamped at 1.0; renders and caches |

An app pulls this **rule**, not the file: it wires its own effects (a swipe, a
panel, a page) to the same sweep, strength, gate, and caching. The reference is
where to read the exact shape; the law above is the canon.
