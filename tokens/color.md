# OLO colour tokens

The canonical palette for every OLO app. Values are seeded from OLO Explorer's
shipping theme (the most developed of the four) and are the baseline — change
them here, never per app. Hex is ARGB (`0xAARRGGBB`).

No Material-You dynamic colour anywhere: the family has one palette, deliberately.

## Brand

| Token | Hex | Note |
|-------|-----|------|
| Clay | `0xFFB95B3B` | the brand orange; deep enough that white text on it meets WCAG AA |
| ClayLight | `0xFFE8A183` | primary in dark theme; inversePrimary in light |
| Stone | `0xFF6E5C50` | warm-neutral secondary |
| StoneLight | `0xFFD6C3B4` | |

## Light scheme (roles)

| Role | Hex |
|------|-----|
| primary | `0xFFB95B3B` (Clay) |
| onPrimary | `0xFFFFFFFF` |
| primaryContainer | `0xFFF6E0D6` |
| onPrimaryContainer | `0xFF4A1E0C` |
| secondary | `0xFF6E5C50` (Stone) |
| secondaryContainer | `0xFFEFE6DE` |
| tertiary | `0xFF3E7F80` (teal) |
| tertiaryContainer | `0xFFCDE5E4` |
| background / surface | `0xFFF7F4EF` (ivory) |
| onSurface | `0xFF1D1A16` |
| surfaceVariant | `0xFFECE5DC` |
| onSurfaceVariant | `0xFF574D45` |
| surfaceTint | `0xFFB95B3B` (Clay) |
| outline | `0xFF8B7F74` |
| outlineVariant | `0xFFD6CCC1` |
| error | `0xFFA50E2E` (crimson, pulled past red so it is not confused with clay) |
| onError | `0xFFFFFFFF` |
| errorContainer | `0xFFF8DCDA` |
| onErrorContainer | `0xFF3B100B` |

Surface ladder (so Material never fills a gap with purple): surfaceBright
`0xFFFBF9F5`, surfaceDim `0xFFDFD8CC`, containerLowest `0xFFFFFFFF`, containerLow
`0xFFFCFAF6`, container `0xFFF3EFE8`, containerHigh `0xFFEDE8DF`, containerHighest
`0xFFE7E1D6`.

## Dark scheme (roles that differ)

primary `0xFFE8A183` (ClayLight) · background / surface `0xFF181613` · onSurface
`0xFFE8E3DA` · surfaceVariant `0xFF49423A` · error `0xFFFFB0BE`. The surface
ladder and containers have parallel dark values; see Explorer's `theme/Theme.kt`
(`DarkColors`) for the full set to lift.

## Status colours (`MaterialTheme.status`)

Transfer / progress state, kept cool so it never reads as the warm brand. Fields:
`running, waiting, paused, done, failed, progressTrack`.

| Field | Light | Dark |
|-------|-------|------|
| running | `0xFF1273BE` | `0xFF7FC0F5` |
| waiting | `0xFF7A6F65` | (lighter variant) |
| paused | `0xFF9C7A0C` | `0xFFE0BE52` |
| done | `0xFF1B7F4B` | `0xFF6FD79B` |
| failed | `0xFF9E0C2B` | `0xFFFFB0BE` |
| progressTrack | `0xFFDCD3C6` | `0xFF39434D` |

## Tile colours (`MaterialTheme.tiles`) — the symbol palette

Each file/symbol kind gets its own hue, so ~9 tiles stay scannable by colour
before the glyph is read. Told apart by **hue, not lightness.** Dark values are
deliberately *lighter* than light ones, because a tile carries a white glyph and
must stay light-on-dark.

| Kind | Light | Dark |
|------|-------|------|
| folder | `0xFFB95B3B` (Clay) | `0xFFD1734F` |
| archive | `0xFF8A6A3B` (ochre) | `0xFFB08A54` |
| image | `0xFF2E8B6B` (green) | `0xFF3FA383` |
| video | `0xFF6A5A9E` (violet) | `0xFF8A7AC0` |
| audio | `0xFFB04A6A` (rose) | `0xFFC96B88` |
| document | `0xFF55606B` (slate) | `0xFF6E7A86` |
| code | `0xFF3E7F80` (teal) | `0xFF55A0A1` |
| app | `0xFF4C7A3E` (green) | `0xFF69985A` |
| other | `0xFF7A7168` (warm grey) | `0xFF938A80` |

(COMIC reuses the archive hue, told apart by an open-book glyph rather than a
tenth colour.)
