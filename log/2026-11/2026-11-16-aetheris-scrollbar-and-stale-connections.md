# Aetheris — scrollbar clicks, and the flake that was really a browser bug

Date: 2026-11-16 (second session) · Repo `drsamonline/The_Browser`
Commits: `eb3a5374`, `1c1e902e`, `93c022d3`, `6e568363`

Continuation of `2026-11-16-aetheris-family-and-first-gap.md`. The previous entry reported the
`AetherisHttpClient` flake as fixed. It was half fixed, and the half that remained turned out to be a
product bug rather than a test bug.

## What I looked at

`The_Browser`: `docs/HANDOVER.md`, `include/aetheris/network/http_client.hpp` (725 lines, header-only
client: pool, cache, cookies, redirects), `src/ui/input_router.{hpp,cpp}`, `src/main.cpp` (window
loop), `src/rendering/scroll_bar.{hpp,cpp}`,
`Tests/AetherisRendering/{TestInputRouter,TestAetherisHttpClient,TestAetherisDomHost}.cpp`.

This repo: `log/2026-11/2026-11-16-aetheris-family-and-first-gap.md`.

## What was wrong

1. **A scrollbar you could see but not click.** `ScrollBar::scroll_for_pointer()` was written and
   tested in the previous session, and nothing called it. `InputRouter::handle_click` sent every
   click below the chrome to `PageClick`, so a click at the right edge hit whatever link was under
   the bar.
2. **`AetherisHttpClient` was still failing, one run in five.** The previous entry fixed the cache
   fixture's 10 s idle `select` and reported the flake closed. Re-running a fresh clone reproduced
   it: `FAILED: stale keep-alive: both requests succeed`, 10.16 s. A different fixture
   (`start_closing_server`) also used a 10 s select, and it exposed something worse.
3. **The browser returns a blank page when a server closes an idle connection.** The client probes a
   pooled socket with `is_alive()` before reuse. A server's FIN can arrive *between* the probe and
   the write, so the request goes into a dead socket, the read returns EOF, and `request_once` handed
   back a response with no body and no error. Servers close idle keep-alive connections constantly;
   this is a real blank-page bug, not a test artefact.
4. **`AetherisDomHost` was a third fixture using an idle timeout as its shutdown signal.** It ran
   three separate browser passes against one server thread that exited after 2 s of silence, so a
   loaded runner lost the server between passes and the failure was reported as a CSP or DOM bug.
5. **The `--version` finding from the previous entry recurred in a different form.** A fresh clone
   and a full rebuild was needed after the sandbox recycled; the toolchain (`cmake`, `ninja`,
   `ziglang`) and the zig wrappers had to be recreated, which is now recorded in `HANDOVER.md` as
   expected behaviour rather than an incident.

## What I changed

**Scrollbar clicks (`eb3a5374`).**

- `InputAction::Kind::ScrollTrack`, plus `InputRouter::set_scroll_bar(visible, content_width,
  bar_width)`. The bar is tested *before* `PageClick`, which is what prevents the fall-through.
- `run_window` reports bar visibility after each frame and applies `ScrollTrack` by recomputing the
  geometry from the current scroll position, so the thumb lands under the pointer.
- Four new assertions in `TestInputRouter`: the edge, the boundary one pixel inside it, the chrome
  strip, and the no-bar case.

**Stale pooled connections (`1c1e902e`).**

- `request_once` records whether the connection came from the pool, and on a send failure, a failed
  header read, or a malformed response clears the pool and retries **exactly once** on a fresh
  connection. It cannot recurse further because the pool is empty on the second attempt.

**Fixture shutdown (`93c022d3`).**

- `AetherisDomHost`'s accept thread runs until an explicit stop flag is set, polled with a 50 ms
  select, set after the third pass. Same pattern as the two `AetherisHttpClient` fixtures.

**Docs (`6e568363`).** `HANDOVER.md` next-work reordered (JS scroll bindings first, thumb dragging
second) and two gotchas added: never use an idle timeout as a fixture's shutdown condition, and
never remove the pooled-connection retry. `CHANGELOG.md` carries all three changes.

## Evidence

    # stale keep-alive, before: ~1 in 5 failed, 10.16 s
    # stale keep-alive, after:
    10 runs, 10 pass, 150-320 ms each

    # full suite, `ctest -j 8`
    run 1: 100% tests passed out of 58
    run 2: 100% tests passed out of 58
    run 3: 100% tests passed out of 58
    run 4: 100% tests passed out of 58

    # after the scrollbar change
    AetherisInputRouter ... Passed 0.04 sec   ("input router: all bindings verified")

Both failures were reproduced before they were fixed: `TestAetherisHttpClient` failed on run 4 of 5
in a direct loop, and the suite failed twice in a row at `-j 8` on `AetherisDomHost` (10.90 s).

## What I deliberately did not do

- **Did not touch the JS layer.** `scrollTop`/`scrollHeight` needs a host bridge from QuickJS into
  the viewport; the viewport exists now, so it is the next session's first job, not something to
  bolt on at the end of this one.
- **Did not implement thumb dragging.** A track click scrolls to a point; a drag needs pointer
  capture between `MouseDown` and `MouseUp`, which is a different change.
- **Did not weaken any assertion to make the suite green.** Two of the three flakes were fixed in
  the product (`HttpClient`) and the fixtures, and the third by removing a shutdown signal that was
  never a valid one. No timeout was raised and no test was excluded.
- **Did not re-enable `AetherisHttpClient` in the release gate.** It passes 10/10 now, but a gate is
  a release decision.
- **Did not touch the other three browser repositories** in this session beyond the family docs
  written earlier today.

## Next

1. `scrollTop` / `scrollLeft` / `scrollHeight` / `scrollWidth` / `clientHeight` bound to the
   viewport, plus `window.scrollTo` and `scrollBy`.
2. Scrollbar thumb dragging with pointer capture.
3. `position: sticky`, now that a scroll offset exists.
4. Re-enable `AetherisHttpClient` in the release gate with the 10/10 evidence.
5. Nodus: `libcss` wiring and the text-frontend plotter — the family's blocking item.
