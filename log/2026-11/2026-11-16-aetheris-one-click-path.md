# Aetheris — one click path, and a flag that parses differently per mode

Date: 2026-11-16 (ninth session) · Repo `drsamonline/The_Browser`
Commit: `34b4d1c6`

Ninth entry today. Follows `2026-11-16-aetheris-idle-timers.md`, whose "Next" item 2 was folding the
last click path.

## What I looked at

`The_Browser`: the geometry-based dispatch block in `run_render`, `dispatch_click_at` in the window,
and the argument parsing for `--click` in both modes.

## What was wrong

`run_render` still carried its own copy of hit-test, walk-up-to-a-handle, dispatch and relayout. The
window had the same logic as `dispatch_click_at`. Two copies of a click is two chances for a click to
behave differently depending on which entry point produced it — the same shape of bug as the page-load
duplication fixed earlier today.

A second problem surfaced while verifying the first: **`--click` parses differently per mode.**

| Mode | Accepted form |
| --- | --- |
| `--render` | `--click <x>,<y>` — one argument, comma separated |
| `--window` | `--click <x> <y>` — two arguments |

## What I changed

- **`run_render` calls `dispatch_click_at`**, with a 1024x768 viewport of its own.
- **`--window` accepts both spellings**, because a flag that parses differently per mode is a trap
  for whoever writes the next test.

## Evidence

    --render --click 200,50   -> [js] MARK render click        rc: 0
    --window --click 200 80   -> MARK button clicked           rc: 0
    --window --click 200,80   -> MARK button clicked           rc: 0

    full suite: 100% tests passed out of 59, twice, at -j 8

I walked into the flag trap myself: the first verification passed `--click 200 50` to `--render`, got
no output, and briefly suspected the refactor had broken dispatch. It had not — the two-argument form
was silently ignored, `click_x` stayed -1, and the block never ran. That is exactly the failure mode
the inconsistency invites, and the reason it is now fixed rather than merely documented.

## What I deliberately did not do

- **Did not add a suite assertion for `--render --click`.** It works and now shares the tested
  function, but no CTest covers the render-side flag. Recorded as next-work item 2.
- **Did not unify the flag into one spelling.** Accepting both is additive and cannot break an
  existing invocation; removing one could.
- **Did not touch the other three browser repositories.**

## Next

1. An exact dirty flag from the JS setters, replacing the fingerprint.
2. A test for `--render --click`.
3. Keys and hover into scripts.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
