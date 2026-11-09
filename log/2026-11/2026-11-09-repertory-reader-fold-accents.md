# repertory-reader — "meniere" could never find "Ménière"

Date: 2026-11-09 · Repo `drsamonline/repertory-reader` · PR #2 (open, not merged)
Links taken: none

## What I looked at
`docs/play/index.html` (1,478 lines: loader, index, search, library), `docs/play/sw.js`,
`manifest.webmanifest`. No tests existed and the repository had **no CI at all**.

## What was wrong
Search lowercased and compared directly, and `rkey` deleted everything outside a-z:

    rkey("Ménière") -> "mnire"      rkey("meniere") -> "meniere"

A reader typing the plain name could not match a remedy written with an accent,
and `Café`/`Cfe` collapsed onto one key. Materia medica text is full of them.

## What I changed
`fold()` — NFD, strip combining marks, lowercase — used by both `rkey` and the
rubric index. It keeps one code unit per precomposed letter, so the match offset
still indexes the original string for the highlight.
`tests/fold.test.js` reads the two definitions out of the page and evaluates them;
`test.yml` is the repository's first workflow.

## Evidence
    node tests/fold.test.js    10 PASS, "fold: OK"
    before (page reverted)     "fold: FAILED — the page does not define fold()/rkey()"
CI run 42660181013: success (13s).

## What I deliberately did not do
- No change to ranking, the 300-hit limit, or the cache strategy.
- No data change: the JSON library is a separate repository.
- No link work: oorep and OpenRep-Deutsch are data projects this app reads; the
  Laravel clinic app is a different product.
- No version bump, no merge.

## Next
Decide on PR #2.
