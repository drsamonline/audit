# search-kit — one keydown, two handlers

Date: 2026-11-09 · Repo `drsamonline/search-kit` · PR #5 (open, not merged)
Links taken: none

## What I looked at
`search-kit.js` (361 lines), `test-node.js`.

## What was wrong
`onKey` was attached to the input **and** to the wrapper. The input is inside the
wrapper, so a keydown bubbles and `onKey` ran twice: one ArrowDown moved the
selection two rows, one Enter picked twice (two rubrics opened in a repertory app).

## What I changed
One handler, on the input. The wrapper keeps a listener only for `Escape`.
`tests/palette-keys.test.js` drives the real palette through a DOM stub that
bubbles and reads the rendered `aria-selected`; `test.yml` runs it.

## Evidence
    new code   6 PASS, "palette keys: OK", exit 0
    old code   FAIL one ArrowDown moves one row (selected 2)
               FAIL Enter picks the selected row (["bravo","bravo"])   2 failed
    test-node.js unchanged: 12 passed
CI: success.

## What I deliberately did not do
- No scoring/tokenising change.
- `lev()`'s "cheap early exit" is still not cheap (it builds the full matrix); a
  performance claim I would rather measure than guess at.
- No link work: tantivy/meilisearch/quickwit/reflex/mango-finder are server or
  index engines against a 361-line in-page ranker.
- No version bump, no merge.

## Next
Decide on PR #5.
