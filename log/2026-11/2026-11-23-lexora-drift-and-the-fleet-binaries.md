# 2026-11-23 — LEXORA: seven numbers that nothing recomputed, and the binaries the estate already had

## What I looked at

`drsamonline/lexora`, end to end: the open PRs, every state document (`STATUS`, `PROGRESS`,
`ROADMAP`, `PATH_TO_V1`, `NEXT_SESSION`, `SESSION_LOG`), the requirements register and its
traceability matrix, the README, the landing page, the benchmark artifacts under `benchmarks/`,
and the harness that produces them. Then, because a claim about "the environment" turned out to be
false, the fleet: `heavenzip`'s `bin/`, `audit`'s own conventions, and `knowledge` for a prior P0
attempt.

## What was wrong

Seven claims in the repository that nothing recomputed, each drifting in a different direction.
None of them failed a build, because none of them was a test.

| Claim | What was true |
|---|---|
| Two open PRs "left" | #50/#51 were green and mergeable; the only unfinished *code* on the repo |
| `README`: "TXT/PDF ingestion is not implemented yet", "English-only" | ingestion, OCR, the query archive, three language plugins and a GUI client had all shipped with tests |
| `ROADMAP`: M3 "Not started", last verified **2026-10-15** | PDF + OCR landed weeks earlier |
| `PROGRESS`: P2 "Not started", 502-test gate from **2026-10-17** | the gate was 765 |
| `docs/index.html`: "no releases yet" | two alpha tags published |
| `PRODUCT_REQUIREMENTS`: **"Not started" × 35**, "no code exists yet" | 30 of them were built and tested |
| `README` benchmark table: `0.3352` for the shipped default | **no committed artifact reports it** |

The last one is the serious one. Recomputed from the artifacts, three different runs were wearing
one label: `0.3367` is revision 4's heldout-only first cut, `0.3360` is revision 5's all-splits run,
and `0.3352` had **no surviving artifact at all** — revision 5's run reused revision 4's file names
and overwrote it. "746 MB" was never that run's size either.

Two more of the same kind came out of the same sweep: the gram index's "5× the stored payload" was
measured once by a generator nobody committed, and `SESSION_LOG` stopped at 2026-11-09 while six
days of merged work had no record.

## What I changed

Sixteen PRs (#50–#65), all merged, gate **765 → 867 passed**, CI green on every one.

**Finished the code that was left.** #50/#51 — a one- or two-character CJK query returned a silent
zero; now answered from a `doc_grams` index (schema v3), with the scan kept for uncovered documents.

**Reconciled the documents with the code.** #52 six state documents; #53 the session gap backfilled
(reconstructed from merge history and *labelled* reconstructed) plus P5.1/P5.2 closed; #57 the three
ratios resolved and the claims checker promoted from advisory to `--strict` in CI; #58 all 70 cells
of the requirements register; #63 the landing page.

**Closed five requirements with instruments rather than sentences.** #54 the LGPL/GPL texts now
travel in the wheel; #55 the cleaning-error audit (ADR-0004's metric, unimplemented since the ADR);
#56 the gram index measured instead of packed (ADR-0025 — the proposal was wrong, the cost is rows
not gram width); #59 dictionary lineage + an offline smoke test; #60 a cost auditor that closes
exactly against the file.

**Built what the blockers needed.** #61 Gujarati (`gu-1`) — the half of REQ-CAN-005 that had no
implementation, and its NFC rule *orders* marks rather than composing letters, because Unicode 15.0
defines zero canonical decompositions in U+0A80–U+0AFF. #62 ADR-0026 (Proposed) for cost-based
selection. #64 `P0_RUNBOOK.md` + `scripts/p0_preflight.py` — P0 was a list of conditions with no
commands. #65 the fleet's binaries.

**Eleven guards, each mutation-tested**, so the same class of drift fails a build next time: cited
paths must exist, state documents must agree on their last-verified date, the claims checker keys on
(revision, system), two ADRs are held to their artifacts, licence texts are SHA-256 pinned, the
offline test removes the socket constructor, the landing page may not deny a release the CHANGELOG
names.

## Evidence

- `main` @ `e22af18`, read back through the API after the last merge, not through raw.
- Gate: **867 passed, 12 skipped** (the conditional plugin/PySide6/ziptastic skips) ·
  `scripts/linkcheck.py` ALL INTERNAL LINKS OK · `scripts/check-benchmark-claims.py --strict` clean.
