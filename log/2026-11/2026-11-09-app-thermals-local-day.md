# app-thermals — the dated override used UTC's day

Date: 2026-11-09 · Repo `drsamonline/app-thermals` · PR #2 (open, not merged)
Links taken: none

## What I looked at
`thermals.js` (302 lines, and its copy at `docs/play/thermals.js`), `test-node.js`
(320 lines, 577 assertions), `.github/workflows/test.yml`.

## What was wrong
`todayISO` used `toISOString().slice(0,10)`. 04:00 IST on 10 November is
`2026-11-09T22:30Z`, so a note written then was dated the 9th — and `activeNotes`
compares a note's `until` against that same string, so the override also expired
a day early. These are the notes whose only purpose is to expire.

## What I changed
`todayISO` builds the date from local components. Both copies patched (the suite
asserts they are byte-identical); three assertions; `test.yml` runs with
`TZ: Asia/Kolkata`.

## Evidence
    TZ=Asia/Kolkata node test-node.js   580 passed
    old code, same TZ                   FAIL 04:00 local is that day (got 2026-11-09), 579 passed 1 failed
    TZ=UTC node test-node.js            580 passed
CI: success.

## What I deliberately did not do
- No change to the note model, makeNote or the expiry semantics.
- No change to search, buildIndex or the bundle.
- No link work: oorep/OpenRep-Deutsch are data projects this app reads.

## Next
Decide on PR #2. This is the second instance of `toISOString().slice(0,10)` in
the fleet (case-kit was the first) — worth a grep across the rest.
