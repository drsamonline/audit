# Aetheris — CSS `:hover` reaches the screen

Date: 2026-11-16 (twelfth session) · Repo `drsamonline/The_Browser`
Commit: `b7fd2df8`

Twelfth entry today. Follows `2026-11-16-aetheris-hover-reaches-scripts.md`, whose "Next" item 3 was
CSS `:hover` on top of the same pointer tracking.

## What I looked at

`The_Browser`: `rendering/visual_state.hpp` (`VisualInteractionState` with `hovered`, `active`,
`focused`, a `generation` counter and dirty flags), `rendering/style.cpp:292` (`:hover` matching
against `interaction_state->hovered`), `RenderDocument::apply_visual_state`, and the window's hover
path added last session.

## What was wrong

The cascade has understood `:hover` for a while, and `apply_visual_state` already rebuilds layout when
the visual state changes. **Nothing fed `VisualInteractionState` from the window.** So a stylesheet's
hover state never appeared: the machinery was complete and unplugged. A button did not change colour
under the pointer, which is the single most common visual affordance on the web.

## What I changed

- The window keeps a `VisualInteractionState` and applies the hovered node on every pointer change
  through `apply_hover_visual_state`, which returns whether the state actually changed so a pointer
  jitter inside one element costs nothing.
- Wired from the router's own hover events **and** from `--move`, so it is verifiable without a
  display.

## Evidence

Checked at the pixel level, not by log line:

    fixture: both divs blue, #a:hover red
    --window <url> 2 /tmp/frames --move 200 80
      hovered div pixel:    (255, 0, 0)
      un-hovered div pixel: (0, 0, 255)

    full suite: 100% tests passed out of 59, twice, at -j 8

The new assertion reads the PPM the window wrote and checks both colours. That matters: an assertion
on `relayouts: 1` would have passed even if the paint were wrong, and this project has already had a
release where the chrome rendered bright red for three versions because of a pixel-format mistake that
no test caught.

## What I deliberately did not do

- **Did not wire `:active` or `:focus`.** `VisualInteractionState` has fields for both; neither has an
  input path in the window yet (`MouseUp` and a focus model).
- **Did not implement `mouseleave`.** Moving the pointer out of the window does not clear the hover.
- **Did not test `mouseout`.** Still one `--move` per run, so the test never leaves an element it
  entered.
- **Did not touch the other three browser repositories.**

## Next

1. `:active` on mousedown/mouseup, and a focus model so `:focus` and `keyup` work.
2. Repeated `--move` so `mouseout` gets a test; `mouseleave` on window exit.
3. An exact dirty flag from the JS setters, replacing the fingerprint.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
