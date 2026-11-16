# Aetheris — the window runs scripts now

Date: 2026-11-16 (fourth session) · Repo `drsamonline/The_Browser`
Commit: `2489ab08`

Fourth entry today. Follows `2026-11-16-aetheris-js-scroll-state.md`, whose "Next" item 1 was
running scripts in the window loop.

## What I looked at

`The_Browser`: `src/main.cpp` — `run_window` (render_frame, the viewport, the input loop) and
`run_render` (fetch, dependency discovery, `DomHost`, `Interpreter`, the handler wiring, CSP check,
script execution, `create_from_document`, `--dispatch` and `--click`), plus `DomHost::release()` and
the QuickJS teardown assertion in `third_party/quickjs/quickjs.c:2700`.

## What was wrong

`run_window` called `RenderDocument::create(body, css, …)` directly. No interpreter was ever
constructed, so **no script ran in a real window**. A page that builds its content in JavaScript —
which is most of the modern web — rendered blank in the window while working under `--render`. The
two entry points had silently diverged: one ran the page, the other only parsed it.

## What I changed

- **`create_scripted_document`** — parse, run inline scripts against the DOM, then lay out. It is
  the script path from `run_render`, lifted into one function.
- **The window owns the interpreter and the DOM host**, declared before the cached page so
  destruction runs document → host → interpreter. The host owns the nodes scripts create; the
  interpreter must outlive the host.
- **`page_dom.release()` before teardown.** Without it, freeing the QuickJS runtime while the host
  still held handles trips `Assertion 'list_empty(&rt->gc_obj_list)' failed` — the render completes,
  prints its summary, and then the process aborts. Exit status 134 on a perfectly good frame.
- **`AetherisWindowScripts`** — a new CTest that drives the real binary in `--window` mode against a
  local fixture and asserts the script's console line appears *and* the exit status is 0.

## Evidence

    AetherisWindowScripts ... Passed 0.30 sec
    full suite: 100% tests passed out of 59

    before: MARK present: True | rc: -6 (SIGABRT, gc_obj_list assertion)
    after:  MARK present: True | rc: 0

    |   [js] MARK window script ran
    | Window 1024x768 (chrome 34px, content 734px, document 734px), backend: headless, tabs: 1

The first attempt at this was a full refactor that moved the block out of `run_render` and passed
`--dispatch` in through a callback. It broke, because `--click` hit-testing also needs the live host
and interpreter *after* layout. That attempt was reverted rather than half-fixed — `main.cpp` was
restored from a backup and confirmed clean (0 compile errors) before the second, narrower approach.

## What I deliberately did not do

- **Did not fold `run_render` and `create_scripted_document` into one path.** That is the right end
  state and it is now item 1 in `HANDOVER.md`, with a note that it has already been attempted once
  and needs a session with room to get it wrong. Shipping a second copy is debt; shipping a broken
  `run_render` would have been a regression in the path every existing test covers.
- **Did not dispatch input events to scripts or re-render on later DOM mutation.** Scripts run once,
  at load. A click that changes the DOM does not repaint yet.
- **Did not add an event-loop tick to the window.** `run_event_loop` runs virtual-time timers once at
  load; a `setInterval` in a window still does nothing.
- **Did not touch the other three browser repositories.**

## Next

1. One script-loading path for `--render` and `--window`, via an `after_scripts` callback.
2. Dispatch router actions into scripts; re-render when a script mutates the DOM.
3. A real timer tick in the window loop, on virtual time, so `setInterval` pages animate.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
