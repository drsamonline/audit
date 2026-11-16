# Aetheris family created, and Aetheris itself takes its first gap

Date: 2026-11-16 · Repos `drsamonline/sorex`, `drsamonline/nodus`, `drsamonline/volumen`,
`drsamonline/The_Browser`
Commits: `The_Browser` `9054e337`, `792df397`, `a73a9758`; three new repositories created

Two pieces of work in one session: a four-browser family was given real trees, and the flagship
was audited and moved past its first blocking gap.

---

## What I looked at

`The_Browser`: `docs/HANDOVER.md` (all 199 lines), `docs/AUDIT.md`, `docs/ROADMAP.md` (§ around
`position: sticky`), `ISSUES.md`, `CHANGELOG.md`, `CMakePresets.json`,
`.github/workflows/build-aetheris.yml` (the version step at line 716), and in `src/`:
`rendering/{paint_executor,render_document,viewport,software_surface,scroll_bar,clip}.{hpp,cpp}`,
`rendering/browser_session.{hpp,cpp}`, `ui/{input_router,window_host,sdl_window,browser_session}.*`,
`main.cpp` (the window loop, `run_render_window`, argument parsing),
`Tests/AetherisRendering/{CMakeLists.txt,TestInputRouter.cpp,TestAetherisHttpClient.cpp,TestPaintBackend.cpp}`.

Upstream sources for the family: `dillo-browser/dillo`, `netsurf-browser/netsurf`,
`ThomasDickey/lynx-snapshots` — cloned, licence headers read, build systems identified.

This repo: `README.md` (the six headings, and the "read state through the API" rule),
`log/2026-11/2026-11-16-heavenzip-bundle-and-autotune.md`.

## What was wrong

**The family had no trees.** Sorex, Nodus and Volumen existed only as a plan in chat. Nothing was
pinned to an upstream commit, and nothing recorded which licences could legally mix — which decides
what a four-browser family can share at all.

**Aetheris: scrolling was declared missing, but the pieces existed and nothing connected them.**
`Viewport` already clamped a scroll offset correctly and `ScrollEvent` was already translated from
SDL. Three disconnections made the feature dead:

1. the painter ignored the offset entirely — `PaintExecutor::execute` had no notion of one, and
   `RenderDocument::render_to_surface` painted from document origin;
2. nothing ever told the viewport how tall the document was, so the clamp pinned scroll to zero
   regardless of input;
3. `InputRouter` dropped wheel events on the floor — `WindowEvent::Kind::Scroll` fell through to
   `default: return InputAction {}`.

**A fourth problem that would have made a working scroll feel broken:** `run_window` kept no
document between frames, so every repaint refetched the page. One wheel notch would have been a
network round trip.

**`AetherisHttpClient` was recorded as "flaky in the LTO size profile".** It is not a network
problem and not an LTO problem. The fixture's accept thread exited when a 10 s idle `select`
expired, so on a loaded runner it could vanish between the two connections the test makes — and
because `join()` waited for that same timeout, every *passing* run cost ten seconds.

