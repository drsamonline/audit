# 2026-11-16 — corpus-extendum, a public-domain library, built and shipped

## What I looked at

A new library was wanted: public-domain books only, readable in the browser,
searchable, growing by itself, with the storage split across repositories so no
single one hits a ceiling. The session started from a plan and ended with a live
site, so this log records the distance between the two.

Before writing a line, the sources were tested rather than trusted:

- **gutenberg.org** — 403 on every path from a datacenter IP, including plain
  `.txt` files.
- **codeload.github.com** — 200, no rate limit, so it became the backbone.
- **jsDelivr** — 200 with `content-type: application/pdf` and
  `access-control-allow-origin: *`.
- **archive.org** — reachable, but its `collection:gutenberg` items carry a
  readme and nothing else. Metadata stubs.
- **Standard Ebooks** — 32 candidate editions checked, and the check itself was
  wrong (see below).

The owner's existing fleet was read for parts: `backup` and `dumps` through
`dumps-6` for the rotation pattern and the evidence that 2 GB repositories work
on this account; `app-lantern` for a vendored pdf.js, epub.js and JSZip bundle;
`repertory-reader` for the support portrait and UPI QR; `web-kit`, `UniRep` and
`kosh` for patterns.

## What was wrong

Nothing existed. That is the honest starting point, and it makes the interesting
part of this entry the things that were wrong *after* it existed.

**The shelf showed ten books while it held twenty-six.** The data was correct on
the server the entire time. `catalog.json` was being served from the browser's
HTTP cache because the CSS and JS carried a version stamp and the JSON did not.
Fixed with `cache: 'no-store'` and a unique `?t=` per load, and made visible
rather than silent by printing `catalogue built <date>` in the shard bar and
`site build <version>` in the footer.

**The reader clipped every page on a phone.** Three separate causes: the toolbar
was one unwrapping row and pushed the page wider than the viewport; the PDF was
fitted to width only, so the bottom was cut; plain text was hard-wrapped at 72
columns, which ran off a 360 px screen.

**An illustrated edition could not be ingested at all.** 57 plates, 153 MB of
path data. WeasyPrint exceeded the time budget. Lowering the resolution changed
nothing, because the cost is parsing paths, not drawing pixels — two rebuilds
spent learning that. PyMuPDF renders an SVG as a document without pulling a
layout engine into every worker, and four workers brought it to 2 m 25 s.

**My slug verification was broken.** `gh api … --jq .name` prints `null` on a
404, and `null` passes a shell truthiness test, so the check reported repositories
that do not exist. Three books 404'd on fetch before this was noticed. Standard
Ebooks also uses initials in slugs — `e-nesbit_`, `g-k-chesterton_`,
`john-keats_poetry` — which accounted for three more.

**The README claimed things that were not built** — in-book search for four
formats, and ingest-side conversion of MOBI, DjVu, DOCX and CBR. Both were
corrected while writing the documentation, before anyone relied on them.

**Vault size counted `.git`**, reporting 138 MB for 87 MB of books.

## What I changed

Two repositories and a documentation set.

`corpus-extendum` — the site (one HTML file, one stylesheet, one script, four
vendored renderers, no build step), the catalogue JSON, six scripts, two
workflows, and eleven documents.

`corpus-extendum-vault-01` — 43 books, each with a typeset PDF, the source EPUB,
plain text, a cover and a `meta.json` recording its rights basis and two hashes.

The rules that make it trustworthy, all enforced in code:

- **Rights gate.** India life + 60 *and* US pre-1930, both must pass, and the
  basis is written into the record so a reader can audit it.
- **Dedupe.** Source reference, then a SHA-256 over normalised text. It has fired
  twice, once blocking a re-ingest of a book already shelved.
- **Rotation.** A vault seals at 600 books or 2.5 GB. The script proves the token
  can create repositories with a create-and-delete probe before touching
  anything real, and refuses cleanly with the exact `gh` command when it cannot.
- **Docs cannot drift.** `update_docs.py` rewrites every count in the
  documentation from the catalogue, and `--check` fails on drift. On its first
  run it caught two numbers I had typed by hand, both wrong.

## Evidence

Read back through the API, not through raw, per this repo's rule:

```
deploy  → completed/success, head 1c899d3
catalogue → 43 books (GET /contents/data/catalog.json)
vault   → 43 books, 146.8 MB, state open (data/shards.json)
render  → headless Chromium, 43 cards in the DOM, hero stat 43
served  → jsDelivr: 200, application/pdf, 12.6 MB (largest file)
```

The mobile reader was verified by rendering it in headless Chromium at 390 px and
820 px against a local copy of a real PDF, after the sandbox proxy was found to
block jsDelivr and made a canvas render look like a failure. The screenshots are
in the library repo under `docs/assets/`.

Documentation mirrored here at `docs/`, with `SYNC.json` recording the source
commit, the sync time and a hash per file.

## What I deliberately did not do

**No translated works.** For a translation the term runs on the translator's
death, and the gate reads only the author's. Verne, Plato, Voltaire and Chekhov
are in Standard Ebooks, obviously public domain in origin, and absent from the
shelf. Adding them would have made the library look bigger and would have made
its one promise false. This is the largest gap and the next thing worth building.

**No dedupe tests 3 and 4.** Work keys are written into the registry and nothing
reads them, so a different edition of the same work can arrive as a second
record. Documented as designed-not-built rather than described as working.

**No format conversion, no in-book search, no archive.org scans.** All specified
and all marked as gaps in the documentation.

**No second vault yet.** 43 books of a 600-book cap; rotation is built, tested
on three paths, and unexercised in anger.

**No force-push, no history rewrite.** One commit message understates the vault
size (156 MB when the catalogue says 122.6 at that moment). Correcting it would
have meant rewriting pushed history for a cosmetic gain, so it stands and the
catalogue's own figure is the one to trust.

## Next

1. **Translator death-year check.** Read the translator from the edition's OPF,
   find the death year, apply the same two-test gate. This unlocks a shelf of
   translations, including the Indian texts the original plan's B4 batch counted
   on — Romesh Dutt's Ramayana and Mahabharata, Kalidasa, the Upanishads.
2. **Dedupe tests 3 and 4**, so a second edition of a shelved work merges instead
   of arriving beside it.
3. **In-book search**, using the plain text already in every vault.
4. **Second batch toward the cap**, and the first real rotation when it fills.
