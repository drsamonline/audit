# kosh — a fifth repository for the family, and the workbench the fleet was missing

Date: 2026-11-11 · Repo `drsamonline/kosh` (created, pushed) · `drsamonline/compfactory` (updated)
Reference read: `drsamonline/ziptastic`, `drsamonline/lexora`, `drsamonline/heavenzip`,
`drsamonline/compfactory`, `drsamonline/HCS`

## What I looked at

Six Windows binaries supplied by the owner — `DeflOpt.exe`, `ECT.exe`, `WABBIE_1.0.exe`,
`SplitSat.exe`, `WinRK312x64.exe`, `decomp.exe` — plus the family repositories above, read
for conventions: the README shape (badges drawn from the tree, a claim table, "what it is
not", the support block), `PROJECT_OVERVIEW.md`, the `AGENT_PROMPT.md` phase rule, the
`docs/FINDINGS.md` discipline that every published number has a command behind it, the
audit rule that a change is done only when it is read back from the API, and ziptastic's
`docs/FORMAT.md` for the CHCE bitstream.

## What was wrong

The fleet had an engine (`ziptastic`), a source vault (`HCS`), an orchestrator
(`heavenzip`) and a coordinator (`compfactory`) — and no workbench. The jobs that happen
*around* compression were being done by five unrelated Windows programs, none of which
verify anything, two of which rewrite files in place with no undo, and one of which
(WABBIE) shipped against debug MSVC runtimes with a CUDA dependency.

Two of the six binaries cannot be read at all, and saying so is part of the record:
`SplitSat.exe` is an obfuscated .NET assembly (private-use Unicode type names, encrypted
string heap), `decomp.exe` is not a valid PE (no section table, high-entropy body), and
`WinRK312x64.exe` is an NSIS installer for a closed format. Nothing was rebuilt from those
three beyond what their imports and headers disclose.

## What I changed

**New repository `drsamonline/kosh`** — the workbench, MIT, 43 tests.

- Engine: split/join with a manifest and per-part SHA-256; a `.kosh` container (format v2,
  per-entry hashes plus a manifest digest over the table of contents); zip/tar/tar.gz/
  tar.zst/tar.xz; lossless PNG/GZIP/ZIP/JPEG re-compression; `verify` (no writes),
  `info` (block table), `doctor` (live round-trip), `bench` (reproducible comparison).
- Family integration: a CHCE stream is **recognised, not decoded** — `kosh scan file.dr`
  reports magic, version, original size and block count and defers to ziptastic. A
  `.kosh` file deliberately does **not** carry the `CHCE` magic, so no decoder is ever
  handed the wrong format. `kosh pack --engine ziptastic|heavenzip` spawns the binary
  across a process boundary, which is the rule that keeps heavenzip GPL-safe.
- Interface: 12 CLI verbs plus a local FastAPI web UI over the same engine, bound to
  `127.0.0.1`, no outbound requests.
- Docs: `PROJECT_OVERVIEW.md`, `PRIVACY.md`, `SECURITY.md`, `CHANGELOG.md`,
  `docs/ORIGINALS.md` (what each binary is, and what replaced it), `docs/ARCHITECTURE.md`,
  `docs/FINDINGS.md` (every number, the Zopfli budget, the rejected ideas),
  `docs/FORMAT.md`, a landing page and a 404 in the fleet's visual language, badges drawn
  by `tools/badges.py` from the tree.

**`compfactory`** — README and `PROJECT_OVERVIEW.md` now say four repositories plus this
coordinator, the licence table has a `kosh` row, and both sync scripts clone it into
`workspace/`.

## Evidence

    pytest -q                                  43 passed (61 s)
    kosh doctor                                ready — round-trip verified, all codecs import
    kosh verify /tmp/a.kosh                    intact, manifest digest verified
    kosh bench --markdown                      table in docs/FINDINGS.md, seed 20261111
    tests/check-scripts.sh (compfactory)       scripts agree: workspace at ../workspace

Push, read back through the API rather than raw:

    GET /repos/drsamonline/kosh                public, main, default branch main
    GET /repos/drsamonline/kosh/contents       README, docs/, kosh/, tests/, tools/, .github/
    GET /repos/drsamonline/kosh/commits/main   6c08d3c "kosh 1.1.0 — the CHCE file workbench"

    compfactory push                           fc00251..c2a2381 main -> main

Measured, not asserted — from `kosh bench`, the same bytes to every codec:

| file | raw | gzip -9 | xz -9 | kosh brotli 11 | best |
| --- | --- | --- | --- | --- | --- |
| records.csv | 634.52 KB | 167,778 | 77,252 | 63,624 | kosh brotli 11 |
| service.log | 2.62 MB | 267,951 | 115,948 | 109,521 | kosh brotli 11 |
| prose.txt | 453.68 KB | 53,462 | 46,204 | 48,591 | xz -9 |

Two bugs were found by the tests rather than by looking: PNG adaptive filtering encoded
each row against a zero "up" neighbour (corrupting images whose chosen filter was Average
or Paeth), and the benchmark corpus carried wall-clock mtimes into the container, so the
"reproducible" table moved by a byte between runs. Both are fixed and both now have a test
that fails if they come back.

## What I deliberately did not do

- **No CHCE bitstream implementation.** Re-implementing `.dr` decoding would break the
  single-purpose rule and produce a second, divergent decoder.
- **No preflate inside kosh.** ziptastic already carries it as
  `src/precompressors/preflate_wrap.cpp`.
- **No engine work at all.** No BWT, rANS, PPMd or context mixing. The bench table is the
  argument: the wins are in format transforms, not another entropy coder.
- **No GPU path**, despite WABBIE's CUDA BSC stage. Blocks compress independently and
  already parallelise on cores.
- **No reconstruction of the three unreadable binaries.** `SplitSat` is obfuscated,
  `decomp.exe` is corrupt, `WinRK`'s payload is closed. Their documentation says so rather
  than inventing behaviour.
- **No merge or rewrite of any existing repository.** `compfactory` got the smallest edit
  that makes the family description true; nothing else was touched.
- **No GitHub Pages enablement.** `docs/index.html` is ready for
  `drsamonline.github.io/kosh/`, but turning Pages on is an owner action (see Next).

## Next

- Enable Pages on `kosh` (Settings → Pages → Deploy from branch → `main` / `/docs`) so the
  landing page goes live at `drsamonline.github.io/kosh/`.
- Run `kosh pack --engine ziptastic` against a built ziptastic. Today the delegation is
  proven against a stand-in binary in `tests/test_family.py`, not against the real engine.
- Add `kosh` to the dashboard and the profile index once Pages is live, so the fleet's
  self-updating pages pick it up.
- Decide whether `kosh optimize` should learn ziptastic's Layer 0 transforms (PDF, WAV,
  SQLite) or whether that stays engine work. Current answer: engine work, but the container
  could carry a recipe.
