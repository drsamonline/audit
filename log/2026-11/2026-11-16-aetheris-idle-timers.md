# Aetheris — an idle timer stops costing a layout per frame

Date: 2026-11-16 (eighth session) · Repo `drsamonline/The_Browser`
Commit: `e0afb858`

Eighth entry today. Follows `2026-11-16-aetheris-one-load-path.md`, whose "Next" item 1 was the JS
dirty flag.

## What I looked at

`The_Browser`: the window loop's timer tick in `src/main.cpp`, `rendering::DomNode` (`name`, `data`,
`attributes`, `children`), and `Interpreter::run_timers`' return value.

## What was wrong

`run_timers` returns true when any timer ran, and the window treated that as "the document changed":
relayout, repaint. So a page with a `setInterval` that changes nothing — a clock between ticks, a
poller waiting on a response, a debounce counter — paid a full layout and a repaint sixty times a
second. The window was doing the right thing for the wrong reason.

## What I changed

- **`document_fingerprint`** — hashes node names, text and attribute content, order-independently.
  The window takes one before the tick and one after, and lays out again only when they differ.
- **Only on pages with timers.** `Interpreter::has_timers()` guards the whole thing, so a static page
  pays nothing at all.
- **`relayouts: N` in the window summary.** The behaviour is now observable from outside, which is
  what makes it testable rather than a claim.

## Evidence

    idle timer, 20 frames:      rc=0 relayouts=0
    timer writing text:         rc=0 relayouts=6

    full suite: 100% tests passed out of 59, twice, at -j 8

The first version hashed string *lengths* instead of content, and reported **0 relayouts** for the
page whose timer wrote "1" through "6" — every value one character long. The test that would have
caught it was written in the same commit; it did catch it, on the first run.

## What I deliberately did not do

- **Did not add an exact revision counter.** A counter incremented by every JS setter would be exact
  and cheaper per frame, but it means touching every mutation site in the JS layer, and the
  fingerprint already covers the cases that matter. The gap is documented in `HANDOVER.md`: a change
  that leaves every string identical (canvas, pseudo-element style) is invisible to a fingerprint.
- **Did not fingerprint at a finer grain.** One traversal per frame on pages with timers is cheap;
  dirty-region tracking is a layout-engine job, not a window-loop one.
- **Did not touch the other three browser repositories.**

## Next

1. An exact dirty flag from the JS setters, replacing the fingerprint.
2. `run_render`'s click dispatch onto `dispatch_click_at`.
3. Keys and hover into scripts.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
