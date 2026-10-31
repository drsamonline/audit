# 2026-10-31 — Session close: seven of the eight requirements

This entry records what was actually landed across 28–31 October, verified against the API on
31 October. Where a number appears, it was re-measured today rather than carried forward.

## What I looked at

All 78 repositories: metadata, topics, homepage, Pages, workflows and their crons, release assets,
README text, LICENSE text, and `docs/index.html` for the 53 repos that have one. Plus the three
meta repos in detail — `dashboard`, `control-panel`, `drsamonline.github.io` — and `Matneo`'s store.

## What was wrong

**Licence badges did not describe their licences.** 56 repos had a defect: 24 carried the same
truncated badge URL (a raw space, so GitHub cut it to "license | PolyForm" in grey), 20 had no badge
at all, 1 used a dynamic badge that renders "NOASSERTION" for PolyForm, and 17 named a licence the
LICENSE file did not grant. Six of those also had `![License: MIT]` alt text over a PolyForm badge.

**The store's Buy button went to the hub.** Every product's `link` was `https://drsamonline.github.io/`
— a project index, not a shop — with `buyLinks` empty and `sourceRepo` pointing at a private repo,
so "View source" 404'd for every visitor.

**Releases shipped without icons.** `today-card.apk` contained 16 files: no `res/`, no `mipmap`,
no `ic_launcher`. `AndroidManifest.xml` had no `android:icon` attribute at all, and `exe/build.py`
never passed `--icon`, so every EXE carried the PyInstaller logo.

**The dashboard failed silently and lied about it.** `refresh.yml` died with `Permission denied`
(exit 126) on `tools/commit-and-verify.sh`, which had lost its executable bit. The data sat 24.4
hours stale while the health pill read "healthy", because the pill was computed from `d.health`
alone and never consulted the staleness the page already calculated.

**The hub had no kits page and no blog.** The kits link was a GitHub search URL; the blog link
pointed at Matneo's blog. Kits were mixed into the front page alongside apps.

**24 landing pages described an app and offered no way to get it**, though 14 of those repos
publish a real APK, EXE or installer.

**The control panel was seven sections of prose** — pipeline, routes, orphans, collisions, guards,
gaps, findings — with no entry point.

## What I changed

- **Licence badges** — three passes: 24 truncated URLs and 28 alt texts repaired; then 10 badges
  corrected and 20 added, driven by reading each LICENSE. Bespoke licences were worded, not
  normalised: `gentle-pediatrics-companion` "Free to use, non-commercial", `mnemosyne-companion`
  "Free for personal study", `skin-case-tracker` "Free for personal and clinical use",
  `homoeopathic-materia-medica-repertory-json` "Free to use, attribution required".
- **Store** — `products.json` and `drsoam.py` now carry an `ENQUIRE` mailto; `landingPage` points at
  each product's own page; `sourceRepo` removed; `products.js` says "Enquire by email" with an
  honest price note; `?v=6` so returning visitors get the new script; blog posts prefer
  `landingPage` over the mailto.
- **Icons** — `tools/make_icons.py` (7 ICO sizes, 5 mipmap densities, round icons, monogram
  fallback), `tools/verify_icons.py` (fails a build whose artefact has no icon), `android:icon` and
  `android:roundIcon` in the manifest, `--icon` in `exe/build.py`, and generation plus verification
  wired into both jobs of `build.yml`.
- **Dashboard** — `bash` prefix on `commit-and-verify.sh`; the health pill now folds staleness in
  and says "stale data"; the page reordered to cards → Needs you → Press → collapsed Statistics.
- **Hub** — `/kits/` (18 kits, grouped by what they give you, each with a "use it when" line),
  `/blog/` (dated updates feed), kits excluded from the front page via `isProject`, nav pointed at
  both new pages.
- **Control panel** — one question, three answers: "Something is broken" (default), "Publish
  something", "Show me everything". The four-stage pipeline is kept, collapsed, under everything.
- **Landing pages** — a download block on 14 pages, labelled from the file names, sizes shown,
  wrapped in markers so re-runs are idempotent.
- **Schedules** — 10 cron entries, mostly weekly; `refresh-hub` moved to 03:37 to clear
  `update-profile` at 03:17.

## Evidence

Measured today, through the API:

    78 repos        0 contradiction   0 broken URL   0 NOASSERTION   0 missing badge
                    63 ok            15 free-text claims (informational)

    14 landing pages  0 api.github.com links, 3 real releases/download links each, 1 block each
                      today-card.apk and the TTB zip both serve 206 with real bytes

    dashboard         refresh green 4 runs in a row after the fix; data.json current
    kit-tests         3 consecutive scheduled successes since 25 Oct
    control-panel     13 element ids preserved, 5 script blocks parse, div 51/51, details 4/4
    hub               53 projects on the front page (71 minus 18 kits), /kits/ and /blog/ live

## What I deliberately did not do

- **Did not let a sweep choose a licence.** The first fix script rewrote every badge to PolyForm,
  including MIT and Apache repos, and reported success. It was thrown away and rebuilt with an
  explicit "is this repo actually PolyForm" guard.
- **Did not treat `HMS` or `open-materia-medica` as contradictions.** Both were reported wrong in an
  early pass: HMS carries a proprietary EULA that explicitly withdraws a previous MIT grant, and
  open-materia's "Apache License 2.0" is a credit to the Android SDK, not its own licence. The
  classifier now reads only the licence's opening 600 characters.
- **Did not add download buttons to the 10 repos with no published assets.** A button there would
  be a lie.
- **Did not merge Matneo's three Tuesday jobs.** They run clean and are 10–20 minutes apart;
  collapsing them would turn three failure signals into one.
- **Did not change any LICENSE file.** The file is the legal text; the badge moves to match it.
- **Did not touch `today-card`'s landing page beyond the download block.** It still serves the app
  itself from the landing slot — that needs a split, not a patch.

## Next

1. **`today-card` landing split** — the app belongs at `docs/app.html`; the landing page should
   sell it, not be it. One repo to establish the pattern.
2. **10 repos with no release assets** — `Matneo`, `SmartNotes`, `The_Browser`,
   `ULTIMATE-WINDOWS-OPTIMIZER`, `app-panchang`, `control-panel`,
   `homoeopathic-materia-medica-repertory-json`, `lexora`, `neon-engine`, `profile-kit`. Either a
   release pipeline or an honest "run it in the browser" link.
3. **7 soft licence claims** — badges that describe use in words while the LICENSE says "all rights
   reserved": `MATERIA-MEDICA-BUILDER`, `smartbill-app`, `unstoppable-mind-companion`,
   `ambient-sound-studio`, `the-symphony-companion`, `whispering-body-first-aid`,
   `boericke-repertory`.
4. **`mnemosyne-companion` and `skin-case-tracker`** — their files forbid redistribution; if sharing
   is intended, the LICENSE must change before the badge can say so.
5. **Item 9** of the original requirements list was cut off in the paste and is still unknown.
