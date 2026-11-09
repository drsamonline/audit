# case-kit — the calendar day was UTC's, not the clinician's

Date: 2026-11-09 · Repo `drsamonline/case-kit` · PR #4 (open, not merged)
Links taken: none

## What I looked at
`case-kit.js` (145 lines, read whole), `test-node.js`, `.github/workflows/test.yml`.

## What was wrong
`day()` used `toISOString()`, which is timezone-free. 04:00 IST on 9 November is
`2026-11-08T22:30Z`, so `summary().created` and `lastEvent` reported the previous
day for anything recorded between midnight and 05:29 IST.

    TZ=Asia/Kolkata  local date: Mon Nov 09 2026
                     summary.created: 2026-11-08

Invisible from a UTC machine, which is where it was written.

## What I changed
`day()` builds the date from local components. Two assertions (04:00 and 23:30
local). `test.yml` runs with `TZ: Asia/Kolkata` — under UTC both assertions pass
against the old code, so the guard would have been theatre.

## Evidence
    TZ=Asia/Kolkata node test-node.js        28 passed, 0 failed
    old code, same TZ                        FAIL … (2026-11-08), 27 passed 1 failed
    TZ=UTC node test-node.js                 28 passed, 0 failed
CI run 42646675294: success.

## What I deliberately did not do
- No format change: `YYYY-MM-DD` unchanged, only which day it names.
- No link work: medplum/ehrbase/openmrs/openemr/fasten/OCA are server-side EHR
  platforms; FHIR mapping would be a new product, not a slice.
- No version bump, no merge.

## Next
Decide on PR #4. Same class of bug is worth a grep across the fleet for
`toISOString().slice(0, 10)`.
