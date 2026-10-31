# 2026-10-31 — Build-pin rollout: 36 apps onto the icon-capable workflow

## What I looked at

Every `build-apps.yml` in the fleet, the reusable workflow they call, the commit each one pins
to, and the APKs those builds actually produce.

## What was wrong

All 36 app repos called the shared workflow at a fixed commit:

    drsamonline/app-builder/.github/workflows/build.yml@34fa725   # 26 October, pre-icon

But that workflow checks out the kit from the **default branch**. Pinned workflow, floating kit —
the worst of both. When `android:icon` landed on main on 28 October, the pinned workflow never ran
the icon-generation step, and 18 repos failed with:

    AAPT: error: resource mipmap/ic_launcher not found

That was fixed on 29 October by `e8f68edd`, which committed default mipmaps into the template and
added `tests/test_manifest_icons.py`. Builds recovered, but every app then shipped the *same*
default monogram, because the generate step still never ran.

A second error of mine: I first reported the APK as having no icons at all. Release builds rename
resources to `res/8c.png`, so a grep for `ic_launcher` finds nothing. The icons were there — ten
PNGs at 48/72/96/144/192, square and round.

## What I changed

Moved all 36 repos from `@34fa725` to `@e40fa69` — the commit that carries the icon work — in seven
batches of six, checking the builds after each before touching the next.

## Evidence

- Batch 1 (6), batch 2 (6), batch 3 (6), batch 4 (6), batch 5 (6), final (5), plus `today-card`
  as the pilot: **36 of 36 builds succeeded.**
- Pin verified in place on a sample across every batch (BLINKTRANSFER, app-panchang,
  idle-city-ages-of-growth, canteen-lan, offline-pdf-toolkit, skin-case-tracker, today-card, seance).
- Icons verified by extracting them from two real signed APKs and looking at them:
  `today-card` renders **TC** on green, `seance` renders **SE** on blue. Different apps, different
  icons — the monogram is generated per app name, not shared.

## What I deliberately did not do

- **Did not switch anyone to `@main`.** Pinning is a deliberate safety decision; the fix is to move
  the pin forward, not to remove it. But see "Next" — the pin is only half a pin while the kit
  floats.
- **Did not touch `docs/index.html` on the 11 other pages that hold app state.** Splitting them is a
  judgement call per page, not a sweep: for `retro-strike`, `idle-city`, `neon-engine`,
  `saga-vn-engine` and `aethelgard-rpg-engine` the page *is* the demo and a split would add a click
  before the thing you came for.
- **Did not add per-app artwork.** Every app currently gets a monogram because none of them ships a
  `docs/icon.png`. Dropping one in any repo makes the next build use it, with no workflow change.

## Next

1. **Fix the half-pin.** `build.yml` is pinned but its kit checkout follows `main`, so a change to
   the kit reaches every app immediately while the workflow does not. Either pin the kit checkout to
   the same ref, or accept floating and stop pinning the workflow — the current state is neither,
   and it is what broke 18 builds.
2. **Real artwork** — a `docs/icon.png` per app; the monogram is a floor, not a finish.
3. Eleven landing pages holding app state, split or left deliberately.
4. Ten repos with no release assets.
5. Seven soft licence claims.
6. Item 9 of the original requirements list — still cut off in the paste.
