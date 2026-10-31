# 2026-10-28 — Fleet audit, and the licence badge pass

First entry. This is the baseline: everything below is measured against the live GitHub API on
28 October 2026, not remembered.

## What I looked at

All 78 public repos under `drsamonline`. For each one: metadata (description, topics, homepage,
licence, Pages), root file listing, workflow files and their cron schedules, release assets,
README text, LICENSE text, and `docs/index.html`. 105 workflow files, 11 cron entries, 78 READMEs,
78 LICENSE files, 54 landing pages.

Three questions came in from the owner, and drove the shape of the pass:

1. Does the profile actually use code from the three repos thanked in its "Built with" section?
2. Is the licence badge broken across repos too, not just on the profile?
3. Which of the eight requirements are done, and what does fixing them look like in batches?

## What was wrong

**The profile thanks three repos but uses one.** `lowlighter/metrics` is a real dependency —
`.github/workflows/metrics.yml` runs it at a pinned commit and the two committed SVG cards are its
output. `avgupta456/github-trends` contributes no code: the embed is inside an HTML comment,
parked until an account exists. `rzashakeri/beautify-github-profile` is a curated list; what came
from it is badge vocabulary. The heading "Built with" overstates two of the three.

**The licence badge was broken in four different ways, across 56 repos.** A raw space in the
shields.io URL truncates the image, so the badge renders "license | PolyForm" in grey. Twenty
repos had no licence badge at all. One used a dynamic `github/license` badge on a PolyForm repo,
which renders the word "NOASSERTION". Seventeen carried a badge naming a licence the LICENSE file
does not grant — and six of those had `![License: MIT]` as alt text in front of a PolyForm badge.

**The "Built with" section is not the only place a claim outran its evidence.** The profile's
`profile-data.json` curates 40 of 78 repos, so 40 — including all 18 kits — fall through to
"Other / New". The workflow is not failing; the curation map fell behind, and `"other"` is a
declared category, so the fall-through is sanctioned by the config.

**Landing pages are not doing a landing page's job.** In `today-card`, `docs/index.html` is
byte-identical to the `index.html` inside its own APK — the app is served from the landing slot.
25 of 54 landing pages link no release asset at all. Nine share one palette (`#0f1115`), twelve
share one accent (`#22c55e`) — that is the concrete form of "every landing page looks the same".

**Release artefacts ship without icons.** `today-card.apk` contains 16 entries: `classes.dex`,
`assets/www/*`, `kotlin/*`, `AndroidManifest.xml`, and a 564-byte `resources.arsc`. No `res/`, no
`mipmap-*`, no `ic_launcher`. The device shows the default Android robot.
`app-builder/build.yml` has zero references to `icon`, `.ico`, `ic_launcher`, `mipmap` or
`adaptive`, so the EXE is iconless too — and no individual repo can fix that, because the shared
builder never sets one.

## What I changed

**Nothing has been written to any repo yet.** The GitHub credential available to this session is
read-only: `gh api` PUT returns `403 Resource not accessible by integration`, and `git push`
returns `403` with "Permission to drsamonline/today-card.git denied". The App is installed without
Contents: write. So this entry records the audit and the prepared change, and the change itself is
blocked on a permission that only the owner can grant.

Prepared and tested, ready to apply the moment write access exists:

- `tools/collect.py` — the collector, writing `state/repos.json`, `schedules.json`,
  `readmes.json`, `licences.json`.
- `tools/diff.py` — snapshot comparison. Prints `no change` when nothing moved, so any output is
  a real difference.
- `tools/licence_check.py` — the section-3 analysis as a script: classifies each LICENSE file by
  its text, parses each badge URL, compares licence *families* (not strings, so "PolyForm" vs
  "PolyForm Noncommercial 1.0.0" is not a false alarm), and checks alt text.
- `tools/fix_licence_badge.py` — B1.2, the encoding fix. Dry run verified: 24 URL fixes and 28
  alt-text fixes across 28 repos, nothing else touched.

## Evidence

Baseline from `licence_check.py` over all 78 repos:

    CONTRADICTION  17      badge names a licence the LICENSE does not grant
    BROKEN URL     18      raw space truncates the badge (24 counting those also in CONTRADICTION)
    NOASSERTION     1      dynamic badge on a repo GitHub cannot classify
    NO BADGE       20      LICENSE present, no badge in the README
    SUMMARY        11      free-text claim ("free to use"), informational only
    ok             11

Actual licence distribution, classified from the LICENSE text rather than the badge:
57 PolyForm Noncommercial 1.0.0, 11 MIT, 7 all-rights-reserved, 1 CC BY-NC-SA 4.0,
1 Apache-2.0, 1 CC0 + GPL-3.0 split.

Two findings that fell out of the licence pass:

- Six repos contain MIT text GitHub does not recognise (`HMS`, `MATERIA-MEDICA-BUILDER`, `Matneo`,
  `boericke-repertory`, `smartbill-app`, `unstoppable-mind-companion` → all `NOASSERTION`). The
  wording has been edited, so the detector fails. Normalising to canonical MIT makes the sidebar
  show "MIT License".
- `homoeopathic-materia-medica-repertory-json` has a genuine split licence — CC0 for the datasets,
  GPL-3.0 for the code. It needs two badges. A single-badge sweep must not flatten it.

## What I deliberately did not do

**I did not let the fix script choose a licence.** The first dry run of `fix_licence_badge.py`
rewrote *every* licence badge it found to PolyForm — including MIT, Apache and all-rights-reserved
repos. It would have turned six true licences into false ones. The guard now is explicit: a repo
is skipped unless its LICENSE text actually contains "polyform noncommercial", and a URL is left
untouched unless it contains a raw space. This is worth recording because the failure was silent
in the summary — it reported "would fix 43 repos" and looked like success.

**I did not touch the 17 contradictions.** A badge saying MIT over a PolyForm LICENSE is a legal
statement, not a typo. The owner has to say which is authoritative. Five of the seven MIT-vs-
PolyForm cases point the same way (badge copied from a template, file correct), but "probably" is
not good enough for a licence.

**I did not rewrite the profile README, the hub, the dashboard or the control panel.** All four
are Phase 5 onward, and three of them depend on the licence and curation work landing first.

**I did not add a licence badge to the 20 repos that lack one.** The three all-rights-reserved
repos need a decision first: the badge should read "All rights reserved" or "Free for personal
use", and those are different claims. Some READMEs already say the latter while the LICENSE says
the former.

## Next

1. Grant Contents: write to the GitHub App, then run `tools/fix_licence_badge.py --apply` — the
   dry run is already verified at 24 URL + 28 alt-text fixes.
2. Answer the licence questions: the 7 contradictions, and the wording for the 7 all-rights-reserved
   repos. That unblocks B1.1 and B1.3.
3. Phase 2 (icons in `app-builder`) — one shared fix, unblocks 40 repos.
4. Phase 5 (profile) — 40 missing `profile-data.json` entries, the "Built with" split, one-liners.
