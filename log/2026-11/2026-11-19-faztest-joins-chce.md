# faztest joins CHCE — and the README's claim was false in one direction and true in the other

Date: 2026-11-19 · Repos `drsamonline/faztest-fast-file-forge`, `audit` · faztest PRs #1–#5

faztest was scaffolded by a hosted app builder as "a compressor that beats xz and 7z in compression and speed",
sat outside the fleet, had no CI, no `LICENSE`, no findings document, and no measurement. It is
now the eighth CHCE repository, held to the same rules as the other seven.

## What it actually is

`public/faztest.mjs` is a **Brotli front end** — `brotliCompressSync` from `node:zlib`, quality
0–11, default 5 — plus a browser path that compresses in WebAssembly workers so files never
reach a server. It ships no codec of its own. Every comparison below is therefore Brotli against
LZMA2 on LZMA2's home ground, and the numbers behave exactly as that predicts.

## The measurement

Silesia corpus, twelve files, 211,938,580 bytes, sizes checked against the twelve expected
sizes, one run per cell, every archive decoded back and compared byte for byte (71 of 72 cells;
the exception is `mozilla` below). Baselines: `ziptastic 1.4.5 -9`, `xz -9e` (liblzma), 7z
LZMA2 preset 9|extreme.

| setting | archive | ratio of raw | time over corpus |
|---|---:|---:|---:|
| faztest -q5 (default) | 59,553,242 | 28.10% | 23 s |
| faztest -q9 | 56,682,211 | 26.74% | 81 s |
| faztest -q11 | 50,332,587 | 23.75% | 796 s |
| xz -9e | 48,456,004 | 22.86% | 241 s |
| 7z LZMA2 9e | 48,456,884 | 22.86% | 244 s |
| ziptastic -9 | 43,401,535 | 20.48% | 622 s |

| claim | measured | verdict |
|---|---|---|
| beats xz on size | +16.98% at `-q9`, +3.87% at `-q11` | **false** |
| beats 7z on size | +16.97% at `-q9` | **false** |
| beats ziptastic on size | +30.60% at `-q9` | **false** |
| beats xz on speed | 81 s against 241 s (3.0×) | **true** |
| beats ziptastic on speed | 81 s against 622 s (7.7×) | **true** |

The verdict is one sentence: **largest of the five, fastest of the five.** `-q11` wins on
exactly two files (`osdb` −0.68%, `xml` −1.04%) and pays 3.3× xz's time to do it. That is a
real product — Brotli trading ratio for time — and it is now what the README says.

## What shipped, per subject

| # | PR | subject | what proves it |
|---|---|---|---|
| 1 | faztest #1 | the benchmark test timed out on every run (vitest's 5 s default against child processes) | `bun run test`: 1 failed/4 passed → **5 passed (5) in 33 s** |
| 2 | faztest #2 | `docs/FINDINGS.md` + `scripts/bench.py` + `scripts/check-claims.py` + README rewritten to the measurement + fleet rules in `AGENTS.md` | `check-claims`: 18 README numbers all present in FINDINGS |
| 3 | faztest #3 | CI: suite, claims gate, CLI contract (round trip, overwrite refusal, non-zero exit on an unknown command) | all three run locally: byte-exact, "Output already exists", `frobnicate` exits 2 |
| 4 | faztest #4 | `LICENSE` (MIT, matching ziptastic) | the repo previously granted nothing |
| 5 | faztest #5 | every trace of the hosted builder removed: its project-metadata directory, the vendor block at the top of `AGENTS.md`, the vendor vite-config wrapper (replaced by an explicit `vite.config.ts`), the error-reporting hook, the `twitter:site` handle, the lockfile release-age exemptions, the README sections | grep for the vendor name → 0 matches · `bun install` clean · tsc no new errors · 5 tests pass · **build unproven here** (1.5 GB virtual cap, Vite 8 rolldown is WASM), gated in CI by #3's new build job |

## Traps this added to the list

1. **A README claim with no gate behind it drifts.** The line "beats xz and 7z" survived because
   nothing measured it. The gate is `scripts/check-claims.py`: every number in the README table
   must exist in `docs/FINDINGS.md` to within rounding, and CI runs it.
2. **A test that always fails is a test nobody reads.** The suite printed 5 tests and 1 failure
   every run; the failure was a 5 s timeout against a benchmark that needs 21 s.
3. **`--only` on `collect.py` cannot see a private repository.** See `docs/known-states.md` —
   `users/{owner}/repos` never lists private repositories, so faztest (like `dumps`, `registry`,
   `forge`, `knowledge`) is absent from `state/repos.json` by construction, not by omission.

## Open

- **The CLI pins `ziptastic 1.4.1`** (URL and SHA-256 in `public/faztest.mjs`); the fleet ships
  1.4.5. Ratio is unaffected on this corpus, but the pin should be bumped and re-verified.
- **`-q11` beats xz on dictionary-friendly content** (`osdb`, `xml`). Whether a per-block
  router should send that content to Brotli and the rest to LZMA2 is a real question — the same
  routing ziptastic already does between nine backends — and it needs a classifier, not a
  whole-file table.
- **`mozilla` at `ziptastic -9` still does not fit a 300-second sandbox step** (four attempts);
  it is measured as two 25,610,240-byte halves summed to 12,353,529, with `xz -9e` on the same
  halves (13,507,344) as the like-for-like baseline. Same limitation ziptastic's own
  `scripts/silesia.sh` documents.
