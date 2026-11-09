# ziptastic — the README's claim table is now checked against FINDINGS.md

Date: 2026-11-10 · Repo `drsamonline/ziptastic` · PR #3 (open, not merged)
Reference links taken: `sharkdp/hyperfine`, `devedse/DeveMultiCompressor` — as the
method to aim at; neither was added, see below

## What I looked at
`README.md` claim table, `docs/FINDINGS.md` (the "single authoritative record"),
`scripts/regression-corpus.sh`, `ci.yml`, `.github/workflows/vendor-check.yml`.

## What was wrong
The README repeats seven FINDINGS rows, hand-copied, for the headline claim; nothing
checked the two still agreed. The numbers do agree today — but the claim had no
guard, and a ratio claim with no guard is the one thing this repository cannot
afford to be casual about.

## What I added
`scripts/check-claims.py` + a CI step. Rows matched by their numbers, not labels
(the README's "Mixed game-asset tree, 6.3 MB, as .tar" is FINDINGS' "tree.tar");
every later numeric cell is a candidate because some rows carry three measurements;
header `-9` / `-9e` flags ignored by requiring byte-count-sized numbers.

## Evidence
    python3 scripts/check-claims.py --verbose   7 rows ok, exit 0
    sed 408,421 -> 408,422 in README            1 row NOT IN FINDINGS, exit 1
CI run 42681018120: success (build + ctest + the new gate).

## What I deliberately did not do
- No change to FINDINGS, the README table or any measurement.
- No hyperfine / per-corpus statistics: the corpus (6.3 MB asset tree, CD image, ISO)
  is not in the tree, and the regression corpus asserts properties, not ratios.
  A timing harness without the fixtures would produce unreproducible numbers.
- No C++ change; no toolchain here, so CI's build + ctest are the proof it compiles.
- No version bump, no merge.

## Next
Decide on PR #3. The real measurement upgrade needs the corpus checked in first.
