# 2026-11 presentation audit

**100 repositories read against the `repo-presentation` skill, one row each, with the delta every
repo still needs — scoped to what that repo actually is.** A kit is not asked for an app
screenshot. A desktop product is not asked for a live demo. Every repo is asked for a landing page,
and every landing page has to be its own design.

This is a measurement, not a plan for later. Every row was produced by the skill's own gate
(`verify.py`) running over a shallow clone of the repo at HEAD, so a repo that reads *ok* here is a
repo that passed the check, not one that was assumed to.

## What I looked at

- **100 repos.** Both GitHub connections in this session resolve to the same account
  (`drsamonline`), so one pass covers the fleet — nothing was left behind by using one.
- **Cloned, not read through raw.** `git clone --depth 1` for all 100 (1.5 GB), then the skill's
  `verify.py` against each working tree. `raw.githubusercontent.com` lags a commit by minutes to
  hours and has made finished work look broken twice in this fleet; it is not evidence.
- **The skill's own surfaces per repo** — landing page, app at `docs/play/`, six local badges,
  screenshots, README support section, the support block, the portrait, offline honesty, Apple
  build targets — plus one thing no script sees: **where the app actually is.**
  `docs/play/index.html` missing is only a fact; whether the app lives at `docs/app.html`, at the
  repo root, in `docs/demo/`, or nowhere at all is the work.
- **And the design of all 74 landing pages** — their CSS class tokens, declared colours, font
  stacks and heading sequences, clustered by similarity. That is `design.md`.

## The scope: what each tier is actually required to carry

The first version of this audit applied the full checklist to all 100 repos and produced 51 "splits"
and 85 missing screenshot sets. Most of those were not gaps — they were the checklist asking a
library for a picture of its interface. The owner's rule is narrower and better:

- **a release build and a live app demo apply to apps, not to kits** — a kit, a forge, an engine is
  code other projects consume, and it has no product UI to screenshot;
- **many apps do not need a live demo, but every repo needs a landing page**;
- **each landing page must be its own design**, not the same page with the title changed.

So each repo carries one of five tiers, and the tier decides the requirement:

| tier | repos | required |
|---|---|---|
| **`app`** | 50 | landing page, a live demo at `docs/play/`, screenshots, badges, support block |
| **`app-no-demo`** | 12 | the same minus the live demo — desktop, extension, server, compiler. The demo band shows screenshots |
| **`kit`** | 28 | landing page, badges, support block. **No demo, no app screenshot** — a library has no product UI |
| **`data`** | 6 | landing page, badges, support block — a dataset, a catalogue, a report, the hub, the shop |
| **`infra`** | 4 | decide first whether it wants a public face at all |

The scoping changes the work a lot. `docs/play/` went from **51 repos needing a split to 6**, and
screenshots from 85 to **47** — because a kit was never going to have an app to photograph.

| surface | required | present |
|---|---|---|
| landing page at `docs/index.html` | 100 | 74 |
| app at `docs/play/index.html` | 50 | 44 |
| six local badge SVGs | 96 | **7** |
| screenshots | 62 | 15 |
| README support section | 100 | **2** |
| support block on the landing page | 100 | **2** |
| support portrait | 96 | **2** |
| nothing loaded from another origin | 100 | 64 (36 accepted shields.io) |
| no Apple build target | 100 | 94 (6 accepted) |

### The defect classes

Grouped by the change that closes them, because that is how the work should be done — one class at
a time across the fleet, not one repo at a time through all of them. The counts are **required**
repos, after the tier scoping and after the two accepted classes are removed.

| class | repos | what it is | the fix |
|---|---|---|---|
| **SUPPORT** | 98 | no support block on the landing page, no portrait, no QR | paste region 1 into the footer, run `support_qr.py` and `support_portrait.py` |
| **README** | 98 | no `## Support` table in the README | the same six handles, as a table, from `assets/readme-template.md` |
| **PORTRAIT** | 94 | no `docs/assets/support-portrait.jpg` | `scripts/support_portrait.py` — part of the same paste |
| **BADGES** | 89 | fewer than six local badge SVGs in `docs/assets/` | `scripts/badges.py`, as the offline fallback beside the live ones |
| **SHOTS** | 47 | no `docs/assets/app-desktop.png`, where an app exists | `scripts/shot.sh`, on a populated route |
| **LANDING** | 26 | no landing page at all | build one from `assets/landing-skeleton.html` — its own design |
| **DESIGN** | 23 | the page exists but is a clone or is plain | `design.md` |
| **SPLIT** | 6 | an app with no `docs/play/` | move the entry and point the demo frame at it |
| **NETWORK-BADGE** | 36 | the landing page loads **shields.io** images | *accepted* — deliberate, see below |
| **APPLE** | 6 | a `.dmg`, a macos runner, a Download-for-Mac button | *accepted* — bills nothing, see below |

Two repos need nothing: `lumen` passes every surface it is required to carry, and `repertory-reader`
passes all of them but still fails three other checks — its landing page is dark-only, it has no
light `--ink`/`--paper` palette for the contrast gate to read, and its README has lost the
`shot:start`/`shot:end` markers the pipeline writes into.

### The design problem

**Six landing pages are two designs, repeated three times each**, and 15 more are plain — few
sections, few colours, no display face of their own. `Scrap-and-Gun`, `dashboard` and `musicgen`
share one page (similarity 0.76–0.78, the same three headings, no declared colours at all);
`BLINKTRANSFER`, `blinkcode-ai` and `helioprism` share another (0.56–0.66). The full measurement,
the method and what "its own design" means are in **`design.md`**.

