# heavenzip — a phase-0 repository that claimed a green build

Date: 2026-11-09
Repo: `drsamonline/heavenzip` · branch `fix/badges-that-tell-the-truth` · PR #2
(open, not merged)
Reference links taken: none
Same session: `2026-11-09-ttb-title-case.md`,
`2026-11-09-neo-string-literal-escapes.md`,
`2026-11-09-lumen-capture-date-and-badge.md`,
`2026-11-09-app-image-toolkit-badges.md`,
`2026-11-09-offline-pdf-toolkit-cli-refusals.md`,
`2026-11-09-feather-router-signatures.md`,
`2026-11-09-cldr-conventional-commits.md`

## What I looked at

All 33 tracked files. None of them is code: `AGENT_PROMPT.md` (the eight-phase
plan), `PROJECT_OVERVIEW.md`, `config/syc.ini` and three profiles, `LICENSE`, six
badge SVGs, the landing page, and `.github/workflows/sync-binaries.yml`.

## What was wrong

The repository is at phase 0 — `src/`, `bin/` and `tests/` are placeholders —
and its front page claimed otherwise:

| badge | said | truth |
|---|---|---|
| build | `green` | no `CMakeLists.txt`, empty `src/`, no build workflow |
| tests | `in CI` | `tests/` holds a `.gitkeep`; no test job exists |
| licence | `PolyForm NC 1.0.0` | `LICENSE` is **MIT** |

The README's own licence badge was unclosed markdown
(`[![Licence](https://img.shields.io/badge/licence-MIT-3f7a52`), so it rendered as
literal text — and it pointed at a network image in a fleet whose rule is local
SVGs. This is the licence-badge drift the top-level `audit` README already names
as one of the reasons it exists; it had reappeared here.

## What I changed

`tools/badges.py` draws all six from the tree: licence name from the first line of
`LICENSE`, build state from `CMakeLists.txt` plus sources under `src/`, test state
from files under `tests/`. Idempotent, so the badges move when the code lands
rather than in advance of it. The README links the local SVGs and states the phase
out loud, pointing at `AGENT_PROMPT.md` §8.

## Evidence

    $ python3 tools/badges.py
    wrote docs/assets/badge-build.svg   -> phase 0
    wrote docs/assets/badge-tests.svg   -> none yet
    wrote docs/assets/badge-licence.svg -> MIT
    wrote docs/assets/badge-live.svg    -> online
    wrote docs/assets/badge-offline.svg -> no network
    wrote docs/assets/badge-deps.svg    -> 0 runtime

    $ grep -n "shields.io" README.md docs/index.html
    (no matches)

Every `aria-label` matches the file it describes; the licence badge now agrees
with `LICENSE`.

## What I deliberately did not do

- **No phase-0 code.** C++20 + CMake, and this environment has no C or C++
  toolchain at all (`gcc`, `clang`, `cc`, `zig`, `tcc`, `cmake`, `make`, `ninja` —
  every one absent), while the repository has no build workflow for CI to stand
  in as the compiler. That is the difference from CLDR, feather and NEO, where CI
  could compile and I could read the result. Phase 0 needs a `CMakeLists.txt` and
  a `build.yml` first; the parser and CLI skeleton should not be written blind.
- **No link work.** Every entry in the list is a compressor or archiver
  (`7-Zip-zstd`, `PeaZip`, `zpaqfranz`, `zpaq`, `zstd`, `brotli`, `lz4`, `borg`,
  `crabz`, `ouch`, `py7zr`, `gompress`, `DeveMultiCompressor`) and
  `AGENT_PROMPT.md` forbids vendoring or linking any of them — heavenzip spawns
  binaries from `bin/` and nothing else. `awesome-compopt` is an index.

## Next

Decide on PR #2. The unblocking step for this repo is not a feature: it is
`CMakeLists.txt` + `.github/workflows/build.yml` + phase 0, in that order, so the
next change to it can be verified rather than asserted.
