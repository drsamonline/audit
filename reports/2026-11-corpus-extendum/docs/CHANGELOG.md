# Changelog

Dated, factual, including the things that went wrong. The library is a static
site and a set of vaults; there are no releases, so this records the build.

---

## 2026-11-16 · The two long books, shelved without a PDF

**Added**
- `--no-pdf`: shelve a book as EPUB and text only, when typesetting it cannot
  finish inside the run budget. The record carries a `notes` field saying what
  was left out and why, so the omission is visible rather than silent.
- Plato's *Dialogues* (trans. Jowett) and Chekhov's collected *Short Fiction*
  (trans. Garnett) are now on the shelf — 65 books. Both had failed twice on the
  290 s ceiling; neither needed a PDF to be worth having.

**Fixed**
- `dedupe.json` stored source refs as a bare list with no slug attached, which
  made `--replace` impossible: a ref could not be traced back to the book that
  owned it, so re-shelving anything was always refused as a duplicate. Refs are
  now a `{ref: slug}` map.
- A `--no-pdf` run crashed on `pdf.name` in its own success message — the copy
  was guarded, the log line was not.

---

## 2026-11-16 · Sixteen more books, and the shelf passes sixty

**Added** — Austen's other five (*Emma*, *Sense and Sensibility*, *Mansfield
Park*, *Northanger Abbey*, *Persuasion*), three Dickens (*Oliver Twist*, *David
Copperfield*, *Bleak House*), two Brontë (*Villette*, *The Tenant of Wildfell
Hall*), two Wells (*The Island of Doctor Moreau*, *The First Men in the Moon*),
*Kim*, *The Wisdom of Father Brown*, *Lord Jim* and *Kidnapped*.

**Note on batching** — *Bleak House* alone exceeded the 290 s ingest budget and
had to be run on its own; every other book in the batch went through three or
four at a time. The constraint is typesetting, not download.

**Corrected** — *Kidnapped*'s ebook id came from the edition's own record as
421, not the 589 typed by hand. Fourth id caught this way.

---

## 2026-11-16 · Bookmarks

**Added**
- `b` or **Mark** drops a bookmark on the current place; `m` or **Marks** lists
  them. Each row shows its label, the time it was dropped and its format, and
  jumps or deletes in one click.
- Stored per book under `corpus-extendum:bookmarks`, using the same position
  object as progress — so a bookmark taken in the text view opens the text view,
  even if the reader is currently showing the PDF.
- One mark per place: pressing twice does not stack duplicates, because the
  comparison is on the position rather than on the timestamp.

**Verified end to end**
- panel opens on Mark · 1 row added · label "40% through" · stored pct 0.4
- duplicate press leaves 1 row · jump from the top lands at 0.40 · panel closes
  on jump · delete empties the list and shows the empty message

---

## 2026-11-16 · EPUB restores where you left it

**Added**
- The reader stores epub.js's own **CFI** alongside the position, so an EPUB
  reopens at the exact place it was closed. The previous entry in this file said
  this needed `book.locations.generate()` — a full pass over the book — and
  deferred it. That was wrong: epub.js emits a CFI on every relocation for free,
  and `rendition.display(cfi)` jumps straight to it. Storing a percentage was
  the thing that needed locations, not restoring a place.

**Verified**
- CFI stored with the position; restore switches the format to EPUB and calls
  `display(cfi)`; a book with no saved position makes no call at all.
- The EPUB *render* still cannot be exercised headless — pdf.js's worker starves
  epub.js under Chromium's virtual time — so this is verified at the logic
  boundary rather than end to end. Said plainly rather than claimed as tested.

---

## 2026-11-16 · Chekhov, once the translator's death was actually read

**Added**
- Constance Garnett to `data/translators.json`, `verified: true`, after reading
  her death from three sources rather than remembering it: 17 December 1946
  (Wikipedia, Britannica, Orlando/Cambridge). Her Chekhov volumes ran 1916–1922,
  so both tests pass — India from 2006, the US well before 1930.
