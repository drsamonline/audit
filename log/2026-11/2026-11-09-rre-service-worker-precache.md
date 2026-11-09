# remedy-relationship-explorer — the landing page's worker precached a file that is not there

Date: 2026-11-09 · Repo `drsamonline/remedy-relationship-explorer` · PR #10 (open, not merged)
Links taken: none

## What I looked at
The three `sw.js` copies, both pages' register() calls, `tests/no-floating-toolbar.test.js`,
`tests/retrofit-web-kit.test.js`, `.github/workflows/test.yml`.

## What was wrong
`cache.addAll(CORE)` rejects on the first 404 and both register() calls are wrapped
in `.catch(()=>{})`, so a stale CORE entry means no offline cache, silently.

    docs/sw.js   (v4, registered by the landing page)  lists app.html,
                                                       manifest.webmanifest — neither exists
    sw.js        (v5, registered by nothing)           lists index.html, app.html — no root index
    docs/play/sw.js (v3)                               correct

The landing page has never had a working service worker; the root copy was dead.

## What I changed
`docs/sw.js` CORE lists what is beside it, VERSION bumped to rre-v6; the root
`sw.js` removed (nothing registers it, no root page); `tests/service-worker.test.js`
checks every worker's CORE against its own directory and runs in CI.

## Evidence
    node tests/service-worker.test.js   OK (both workers)
    old workers restored                2 failed [app.html], [index.html, app.html]
    node tests/no-floating-toolbar.test.js   9/9
CI: success.

## What I deliberately did not do
- No app change: docs/play/index.html and its worker were already correct.
- No change to the caching strategy or to the `.catch(()=>{})` on register —
  whether a user should be told that offline is broken is a separate question.
- No link work: oorep/OpenRep-Deutsch are data projects; the Laravel clinic app
  is a different product.
- No version bump, no merge.

## Next
Decide on PR #10.
