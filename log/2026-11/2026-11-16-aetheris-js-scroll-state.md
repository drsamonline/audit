# Aetheris — scroll state reaches JavaScript

Date: 2026-11-16 (third session) · Repo `drsamonline/The_Browser`
Commit: `fc7f3b5b`

Third entry for this repo today. Follows `2026-11-16-aetheris-scrollbar-and-stale-connections.md`,
whose "Next" item 1 was the JS scroll bindings.

## What I looked at

`The_Browser`: `src/js/{js.hpp,js.cpp}` (the QuickJS host: `setup_globals`, the `interpreter_for`
context-opaque helper, the `define_function` idiom, the host-hook members `element_lookup` /
`create_element` / `query_selector`), `src/main.cpp` `run_render` (where the DOM handles and
`window.innerWidth` are installed), `third_party/quickjs/quickjs.h`
(`JS_NewCFunctionMagic` takes six arguments, `cproto` included), and
`Tests/AetherisRendering/{TestAetherisJs,TestAetherisDomHost}.cpp`.

## What was wrong

Nothing implemented the scroll half of the DOM. `document.scrollTop`, `document.scrollingElement`,
`scrollHeight`, `window.scrollTo` and `window.scrollBy` were all absent, so any page with a sticky
header, a scroll-to-top button or a lazy loader threw a `TypeError` on load and stopped running.
The scroll machinery added earlier today existed in C++ only, with no way for a page to see or
drive it.

A second gap surfaced while wiring it: `run_window` never constructs an `Interpreter`, so scripts do
not run in the interactive window at all. `--render` runs them; the window does not.

## What I changed

- `js::ViewportMetrics` and two host hooks on `Interpreter` — `viewport_metrics` and
  `scroll_target` — following the existing hook style rather than inventing a new one. Both
  optional: with no host the properties read zero and writes are ignored, so `--eval` is unaffected.
- One installer puts six properties on an object, with the field carried in the QuickJS magic value,
  so there is no per-property function to drift. `scrollTop`/`scrollLeft` writable;
  `scrollHeight`/`scrollWidth`/`clientHeight`/`clientWidth` read-only, as the DOM specifies.
- Installed on `document`, `document.scrollingElement`, `documentElement` and `body` — pages reach
  for all four — with `window.scrollX`/`scrollY`, `window.scrollTo`/`scrollBy` and the bare globals.
- `--render` supplies metrics from the laid-out document (real `scrollHeight`) and records scroll
  requests, so a script that scrolls and then reads back sees its own scroll.

## Evidence

    AetherisJs ....... Passed 0.16 sec     (7 new assertions)
    AetherisDomHost .. Passed 0.86 sec     (properties present on scrollingElement,
                                            documentElement and window in a real render)
    full suite: 100% tests passed out of 58, twice, at -j 8

The assertions cover: reading from the host, `scrollingElement` mirroring `document`,
`scrollTo` reaching the host and being visible to the next read, `scrollBy` being relative,
`scrollHeight` refusing a write, and the no-host default of zero.

Build note: `JS_NewCFunctionMagic` is a six-argument inline taking `cproto`; the five-argument call
compiled in my head and not in the tree, which cost one build cycle.

## What I deliberately did not do

- **Did not wire the interpreter into `run_window`.** It is the bigger gap, but it is a structural
  change to the window loop (script execution, event dispatch, when to re-layout) and rushing it at
  the end of a session is how a window loop starts crashing. It is now item 1 in `HANDOVER.md`.
- **Did not make `scrollHeight` force a layout.** In `--render`, scripts run before the document is
  laid out, so a page reading `scrollHeight` during initial execution gets zero. Browsers force
  layout on that read; this engine does not yet. Recorded rather than faked.
- **Did not add `getBoundingClientRect`, `offsetTop`, `pageYOffset` or `scrollIntoView`.** Same
  family, but each needs geometry the DOM layer does not expose yet.
- **Did not touch the other three browser repositories.**

## Next

1. Run scripts in the window loop: `Interpreter` in `run_window`, dispatch events from the router,
   re-render when a script mutates the DOM.
2. `scrollHeight` forces layout, so a script sees the real height during first execution.
3. `getBoundingClientRect` and `scrollIntoView` on top of the geometry that already exists.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
