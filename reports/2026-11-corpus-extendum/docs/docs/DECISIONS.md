# Decisions

Each entry records a choice, the evidence behind it, and what it costs. Written
so that a future reader — including me — can tell a considered decision from an
accident.

---

## D1 · Books live in separate vault repos, served by jsDelivr, not GitHub Pages

**Decision.** The library repo holds HTML and JSON only. Book files live in
`corpus-extendum-vault-NN` and are served from
**`raw.githubusercontent.com`**, with `cdn.jsdelivr.net/gh/…` kept as a fallback.
Vaults have no Pages site.

**Revised after measurement.** jsDelivr was the primary route until it stopped
being reliable at this size. Measured against the 212 MB vault:

| File | jsDelivr | raw |
|---|---|---|
| `pride-and-prejudice.pdf` | 200 | 200 |
| `pride-and-prejudice.epub` | **404** | 200 |
| `meditations.epub` | **timeout** | 200 |
| `goody-two-shoes.pdf` | **timeout** | 200 |
| `tao-te-ching.txt` | **403** (50 MB package limit) | 200 |

A CDN that returns 404 for one EPUB, hangs on another, and serves the PDF beside
it is worse than no CDN: epub.js swallows the failure and the reader shows a
blank pane with no error. raw served every file tested and sends
`access-control-allow-origin: *`, which is the only property the readers need.

**Why.** Pages caps a published site at **1 GB**; a vault is built for **2.5 GB**.
Two vaults on Pages would simply fail to deploy. jsDelivr also answers with the
right `Content-Type`, supports range requests, caches at the edge, and sends
`Access-Control-Allow-Origin: *` — verified with `curl`, not assumed. That last
header is what allows pdf.js to read a PDF from a different origin than the page.

**Cost.** A dependency on a third-party CDN, and a 20 MB per-file ceiling that
illustrated editions can approach.

**And one limit found the hard way:** jsDelivr refuses **text** files from a
repository over 50 MB — its package limit — while continuing to serve PDFs,
EPUBs and covers from the same repository. Measured directly: from a 139 MB
vault, `tao-te-ching.pdf` returned 200 and `tao-te-ching.txt` returned 403 with
"Package size exceeded the configured limit of 50 MB". So plain text is fetched
from `raw.githubusercontent.com`, which has no such limit, and binary files try
the CDN first and fall back to raw. Anything that reads a text file must use
that route.

---

## D2 · 600 books / 2.5 GB per vault

**Decision.** A vault seals at 600 books or 2.5 GB, whichever comes first.

**Why.** The owner's existing `backup` rotation runs `dumps` through `dumps-6`
at up to 2.0 GB per repo, which proves repositories of that size work fine on
this account. The first draft said 900 MB; that was too small for a shelf
averaging 3.4 MB a book and would have meant a rotation every few hundred
titles.

**Cost.** A clone of a full vault is ~2.5 GB. Acceptable: nobody clones a vault
to read a book.

---

## D3 · Dedupe on the hash of normalised text

**Decision.** Identity is checked by source reference, then by a SHA-256 over
*normalised* text — boilerplate stripped, lowercased, punctuation and digits
removed, whitespace collapsed.

**Why.** A raw byte hash is useless: two sources of the same book never produce
the same bytes. Normalisation is what makes the digest comparable across
Gutenberg, Standard Ebooks and a scan.

**Cost.** Normalisation will not make a 1902 printing and a 1990 scholarly
edition hash identically. That is what the work-key and trigram tests are for,
and both are now built — the trigram threshold at 0.62 after measuring that no
real near-duplicate reaches the 0.92 the design proposed. The gate is tuned to prefer a false *non*-duplicate over a false
duplicate: a missing book is visible, a library that lies about its size is not.

---

## D4 · Translations are gated on a verified translator, not refused outright

**Decision.** A translated work may be shelved only when the edition names its
translator *and* that translator appears in `data/translators.json` with
`verified: true` and a source that was read.

**Why.** For a translation the copyright term runs on the translator's death.
The author gate cannot see that person, so shelving Verne because Verne died in
1905 would be exactly the quiet error this library claims not to make. The first
version of this library refused translations entirely, which was correct but
useless. A curated registry with evidence is the smallest thing that is both
safe and useful.

**Cost.** Adding a translated book now needs a human to read a source and write
an entry. That is the point — the entry records where the death year came from.
Editions that credit a publisher instead of a person (the Modern Library
*Candide*) can never pass, and should not.

## D5 · Standard Ebooks first, Gutenberg mirror second

**Decision.** Where a Standard Ebooks edition exists, use it. Otherwise build
from the GITenberg mirror of Project Gutenberg.

**Why.** Standard Ebooks editions are **CC0** — the editing and typesetting are
dedicated to the public domain, so redistribution is unambiguous — and their
typography is far better than a raw dump. gutenberg.org itself returns **403 to
every request from a datacenter IP**, tested on every path including plain
files, so it cannot be the backbone of a weekly job.

**Cost.** SE's catalogue is smaller. The Gutenberg path produces a plainer EPUB.

---

## D6 · The PDF is ours, not the source's

**Decision.** Typeset every PDF with WeasyPrint from the edition's XHTML, at A5,
with our own title page. Ship the source EPUB as the authentic edition.

**Why.** Most Gutenberg titles have no PDF at all — checked: the format list for
every book examined offers EPUB, text and HTML, and no PDF. Typesetting also
means every book looks like it belongs to the same library instead of ten
different decades of scanning.

**Cost.** Our PDF is not the edition; the EPUB is. Both are offered, and the
title page says where the text came from.

