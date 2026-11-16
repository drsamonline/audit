# Aetheris — hover reaches page scripts

Date: 2026-11-16 (eleventh session) · Repo `drsamonline/The_Browser`
Commit: `06b8a610`

Eleventh entry today. Follows `2026-11-16-aetheris-keys-reach-scripts.md`, whose "Next" item 3 was
hover into scripts.

## What I looked at

`The_Browser`: the window's input switch (`PageHover` had no case at all), `dispatch_click_at` and its
hit-test, and `InputRouter`'s hover branch, which computes `PageHover` with the pointer position.

## What was wrong

The router computed the hover and the window dropped it. A page's `mouseover` and `mouseout` handlers
never ran — the same shape as the click bug two sessions ago: the action existed, the consumer did not.

## What I changed

- **`node_at`** — the hit-test and walk-up-to-a-JavaScript-handle logic, shared by clicks and hover,
  so the two cannot disagree about what is under the pointer.
- **`hover_at`** — dispatches `mouseout` on the element being left, `mouseover` on the one being
  entered, and reports whether the element changed at all, so a pointer jitter inside one element
  costs nothing.
- **`--move <x> <y>` on `--window`** — one move after load, which is how this is verified headlessly.
- Repaints only when a handler changed the document, reusing the timer fingerprint.

## Evidence

    --window <fixture> 2 --move 200 80
      |   [js] MARK over a
      | Window ... events handled: 0, relayouts: 0

    full suite: 100% tests passed out of 59, twice, at -j 8

The fixture stacks two 400x100 divs at the top of the content area, so window y 80 (minus the 34 px
chrome) lands in the first one.

## What I deliberately did not do

- **Did not test `mouseout`.** It is dispatched, but the CLI takes a single `--move`, so the test
  never leaves an element it entered. Two moves would need the flag to repeat; noted rather than
  faked with a second flag.
- **Did not implement CSS `:hover`.** This is the JavaScript half only; a stylesheet's hover state
  needs the visual-state machinery that already exists for other pseudo-classes.
- **Did not dispatch hover when the pointer leaves the window.** No `mouseleave` equivalent yet.
- **Did not touch the other three browser repositories.**

## Next

1. An exact dirty flag from the JS setters, replacing the fingerprint.
2. `keyup` and a focused element.
3. Repeated `--move` so `mouseout` gets a test, and CSS `:hover` on top of the same tracking.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
