# 2026-11 presentation audit

**100 repositories read against the `repo-presentation` skill, one row each, with the delta every
repo still needs. Two repos are finished. Ninety-eight are not, and most of the gap is four things
pasted in the same way 98 times.**

This is a measurement, not a plan for later. Every row was produced by the skill's own gate
(`verify.py`) running over a shallow clone of the repo at HEAD, so a repo that reads *ok* here is a
repo that passed the check, not one that was assumed to.

## What I looked at

- **100 repos.** Both GitHub connections in this session resolve to the same account
  (`drsamonline`), so one pass covers the fleet — nothing was left behind by using one.
- **Cloned, not read through raw.** `git clone --depth 1` for all 100 (1.5 GB), then the skill's
  `verify.py` against each working tree. `raw.githubusercontent.com` lags a commit by minutes to
  hours and has made finished work look broken twice in this fleet; it is not evidence.
- **Ten surfaces per repo**, the skill's own list: landing page, app at `docs/play/`, six local
  badges, screenshots, README support section, the support block, the portrait, theme inheritance,
  offline honesty, and Apple build targets.
- **Plus one thing no script sees: where the app actually is.** `docs/play/index.html` missing is
  only a fact; whether the app lives at `docs/app.html`, at the repo root, in `docs/demo/`, or
  nowhere at all is the work. That classification is in `fleet-table.md` as the `shape` column.

## What was wrong

### The surfaces, counted

| surface | passing | of 100 |
|---|---|---|
| landing page at `docs/index.html` | 74 | |
| app at `docs/play/index.html` | 49 | |
| six local badge SVGs | **7** | |
| screenshots | 15 | |
| README support section | **2** | |
| support block on the landing page | **2** | |
| support portrait | **2** | |
| support block inherits the page theme | 2 | |
| nothing loaded from another origin | 64 | |
| no Apple build target | 94 | |

The two repos that carry the whole treatment are `lumen` and `repertory-reader`. `lumen` passes all
ten surfaces and is the reference shape for everything below. `repertory-reader` passes all ten
surface checks and still fails three others — its landing page is dark-only, it has no light
`--ink`/`--paper` palette for the contrast gate to read, and its README has lost the
`shot:start`/`shot:end` markers the pipeline writes into.

### The six defect classes

Grouped by the change that closes them, because that is how the work should be done — one class at
a time across the fleet, not one repo at a time through all six.

| class | repos | what it is | the fix |
|---|---|---|---|
| **SUPPORT** | 98 | no support block on the landing page, no portrait, no QR | paste region 1 into the footer, run `support_qr.py` and `support_portrait.py` |
| **README** | 98 | no `## Support` table in the README | the same six handles, as a table, from `assets/readme-template.md` |
| **BADGES** | 93 | fewer than six local badge SVGs in `docs/assets/` | `scripts/badges.py` with this repo's real claims |
| **SHOTS** | 85 | no `docs/assets/app-desktop.png` | `scripts/shot.sh`, on a populated route |
| **NETWORK-BADGE** | 36 | the landing page loads **shields.io** images | replace with the local SVGs |
| **SPLIT** | 51 | no app at `docs/play/` | per repo — see below |
| **LANDING** | 26 | no landing page at all | build one from `assets/landing-skeleton.html` |
| **APPLE** | 6 | a `.dmg`, a macos runner, a Download-for-Mac button | delete the target |

One of these is a **defect, not an omission**, and it is the one worth doing first:

- **`NETWORK-BADGE` (36 repos).** The landing page of a repo whose whole promise is "offline, no
  server, no tracking" loads its own description from `img.shields.io`. Every one of those pages
  contradicts its product in the first 200 pixels. `CLDR`, `HMS`, `NEO`, `TTB`, `The_Browser`,
  `Matneo`, `SmartNotes`, `lexora`, `neon-engine` and 27 others.

### Left alone: the six Apple targets

`dance-fight`, `eon-commando`, `neon-runner`, `retro-strike` and `remedy-relationship-explorer`
offer a `.dmg`; `remedy-relationship-explorer` also runs a whole `build-desktop.yml` on
`macos-latest` (tags only — `push: tags: ['v*']`); `lockhtml`'s `ci.yml` puts `macos-latest` in a
matrix that runs on every push. The estate ships Windows, Linux and Android, so these are wrong on
their face — but the owner asked whether they cost him money, and they do not:

