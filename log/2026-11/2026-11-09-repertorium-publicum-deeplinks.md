# Repertorium Publicum — a deep link for "meniere" could not reach "Ménière"

Date: 2026-11-09 · Repo `drsamonline/Repertorium-Publicum` · PR #8 (open, not merged)
Links taken: none

## What I looked at
`pipeline/app_template.html` (1,846 lines), the built `docs/play/index.html`,
`pipeline/build_app.py`, `tests/enhancements.test.mjs` (browser suite, 32 checks).

## What was wrong
`norm()` lowercased then deleted every character outside a-z. Deep links resolve a
remedy through it on both sides, so a remedy written "Ménière" normalised to
"mnire" while a link typed "meniere" normalised to "meniere" — the link opened
nothing, silently.

## What I changed
`norm()` folds first (NFD, drop combining marks), then lowercases and strips. The
build script needs `kent.json`, which is not in this environment, so the built page
was edited to match the template by hand — and an assertion now compares the two
copies of `norm()` so they cannot drift.

## Evidence
    CHROME=… node tests/enhancements.test.mjs    PASS 34  FAIL 0
    both copies reverted                          PASS 33  FAIL 1
                                                  (norm() folds accents)
CI: success.

## What I deliberately did not do
- No rebuild (no data checkout here); the copies are kept identical by assertion.
- No change to rubric search, the case builder or the deep-link format.
- No link work: oorep and OpenRep-Deutsch are data projects.

## Next
Decide on PR #8. Third instance of the accent-stripping class in this session
(repertory-reader, this repo, and the fleet-wide `rkey` pattern).
