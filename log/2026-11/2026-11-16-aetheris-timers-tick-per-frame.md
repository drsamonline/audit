# Aetheris — repeating timers tick once per frame

Date: 2026-11-16 (sixth session) · Repo `drsamonline/The_Browser`
Commit: `9a28bb16`

Sixth entry today. Follows `2026-11-16-aetheris-clicks-reach-scripts.md`, whose "Next" item 2 was
the timer tick.

## What I looked at

`The_Browser`: `Interpreter::run_event_loop` in `src/js/js.cpp` (it jumps virtual time to each
timer's due time and fires it, up to `max_tasks`, which defaults to 1000), `Timer` and `m_timers`,
`run_timers` call sites in `src/main.cpp`, and the window loop's frame iteration.

## What was wrong

`run_event_loop` is the right tool for a headless renderer that wants to finish a page quickly, and
the wrong tool for a window. At load it drained the whole queue: a page with `setInterval(fn, 50)`
fired **1000 times before the first frame**, then never again. So an animated page either flooded
the console at startup and then froze, or — with fewer queued tasks — simply stopped moving.

Two consequences worth separating:

1. **Load-time drain.** `create_scripted_document` called `run_event_loop()`, whose default budget is
   1000 firings of a repeating timer.
2. **No clock between frames.** Nothing advanced virtual time in the window loop, so a timer
   scheduled for 50 ms could never come due in a loop that does not wait.

## What I changed

- **`Interpreter::run_timers(budget_ms, max_tasks = 16)`** — advances virtual time by at most one
  frame and fires only the timers due inside it, returning whether anything ran. The clock advances
  even when nothing was due, otherwise a 50 ms timer never arrives in a 16 ms loop.
- **`fire_timer`** — the firing and rescheduling body extracted, so `run_event_loop` and `run_timers`
  share one implementation and cannot drift.
- **The window ticks 16 ms per iteration**, relayouts when a timer ran, and repaints.
- **Load-time runs `run_timers(0.0)`** — only timers already due, never a drain.

## Evidence

    before (reasoned from the code, then confirmed by the failing assertion):
      20 frames, 50 ms interval -> 1000 firings at load, 0 afterwards
    after:
      rc: 0 | tick count: 6
      |   [js] TICK 1
      |   [js] TICK 2  ... TICK 6

    full suite: 100% tests passed out of 59, twice, at -j 8
    AetherisWindowScripts ... Passed 1.57 sec (three scenarios: load, click, timers)

The new assertion checks both directions: the timer must fire more than once, and fewer than 100
times. A test that only checked "fired at least once" would have passed against the old behaviour.

One self-inflicted detour: the first version of the timer scenario failed because the test helper
hardcoded `--window <url> 2`, so 2 frames gave 32 ms of virtual time and the 50 ms interval never
came due. The helper now takes a frame count.

## What I deliberately did not do

- **Did not add a dirty flag from the JS layer.** A timer that ran forces a relayout and a repaint
  even if it touched nothing. A mutation counter would make repaints honest and let an idle
  `setInterval` stop costing frames. Recorded as item 2 in `HANDOVER.md`.
- **Did not drive timers from wall-clock time.** Virtual time keeps the renderer deterministic and
  testable; a wall-clock timer would make the frame output depend on machine speed.
- **Did not touch `run_render`'s event loop.** It keeps `run_event_loop` semantics, which is what a
  one-shot render wants.
- **Did not touch the other three browser repositories.**

## Next

1. One script-loading path and one click path for `--render` and `--window`.
2. A JS mutation counter so repaints follow real changes.
3. Keys and hover into scripts.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