**The strict build did not pass.** `src/rendering/png.cpp` declared `kMaxCodes`, unused, which
`-Werror` rejects. So the gate `HANDOVER.md` describes ("compile touched files with `-Werror`; CI
uses it") could not have been green on this tree.

**`--version` lied.** It printed `v0.5.3`; the released tag is `v0.6.2`, published 02:19 the same
day. This is the exact finding `docs/AUDIT.md` records as fixed in an earlier batch — it recurred.

**Two smaller discoveries.** A strict *Debug* build fails in every translation unit before reaching
our code: the project defines `_FORTIFY_SOURCE`, glibc warns it needs `-O`, and `-Werror` promotes
the warning. And `--render-window` has no `file://` backend, so it cannot render a local page
("Resource is not cached and no backend supports the URL").

## What I changed

**The family — three repositories, each a vendored fork with provenance.**

| Repo | Name | Upstream at | Licence as found in the tree |
|---|---|---|---|
| `sorex` | *shrew* | Dillo `6856c50` | GPL-3.0-**or-later** |
| `nodus` | *knot* | NetSurf `f08191a` | GPL-2.0-**only** + OpenSSL exception |
| `volumen` | *scroll* | Lynx `7f67078` | GPL-2.0-**only** |

Each carries the upstream tree at that commit, a second scaffolding commit, and `SOURCES.md`,
`PLAN.md`, `DESIGN.md`, `INNOVATIONS.md`, `ROADMAP.md`, `START_PROMPT.md`, `AGENTS.md`,
`PATCHES.md`, `FAMILY.md` and `shared/vinculum/` (config schema, capability manifest, handoff
protocol, session format, keymap, search engines, Lite Rendering Profile). Upstream is a git remote,
not a GitHub network fork — the app token cannot create forks, and a remote is better for a tree
meant to diverge.

The licence read produced the one finding that shapes the family: **Nodus and Volumen are both
GPL-2.0-only, so they are the only free code corridor.** Sorex (GPL-3.0-or-later) cannot exchange
source with either. The NetSurf helper libraries (`libcss`, `libdom`, `libhubbub`, `libnsgif`…) are
**MIT**, so they may go into all four repos including the MIT Aetheris — that is the family's real
shared asset. `FAMILY.md` was added to `The_Browser` so the group is visible from the flagship.

**Aetheris — scrolling.**

- `PaintOffset` added to `PaintExecutor::execute`; every rectangle, clip rects included, is
  translated, and commands outside the surface are culled before rasterising. Scrolling repaints;
  it never re-lays out.
- `RenderDocument::render_to_surface` gained an offset overload; `document_rect()` exposes the
  laid-out height.
- `InputRouter` gained `Scroll` (wheel notches), `ScrollPage` and `ScrollEdge`, with
  Space/PageUp/PageDown/Home/End mapped in the SDL backend. Page keys do not fire while the address
  bar has focus.
- `ScrollBar` is new: geometry, pointer mapping and painting as pure functions, so the thumb and a
  future hit-test cannot disagree.
- `run_window` keeps the loaded `RenderDocument` until a navigation or reload dirties it, and owns a
  local `Viewport` (the UI session is deliberately free of rendering).
- `--render-window --scroll-y <px>` renders a scrolled view — the only way to look at a long page
  from a headless machine.

**Aetheris — the other fixes.** The HTTP fixture stops on an explicit flag instead of an idle
timeout. The unused `kMaxCodes` is gone. `--version` and the banner report `v0.6.2`.

## Evidence

Build from scratch, no system compiler, zig wrappers per `HANDOVER.md`:

    cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=zigcc ...
    cmake --build build --parallel        → exit 0
    ctest --test-dir build --no-tests=error  → 100% tests passed out of 57

After the work:

    ctest --test-dir build -j 8    → 100% tests passed out of 58   (5.14 s, then 5.20 s)
    ctest -R AetherisHttpClient    → Passed 0.09 s   (was 10.04 s)
    full suite serial              → 25.73 s before, 5.02–5.20 s after
    ./build/bin/aetheris --version → Aetheris Browser v0.6.2

Renders, at three offsets, over loopback (the file scheme has no backend on that path):

    scroll 0     → document 2640px, content 734px, scroll 0px     bands 0–1, thumb at top
    scroll 800   → scroll 800px                                   bands 2–3, thumb moved
    scroll 2000  → scroll 1906px                                  clamped to max, thumb at end

The clamp is the number to trust: 2640 − 734 = 1906, and asking for 2000 produced 1906.

Strict build: `-Werror` clean for every file I touched —
`scroll_bar.cpp.o`, `paint_executor.cpp.o`, `render_document.cpp.o`, `input_router.cpp.o`,
`main.cpp.o`, `png.cpp.o`, `TestScrolling.cpp.o`, `TestInputRouter.cpp.o`,
`TestAetherisHttpClient.cpp.o`. Not verified: `sdl_window.cpp` is not compiled in this
configuration (no SDL2), so the six key-name lines are unverified by compilation.

## What I deliberately did not do

- **Did not rewrite the layout engine or add a `scrollTop` binding.** `scrollTop` needs a host
  callback from QuickJS into the viewport; the viewport now exists, so it is a small job for the
  next session rather than something to rush in this one.
- **Did not wire scrollbar *clicks*.** `ScrollBar::scroll_for_pointer()` is written and tested, but
  the router has no `ScrollTrack` action yet, so the wheel and the keys are the only inputs. Half a
  day, and recorded in `HANDOVER.md`.
- **Did not add a fifth repository.** The family is four browsers and a contract; the landing page
  waits in the hub repo until the projects are finished.
- **Did not touch other repositories, build directories or caches.** The environment is shared and
  the handover says so twice.
- **Did not re-enable `AetherisHttpClient` in the release gate.** The flake is fixed and evidenced,
  but changing a release gate is a release decision, not an audit one.
- **Did not bump the version or move a tag.** Only the stale string was corrected to match the tag
  that already exists.
- **Did not run the Windows-only tests.** No Windows here; the `SDL_Init` hang still needs one
  diagnostic from the owner rather than another guess.

## Next

1. `scrollTop`/`scrollHeight`/`scrollLeft` in the JS layer, bound to the viewport.
2. Scrollbar click and drag, via a `ScrollTrack` action.
3. `position: sticky` — now unblocked, previously impossible.
4. Re-enable `AetherisHttpClient` in the release gate with the 0.09 s evidence.
5. Sorex: the control socket as a documented API. Nodus: `libcss` wiring and the text-frontend
   plotter. Volumen: freeze `--format=text`, then the structure tree.
6. The Windows `SDL_Init` hang: one diagnostic, not a guess.
