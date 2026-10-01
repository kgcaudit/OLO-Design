# FileKind — the canonical kind set and maps

Every OLO app that shows files maps a name to a `FileKind`, a kind to a hue, and
a kind to a tile glyph. **The kind set and these maps are identical across all
apps** — the same file type wears the same colour and the same glyph everywhere,
which is the whole point of a shared symbol world. Seeded from OLO Explorer
(`ui/FileKind.kt`, `ui/FlatIcon.kt`). Change it here first, then flow out.

## The kinds

Coarse on purpose: colouring a row lets a list be *scanned* rather than read,
and a scan tells six or seven things apart, not thirty. So "a picture" is one
kind whether jpg or heic, and anything unrecognised is `OTHER`, not guessed.

| FileKind | Tile glyph | Hue (`MaterialTheme.tiles`) |
|----------|-----------|------------------------------|
| `FOLDER` | `ic_tile_folder` | `folder` |
| `ARCHIVE` | `ic_tile_archive` | `archive` |
| `COMIC` | `ic_tile_comic` | `archive` — same hue, open-book glyph; a tenth colour would not survive a scan |
| `IMAGE` | `ic_tile_image` | `image` |
| `VIDEO` | `ic_tile_video` | `video` |
| `AUDIO` | `ic_tile_audio` | `audio` |
| `DOCUMENT` | `ic_tile_document` | `document` |
| `EBOOK` | `ic_tile_book` | `document` — same hue as DOCUMENT, open-book glyph |
| `CODE` | `ic_tile_code` | `code` |
| `APP` | `ic_tile_app` | `app` |
| `OTHER` | `ic_tile_document` | `other` |

Nine content hues (`folder, archive, image, video, audio, document, code, app,
other`), eleven kinds — two of them ride a shared hue and are told apart by
glyph: `COMIC` rides `archive`, and `EBOOK` rides `document`. `OTHER` wears the
`document` glyph but the `other` hue.

`EBOOK` is the newest kind (2026-10, decided here): an e-book (epub) gets the
open-book `ic_tile_book` glyph while keeping the `document` slate hue — the same
move `COMIC` makes on the `archive` hue. It came from the OLO eBook app, whose
library wanted a book read apart from a plain document at a glance. Two things
were deliberately *not* adopted from eBook's own tiles: its teal for epub (teal
is `code`'s hue, and moving `code` would break the baseline), and its line-glyph
style (the family stays two-tone white fill). So `EBOOK` is document-slate +
a two-tone-fill open book. `ic_tile_book` carries no panel lines, which is what
tells it from `ic_tile_comic` (open book *with* panel lines, on the archive hue).

## Extension → kind

By extension only: a listing gives a name and a directory flag, and a server is
under no obligation to give a type. A name with no extension, or an extension
not in this table, is `OTHER`. A directory is always `FOLDER`.

| Kind | Extensions |
|------|------------|
| `ARCHIVE` | `zip rar 7z tar gz bz2 xz tgz iso alz egg a00 a01` |
| `COMIC` | `cbz cbr cb7 cbt` |
| `IMAGE` | `jpg jpeg png gif webp bmp heic heif tiff tif svg` |
| `VIDEO` | `mkv mp4 avi mov wmv flv webm m4v mpg mpeg ts m2ts` |
| `AUDIO` | `mp3 flac wav aac ogg m4a wma opus` |
| `EBOOK` | `epub` |
| `DOCUMENT` | `pdf doc docx xls xlsx ppt pptx txt md rtf odt hwp srt smi ass vtt sub` |
| `CODE` | `kt java py js ts json xml yml yaml html css sh c cpp h rs go rb php` |
| `APP` | `apk aab apks xapk` |

Notes carried from Explorer, kept so the table does not drift as apps copy it:

- **`alz`, `egg`** are ESTsoft's, everywhere in Korea, and Explorer opens both —
  so they are archives, not unknown files.
- **`cbz/cbr/cb7/cbt`** are archives underneath but common enough on a phone full
  of manga to earn the open-book `COMIC` tile, so a shelf of them is told from a
  shelf of plain zips.
- **Subtitles** (`srt smi ass vtt sub`) are `DOCUMENT`: they are text and sit
  beside the film they belong to; they should not look like a video.
- **`epub`** is `EBOOK`, not `DOCUMENT`: an e-book earns the open-book tile so a
  shelf of them reads apart from plain documents. **`pdf` and `txt` stay
  `DOCUMENT`** (document-slate, document glyph) across the family — an app that
  wants to tell pdf from txt inside its own UI may do so locally, but the family
  kind set does not split them. Other e-book formats (`mobi`, `azw3`, …) are not
  in the family set yet; add them here first if an app needs them.

## How an app adopts this

Copy the kind set, both maps, and this extension table verbatim into the app's
own browse/list code (Explorer keeps them in `ui/FileKind.kt` and the
`colourFor(kind)` function in `ui/FlatIcon.kt`). An app may key on a kind for its
own behaviour (Explorer's `looksMedia`, `looksPdf`, `looksEpub`, `looksVideo` are
examples) but may not change the kind set or the maps in its own tree — a change
lands here first.
