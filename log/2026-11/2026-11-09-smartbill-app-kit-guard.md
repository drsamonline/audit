# smartbill-app — a retired test that asserted nothing

Date: 2026-11-09 · Repo `drsamonline/smartbill-app` · PR #4 (open, not merged)
Links taken: none

## What I looked at
`index.html` (1,024 lines, single-page Vue), `docs/play/index.html`, the GST
totals block, the export paths, `tests/retrofit-export-kit.test.js`,
`.github/workflows/build-apps.yml`.

## What was wrong
The retrofit test was retired on 2026-10-28 — correctly — by replacing its
assertions with `console.log("retired…"); process.exit(0)`. A test that always
passes is worse than no test, because the suite counts it as coverage.

The rule it was retired *for* had no check in this repository; the header says the
guard lives in `app-builder/tools/kit-guard.py`, which protects new builds, not
this repo.

## What I changed
The same file asserts the rule: neither page loads an `export-kit`/`web-kit`
script or calls `Export.save(`/`WebKit.`; `exportWord` still builds its own
`new Blob([...], {type:'application/msword'})`; backup still serialises JSON
itself. Header keeps the history (d55428e, 5fde56f, e225a6e).

## Evidence
    node tests/retrofit-export-kit.test.js   -> 7 ok, "retrofit guard: OK", exit 0
    inject <script src="export-kit.js">      -> FAIL, 1 problem(s), exit 1
CI run 42646489541: success.

## What I deliberately did not do
- No app change: GST maths, totals and exports untouched.
- No link work: the list is server-side billing/EHR suites and vendor marketing
  against a single-file Vue app with no backend.
- No version bump, no merge.

## Next
Decide on PR #4.