- **The Duel** (Chekhov, trans. Garnett), the first Russian translation on the
  shelf.

**Not shelved**
- Chekhov's collected *Short Fiction* — six source volumes, too slow to typeset
  inside the 290 s ingest budget. It joins Plato's *Dialogues* in needing a long
  run rather than a longer timeout.

**Corrected**
- The ingest took the ebook id from the edition's own record again: 13416 →
  13505. That mechanism has now caught three wrong ids typed by hand.

---

## 2026-11-16 · It remembers where you were

**Added**
- Reading position saved per book in local storage, restored on reopen, with the
  **format** stored alongside the place — the reader always opens a book as PDF,
  so without that a book last read as text restored into the wrong view.
- A *Continue reading* rail on the shelf: newest first, up to eight, each with a
  progress bar and a one-button clear.
- Saves on close, on page turn, on scroll (debounced) and on section change.

**Known limitation, stated rather than hidden**
- An EPUB reopens at the start of the book. epub.js can only jump by percentage
  once its locations are generated, and generating them costs a full pass over
  the book. Deferred rather than faked.

**Removed**
- A `Bookmark` button I had added to the markup before wiring it. A dead control
  is worse than an absent one, and this project has already shipped one of those.

---

## 2026-11-16 · Two skills applied: legal attribution, and a code review

Ran `repo-legal-docs` and `code-review-and-release-gate` against the repository
rather than guessing what they would say.

**Legal — `repo-legal-docs`**
- Its scanner found the legal surface complete but flagged bundled assets. It
  was right: **pdf.js (Apache-2.0), epub.js (BSD-2-Clause) and JSZip (MIT or
  GPLv3) were shipped without being named anywhere**, and neither were the two
  Google Fonts. Apache-2.0 in particular expects its notice to travel.
- `NOTICE.md` rewritten with a component table, version, licence and a link to
  the full text of each; the two missing licence files fetched from their own
  repositories and added under `assets/vendor/`.
- `LEGAL-INDEX.md` added, listing each document and stating what is
  deliberately absent — no TERMS, because there is nothing to agree to; no EULA,
  because no binary is distributed.

**Code review — `code-review-and-release-gate`**
- `scripts/ingest.py:1039,1122` — the library directory was assumed to be a
  sibling named `corpus-extendum`. In CI the vault clones to `../vaults/<name>`,
  so the dedupe registry was written to a directory invented beside the vault,
  silently and to the wrong place. Now `--library`, with a warning when the
  default does not exist.
- `assets/app.js:218` — jumping from a search hit waited a fixed 350 ms for an
  asynchronous text render, which loses the race on a large book and does
  nothing. Now waits for the paragraph itself.
- `assets/app.js:390` — the EPUB path had no raw fallback while the PDF path
  did, so a CDN refusal ended the book. Now falls back, with a per-book retry
  flag (which my own first version forgot to reset).

---

## 2026-11-16 · Search inside a book, and a CDN limit worth knowing

**Added**
- In-book search: `Find` in the reader toolbar, or `Ctrl/⌘+F`, or `/`. It
  searches the plain text every vault already holds, lists matches with context,
  and a click switches to the text view, scrolls to the paragraph and highlights
  it. Works at every width, including phones where the side panel is hidden.

**Fixed**
- Plain text was being fetched from jsDelivr, which **refuses text files from a
  repository over 50 MB**. The vault is 139 MB, so every `.txt` returned 403
  while the PDFs beside them returned 200. Text now comes from
  `raw.githubusercontent.com`; binary files try the CDN and fall back to raw.
  Found by a search that returned zero matches on a book full of the word.

---

## 2026-11-16 · The two dedupe tests that catch what a hash cannot

**Added**
- **Work key** (`surname|title|year`, subtitle stripped): a match means another
  edition of a shelved work, so it is recorded in the canonical record's
  `editions[]` instead of becoming a second card.
