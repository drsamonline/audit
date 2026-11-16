# Aetheris — one page-load path, and the bug it was hiding

Date: 2026-11-16 (seventh session) · Repo `drsamonline/The_Browser`
Commit: `e2d63be6`

Seventh entry today. Follows `2026-11-16-aetheris-timers-tick-per-frame.md`, whose "Next" item 1 was
folding the two script-loading paths into one.

## What I looked at

`The_Browser`: `src/main.cpp` — `create_scripted_document` (the copy added yesterday for the window)
and `run_render`'s own block, line by line, plus the `--dispatch` and `--click` blocks that need the
live `DomHost` and `Interpreter` after layout.

## What was wrong

Two copies of the same 120-line sequence: parse, build the DOM host, construct the interpreter, wire
the handlers, check CSP, run scripts, dispatch `DOMContentLoaded`/`load`, run timers, append
`document.write` output, lay out. One copy lived in `run_render`; the other was written yesterday for
the window.

That duplication is not cosmetic — it is the mechanism of yesterday's bug. `run_window` called
`RenderDocument::create` directly and nobody noticed for months, because there was no single place
where "a page load" was defined. Any future entry point can make the same mistake.

## What I changed

- **`create_scripted_document` is the only copy.** It takes the interpreter, DOM host and viewport
  state by reference, so the caller keeps using them after layout — which is exactly what
  `--dispatch` and `--click` need, and why the first attempt at this refactor failed.
- **A `timer_budget_ms` parameter** carries the one real difference between the entry points: a
  one-shot render drains the timer queue (negative budget), a window leaves it to the frame loop
  (zero, then 16 ms per frame).
- **`--dispatch` moved into `run_render`** and relayouts after firing. A window has no use for it.
- **`main.cpp`: 2615 → 2486 lines.**

## Evidence

    full suite: 100% tests passed out of 59, twice, at -j 8
    AetherisDomHost ...... (exercises --render with --dispatch)
    AetherisWindowScripts  (load, click, timers)

    src/main.cpp before: 2615 lines
    src/main.cpp after:  2486 lines

Two mistakes on the way, both caught by the compiler and the suite rather than by the user:

1. The first edit replaced the *helper's* copy of the block instead of `run_render`'s, because
   `std::string::index` found the first occurrence. Fixed by bounding the search to run_render's body.
2. The dedupe silently dropped `--dispatch` (it lived inside the replaced region), and
   `AetherisDomHost` failed with 13.83 s and no clear message. Restoring it after the call, with a
   relayout, brought the suite back to green.

## What I deliberately did not do

- **Did not add a JS dirty flag.** A timer that ran still forces a relayout and a repaint whether or
  not it touched the DOM. That is the next item in `HANDOVER.md`.
- **Did not unify `--click` with `dispatch_click_at`.** `run_render` still has its own hit-test and
  dispatch block; the window has `dispatch_click_at`. They should be one function, and after today
  the pattern for doing it safely is established: take the host by reference, keep the caller's
  post-layout work where it is.
- **Did not touch the other three browser repositories.**

## Next

1. A JS mutation counter so repaints follow real changes.
2. `run_render`'s click dispatch onto `dispatch_click_at`.
3. Keys and hover into scripts.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
