# Session prompt — paste this to start the next session

You are continuing work on the CHCE fleet (ziptastic, heavenzip, HCS, kosh, lexora, corpus-extendum,
faztest, audit) for Dr Sohil Momin.

**First: read `audit/docs/HANDOVER-2026-11-18.md`.** It has the fleet state, what shipped, the one
blocker, the standing rules, and nine traps this project has already paid for. Then read
`ziptastic/docs/FINDINGS.md` — it is the authority for any number you quote.

## Standing rules — these are not optional

- **Read the docs before working**: ziptastic's and the audit's. Every session starts there.
- `docs/FINDINGS.md` is the authority for any number quoted anywhere else.
- **Classification by content, never by extension.**
- An unimplemented command refuses with a non-zero exit and names the phase. Never no-op.
- **Nothing is done until a command has run and its output has been read.**
- **Never merge without reading the CI steps**, not just the green conclusion. A job that skipped the
  new step proves nothing.
- One PR per subject, conventional commits, PR body says what was wrong and what proves it fixed.
- **When a trap is hit twice, write a gate, not a paragraph.**
- Do not poll CI in sleep loops. Verify locally, then check once.
- **Measure instead of arguing** — a sweep over a corpus, never one file.
- Never claim a tool is absent until you have searched by content, not filename.
- File a bug in another repo with a minimal reproducer rather than patching around it.
- **Report in tables and bullets, no paragraphs.** Re-verify every number in every reply.
- Always document everything. Easy wins first, reach early for a release.
- One fixture is not a class. If a number comes from a file you chose, say so.

## Where things stand

- **ziptastic v1.4.5** — 38/38 ctest, corpus 20/20, holdout clean, Pareto tool shipped.
- **heavenzip** phase 7 complete; similarity ordering measured and shipped.
- **HCS** 66 SOURCES rows; bzip2/lrzip/blosc2/libarchive/7zip-cli added.
- **lexora v0.2.0-alpha.1** released (wheel verified by downloading it back).
- **kosh** → `zipkosh` built and proven, **not published** (needs `PYPI_API_TOKEN`).
- **corpus-extendum** — PDFium for PDF rendering; docling rejected on measurement.
- **faztest** — joined 2026-11-19: Brotli front end, measured on Silesia, `docs/FINDINGS.md` is
  its authority, CI added, MIT, hosted-builder scaffolding removed. PRs #1–#4, #6, #7 merged.
  The production build is **verified**: `ulimit -v unlimited && bun run build` → 3.76 s,
  `.output/` 1.6 MB, and `vite dev` serves HTTP 200. The `build` job in CI keeps it checked.
- All eight repos: 0 open PRs, 0 open issues.

## The blocker is gone

**OpenZL is built and benchmarked** (2026-11-19). The recorded blocker — `make` — was wrong three
ways: CMake drives Ninja, `ulimit -v` is a soft cap (`ulimit -v unlimited`), and the real cost is
xgboost's `ExternalProject`, which `zli` does not link. Recipe and numbers:
`log/2026-11/2026-11-19-openzl-benchmarked.md`.

**lzbench is done as well** — it ships prebuilt Linux binaries (v2.4), so no build was needed. The
field is on record: ziptastic first on ratio, last on speed, and beaten by bzip3 on every text
file. See ziptastic `docs/HARNESS_MEASURED.md`.

## What to do, in order

1. ~~OpenZL~~ **done 2026-11-19**: `zli 0.3.0` built (Ninja + zig cc, ml_selector patched out),
   `list-profiles` run, Silesia benchmarked. ziptastic is 31% smaller than `serial` and 35× slower;
   OpenZL's `sao` profile is 46.6% smaller than ziptastic in 1/60th the time. See
   `docs/OPENZL_MEASURED.md`.
2. ~~Build lzbench~~ **done 2026-11-19**: prebuilt Linux binary from the v2.4 release, no build.
   Nine codecs measured; bzip3 beats ziptastic on all seven text files. The bounded next step is
   to compare ziptastic's own BWT backend against bzip3 on those seven.
3. **Bump vendored liblz4 to 1.11.0**, re-run the corpus, count changed frames. The question is
   already answered and the bump is measured safe — see `ziptastic/docs/LZ4_MEASURED.md`.
4. **Publish `zipkosh`** when the token exists.
5. **SQLite column transform** — only after `scripts/column_filter_probe.py` runs on a **real**
   database. There is none in the sandbox; the probe is the gate, not a formality.
6. **corpus-extendum**: replace PyMuPDF for SVG plates with `resvg` (MPL-2.0) if it renders the traced
   plates correctly — the last AGPL dependency.

## Environment

The sandbox wipes `cmake`, `ninja`, `ziglang` and `/tmp` between sessions. Before diagnosing any build
failure: `pip install ninja cmake ziglang`, recreate `/scratch/work/tc/gcc` and `g++` wrappers pointing
at `zig cc`/`zig c++`, and set `ZIG_GLOBAL_CACHE_DIR`, `ZIG_LOCAL_CACHE_DIR`, `TMPDIR` under
`/scratch/work`. `/tmp` is a 64 MB tmpfs — put venvs under `/scratch/work`.
