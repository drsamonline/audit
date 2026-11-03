# 2026-11-03 — presentation audit of the whole fleet

## What I looked at

Every one of the 100 repositories on `drsamonline`, cloned at HEAD (`--depth 1`, 1.5 GB) and read
with the `repo-presentation` skill's own gate, `verify.py`. Both GitHub connections in the session
resolve to the same account, so one pass covers the fleet.

Ten surfaces per repo — landing page, app at `docs/play/`, six local badges, screenshots, README
support section, the support block, the portrait, theme inheritance, offline honesty, Apple build
targets — plus the thing the script cannot see: where the app actually lives today.

Then the owner scoped it, and the scope changed the work more than the measurement did:

- **a release build and a live demo apply to apps, not to kits** — a kit, a forge, an engine has no
  product UI to screenshot, so asking it for `docs/play/` and `app-desktop.png` is asking for a
  picture of nothing;
- **many apps do not need a live demo, but every repo needs a landing page**;
- **each landing page must be its own design**, not one page with the title changed.

So every repo now carries a **tier** — `app` (50), `app-no-demo` (12), `kit` (28), `data` (6),
`infra` (4) — and the tier decides which surfaces are required. And all 74 landing pages were
fingerprinted: CSS class tokens, declared colours, font stacks and heading sequences, clustered by
similarity.

## What was wrong

Two of 100 repos carry the whole treatment. `lumen` passes all ten surfaces; `repertory-reader`
passes all ten surface checks and still fails three others.

The rest is concentrated in a few omissions, once the scope is right:

| | required repos |
|---|---|
| no support block on the landing page | 98 |
| no `## Support` section in the README | 98 |
| no support portrait | 94 |
| fewer than six local badge SVGs | 89 |
| no screenshot in `docs/assets/` | 47 |
| no landing page at all | 26 |
| **the page is a clone or is plain** | **23** |
| no app at `docs/play/` | **6** |
| loads shields.io images | 36 (accepted) |
| offers a macOS/iOS build | 6 (accepted) |

The scoping is the finding: `docs/play/` went from 51 repos to **6**, screenshots from 85 to **47**.
Under the full checklist the kits were the heaviest block of work in the fleet; under the right
scope they are one job — a landing page that explains an API — and there is no release build to
produce for them at all.

The last two read as wrong rather than missing, and the owner has since ruled on both — see *What I
deliberately did not do*. A repo whose promise is "offline, no server, no tracking" that loads its
own description from `img.shields.io` contradicts its product above the fold — 36 of them do, and
that is deliberate. Six repos offer a `.dmg`: `dance-fight`, `eon-commando`, `neon-runner`,
`retro-strike`, `remedy-relationship-explorer` (which also runs `build-desktop.yml` on
`macos-latest`) and `lockhtml` (a macOS runner in `ci.yml`) — and that bills nothing.

### Two real bugs, found while checking two pages the owner called finished

`musicgen` and `Scrap-and-Gun` share a template line for line, and both carry the same two faults:

- the "In the browser" card links to `…/play/play/` — a doubled path, and there is no
  `docs/play/play/` in either repo, so that link has nothing to serve. The hero CTA and the footer
  link point at `…/play/`, which is right;
- `<link rel="icon" href="play/icon.svg">`, but there is no `icon.svg` in `docs/` or in
  `docs/play/` in either repo, so the favicon 404s.

Not a bug: `musicgen`'s README says *iOS: Share → Add to Home Screen*. That is a PWA install
instruction, not a build target — the Apple sweep flags it and is wrong to. Left alone.

The sandbox cannot reach `drsamonline.github.io`, so both findings are read from the repo tree, not
from a live request. That is enough: a URL with no file behind it in the published tree has nothing
to serve.

## What I changed

Nothing in any of the 100 repos. This session wrote the measurement only:

- `reports/2026-11-presentation-audit/README.md` — the scope and its five tiers, the required-vs-
  present table, the defect classes, and the order to work in
- `reports/2026-11-presentation-audit/design.md` — the 74 landing pages clustered by similarity,
  the two clone sets, the plain list, and what "its own design" means
- `reports/2026-11-presentation-audit/fleet-table.md` — 100 rows, tier and surfaces, `—` where the
  tier does not require a surface
- `reports/2026-11-presentation-audit/per-repo.md` — one block per repo: tier, what is already
  right, what is not required, and the smallest set of changes that closes the gap
- `state/presentation-audit.json` — the same, machine-readable
- `tools/presentation_audit.py` — the walker. Rewritten this session: it now carries the tier map,
  the per-tier requirements, the accepted classes and the design clustering, so a re-run reproduces
  this report instead of contradicting it. `tools/verify.py` is the skill's gate, copied verbatim.

Then the owner ruled on the repos the checklist had misread, and the tiers changed again:

| ruling | effect |
|---|---|
| `neon-games` is a **hub** — two games on `neon-engine`, no split | new `hub` tier; the page links to `play/dead-zone/` and `play/neon-police/` |
| `aethelgard-games` is a hub too — two games, two engines | `hub` |
| **engines get a landing page and never a demo** | new `engine` tier: `neon-engine`, `aethelgard-rpg-engine`, `saga-vn-engine`, `weft8-kit` |
| `dashboard`, `control-panel`, `app-companion-forge`, `audit` are **Forge tooling** — no public face | new `tool` tier (not `skills`, which stays public) |
| kits and engines carry **landing page + badges + support block** | confirmed, not changed |
| `musicgen` and `Scrap-and-Gun` are finished pages | design flags cleared; both are reference now |
| `BLINKTRANSFER`, `blinkcode-ai`, `helioprism` — same family, **all three still get their own design** | kept as work |

