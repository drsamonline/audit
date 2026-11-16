# The pipeline

How a book gets from a source repository onto the shelf, and what can go wrong
at each step.

```
fetch ──▶ rights gate ──▶ typeset PDF ──▶ build EPUB ──▶ extract text ──▶ hash
                             │                                             │
                             └──── dedupe gate ◀───────────────────────────┘
                                        │
                                   shelve in vault
```

Run it:

```bash
python3 scripts/ingest.py --vault ../corpus-extendum-vault-01 --only 1342
python3 scripts/ingest.py --vault ../corpus-extendum-vault-01 --only 84,1661,35
python3 scripts/ingest.py --vault ../corpus-extendum-vault-01 --all
python3 scripts/ingest.py --vault ../corpus-extendum-vault-01 --only 11 --replace
```

| Flag | Meaning |
|---|---|
| `--vault` | path to a vault checkout (required) |
| `--only` | comma-separated ids from the `BOOKS` table |
| `--all` | every book in the table |
| `--replace` | drop an existing copy and its registry entries first |
| `--keep-work` | keep the temporary working directory |

| Env | Meaning |
|---|---|
| `CE_MAX_PX` | max pixel size for plates (default 900) |
| `CE_WORK` | working directory (default `/scratch/work/_tmp`) |

## 1 · Fetch

Sources are tried in this order, and the choice is recorded in the book's
`source` field so it is never a guess later.

**Standard Ebooks** (nine books in ten). Their editions are CC0 and their
typography is better than anything a raw text dump will give you. The whole
source tree is downloaded as a tarball from
`codeload.github.com/<org>/<repo>/tar.gz/refs/heads/master`.

*Why codeload and not the API:* the API allows 60 unauthenticated requests an
hour and returns a tarball via a redirect; codeload serves the same archive with
no limit at all. A batch of forty books would hit the API ceiling; it will not
hit codeload's.

*Why not gutenberg.org:* it returns **403 to every request from a datacenter
IP**. This is tested, not assumed — every path, including plain files, is
refused. A pipeline that depends on it only works from a residential
connection, which is no way to run a weekly job.

**GITenberg** is the fallback: Project Gutenberg texts mirrored as GitHub
repositories, so they arrive through the same codeload path. The book is built
from the `.txt`, and a valid EPUB3 is assembled from it.

**archive.org** is declared in the design and **not implemented**. Its
`collection:gutenberg` items are metadata stubs with no text — checked. Real
scans live in `opensource` and `americana`, which is a different adapter.

### Internet Archive

A different kind of source: a scan, not a text. The PDF is the archive's own and
is not re-typeset; the OCR text (`_djvu.txt`) is required, because that is what
makes the book searchable and what the EPUB is built from.

The item's own rights statement is read first and the item refused unless it is
marked public domain. That is necessary, not sufficient — a search on
`possible-copyright-status:NOT_IN_COPYRIGHT` returns 2001 books — so the author
gate runs on top of it. Anonymous works take the publication-only branch.

## 2 · The rights gate

```python
rights = f"author d. {death}; first published {year} — public domain in India
          (life + 60) and the United States (pre-1930)"
```

Both tests must pass. The basis is written into the record, so a reader can
audit the claim rather than trust it, and a future audit can recompute it.

**The translator problem.** For a translation, the term runs on the
*translator's* death, not the author's. `ingest.py` has no translator lookup, so
**translated works are not ingested at all** — Verne, Plato, Voltaire and
Chekhov are deliberately absent for this reason. `Meditations` carries a
`translator` block because George Long (d. 1879) was entered by hand.

