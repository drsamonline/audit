# Decisions

Each entry records a choice, the evidence behind it, and what it costs. Written
so that a future reader — including me — can tell a considered decision from an
accident.

---

## D1 · Books live in separate vault repos, served by jsDelivr, not GitHub Pages

**Decision.** The library repo holds HTML and JSON only. Book files live in
`corpus-extendum-vault-NN`, and are served through
`cdn.jsdelivr.net/gh/…` with `raw.githubusercontent.com` as the download
fallback. Vaults have no Pages site.

**Why.** Pages caps a published site at **1 GB**; a vault is built for **2.5 GB**.
Two vaults on Pages would simply fail to deploy. jsDelivr also answers with the
right `Content-Type`, supports range requests, caches at the edge, and sends
`Access-Control-Allow-Origin: *` — verified with `curl`, not assumed. That last
header is what allows pdf.js to read a PDF from a different origin than the page.

**Cost.** A dependency on a third-party CDN, and a 20 MB per-file ceiling that
illustrated editions can approach.

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
edition hash identically. That is what the (unbuilt) work-key and trigram tests
are for. The gate is tuned to prefer a false *non*-duplicate over a false
duplicate: a missing book is visible, a library that lies about its size is not.

---

## D4 · Translations are refused until the translator can be checked

**Decision.** No translated work is ingested. Verne, Plato, Voltaire and
Chekhov are absent despite being available and obviously public domain in
origin.

**Why.** For a translation the copyright term runs on the **translator's**
death. The gate computes the author's. Shelving Jules Verne because Verne died
in 1905 would be exactly the quiet error this library claims not to make.

**Cost.** A large part of world literature is unreachable until the pipeline can
read a translator's dates from the edition. This is the single most valuable
piece of work left.

---

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
