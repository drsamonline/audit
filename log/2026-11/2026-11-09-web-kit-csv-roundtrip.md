# web-kit — a quoted newline became two CSV rows

Date: 2026-11-09 · Repo `drsamonline/web-kit` · PR #7 (open, not merged)
Links taken: none

## What I looked at
`web-kit.js` (263 lines: storage, i18n, csv, theme, a11y, pwa, seo, ui),
`test-node.js`, `test-naughty.js`.

## What was wrong
`toCSV` quotes a field containing a comma, a quote or a **newline** — correctly.
`fromCSV` split the whole text on `\n` before parsing, so that quoted newline
ended the row: the note came back truncated and every field after it was read as
part of a second row. Notes, patient records and food logs all contain line
breaks; this is the export→import path of every app that vendors the kit.

    rows: [{note:"line one\nline two", qty:"2"}]
    back: [{note:"line one"}, {note:"line two,2"}]

## What I changed
`fromCSV` parses the whole text with one state machine: only a newline outside
quotes ends a row. Blank lines still skipped; quoting and the injection guard
untouched.

## Evidence
    node test-node.js        19 passed (3 new assertions)
    before                   17 passed, 2 failed
    node test-naughty.js     133 strings through 6 paths, all checks passed
CI: success.

## What I deliberately did not do
- `toCSV` unchanged, including `Object.keys(rows[0])` as the column set.
- No DOM-side change (theme/ui/a11y/seo/pwa covered by test/index.html).
- No link work: workbox, vite-plugin-pwa, react-boilerplate, sqlsync are a
  bundler plugin, a framework starter and a sync engine against a single file
  that must work from file:// with no build step.
- No version bump, no merge.

## Next
Decide on PR #7.
