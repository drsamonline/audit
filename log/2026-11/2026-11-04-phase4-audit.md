# 2026-11-04 — Phase 4 audited against the live estate

Phase 4 is "Landing pages vs app pages". Five batches. Measured today across all 101
repositories, by reading every `docs/index.html` and `docs/app.html`.

## Verdict: NOT complete. Three of five batches are unfinished.

| Batch | Requirement | Status |
|---|---|---|
| B4.1 | write the rule + template before touching a repo | **missing** - no template file in forge anywhere sensible |
| B4.2 | `today-card` split into landing + app | **done** - landing is 6,430 bytes, nothing is duplicated |
| B4.3 | the 25 landings with no download get one | **10 done, 15 still without** |
| B4.4 | `Scrap-and-Gun`, `neon-velocity` get landings | **half** - Scrap-and-Gun yes, neon-velocity still missing |
| B4.5 | the 9 sharing `#0f1115`/`#22c55e` get their own accent | **not done** - 27 landings still on the shared palette |

## What the estate actually looks like

    101 repositories
     98 have docs/index.html
     52 have a separate app page (docs/app.html or docs/play/)
      0 have index.html identical to app.html      <- the split held everywhere
      3 have no landing at all: forge, neon-velocity, registry

That "0 identical" is the good news: wherever a page was split, it stayed split. The old
failure - one file serving as both landing and app - is gone from the corpus.

## B4.3 - 15 landings with no download link

    Matneo, NEO, SmartNotes, The_Browser, app-organon-reader, audit, control-panel,
    knowledge, lexora, musicgen, repertory-reader, weft8-classroom, weft8-compare,
    weft8-hardware, weft8-kit

Five of those - Matneo, SmartNotes, The_Browser, control-panel, lexora - are on the
"no release assets, landing only" list the owner approved, so having no download is correct
for them. The other ten need checking individually: some have releases that are simply not
linked, some may have none.

## B4.4 - one page still missing

`neon-velocity` has no landing. `Scrap-and-Gun` now does (7,988 bytes). `forge` and
`registry` are tooling and meta, which the plan says need no landing.

## B4.5 - the biggest gap

27 landing pages still use `#0f1115` with `#22c55e`:

    BLINKTRANSFER, CLDR, ULTIMATE-WINDOWS-OPTIMIZER, aethelgard-rpg-engine,
    app-companion-forge, app-image-toolkit, app-organon-reader, astro-kit, audit,
    blinkcode-ai, book-kit, case-kit, compress-kit, control-panel, crypto-kit,
    export-kit, frame-kit, game-kit, helioprism, knowledge, ... 7 more

The plan named 9; the estate has 27. Worth understanding why: the app-theming sweep themed
the APPLICATIONS (`docs/app.html`, `docs/play/`), not the LANDING pages. So the apps look
individual and the front doors still look like each other - which is the opposite of what
B4.5 asked for, and the opposite of what a visitor sees first.

## To finish Phase 4

  1. B4.5 first - it is the visible one. Give the 27 landings their own accent and screenshot
     set, reusing the palette each app already has.
  2. B4.4 - build neon-velocity's landing.
  3. B4.3 - check the ten remaining for real release assets and link them; leave the five
     that genuinely have none.
  4. B4.1 - commit the template the plan required, so the pages that remain follow one rule
     rather than 27 improvisations.
