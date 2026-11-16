# The page

One HTML file, one stylesheet, one script, four vendored libraries. No
framework, no build step, no bundler. You can read all of it in an afternoon.

```
index.html          the shell — markup only, every list is rendered by JS
assets/app.css      design tokens, layout, the reader
assets/app.js       data loading, shelf, reader, four renderers
assets/vendor/      pdf.js · pdf.worker · epub.js · JSZip   (~1.7 MB, lazy)
data/               catalog · shards · categories · search-index
docs/assets/        README screenshots, support portrait, UPI QR
```

## Load order

`index.html` loads JSZip, then epub.js, then pdf.js, then `app.js`. epub.js is a
UMD bundle that expects a global `JSZip`, so the order is not cosmetic. All four
are vendored: a reading page makes no third-party request except Google Fonts,
which you can block without losing anything but the exact typeface.

## Data flow

```
boot()
  fetch data/catalog.json      ┐
  fetch data/shards.json       ├─ ?t=<Date.now()> and cache:'no-store'
  fetch data/categories.json   ┘
  fetch data/search-index.json
       │
       ├─ statBooks / statVaults / statCats / shard meter
       ├─ renderCats()  → the rail, with counts
       └─ render()      → the grid
```

Every fetch carries a unique query stamp. This is not belt-and-braces
paranoia — it is [D9](DECISIONS.md#d9--data-is-never-served-from-cache), written
after the shelf spent an hour showing ten books while the server held twenty-six.

## The two functions that matter

**`render()`** filters `state.catalog` by category and by query tokens, sorts,
and writes the grid. Search matches on `search-index.json` tokens (prefix match
per word, all words must hit), not on a live walk of the catalogue — so it stays
fast as the shelf grows.

**`cdn(book, fmt)`** turns a record into a URL:

```js
`${shards[book.vault].cdn}/books/${book.slug}/${book.slug}.${fmt}`
```

The page never hardcodes a repository name. That is what lets a second vault
appear without a code change: `build_catalog.py` writes the new shard into
`shards.json`, and every book in it resolves.

## The reader

One shell, a switch on format:

| Format | Renderer | Notes |
|---|---|---|
| `pdf` | pdf.js canvas, or the native viewer at ≤820 px | see below |
| `epub` | epub.js, `flow: 'scrolled'` | best view on a phone |
| `txt` | `<pre>` wrapped by the browser | no fixed column count |
| `json` | the book's own `meta.json`, syntax-highlighted | the record *is* the content |

**Why two PDF paths.** A canvas I scale myself cannot be pinched, cannot scroll
past page one without me redrawing it, and needs the fit maths right on every
viewport. Under 820 px the reader hands the PDF to the browser's own viewer in a
full-width frame. Above it, pdf.js draws a page and `fitScale()` fits it to the
**smaller** of the width and height ratios, so a whole page always fits. A
resize or rotation re-fits after 180 ms rather than reopening the book. If the
canvas path throws, the native viewer takes over — a blank pane is never an
acceptable outcome.

**`withTimeout`** wraps the pdf.js document load in a 30-second race. Without it,
a stalled fetch looked exactly like an empty page, which cost a debugging round.

## Design tokens

Every colour is a CSS variable in `:root`, with a dark set under
`html[data-theme="dark"]`. The theme toggle only flips that attribute.

| Token | Light | Role |
|---|---|---|
| `--paper` | `#FAF7F2` | page |
| `--ink` | `#16130F` | text |
| `--accent` | `#8C3A2B` | oxblood — the mark, italics, links |
| `--teal` | `#1F4E46` | vault green — category tags, "open" state |
| `--gold` | `#A8823F` | spare |
| `--line` / `--line-2` | `#E2DACD` / `#D3C8B7` | rules and borders |

Type: **Fraunces** for display and the reading page (a serif with optical
sizing), **Inter** for UI at 11–14 px, system serif fallback throughout. The
reader's own page is a different visual world on purpose: dark chrome around a
paper page, so the book is the only bright thing on screen.

## Breakpoints

| Width | What changes |
|---|---|
| ≤ 880 px | nav links and the brand subtitle hide; the search field takes the row |
| ≤ 820 px | reader toolbar wraps; side panel hides; native PDF viewer; larger reader type |
| ≤ 480 px | download button hides, format chips shrink |

The toolbar wrapping at 820 px is a fix, not a preference: as one unwrapping row
it pushed the page wider than a phone viewport, and the book was clipped.

## Accessibility notes

- The reader is `role="dialog" aria-modal="true"`, `Esc` closes it, and focus
  returns to the card that opened it.
- `/` focuses search from anywhere; `←` `→` turn PDF pages.
- Every cover has alt text; a card whose cover 404s falls back to a typographic
  placeholder rather than an empty box.
- Colour is never the only signal: "open" is also a word, formats are also text.

Known gaps: no skip link, and the canvas-rendered PDF is not screen-reader
accessible — the native viewer path is, which is another reason phones get it.

## Performance

The shell is ~11 KB of HTML, 17 KB of CSS, 13 KB of JS, plus fonts. A reader who
opens one text file downloads no PDF engine, because each renderer is fetched
only when that format is opened. Covers and books come from jsDelivr with edge
caching; the library repo itself stays under 5 MB including the vendored
libraries and the README screenshots.
