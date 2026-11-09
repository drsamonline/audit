# TTB — title case did not lowercase, and stopped at an apostrophe

Date: 2026-11-09
Repo: `drsamonline/TTB` · branch `fix/title-case-converter` · PR #7 (open, not merged)
Reference links taken: none
Same session: `2026-11-09-neo-string-literal-escapes.md`,
`2026-11-09-lumen-capture-date-and-badge.md`,
`2026-11-09-app-image-toolkit-badges.md`,
`2026-11-09-offline-pdf-toolkit-cli-refusals.md`,
`2026-11-09-feather-router-signatures.md`,
`2026-11-09-cldr-conventional-commits.md`

## What I looked at

`tools/text.js`, `tools/t-text-calc.js`, `test.mjs`, `data/inputs.js`,
`data/tools.js`, `package.json`. The suite runs under plain Node, so this one is
verifiable locally rather than in CI only.

## What was wrong

`Case converter` in title mode was one expression that only ever uppercased:

    HELLO WORLD      ->  HELLO WORLD      (a case converter that changes nothing)
    hello WORLD      ->  Hello WORLD
    don't stop       ->  Don'T Stop       (\b treats the apostrophe as a boundary)

Found by probing the dispatcher with known-answer inputs rather than by reading —
the tool resolves and returns plausible output, which is why nothing caught it.

## What I changed

One expression: the word is matched whole — a letter followed by letters, `'` or
the right single quote — and its tail is lowercased.

    HELLO WORLD      -> Hello World
    hello WORLD      -> Hello World
    don't stop       -> Don't Stop
    well-known fact  -> Well-Known Fact
    मेरा नाम          -> मेरा नाम

`Title case (AP/Chicago/APA)` is a separate tool and is untouched: it does the
style-guide job, this is the plain converter.

## Evidence

    $ node test.mjs
    dispatcher: 564/564 resolved, 77 need specific input (ok)
    OK — 564 tools, 18 categories, 226 with custom inputs

Four assertions added. Reverting `tools/text.js` alone and re-running:

    AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:
    + 'HELLO WORLD'
    - 'Hello World'

Three of the four fail on the old code. CI run 42641616755, job `validate`:
success.

## What I deliberately did not do

- **No link work.** The list is other MV3 extensions — `vimium-c`, `tridactyl`,
  `ublacklist`, `floccus`, `scriptcat`, `bitwarden/clients`, `Authenticator`,
  `libredirect`, `automa`, `Traduzir-paginas-web`, `ext-saladict` — plus
  `extension.js` (a build framework this repo does not need: `build.mjs` already
  produces four browser bundles), `Awesome-WebExtensions` and
  `awesome-browser-extensions-for-github` (indexes), and `topics/webextension`
  (a topic page). Nothing in the list is a defect fix or a slice.
- **No count change.** README, `ALL_TOOLS.md` and the suite all say 564; the
  kickoff prompt's 563 is the stale number, not the repo's.
- **No version bump, no merge.**

## Next

Decide on PR #7. The probe that found this is cheap and repeatable — feeding
every tool a known-answer input would catch the next one the same way, and
`test.mjs` currently covers only a handful of tools with real assertions.
