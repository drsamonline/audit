# 2026-11-03 — presentation audit of the whole fleet

## What I looked at

Every one of the 100 repositories on `drsamonline`, cloned at HEAD (`--depth 1`, 1.5 GB) and read
with the `repo-presentation` skill's own gate, `verify.py`. Both GitHub connections in the session
resolve to the same account, so one pass covers the fleet.

Ten surfaces per repo — landing page, app at `docs/play/`, six local badges, screenshots, README
support section, the support block, the portrait, theme inheritance, offline honesty, Apple build
targets — plus the thing the script cannot see: where the app actually lives today.

## What was wrong

Two of 100 repos carry the whole treatment. `lumen` passes all ten surfaces; `repertory-reader`
passes all ten surface checks and still fails three others.

The rest is concentrated in four omissions and two defects:

| | repos |
|---|---|
| no support block on the landing page | 98 |
| no `## Support` section in the README | 98 |
| fewer than six local badge SVGs | 93 |
| no screenshot in `docs/assets/` | 85 |
| no app at `docs/play/` | 51 |
| no landing page at all | 26 |
| **loads shields.io images** | **36** |
| **offers a macOS/iOS build** | **6** |

The last two are wrong rather than missing. A repo whose promise is "offline, no server, no
tracking" that loads its own description from `img.shields.io` contradicts its product above the
fold — 36 of them do. And six repos still offer a `.dmg`: `dance-fight`, `eon-commando`,
`neon-runner`, `retro-strike`, `remedy-relationship-explorer` (which also runs
`build-desktop.yml` on `macos-latest`) and `lockhtml` (a macOS runner in `ci.yml`).

## What I changed

Nothing in any of the 100 repos. This session wrote the measurement only:

- `reports/2026-11-presentation-audit/README.md` — the surface table, the six defect classes, and
  the order to work in
- `reports/2026-11-presentation-audit/fleet-table.md` — 100 rows, ten surfaces, and each repo's
  shape
- `reports/2026-11-presentation-audit/per-repo.md` — one block per repo: what is already right,
  what is missing, and the smallest set of changes that closes it
- `state/presentation-audit.json` — the same, machine-readable
- `tools/presentation_audit.py` — the walker, and `tools/verify.py`, the skill's gate copied
  verbatim so the audit is reproducible without the skill installed

## Evidence

The audit is reproducible from this repo:

    python3 tools/presentation_audit.py <parent-dir-of-repos>
    → 100 repos · apply 75, apply-lite 17, decide 7, skip 1

`verify.py --audit` was run per repo and its action strings are what `per-repo.md` prints, so no step
in that file is a suggestion invented for the report. Every shape in the `shape` column was checked
by opening `docs/index.html` and reading what it is: a landing page, the app itself, a generated
report, or nothing.

Two shapes were hand-corrected because no heuristic distinguishes a product page from a page about
a product: `app-organon-reader` and `control-panel` keep the app at `docs/index.html`, and
`neon-games` keeps two games at `docs/play/dead-zone/` and `docs/play/neon-police/` with no
`docs/play/index.html` between them. Those three are named in `tools/presentation_audit.py` rather
than guessed at.

## What I deliberately did not do

- **Did not touch a single repo.** The skill's first move is a read, not a write, and a 100-repo
  session that starts by editing is a session that churns 100 repos before anyone has agreed what
  the target is.
- **Did not mark the seven infrastructure repos as work.** `backup`, `compfactory`, `HCS`,
  `heavenzip`, `ziptastic`, `audit` and `drsamonline` are marked `decide`, not `apply`. A tip jar on
  a compression library that nobody installs is a question for the owner, not a checklist item.
- **Did not copy the support block into this repo.** It stays in the skill's
  `assets/support-block.html`. A second copy here would be a second source of truth for six handles
  that are meant to be identical everywhere.
- **Did not rebuild `lumen`.** It passes. It is the reference, and the report says so.
- **Did not add a CI gate for this.** The check needs 100 clones; that belongs in a scheduled job
  with a cache, not in a per-push workflow. It is in `Next`.

## Next

Work by class, not by repo — the paste that has to be identical 98 times is worth doing while it is
still one habit:

1. the six Apple targets (correctness, not cosmetics)
2. the 36 network badges — one mechanical fix per repo
3. the 98 support blocks, with `verify.py . --fix` for the QR and the portrait
4. the 98 READMEs
5. the 51 splits and the 26 landings — the design work, which does not batch

Then re-run `tools/presentation_audit.py` and record the new surface table here. The rollout is
finished when the support column reads 100, not when the last commit lands.
