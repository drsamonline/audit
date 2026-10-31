# 2026-10-31 — Drawn icons: 36 apps, one glyph each

## What I looked at

Every app repo's name, description and landing page, then the icon the build was actually producing.

## What was wrong

Every app shipped the same icon. `make_icons.py` had a monogram fallback, and because no repo
carried its own artwork, all 36 fell back to it. A monogram is a floor, not a design - two letters on
a tile tells a user nothing about what the app does, and 36 identical-looking tiles in an app drawer
is worse than 36 different ones.

## What I changed

Authored one SVG per app, drawn for what that app is, and committed both forms to each repo:

    docs/icon.svg   48x48 viewBox, editable source
    docs/icon.png   512x512 render, what the build consumes

`make_icons.py` already prefers `docs/icon.png`, so no workflow change was needed. The PNG is
committed rather than relying on `cairosvg` being installable in CI, where the cairo system library
is an extra moving part.

The glyph map, by what the app is:

    calendar    today-card                  envelope   seance
    receipt     smartbill-app               search     kent-repertory-explorer
    book        boericke-repertory, offline-pdf-toolkit
    book-open   open-materia-medica, read-live-transform-app
    pen         MATERIA-MEDICA-BUILDER, chalk-lan
    network     remedy-relationship-explorer
    brain       mnemosyne-companion         hand       skin-case-tracker
    lock        app-encrypted-case-log, lockhtml
    pulse       gentle-pediatrics-companion, bmi calculator
    cross       whispering-body-first-aid   sun-moon   app-panchang
    grid        base-bench                  wave       ambient-sound-studio
    note        dance-fight, the-symphony-companion
    quill       app-poets-studio            crosshair  retro-strike
    bolt        neon-runner, unstoppable-mind-companion
    joystick    neon-games                  city       idle-city-ages-of-growth
    flag        aethelgard-games, conqueror-os
    transfer    BLINKTRANSFER               camera     blinkcode-ai
    prism       helioprism                  cup        canteen-lan
    terminal    app-companion-forge

Colours follow the app: green for today-card, indigo for seance, teal for kent, orange for panchang.
Where two apps share a glyph they differ in colour and in the second idea behind them - `lock` for
the encrypted case log is red, for lockhtml it is slate.

## Evidence

- 36 SVGs authored, 36 rendered to 512px PNG, committed as one commit per repo.
- All builds triggered by those commits: **success** on every one sampled (today-card, seance,
  smartbill-app, kent-repertory-explorer, neon-runner, retro-strike, BLINKTRANSFER, app-panchang,
  open-materia-medica).
- Icons verified by extracting them from two rebuilt APKs and looking at them: today-card renders a
  green calendar, seance an indigo sealed envelope. The monogram fallback is no longer reached.

## What I deliberately did not do

- **Did not generate the icons from the app name alone.** Initials are what you get when nobody
  looked at the app.
- **Did not add `cairosvg` to the build.** Committing the rendered PNG keeps the CI dependency list
  unchanged - a build that needs a system graphics library to draw an icon is a build that will
  break on a runner image update.
- **Did not touch the 10 repos that publish no release assets.** An icon is for a thing you install;
  they have nothing to install yet.

## Next

1. Bump the remaining 35 apps to `d7c4e0cb` so the pinned-kit fix reaches them.
2. Where an app later ships real artwork, replace `docs/icon.png` and the next build uses it.
3. Item 9 of the original requirements list - still unknown.
