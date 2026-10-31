# 2026-10-31 — Seven landings off the shared palette

## What I looked at

Every `docs/index.html` in the fleet, checking for the shared web-kit palette
(`--bg:#0f1115`). Seven still carried it: aethelgard-rpg-engine, app-companion-forge,
app-panchang, app-poets-studio, base-bench, canteen-lan, chalk-lan.

## What was wrong

Recolouring one skeleton seven times is not a design. The complaint was that these pages
looked alike, and they did - same structure, same rhythm, different hex.

## What I changed

Six pages rebuilt across four structural families, chosen to suit what each thing is:

| Repo | Family | Look |
|---|---|---|
| app-companion-forge | terminal | window chrome, `$` prompts, mono, green on near-black |
| app-panchang | almanac | warm cream, saffron rule, ruled label/value rows |
| app-poets-studio | poem | centred narrow column, italic serif, rose |
| base-bench | bench | graph-paper grid, tabular rows, technical blue, mono |
| canteen-lan | board | rounded note cards, orange, friendly |
| chalk-lan | board | same family, whiteboard blue, different copy and type |

**aethelgard-rpg-engine was deliberately left alone.** Its `docs/index.html` is the app itself
(53 KB, `requestAnimationFrame`, `localStorage`), not a landing page. Replacing it would have
deleted a game engine. It needs a split before it can have a design of its own, and that is a
decision rather than a script.

## A near-miss worth recording

My first draft pointed every "open" button at `index.html` - which, once the page *is* the
landing, would have looped the visitor back to where they started. The real app in all six
repos lives at `docs/play/`. Caught by listing each repo's `docs/` before shipping.

## Evidence

- Six pages committed, 3.5-4.2 KB each, each with its own palette and type stack.
- All six builds: **success**.
- Rendered each family with headless Chromium and looked at it before committing.

## Next

- aethelgard-rpg-engine: split, or leave the app as the page.
- The 34 apps still on the web-kit app theme; today-card and seance are themed, these are not.
- AUDIT_TOKEN in this repo's secrets, so the health page can see the private-repo jobs.
