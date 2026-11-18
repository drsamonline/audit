# Session prompt — paste this to start the next session

You are continuing work on the CHCE fleet (ziptastic, heavenzip, HCS, kosh, lexora, corpus-extendum,
faztest, audit) for Dr Sohil Momin.

**First: read `audit/docs/HANDOVER-2026-11-18.md`.** It has the fleet state, what shipped, the one
blocker, the standing rules, and eight traps this project has already paid for. Then read
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
  its authority, CI added, MIT, hosted-builder scaffolding removed. PRs #1–#4 and #6 merged.
  The production build is unproven in the sandbox (1.5 GB virtual cap, Vite 8's rolldown is
  WASM) and is gated by the `build` job in CI — check that job before trusting the build.
- All eight repos: 0 open PRs, 0 open issues.

## The one blocker

**`make` is not installed in the sandbox.** It blocks OpenZL (the benchmark that opened this work and
the only external check on the engine's central claim) and lzbench (the fair codec harness). Fix that
first — `sudo apt install make`, or provide a machine that has it.

## What to do, in order

1. **Install `make`**, then build OpenZL's `zli` (`cmake --build build --target zli`), run
   `zli list-profiles`, and benchmark the fleet corpus against ziptastic. This is the highest-value
   item in the project and it has been blocked on a compiler twice.
2. **Build lzbench** in the same environment and record ziptastic against its bundled codecs.
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