`docs/play/` is now **4 repos** (`app-lantern`, `app-organon-reader`, `seance`, `today-card`),
screenshots 45, and the redesign set is 3 clones plus 15 plain pages of which 5 are exempt — 10 for
the owner to judge, listed with live links in `design.md`.

## Evidence

The audit is reproducible from this repo:

    python3 tools/presentation_audit.py <parent-dir-of-repos>
    → 100 repos · tiers app 50, app-no-demo 12, kit 28, data 6, infra 4
    → work: BADGES 89, SHOTS 47, README 98, SUPPORT 98, PORTRAIT 94, SPLIT 6, LANDING 26

    python3 tools/presentation_audit.py <parent-dir-of-repos> --design
    → 3 repos: Scrap-and-Gun, dashboard, musicgen            (0.759–0.778)
    → 3 repos: BLINKTRANSFER, blinkcode-ai, helioprism       (0.555–0.658)

`verify.py --audit` was run per repo and its action strings are what `per-repo.md` prints, so no step
in that file is a suggestion invented for the report.

Two things are hand-decided rather than measured, and both are named in `tools/presentation_audit.py`
rather than guessed at: **the tier map** (no file listing tells you whether a repo is a product or a
library) and **three app locations** (`app-organon-reader` and `control-panel` keep the app at
`docs/index.html`, and `neon-games` keeps two games at `docs/play/dead-zone/` and
`docs/play/neon-police/` with no `docs/play/index.html` between them).

The design clustering is a measurement: Jaccard overlap of CSS class tokens and declared hex
colours, weighted with the heading sequence and the page size. It found the two clone sets without
being told where to look, which is the only reason to trust the finding.

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
- **Did not touch the six Apple targets, after checking what they cost.** The owner asked whether a
  macOS build target bills him anything, and it does not: all 100 repos are public, and GitHub
  Actions is free for public repositories, macOS runners included. A `.dmg` button is a link; a
  TestFlight mention enrols nobody in the US$99/yr Developer Program. What is left is honesty, not
  money — `remedy-relationship-explorer`'s `build-desktop.yml` only runs on `v*` tags, but
  `lockhtml`'s `ci.yml` puts `macos-latest` in a matrix on every push, so four macOS jobs per push
  are spent on a platform this estate does not ship. Recorded, not fixed. **This reverses the moment
  a repo goes private** — the macOS multiplier applies to a private repo's included minutes, and
  four jobs × four Python versions at ten times the Linux rate is a real bill.
- **Did not change the 36 shields.io badge sets, after being told they are deliberate.** They were
  chosen because the committed SVGs kept going stale and breaking; a shields.io badge carries live
  status — release version, last commit, CI state — that a static file cannot. So the finding stays
  in the measurement and comes out of the work list: `tools/presentation_audit.py` now carries an
  `ACCEPTED` map and reports these under `accepted`, and `--strict` is the flag that puts them back.
  What is not fixed by deciding it: `verify.py` will keep failing the offline check on those 36
  repos, so a future CI gate must allowlist `img.shields.io` instead of expecting green; a visitor
  with no network sees broken images where the badges are; and the page still contradicts its own
  offline claim. If one repo ever has to be genuinely self-contained, the cheap middle path is
  `onerror` on the `img` pointing at a committed fallback — not a swap of the whole badge set.
- **Did not ask a kit for a release build, a live demo or an app screenshot.** The first version of
  this audit did, and it produced 51 "missing demos" and 85 "missing screenshots" that were mostly
  the checklist asking a library for a picture of an interface it does not have. The owner's rule —
  release builds and live demos are for apps; a landing page is for everyone — is the correct scope,
  and it is now in the tool as the tier map, not as a note in a report.
- **Did not treat a finished page as broken.** `musicgen` and `Scrap-and-Gun` measured as clones of
  each other and of `dashboard`; the owner says both are finished, and they are — the similarity is
  a shared template, not a defect. They stay out of the redesign list. `dashboard` is Forge tooling
  and needs no public face at all.
- **Did not fix the two bugs in `musicgen` and `Scrap-and-Gun`.** A doubled `play/play/` demo link
  and a favicon pointing at an `icon.svg` that does not exist are two-word fixes, but the owner
  asked to be told, not edited. They are recorded above.
- **Did not redesign anything this session.** 23 pages are flagged — six clones, 15 plain, five still
  on the skeleton's heading — and each one is a design decision that needs the subject, not a
  template. `design.md` measures the problem and `per-repo.md` says what each page needs; the pages
  themselves are untouched.
- **Did not add a CI gate for this.** The check needs 100 clones; that belongs in a scheduled job
  with a cache, not in a per-push workflow. It is in `Next`.

## Next

Work by class, not by repo — the paste that has to be identical 98 times is worth doing while it is
still one habit:

1. the 98 support blocks, with `verify.py . --fix` for the QR and the portrait
2. the 98 READMEs
3. the 18 redesigns and the 26 landings — the design work, which does not batch
4. the 4 splits and the 45 screenshot sets — small now, done per repo as the page is touched

`musicgen` and `Scrap-and-Gun` go **last**, by the owner's instruction: both are finished pages, so
what is left on them is the estate-wide block and badge rollout, not the page.

Waiting on the owner: which of the 10 plain pages in `design.md` to redo, whether the four
`weft8-*` pages are a deliberate family, and whether the four split candidates — `app-lantern`,
`app-organon-reader`, `seance`, `today-card` — need a landing page at all or should be left as they
are.

Not in that list, and not to be raised again without new information: the shields.io badges (a
deliberate choice, accepted) and the six Apple targets (they bill nothing while the repos are
public). Delete `lockhtml`'s macOS runner if that repo is ever made private.

Then re-run `tools/presentation_audit.py` and record the new surface table here. The rollout is
finished when the support column reads 100, not when the last commit lands.