- A **fresh clone** at `e33fc7c`: `pip install -e .` + `pytest -q` → 847 passed, 3 skipped; with all
  three language plugins → the same, same three skips.
- Requirements: **35 → 4 open** (BMK-003 gate G2, CAN-007 reviewers, RES-001 second machine class,
  CAN-006 feature absent), each naming its module and test.
- The measurement that changed a decision (`benchmarks/results-selector-probe.json`, one 721 KB
  file, tool versions recorded):

      chce (ziptastic 1.4.5)   207,338 B  0.2876
      ppmd (7z 26.05)          208,461 B  0.2891
      brotli -q 11 (1.2.0)     244,286 B  0.3388
      xz -9 CLI (5.8.4)        249,208 B  0.3457
      zstd L19                 253,155 B  0.3511
      zstd L9 (default)        271,004 B  0.3759

  A selector would pick CHCE: **23.49 % smaller than the shipped default**, not the 6.59 % a
  level-only comparison suggested. And PPMd is **0.54 % larger** than CHCE at ~5.8× the speed — so
  OQ-18's "PPMd as the max-ratio preset" is a speed argument, not a size one.

## What I deliberately did not do

- **Did not implement ADR-0026.** It is Proposed, and this repo's own rule is that an implementation
  does not start from a Proposed ADR. The owner decides.
- **Did not decide OQ-18** with a one-file measurement, and did not let the ADR imply it had.
- **Did not invent a P0 number.** The protocol run needs a 1 GiB corpus, `xz`, ~2 GB disk and 6–8
  hours; the preflight refuses rather than estimating.
- **Did not fabricate the missing session record.** The 2026-11-09 → 2026-11-23 backfill is a table
  built from merge history and says so in its own heading.
- **Did not silently replace the withdrawn `0.3352`.** It is marked withdrawn in the README, with
  the reason, because a number that disappears looks like it was never wrong.

## Next

1. **P0** — `docs/P0_RUNBOOK.md` §0–§3 with `--bin-dir ~/heavenzip/bin`. Closes REQ-BMK-003,
   unblocks `.lxdb`, supplies the second machine class. Owner (P7.1/P7.2).
2. **ADR-0026** — accept or reject; either is defensible with the numbers attached.
3. **REQ-CAN-007** — two reviewers on the cleaning worksheet; the instrument is ready (P7.9).
4. **`knowledge` has no LEXORA entry** — the black box holds no run log for this repo at all. If P0
   is attempted, that is where its log belongs.

## The lesson worth keeping

"Absent from the environment" and "absent from the estate" are different claims, and I recorded the
first as if it were the second — then built an ADR around the gap it created. `heavenzip`'s `bin/`
had `ziptastic`, `xz`, `7z`, `brotli` and `zstd` the whole time. A container's inventory is not the
fleet's; when a measurement is blocked on a binary, the next question is *where in the estate is
it*, not *what can I claim without it*.

## Addendum, later the same day — a tool nobody had pointed at the repo

After the log entry above was merged, `tools/presentation_audit.py` was run against `lexora` for the
first time. It had never been. The result:

    repo      tier          verdict  landi app badge shots readm suppo portr theme offli platf
    lexora    app-no-demo   apply     ok   n/a   XX    wr    ok    XX    ok   n/a    ok    ok

Three classes of work, none of them caught by anything in that repository:

- **BADGES** — no local badge set. Now `scripts/badges.py` draws the six into `docs/assets/` in the
  page's own palette. The collision worth recording: the standard wants a *tests* badge from the
  repo's own suite, and the repo forbids a static test count because a number nothing recomputes
  decays silently. Both are right; the badge says `green — see CI`, a condition rather than a
  number, with the count in the live badge.
- **SUPPORT** — the landing page printed the UPI VPA with **no `upi://pay` intent link**, so the one
  handle a phone can act on was a string it could not use, and the block carried no `data-support`
  marker, so this very tool could not see it. Both fixed.
- **SHOTS** — **not fixed, deliberately.** `app-desktop.png` needs the `[gui]` extra and a
  Qt-capable machine, and `app-mobile.png` would be a *mobile* screenshot of a desktop application.
  Fabricating one to satisfy a checklist is the failure the rest of the day was spent removing.

After: `badges ok`, `support ok`, `shots wr` — three classes down to one.

**The lesson is not "a repo was non-compliant".** The tool existed, the standard existed, and nobody
had run it — which from the repository's point of view is indistinguishable from not having either.
`lexora` #66, `tests/test_presentation.py` (11 tests) now holds the parts it can check alone.