---

## D7 · Plates rasterised with PyMuPDF, four at a time

**Decision.** Vector plates are rendered to JPEG at 900 px. Up to eight go
through one WeasyPrint pass; more than eight go to a four-worker process pool
using PyMuPDF.

**Why.** Through the Looking-Glass carries **153 MB of path data across 57
plates**. WeasyPrint exceeded the time budget on it. Lowering the resolution
changed nothing — the cost is parsing paths, not drawing pixels. PyMuPDF opens
an SVG as a document without dragging a layout engine into every worker, which
brought it to 2 m 25 s.

**Cost.** Plates are 900 px, not print resolution. For screen reading that is
indistinguishable; for printing it is not.

---

## D8 · Phones get the browser's own PDF viewer

**Decision.** At ≤ 820 px the reader hands the PDF to the native viewer in a
full-width frame. Above that it draws pages to a canvas with pdf.js.

**Why.** A canvas I scale myself cannot be pinched, cannot scroll past page one
without me redrawing it, and getting the fit maths right on every viewport is
work the browser has already done. The first version clipped the bottom of every
page on a phone because it fitted on width only.

**Cost.** Two code paths, and the native viewer looks different per browser.

---

## D9 · Data is never served from cache

**Decision.** Catalogue fetches use `cache: 'no-store'` **and** a `?t=<timestamp>`
query. Asset URLs carry an explicit version.

**Why.** The shelf showed ten books for a while after it held twenty-six. The
data was correct on the server the entire time; the browser was answering from
its HTTP cache because the JSON had no version and no cache directive. A 15 KB
file is not worth caching if the cost is showing the wrong library.

**Cost.** No caching of a 65 KB file. Negligible.

---

## D10 · The catalogue is derived, the vault is the record

**Decision.** `data/catalog.json` is rebuilt from the vaults' `meta.json` files
on every scan and is never edited by hand.

**Why.** A derived catalogue can be deleted and regenerated. It also means the
weekly scan is a rebuild, not an accumulation of edits, so drift is impossible
by construction.

**Cost.** The site shows what the last scan saw. Hence `built` in `shards.json`
and the date printed in the shard bar — staleness is visible rather than silent.

---

## D11 · Zero runtime dependencies on the page

**Decision.** No framework, no build step, no CDN for the viewer libraries. All
four renderers are vendored in `assets/vendor/`.

**Why.** A reading page should make no third-party request, and a CDN outage
should not take the shelf down. The bundle came from the owner's own
`app-lantern` repo, which already vendored pdf.js, epub.js and JSZip — reused
rather than re-fetched.

**Cost.** ~1.7 MB in the library repo, lazy-loaded per format.

---

## D12 · PyMuPDF confined to SVG plates; PDF rendering moved to PDFium

**Decision.** Every PDF page render now goes through `pypdfium2` (PDFium, the
renderer inside Chrome). PyMuPDF remains in exactly one function, `_render_one`,
which rasterises an **SVG** plate.

**Why.** PyMuPDF is AGPL-3.0. That is fine for outputs and fine for a local build
tool, but it stops being fine the day this pipeline is served as a web app or
relicensed. Three of the four PDF-render sites had no reason to carry it.

**Evidence the swap is safe.** The same 1250×1250 page rendered both ways:
**mean absolute difference 0.86/255**, 1.49% of pixels differing by more than 8 —
the antialiasing gap between two independent rasterisers, at a 900 px JPEG q82
output.

**Why SVG keeps PyMuPDF.** PDFium cannot open an SVG. The alternatives are worse
for these files: cairosvg renders the fill-heavy traced plates as solid black
squares, and routing through WeasyPrint pulls a layout engine into every worker,
which is the cost D7 exists to avoid.

**So the AGPL dependency is reduced, not removed.** What would remove it: a
permissive SVG rasteriser that renders these traced plates correctly — `resvg`
(MPL-2.0) is the candidate — verified against the black-square failure before it
replaces anything.

---

---

## D13 · Docling considered for the text step — rejected, measured

**Considered.** Replacing the spine text extraction with `docling` (MIT, IBM), which parses EPUB
and PDF into a lossless structured document.

**Rejected on three measurements, 2026-11-18.**

1. **The install is 6.4 GB.** `pip install docling` pulls `torch` (1.2 GB), `torchvision`,
   `transformers` and the NVIDIA CUDA runtime (**3.0 GB**). The library's declared *core*
   dependencies are light — that is what made it look cheap — but the published metapackage is not.
2. **It cannot run on a modest machine.** It failed to initialise in a 2 GB-RAM environment
   (`OpenBLAS: memory allocation still failed`, then `SystemError`). This pipeline is meant to run
   offline on ordinary hardware.
3. **It would replace something already exact.** The current extractor reads the *authored* XHTML
   from the EPUB spine and strips tags. Run against the shipped `alice-in-wonderland.epub` it
   reproduces the shipped `.txt` at **100.00% similarity** (144,841 against 144,842 characters —
   one trailing newline). There is no inference to improve: the text was authored, not rendered.

**Where it would earn its weight:** a pipeline that starts from *scanned* PDFs, where layout has to
be inferred. This one typesets its own PDFs from the EPUB, so that case does not arise. If a
scanned-only book ever enters the shelf, docling is the tool to reach for — on a workstation, as a
one-off, not as a runtime dependency.

**The lesson, since this looked obviously good:** "the core dependencies are light" is a statement
about a `pyproject.toml`, not about what `pip install` does. Measure the install, then decide.