### Decided, not defects: shields.io badges and Apple targets

Two classes look like defects and are not, because the owner looked at them and said no. They stay
measured — the surface column above keeps saying what is true — but they are not work. A re-run of
the audit lists them under `accepted`, and `--strict` is the flag that puts them back on the list.

**`NETWORK-BADGE` (36 repos).** The landing page of a repo whose whole promise is "offline, no
server, no tracking" loads its own description from `img.shields.io`. `CLDR`, `HMS`, `NEO`, `TTB`,
`The_Browser`, `Matneo`, `SmartNotes`, `lexora`, `neon-engine` and 27 others. **These are
deliberate.** A committed SVG goes stale the day after it is generated; a shields.io badge carries
live status — release version, last commit, CI state, stars — that a static file cannot. The fleet
had recurrent broken local badges, and this replaced them. The cost is real and worth stating
plainly: a visitor with no network sees broken images where the badges are, the page contradicts its
own offline claim, and `verify.py` will keep failing the offline check on those 36 repos, so any
future CI gate must allowlist `img.shields.io` rather than expect them to go green. Accepted on that
basis. If a repo ever needs to be genuinely self-contained, the middle path is one attribute —
`onerror` on the `img`, pointing at a committed fallback — rather than a swap of the whole badge set.

### The six Apple targets

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

### What the kits do not need

The 28 `kit` repos — the 19 `*-kit` libraries, `app-companion-forge`, the three engines, the
`weft8-*` pack, `app-builder`, `profile-kit` — keep their demo at the repo root, which GitHub Pages
does not serve. Under the first version of this audit that read as "no landing page, no demo, no
screenshots" and put them in the heaviest work class. Under the owner's scoping it is one job: **a
landing page that explains the API**, plus badges and the support block. No `docs/play/`, no app
screenshot, no release build — there is no product UI to photograph.

Four repos are marked **`decide`** — `backup`, `compfactory`, `HCS`, `heavenzip`. Infrastructure
nobody installs. Whether it wants a landing page and a tip jar is the owner's call, not something a
checklist should decide.

## The order to work in

Not by repo — by class, smallest blast radius first, so that the paste that has to be identical 98
times is done while it is still one habit.

1. **The 98 support blocks.** Copy the four scripts into `tools/`, run
   `verify.py . --fix` for the QR and the portrait, paste both regions, bump the service worker's
   `CACHE`, refresh the footer stamp. One commit per repo, text first, PNGs one at a time.
2. **The 98 READMEs.** The same handles as a table under `## Support`, plus the
   `<!-- shot:start -->` block where it has been lost.
3. **The 23 redesigns and the 26 landings.** This is the design work and it does not batch: each
   repo gets its own idea, its own palette, its own display face. `design.md` says which pages are
   clones and which are plain; `per-repo.md` says, per repo, what the page is and what to do.
4. **The 6 splits and the 47 screenshot sets.** Small now, because a kit is not asked for a picture
   of an interface it does not have. Do them per repo as the page is touched.
5. **Re-run the audit and write the log entry.** The number that matters is the surface table at the
   top of this file; when the `SUPPORT` column reads 100, the rollout is done.

Two classes are deliberately not in this list: the shields.io badges and the six Apple targets. Both
are decisions, not omissions — see **Decided, not defects** above. They will keep showing `FAIL` in
the surface table, because the table records what a page does, not what was agreed about it.

## Files

    README.md                        this measurement and the order to work in
    design.md                        the 74 landing pages, clustered by design similarity
    fleet-table.md                   all 100 repos, tier and surfaces, one row each
    per-repo.md                      one block per repo: what is right, what is missing, what to build
    ../../state/presentation-audit.json   the same, machine-readable, one object per repo
    ../../tools/presentation_audit.py     the walker that produced it
    ../../tools/verify.py                 the skill's gate, copied verbatim — do not edit here

The support block, the landing skeleton and the four asset scripts stay in the skill
(`assets/support-block.html`, `assets/landing-skeleton.html`, `scripts/`). They are deliberately not
copied here: six handles × 100 repos is 600 chances to mistype, and a second copy of the block is a
second source of truth. Paste from the skill, never from a repo's own copy.

`per-repo.md` carries a tier and a verdict per repo:

- **`apply`** (95) — work out the required surfaces for its tier. What that means is decided by the
  tier, not by the verdict.
- **`decide`** (4) — `backup`, `compfactory`, `HCS`, `heavenzip`; whether they want a public face is
  the owner's call.
- **`skip`** (1) — `lumen`. Leave it alone.

## How to re-run it

    gh auth login
    python3 tools/presentation_audit.py /path/to/parent-dir-of-repos
    python3 tools/presentation_audit.py /path/to/parent-dir-of-repos --json state/presentation-audit.json
    python3 tools/presentation_audit.py /path/to/parent-dir-of-repos --design   # the design clusters
    python3 tools/presentation_audit.py /path/to/parent-dir-of-repos --strict   # accepted classes as work

`tools/verify.py` is the skill's `scripts/verify.py`, copied in unchanged so the audit is
reproducible without the skill installed. A change to it belongs in the skill, not here. The walker
needs the repos on disk; it clones nothing itself.

The tier map is a small hand-decided table in `tools/presentation_audit.py`, because no file listing
tells you whether a repo is a product or a library. Everything else — the surfaces, the classes, the
design fingerprints — is measured.
