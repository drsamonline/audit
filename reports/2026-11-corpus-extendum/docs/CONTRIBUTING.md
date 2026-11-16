# Contributing

The library is small and opinionated on purpose. The rules below are what keeps
it trustworthy; they are not up for negotiation, but almost everything else is.

## Proposing a book

Open an issue with the title, author, and where a public-domain edition lives.
The book will be accepted if, and only if:

1. **It is public domain in both India and the United States.** Author died
   before 1966 *and* first published before 1930. One test is not enough.
2. **Its edition is redistributable.** Standard Ebooks (CC0) is ideal. Project
   Gutenberg text is fine, provided the trademark terms are respected. A modern
   scholarly edition is almost never fine, whatever the underlying text's age.
3. **It is not a translation**, unless the translator's death year can be
   established. See [docs/RIGHTS.md](docs/RIGHTS.md#translations).
4. **It is not already here**, in any format or edition. A second copy of a text
   is a bug, not an addition.

Books that fail these are not rejected out of caution — they are refused
because the library's single promise is that everything on it is free to read,
keep and redistribute.

## Reporting a wrong record

This is the most valuable contribution you can make. If a rights basis, a title,
an author or a date is wrong, open an issue quoting the record:

```json
"rights": { "basis": "author d. 1930; first published 1892 — …" }
```

The fix is one commit to that book's `meta.json` and one line removed from the
vault's `index.txt`. A sealed vault can be corrected this way; it just cannot be
added to.

## Reporting a broken book

Say which title, which format, and what happened. The reader has four renderers
and they fail differently:

- **PDF blank or stalled** — say whether you are on a phone (native viewer) or
  desktop (canvas), and whether the note under the frame names a viewer.
- **EPUB blank** — the console error matters; epub.js is strict about malformed
  archives.
- **Text cut off** — say the screen width.

## Code

Small, readable, dependency-free. The site has no build step and should keep it
that way; the scripts use the Python standard library plus WeasyPrint, Pillow and
PyMuPDF, and nothing else.

Before proposing a change to the reader, read
[docs/FRONTEND.md](docs/FRONTEND.md) — particularly why phones get the native PDF
viewer. Two of those choices were made after real bugs and reverting them will
reintroduce those bugs.

## Commit style

Plain and factual, in the imperative: `shelf: add Jane Eyre`,
`reader: fix the mobile layout`, `docs: document the pipeline`. Say what changed
and, where it is not obvious, why. Do not describe a fix as done unless a
command produced the output that proves it — that rule is in the docs for a
reason, and it was learned the hard way.

## Licence of contributions

By contributing you agree your work is released under **CC0 1.0**, the same as
the catalogue, the typesetting and the site. A library that gates its own
catalogue behind a licence has misunderstood the assignment.
