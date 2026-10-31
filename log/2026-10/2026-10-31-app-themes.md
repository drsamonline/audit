# 2026-10-31 — Every app gets its own look, and the guard learns about placeholders

## Result

34 apps carry their own palette, type and shape. 32 build green. The other two
(`neon-engine`, `Scrap-and-Gun`) have no build pipeline at all. Zero red.

## How the theming works

web-kit writes the palette as INLINE styles on `<html>`, so a plain `:root` rule loses.
The override therefore carries `!important` — but it is keyed on
`html[data-theme="dark"]` / `html[data-theme="light"]`, which web-kit sets, and each app
gets a considered palette in BOTH modes. That keeps the in-app theme toggle working,
which the first two apps (today-card, seance) lost when they were themed by hand.

Type and shape are per app rather than one skeleton recoloured: serif with generous
corners for the repertory apps, tight mono for the calculators and games, rounded for
the companion apps.

## Four exclusions, with reasons

| Repo | Why |
|---|---|
| aethelgard-rpg-engine | the owner's call: its page links both games and was working |
| whispering-body-first-aid | its build enforces "the demo must be the app"; theming the app alone broke that parity. Reverted, green |
| dashboard | tooling, not a product app |
| profile-kit | a kit, not a product app |

## The guard caught me, twice

**First**, on lockhtml: `✗ DATA: embedded JSON block 0 no longer parses`. My insertion
replaced the FIRST `</body>`, and lockhtml embeds HTML containing that string, so the
style landed inside its data block. Fixed to insert at the LAST `</body>`.

**Second**, and worse: having reverted lockhtml to the exact bytes that built green, it
STILL failed. The guard validated the JSON block whenever the file changed, and
lockhtml's block contains `__PAYLOAD__` — a build-time token that only becomes JSON after
substitution. So any edit to that file, including a pure revert, tripped it.

The fix is in `tools/retrofit-parity.py`: a block matching a placeholder pattern
(`__TOKEN__` or `{{...}}`) is recorded as `placeholder`, not `broken`.

Then I got that wrong too: I changed the status label but left the check as
`if status != "ok"`, so placeholders still failed. The build log gave it away — the error
read `no longer parses — __PAYLOAD__`, showing my new code had run and still rejected it.
The check is now `if status == "broken"`.

Verified: genuinely broken JSON still fails, placeholders pass, and the themed lockhtml
now builds green.

## Evidence

- 34/34 themeable apps carry `id="app-theme"`; 32 builds green, 0 red, 2 without pipelines.
- Guard unit-checked against four cases: valid, broken, `__PAYLOAD__`, `{{data}}`.
- lockhtml re-run twice: green after the guard fix, green again after the theme.

## Next

- aethelgard-rpg-engine has only `ci.yml` and no build pipeline; its red status is a stale
  run from 23 October, not a live failure.
- AUDIT_TOKEN still needed in this repo's secrets for the health page to see private repos.
- Forge's seven reusable workflows are still called by nothing.