- **Trigram similarity**: a title close enough to be the same book is held in
  `data/review-queue.json` and never auto-added.

**Corrected**
- The threshold was 0.92 in the design, which is unreachable: real
  near-duplicates score 0.68–0.88 while different works by the same author sit
  at 0.00–0.47. It is now 0.62, set from measurement, with the pairs recorded in
  the docstring so the number can be argued with.

---

## 2026-11-16 · Translations, gated on the translator

**Added**
- `data/translators.json` — a registry of translators with a verified death year
  and the source it came from. Towle (d. 1893), Jowett (d. 1893), Legge (d. 1897)
  and Long (d. 1879) were checked against sources and entered.
- A translator gate in `ingest.py`: the edition's `trl` contributor is read from
  the OPF, matched against the registry, and refused unless verified — then the
  same two tests are applied to the translator, plus the translation's own
  publication year.
- Three translated books: Epictetus' *Discourses* (Long), the *Tao Te Ching*
  (Legge) and *Around the World in Eighty Days* (Towle).

**Refused by the gate, as intended**
- Constance Garnett — death believed 1946, but no source read yet, so Chekhov waits.
- F. A. Malleson, F. H. Peters, and the Modern Library *Candide* — the last
  credits a publisher rather than a person and can never pass.

**Not shelved**
- Plato's complete *Dialogues* (Jowett). Typesetting all of Plato takes 4 m 50 s,
  past the 290 s ingest budget. It needs a long run, like the illustrated editions.

---

## 2026-11-16 · Reader controls for every format

**Fixed**
- The turn controls were hidden for EPUB, text and JSON, so those formats had no
  way to move at all. `turn(dir)` now dispatches per format: pages for a PDF,
  sections for an EPUB, a screenful for text and JSON.
- EPUB used `flow: 'scrolled'`, which shows one section and offers no route to
  the next. `scrolled-continuous` scrolls the whole book.
- `renderTo()` ran before the archive had opened, which produced an empty box
  and no error. It waits for `book.ready` now.
- epub.js measures its container when it attaches; if that happens before layout
  settles the iframe is shorter than the box. It re-measures after attach and on
  rotate.
- A late PDF failure could take over the reader after the user had switched to
  another format. Every async continuation now checks the format first.
- The position readout never updated for text or JSON; it now reports a
  percentage as you scroll.

**Added**
- Keyboard: arrows, PageUp/Down, Space, Home/End, `1`–`4` to switch format,
  `Esc` to close.

**Not done**
- An automated reader test. Chromium's virtual time does not advance Web
  Workers, so pdf.js cannot render headless, and a hung pdf.js starves epub.js.
  The method that does work is written up in `docs/FRONTEND.md` rather than
  shipped as a test that fails for environmental reasons.

---

## 2026-11-16 · Documentation, rotation, and the illustrated edition

**Added**
- `docs/` — architecture, pipeline, data model, operations, decisions, rights.
- `scripts/rotate_vault.py` — seals a full vault and opens the next, with a
  token preflight that creates and deletes a throwaway repo before touching
  anything real. Exits 3 and prints the exact `gh` command when it cannot.
- Rotation step in `scan.yml`, which opens an issue when rotation is blocked.
- Sixteen books: Wells, Shelley's *The Last Man*, Haggard, *The Hound of the
  Baskervilles*, *Father Brown*, *The Moonstone*, *The Woman in White*,
  *Through the Looking-Glass*, *Wind in the Willows*, *The Secret Garden*,
  *Five Children and It*, *Leaves of Grass*, Keats, *Walden*, Emerson's
  *Essays*, *Leviathan*, *On Liberty*.

**Fixed**
- Illustrated editions could not finish inside the ingest budget. WeasyPrint
  cannot get through 153 MB of path data in 57 plates; lowering the resolution
  did not help because the cost is parsing, not drawing. Plates now render in a
  four-worker pool using PyMuPDF: 2 m 25 s for *Through the Looking-Glass*.