- **All 100 repos are public, and GitHub Actions is free for public repositories** — standard
  runners, macOS included. A `macos-latest` job on a public repo bills nothing. The 10× macOS
  multiplier applies to the *included minutes of a private repo*; there is no such quota here.
- **A `.dmg` button is a link.** A link to a release asset costs nothing, whether or not the asset
  exists.
- **App Store and TestFlight cost nothing to mention.** The only Apple charge is the Developer
  Program membership (US$99/yr), and no repo can enrol anyone in that.

So they stay. What is left is not billing but honesty: a Download-for-Mac button that 404s, and
`lockhtml` spending four macOS jobs per push on a platform it does not ship. Worth cleaning up when
the page is being edited for another reason — not worth a session of its own.

**One condition changes this.** If any of these repos is ever made private, `lockhtml`'s matrix
becomes four macOS jobs × four Python versions per push, billed at ten times the Linux rate. That
is the moment to delete the runner, not the moment to discover it on an invoice.

### What is not a defect

The 19 `*-kit` repos (`art-kit`, `web-kit`, `game-kit`, `lan-kit`, `crypto-kit`, …) keep their demo
at the repo root, which GitHub Pages does not serve, so they have no landing page and no demo. That
is a real gap, but it is not the same gap as a missing support block: a kit's public face is a
documentation page with a live demo of the primitives, not a product page. They are `apply` in the
table, with `no-docs` as their shape, and they are the largest single block of work in the fleet.

Seven repos are marked **`decide`** — `backup`, `compfactory`, `HCS`, `heavenzip`, `ziptastic`,
`audit` and `drsamonline`. These are infrastructure, a report, or the profile README. Whether a
repository that nobody installs wants a landing page and a tip jar is the owner's call, not
something a checklist should decide. They are listed with what the check found and left alone until
that call is made.

## The order to work in

Not by repo — by class, smallest blast radius first, so that the paste that has to be identical 98
times is done while it is still one habit.

1. **The 36 network badges.** One mechanical fix per repo: generate the six local SVGs, then
   replace every `img.shields.io` `src` with `assets/badge-<name>.svg`. The offline check should go
   from 64 to 100.
2. **The 98 support blocks.** Copy the four scripts into `tools/`, run
   `verify.py . --fix` for the QR and the portrait, paste both regions, bump the service worker's
   `CACHE`, refresh the footer stamp. One commit per repo, text first, PNGs one at a time.
3. **The 98 READMEs.** The same handles as a table under `## Support`, plus the
   `<!-- shot:start -->` block where it has been lost.
4. **The 51 splits and the 26 landings.** This is the design work and it does not batch: each repo
   gets its own idea, its own palette, its own display face. `per-repo.md` says, per repo, where the
   app is today and where it should go.
5. **Re-run the audit and write the log entry.** The number that matters is the surface table at the
   top of this file; when the `SUPPORT` column reads 100, the rollout is done.

The six Apple targets are deliberately not in this list — see **Left alone: the six Apple targets**
above. They cost nothing while the repos are public.

## Files

    README.md                        this measurement and the order to work in
    fleet-table.md                   all 100 repos, ten surfaces, one row each
    per-repo.md                      one block per repo: what is right, what is missing, what to build
    ../../state/presentation-audit.json   the same, machine-readable, one object per repo
    ../../tools/presentation_audit.py     the walker that produced it
    ../../tools/verify.py                 the skill's gate, copied verbatim — do not edit here

The support block, the landing skeleton and the four asset scripts stay in the skill
(`assets/support-block.html`, `assets/landing-skeleton.html`, `scripts/`). They are deliberately not
copied here: six handles × 100 repos is 600 chances to mistype, and a second copy of the block is a
second source of truth. Paste from the skill, never from a repo's own copy.

`per-repo.md` carries a verdict per repo:

- **`apply`** (75) — the full treatment, including the `docs/play/` split.
- **`apply-lite`** (17) — landing page, README and support block; there is no web app to embed, so
  the demo band shows the screenshots instead of an iframe.
- **`decide`** (7) — infrastructure; whether it wants a public face is the owner's call.
- **`skip`** (1) — `lumen`. Leave it alone.

## How to re-run it

    gh auth login
    python3 tools/presentation_audit.py /path/to/parent-dir-of-repos
    python3 tools/presentation_audit.py /path/to/parent-dir-of-repos --json state/presentation-audit.json

`tools/verify.py` is the skill's `scripts/verify.py`, copied in unchanged so the audit is
reproducible without the skill installed. A change to it belongs in the skill, not here. The walker
needs the repos on disk; it clones nothing itself.
