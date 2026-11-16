# Aetheris — CSS `:active` reaches the screen

Date: 2026-11-16 (thirteenth session) · Repo `drsamonline/The_Browser`
Commit: `8b03b68d`

Thirteenth entry today. Follows `2026-11-16-aetheris-css-hover.md`, whose "Next" item 1 was `:active`
on mousedown/mouseup.

## What I looked at

`The_Browser`: `VisualInteractionState::set_active`, `style.cpp`'s `:active` matching, and
`InputRouter::handle` — where `WindowEvent::Kind::MouseUp` had **no case at all**, not even a
`default` that did something with it.

## What was wrong

Same shape as hover, one step further along: `set_active` existed, the cascade honoured `:active`,
and the router never produced a press or a release event the window could act on. Buttons did not
respond to being pressed, which is the second most common affordance on the web after hover.

## What I changed

- **`MouseUp` becomes a `Release` action** below the chrome.
- **A press sets the element under the pointer active; a release clears it**, through
  `apply_active_visual_state`, which returns whether the state changed.
- **`--press <x> <y>` on `--window`** leaves the press in place, because a frame is the only way to
  see `:active` without a display.

## Evidence

Checked at the pixel level, from the frame the window wrote:

    fixture: both divs blue, #a:active{background:#00ff00}
    --window <url> 2 /tmp/frames --press 200 80
      pressed div pixel: (0, 255, 0)
      other div pixel:   (0, 0, 255)

    full suite: 100% tests passed out of 59, twice, at -j 8

The assertion reads the PPM through a small `frame_pixel` helper rather than trusting `relayouts: 1`,
for the same reason as the hover test: a relayout can happen and the surface still be wrong.

## What I deliberately did not do

- **Did not change click semantics.** A click still dispatches on press, as before; `:active` is
  visual state only. Moving dispatch to release is the browser-correct behaviour and a bigger change
  than this session could verify.
- **Did not implement `:focus`.** `VisualInteractionState` has a `focused` field and the cascade
  honours it, but there is no focus model: no element is ever focused, so every key goes to
  `document`.
- **Did not reuse the frame reader in the hover test.** The new helper duplicates the parsing that
  test already had inline. Both should call `frame_pixel`; noted rather than done at the end of a
  session.
- **Did not touch the other three browser repositories.**

## Next

1. A focus model, so `:focus` and `keyup` work and keys reach the right element.
2. Click dispatch on release rather than press, with `:active` held for the duration.
3. The hover test switched onto `frame_pixel`, removing the duplicate parser.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.
