# ai-bridge — the CDP surface pinned, and the Windows job made green

Date: 2026-11-10 · Repo `drsamonline/ai-bridge` · PR #5 (open, not merged)
Reference links taken: `marty90/PyChromeDevTools` (smallest useful CDP surface) —
as the principle, no code

## What I looked at
`bridge/src/cdp/controller.ts`, `test/cdp-attach.cjs`, `test/native-messaging.cjs`,
`test/shell.cjs`, `scripts/install-native-host.mjs`, `scripts/run-suites.mjs`,
`package.json`, `ci.yml`. Local build + suites: 39/39 cdp, 33/33 contract, 26/26
statemachine, 37/37 compress-t0, 45/45 compress-t1, 10/10 doctor, 27/27 routing,
22/22 api-resilience.

## What was wrong / missing
1. No guard on which CDP commands the bridge may send. The attach-only policy is
   pinned; the command surface was not. Two commands today.
2. `manifestPath()` used `path.join`, so a *Linux* manifest path built on Windows
   came out with backslashes — the Windows job's red check.
3. `test/shell.cjs` used `/tmp` for its temp home; Windows has none, so the suite
   died with ENOENT before its first check.

## What I changed
`test/cdp-surface.cjs` (allowlist + stale-entry check, wired into `test:all`);
`path.posix.join` / `path.win32.join` per platform in the installer;
`os.tmpdir()` in the shell suite.

## Evidence
    node test/cdp-surface.cjs            5/5; injecting Network.enable → 2 FAILED
    node test/native-messaging.cjs       25/25 (was 24/25 on Windows)
    node test/shell.cjs                  10/10 (was ENOENT on Windows)
    run 42695569807                      conclusion success — both jobs green
                                         (Windows was red on main)

## What I deliberately did not do
- No change to what the bridge sends; the surface already matched the list.
- No action caching (stagehand idea) — a feature with a cache key to design.
- No version bump, no merge.

## Next
Decide on PR #5. Windows is green again, so the suite that guards this repo now
means something on both platforms.
