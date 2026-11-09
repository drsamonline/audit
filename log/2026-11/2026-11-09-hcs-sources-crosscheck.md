# HCS — the manifest nobody checked against the vault

Date: 2026-11-09
Repo: `drsamonline/HCS` · branch `feat/check-sources-against-old` · PR #3
(open, not merged)
Reference links taken: none
Same session: `2026-11-09-heavenzip-badges.md`, `2026-11-09-ttb-title-case.md`,
`2026-11-09-neo-string-literal-escapes.md`, `2026-11-09-lumen-capture-date-and-badge.md`,
`2026-11-09-app-image-toolkit-badges.md`,
`2026-11-09-offline-pdf-toolkit-cli-refusals.md`,
`2026-11-09-feather-router-signatures.md`,
`2026-11-09-cldr-conventional-commits.md`

## What I looked at

`SOURCES` (50 rows), `scripts/check-vendor.sh`, `tools/manifest.py`,
`.github/workflows/vendor-check.yml`, `README.md`, and the 52 directories under
`old/` — a vault of 6,492 tracked files of pinned third-party source.

## What was wrong

`check-vendor.sh` proves every directory under `old/` has content. It never reads
`SOURCES`, so the manifest — "the machine-readable list of every source" that
consumers read — can say anything at all. Two directions of drift were possible
and neither was checked: an id that resolves to no directory, and a directory
with no row.

Reading both sides by hand found seven real problems: `csc` listed twice with no
directory under either, and five vendored directories (BARF, BBB, FLZP, FPAQF2,
SR3A) with no row at all — no upstream, licence or integration recorded.

The README also referred to `SOURCES.md` four times. The file is `SOURCES`.

## What I changed

`tools/check-sources.py`, wired into `vendor-check.yml` as an advisory step. An
id resolves exactly or by the `-master`/`-dev`/`-main` suffix the vault actually
uses, longest id first so `preflate-rs` claims `preflate-rs-main` instead of
colliding with `preflate`. Sections that are not claims about the tree
(`Pending Additions`, `Submodule entries`, `Licence corrections`) are parsed but
not enforced.

## Evidence

    $ python3 tools/check-sources.py
    SOURCES rows: 50 (50 enforced), old/ directories: 52
      SOURCES lists 'csc' but old/ has no such directory …
      old/BARF is vendored but has no SOURCES row …
      old/BBB … old/FLZP … old/FPAQF2 … old/SR3A …
    7 problem(s).

CI run 42642954934, job `vendor`: success —

    vendor OK: 52 source directories present, all gitlinks mapped
    7 problem(s).
    advisory: not failing the build

## What I deliberately did not do

- **No manifest repair.** Six of the seven findings are judgement calls: whether
  `csc` is vendored at all, and what the upstream, licence and integration of
  BARF/BBB/FLZP/FPAQF2/SR3A are — five single-file compressors carrying `.exe`
  files, with no README and no upstream recorded anywhere in the tree. Writing a
  guessed URL and SPDX identifier into a provenance manifest is worse than the
  gap, so the checker reports and the decision stays with the maintainer.
- **No id renames.** 22 ids resolve by suffix today (`xz` → `xz-master`), so the
  checker is green on them. Making the id column literally equal the directory
  name is a separate data edit and would have buried the real findings in a
  22-row diff.
- **No link work.** Every entry is a compressor or archiver this vault already
  vendors or has chosen not to; a source vault does not adopt code, it pins it,
  and `pin` is still `TBD` for every row — which is the next real gap in this
  repo, and a bigger one than any link.
- **No version bump, no merge.**

## Next

Decide on PR #3, then the two data questions above. After that, promoting the
step is one word: drop `--advisory`.
