# Offline PDF Toolkit — the CLI refuses a selection that lands on no page

Date: 2026-11-09
Repo: `drsamonline/offline-pdf-toolkit` · branch `fix/cli-refuses-empty-selection` · PR #5
(open, not merged)
Reference links taken: none new — see "What I deliberately did not do"
Same session: `2026-11-09-cldr-conventional-commits.md`,
`2026-11-09-feather-router-signatures.md`

## What I looked at

`cli/pdfkit.mjs` (663 lines, new in 1.16.0), `cli/test/run.py`, `cli/README.md`,
`ENHANCEMENTS.md` (shipped / open / refused), `CHANGELOG.md` to 1.16.1, and
`.github/workflows/build-apps.yml`. The CLI drives the same vendored pdf-lib and
qpdf the app does, and `cli/test/run.py` checks every output with PyMuPDF rather
than trusting the CLI's own report.

## What was wrong

`--pages 90-100` in a six-page file ran to completion, exit 0:

    delete --pages 90-100   "removed 0 of 2 pages" · file written unchanged
    rotate --pages 90-100   "rotated 0 of 2 pages"
    order  --pages 90-100   "0 pages in the new order" · a document with no pages
    split  --ranges 90-100  one file, no pages

A single out-of-range page already died (`page 99 is not in this document`); a
*range* that selected nothing did not. This is the failure mode 1.16.1 already
refused twice — a file that opens and is not what was asked for.

Two neighbours, same shape: a value-taking flag at the end of the line took
whatever it found (`rotate --pages` with no value silently meant *every page*;
`-o` with no value fell back to the default name and wrote beside the input),
and writing onto a directory printed a raw `EISDIR: illegal operation on a
directory, open '…'`.

## What I changed

- `pick()` dies with exit 2 when the selection resolves to nothing:
  `"90-100" selects no page — this document has 6`. All four commands inherit it.
- A range that only runs off the end still clamps (`--pages 1-99` means "to the
  end"), and a test now pins that so the fix cannot over-correct.
- A value-taking flag at the end of the line is a usage error (`--pages needs a
  value`, `-o needs a file`).
- A write failure names the path and the reason.
- `cli/README.md` states the rule and the exception; `CHANGELOG.md` gets an
  `[Unreleased]` section. `VERSION` untouched.

## Evidence

Local, against the vendored engines, every output read back with PyMuPDF:

    $ python3 cli/test/run.py
    55/55 checks passed

Against the unpatched `pdfkit.mjs` with the new tests kept: **10 of 11 fail**,
and the one that passes is the clamping guard, which must hold both ways.

In CI, run 42625252874, `CLI (pdfkit)` job: success, log line
`55/55 checks passed` with the new checks named individually.

**The run as a whole is red, and not because of this branch.** The `Shell size
budget` job fails: `docs/play/index.html is 168552 bytes (164 KB), 52661
gzipped` against a 160 KB / 52 KB ceiling — 661 bytes over gzipped. It has been
failing on `main` since 2026-11-07 (runs 42353676524, 42355047163, 42575892542,
42609608376) and there is a commit named "ci: measure the page that ships - and
it is over budget". Not touched here: shrinking the shell is a different piece
of work and the maintainer has it open in `ENHANCEMENTS.md`.

## What I deliberately did not do

- **No new link work.** This project has already mined its list: qpdf and
  pdf.js/pdf-lib are vendored, PyMuPDF is the independent checker in
  `cli/test/run.py`, and OCRmyPDF's function is the vendored OCR engine.
  Rejected, one line each: `pikepdf`, `pypdf`, `pdfplumber` — Python engines
  duplicating qpdf/pdf-lib inside a browser app. `PyMuPDF` as an engine — same.
  `WeasyPrint` — needs a server; this ships as one offline page. `pdfcpu`,
  `go-wasm-pdfcpu` — a Go tool, and Repair was written, tested and removed here
  because qpdf refuses both damage cases it would exist for. `jsPDF`,
  `html2pdf.js`, `svg2pdf.js` — PDF *generation*; pdf-lib already writes.
  `canvas-editor` — an editor; this is read-only. `vue-pdf`, `react-pdf-js` —
  framework wrappers around the pdf.js already inlined. `pdf2json` — `info
  --json` covers the same ground. `minimalpdfcompress`, `localpdfmerger`,
  `PdfCompressor`, `pdfEasyCompress` — one-feature browser demos against a
  twelve-command CLI. `JS2PDFInjector` — not a document tool. The three
  `awesome-*` lists, `awesome-ocr`, `awesome-wasm` — indexes.
- **The app's `parseRanges` still clamps silently.** It is interactive: the page
  grid changes under the user's hands and nothing is written on their behalf.
  The CLI writes a file and reports success, which is why the strictness belongs
  there. Recorded rather than quietly diverging.
- **No version bump, no merge.**

## Next

Decide on PR #5. Separately: the shell is 661 gzipped bytes over its own
ceiling, which is now the only red job on this repo's main branch.
