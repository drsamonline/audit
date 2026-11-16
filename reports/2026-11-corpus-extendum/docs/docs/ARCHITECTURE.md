# Architecture

Corpus Extendum is a static site plus a set of storage repositories. There is no
server, no database and no build service. Everything the reader sees is a file
in a git repository, and everything a book needs is a file in a different one.

```
   sources                     ingest                     storage                the site
┌──────────────┐        ┌──────────────────┐        ┌──────────────────┐      ┌────────────┐
│ Standard     │        │ scripts/         │        │ corpus-extendum- │      │ corpus-    │
│ Ebooks       │───────▶│ ingest.py        │───────▶│ vault-01         │      │ extendum   │
│ (GitHub,     │        │  · rights gate   │        │  books/<slug>/   │      │ index.html │
│  CC0)        │        │  · typeset PDF   │        │  index.txt       │      │ assets/    │
├──────────────┤        │  · build EPUB    │        │  manifest.json   │      │ data/      │
│ GITenberg    │        │  · dedupe        │        └──────────────────┘      └────────────┘
│ (PG mirror)  │        └──────────────────┘                 │                     │
├──────────────┤                 │                            │ jsDelivr            │ GitHub
│ archive.org  │                 ▼                            │ raw.githubusercontent│ Pages
│ (planned)    │        ┌──────────────────┐                  ▼                     ▼
└──────────────┘        │ scripts/         │            ┌──────────┐         ┌────────────┐
                        │ build_catalog.py │───────────▶│ data/    │────────▶│  reader    │
                        │ scripts/         │            │ catalog  │         │  in page   │
                        │ rotate_vault.py  │            │ shards   │         └────────────┘
                        └──────────────────┘            └──────────┘
```

## The split that matters

**The library repo holds no books.** It holds HTML, CSS, JavaScript, the
catalogue JSON and the scripts that produce them. It stays a few hundred
kilobytes however large the collection grows, which is what keeps the page fast
and the deploy trivial.

**The vault repos hold no HTML.** They hold book files and two manifests. They
are deliberately not GitHub Pages sites: Pages caps a published site at 1 GB,
and a vault is built to reach 2.5 GB. Books are served through jsDelivr
(`cdn.jsdelivr.net/gh/...`) with `raw.githubusercontent.com` as the fallback for
downloads. jsDelivr was chosen because it answers with the right
`Content-Type`, supports range requests, caches at the edge, and sends
`Access-Control-Allow-Origin: *` — which is what lets pdf.js fetch a PDF from a
different origin than the page.

**The catalogue is derived, never authoritative.** `data/catalog.json` is
rebuilt from the vaults' own `meta.json` files on every scan. Delete it and the
next run recreates it. The vaults are the record.

## Components

| Component | What it is | Where |
|---|---|---|
| Shelf page | One static HTML file, no framework | `index.html` |
| Reader | One component, four renderers | `assets/app.js` |
| Catalogue builder | Vault records → JSON, index, search tokens | `scripts/build_catalog.py` |
| Ingest | Source → verified, typeset, shelved book | `scripts/ingest.py` |
| Rotation | Seal a full vault, open the next | `scripts/rotate_vault.py` |
| Screenshots | README images drawn from real assets | `scripts/make_shots.py` |
| Reader QA | Headless Chromium at phone widths | `scripts/shoot_reader.py` |
| Deploy | Push to `main` → Pages | `.github/workflows/deploy.yml` |
| Scan | Weekly rebuild + rotation check | `.github/workflows/scan.yml` |

## Runtime dependencies

The page has none. The scripts need Python 3.11+, `weasyprint` (typesetting),
`pillow` (covers, image scaling) and `pymupdf` (rendering vector plates, reading
page counts). Every GitHub call is `urllib` — no SDK, no `requests`.

## Status of each piece

This document marks every feature as **built**, **designed** (specified,
not implemented) or **planned** (an intention). Anything unmarked in this repo
should be assumed built and working.

| Piece | Status |
|---|---|
| Static shelf, search, filters, sort | built |
| PDF (canvas on desktop, native viewer ≤820px) | built |
| EPUB (epub.js), plain text, JSON record view | built |
| Rights gate (author death + 60, US pre-1930) | built |
| Dedupe tests 1–2 (source ref, normalised text hash) | built |
| Dedupe tests 3–4 (work key, trigram similarity) | designed |
| Vault rotation with token preflight | built |
| Weekly scan and rebuild | built |
| In-book search | planned |
| Translator death-year check | planned |
| Format conversion (MOBI, DjVu, DOCX, CBR…) | planned |
| archive.org source adapter | planned |
| Reading progress, bookmarks | planned |