- README claimed in-book search and format conversion that were never built.
  Corrected, with a status column instead.

**Found**
- Standard Ebooks uses initials in its slugs (`e-nesbit_`, `g-k-chesterton_`,
  `john-keats_poetry`). Three books 404'd before this was noticed.
- The slug check itself was broken: `gh api --jq .name` prints `null` on a 404,
  and `null` passes a shell truthiness test, so the check reported repos that do
  not exist. Verification now goes through codeload.

---

## 2026-11-15 · The reader, the cache, and the first forty-two

**Added**
- Mobile reader: at ≤820 px the PDF goes to the browser's own viewer in a
  full-width frame; above that, pdf.js draws pages to a canvas. If the canvas
  fails, the native viewer takes over rather than leaving a blank pane.
- `?t=<timestamp>` and `cache: 'no-store'` on every data fetch; versioned asset
  URLs; `site build <version>` printed in the footer.
- A visible `catalogue built <date>` line in the shard bar, so staleness is
  visible instead of silent.
- Twenty-six books across twelve categories, including the first illustrated
  edition (*Alice*), which needed its 42 vector plates rasterised.

**Fixed**
- **The shelf showed ten books after it held twenty-six.** The data was correct
  on the server the whole time; the browser was answering from its HTTP cache
  because the JSON had no version and no cache directive. The CSS and JS were
  versioned and the data was not.
- `disableAutoFetch: true` made pdf.js use range requests, which hang against any
  server that does not answer them. Removed. Added a 30 s timeout so a stall
  surfaces as an error.
- The reader toolbar was one unwrapping row, which pushed the page wider than a
  phone viewport and clipped the book.
- The PDF was fitted to width only, so the bottom of every page was cut off on a
  phone.
- Plain text was hard-wrapped at 72 columns, which ran off a 360 px screen.
- Vault size counted `.git`, reporting 138 MB for 87 MB of books.

**Found**
- `drsamonline.github.io` is not on this environment's egress allowlist, so the
  live site can only be read through a fetch tool, not `curl`.
- The GitHub CLI token can push but cannot administer: Pages, topics and workflow
  dispatch all return 403 through `gh`, and all work through the GitHub MCP.

---

## 2026-11-15 · Publication

**Added**
- `corpus-extendum` (Pages, workflow build type) and
  `corpus-extendum-vault-01`, both public, with topics, description and homepage.
- Ten seed books, one per category, each public domain in India *and* the US.
- `ingest.py`, `build_catalog.py`, `make_shots.py`, `deploy.yml`, `scan.yml`.
- Vendored pdf.js, epub.js and JSZip — reused from the owner's own
  `app-lantern` repo rather than fetched from a CDN.

**Found**
- An installed GitHub App **cannot create repositories** — 403 on both GraphQL
  and REST. The GitHub MCP can. That asymmetry shaped everything after.
- gutenberg.org returns **403 to every request from a datacenter IP**, including
  plain file paths. The pipeline reads Standard Ebooks and the GITenberg mirror
  instead, both served by GitHub.
- Most Gutenberg titles have **no PDF at all**, so the PDFs had to be typeset.

---

## Known gaps

Listed here so they are not mistaken for finished work:

| Gap | Consequence |
|---|---|
| Translator death-year check | no translated work can be shelved — Verne, Plato, Voltaire, Chekhov |
| Dedupe tests 3–4 | a different edition of the same work can arrive as a second record |
| In-book search | the reader has no text layer to search |
| Format conversion | MOBI, DjVu, DOCX, CBR are not handled |
| archive.org adapter | scans are unreachable |
| Reading progress, bookmarks | not built |
| Blueprint document | the v2 HTML blueprint predates the built system (600 books, jsDelivr, native mobile viewer); `docs/` supersedes it |