This is the most important known limitation in the system. See
[DECISIONS.md](DECISIONS.md#d4-translations-are-refused-until-the-translator-can-be-checked).

## 3 · Typeset the PDF

WeasyPrint, A5, Liberation Serif, justified, hyphenated, page numbers in the
footer. The spine is read from the edition's `content.opf`, front matter
(half-title, title, imprint, colophon, uncopyright) is dropped, and a title page
in the library's own style is printed in its place — which also keeps the
attribution honest, since it names the source edition.

*The spine is re-read from the shrunk copy, not the original.* Shrinking
rewrites image references inside the tree, so reading from the original resolves
to files that no longer exist and the illustrations vanish silently. This cost
one debugging round; it is written down so it does not cost another.

## 4 · Plates

Illustrated editions are the hard case, and the numbers explain why: Alice is
42 plates of ~760 KB; Through the Looking-Glass is 57 plates totalling **153 MB
of path data**.

- **One to eight plates** → one WeasyPrint document with a page per plate.
- **More than eight** → a process pool, four workers, each rendering one plate
  with PyMuPDF (`pymupdf.open(svg)` treats an SVG as a document).

*Why not lower the resolution:* the cost is parsing the paths, not drawing the
pixels. Dropping from 900 px to 520 px changed nothing.
*Why PyMuPDF in the workers:* WeasyPrint pulls a full layout engine into every
process for a job that produces one image. PyMuPDF does not. Looking-Glass went
from exceeding a 290-second budget to 2 m 25 s.

Plates are saved as JPEG at `CE_MAX_PX` (default 900) and quality 82, and the
`src` references in the XHTML and the `content.opf` media types are rewritten to
match.

## 5 · EPUB

The Standard Ebooks source tree **is** an EPUB layout (`src/mimetype`,
`src/META-INF/`, `src/epub/`), so the EPUB is that tree re-zipped with `mimetype`
first and uncompressed — apart from the shrunk plates. GITenberg books get a
minimal but valid EPUB3 assembled from the text.

## 6 · Text and hash

Plain text is extracted from the spine, tags stripped, entities resolved. Two
hashes are stored:

- `file_sha8` — proves a file has not been silently replaced.
- `text_sha256` — the dedupe key, over **normalised** text: lowercased, Project
  Gutenberg boilerplate removed, punctuation and digits stripped, whitespace
  collapsed.

A raw byte hash is useless for dedupe, because two sources of the same book
never produce the same bytes.

## 7 · The dedupe gate

Before a file is committed, two tests run:

1. `source_ref` already in `data/dedupe.json` → refuse, never fetched.
2. `text_sha256` already registered → refuse as a duplicate of that slug.

Then the two tests that catch what a hash cannot:

3. **Work key** — `surname|title|year`, subtitle stripped. A match means this is
   another edition of a work already shelved: the ingest records it in the
   canonical record's `editions[]` and does **not** create a second card.
4. **Trigram similarity ≥ 0.62** with the same author — a title close enough to
   be the same book. Held in `data/review-queue.json`, never auto-added.

The 0.62 threshold is measured, not chosen. Real near-duplicates: *The
Adventures of Huckleberry Finn* vs *Adventures of Huckleberry Finn* 0.88,
*Pride and Prejudice* vs *Pride & Prejudice* 0.68. Different works by the same
author: *Dracula* vs *Dracula's Guest* 0.47, *Jane Eyre* vs *Villette* 0.00. The
original design specified 0.92, which no real near-duplicate reaches — it would
never have fired.

The gate has fired in anger twice: once blocking a re-ingest of Alice, once
when `--replace` was needed and absent.

`build_catalog.py` is the final authority. It recomputes identity across *every*
vault; if two records share a text hash, the later one is marked `quarantined`
in its `meta.json` and disappears from the site. Files in a sealed vault are
never deleted — the catalogue simply stops showing the book.

## 8 · Shelve

`books/<slug>/` receives the PDF, EPUB, text, `cover.jpg` and `meta.json`. The
vault's `index.txt` and `manifest.json` are rewritten by `build_catalog.py`, not
by the ingest script — one writer per file.

## Failure modes seen in practice

| Symptom | Cause | Fix |
|---|---|---|
| `tarball failed … 404` | wrong slug. Standard Ebooks uses **initials**: `e-nesbit_`, `g-k-chesterton_`, `john-keats_poetry` | check the slug against codeload, not the API |
| API says the repo exists, codeload 404s | the API check was wrong: `--jq .name` prints `null` on a 404, and `null` passes a shell truthiness test | verify with a codeload HEAD |
| `id corrected from the source record: 120 → 27780` | the hand-typed Gutenberg id was wrong; the edition's own `dc:source` is right | nothing — the script prefers the record and logs it |
| ingest dies at ~290 s | an illustrated edition | see §4 |
| tar: `Cannot write: No space left on device` | `/tmp` is a 64 MB tmpfs | `CE_WORK` defaults to real disk |
| illustrations missing from the PDF | spine read from the original tree | see §3 |
| plate is a solid black square | cairosvg mis-renders these fill-heavy paths | use WeasyPrint or PyMuPDF |
