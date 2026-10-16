# OLO layout tokens

Shared spacing, sizing, and the one responsive breakpoint. Seeded from OLO
Calendar (`design/Layout.kt`), kept here so every app lays out to the same
measures — change them here, never per app. In Compose these are `Dp` constants
(Explorer/Calendar name the object `OloLayout`).

## The breakpoint

| Token | Value | Meaning |
|-------|-------|---------|
| WideBreakpoint | `600.dp` | at/above this width an app may switch to its wide layout — a navigation **rail** + two panes instead of a **drawer** + single pane |

`600.dp` is the family's one width switch; it is the same width at which a sound
effect is allowed to spatialise (see `sound.md`), because both mean "this is a
real wide surface, not a phone held upright."

## Shared primitives

| Token | Value | Used for |
|-------|-------|----------|
| TouchTarget | `48.dp` | minimum touch target |
| IconSize | `24.dp` | a control glyph in a bar or row (matches the `ic_menu_*` / `ic_action_*` viewport) |
| TopBarHeight | `56.dp` | the top app bar |
| ContentMargin | `16.dp` | side margin of lists and sheets |
| DrawerWidth | `280.dp` | a modal / standard navigation drawer |
| RailWidth | `96.dp` | the navigation rail used instead of the drawer past `WideBreakpoint` |

## Calendar grid (OLO Calendar)

The month grid is laid tighter than Material's 16dp so the cells stay wide
(Samsung's calendar sits near 11dp); the rest are the calendar's own measures.

| Token | Value | Meaning |
|-------|-------|---------|
| GridMarginCompact | `12.dp` | side margin of the month grid on a phone |
| GridMarginWide | `24.dp` | side margin of the month grid on a wide surface |
| CellGap | `3.dp` | gap between day cells |
| LinesRow | `52.dp` | week-row height in the month view's "lines" stage |
| QuickBarSpace | `84.dp` | room kept clear at the bottom for the floating quick-add bar |

An app uses only the tokens it needs and may add its own; it does not change
these baseline values locally.
