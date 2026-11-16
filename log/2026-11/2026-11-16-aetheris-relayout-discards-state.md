# Aetheris — `:focus` works, and the bug was in `relayout()`

Date: 2026-11-16 (seventeenth session) · Repo `drsamonline/The_Browser`
Commit: `2ade6788`

Third attempt at the focus model, and the first that shipped. The previous two were reverted; this
entry records why the fault was never in the place the first two entries looked.

## What I looked at

`The_Browser`: `RenderDocument::relayout()` and `apply_visual_state()`, `node_at`, `hover_at`, and the
window's `--click`, `--move` and `--key` paths.

## What was wrong

`RenderDocument::relayout()` rebuilt the layout tree **with no interaction state**:

    m_layout_root = LayoutTreeBuilder {}.build(m_document.root(), m_stylesheet);

Every call to `relayout()` therefore discarded `:hover` and `:focus`. `dispatch_click_at` calls
`relayout()` immediately after a click focuses an element — so focus was set correctly, the cascade
rebuilt correctly, and then relayout threw it away before a frame was drawn.

That is why two sessions of focus-model work looked like a focus-model bug and was not one.

## How it was found

Not by reading. By three prints and one control experiment:

1. Print inside `node_at`: the click path **did** return a valid DOM node (`dom=0x…0c80`), at the same
   coordinates where hover returned one. The first two entries had assumed it returned null.
2. Print the focused pointer after `set_focused`: it **was** set.
3. Read the pixel: unchanged.
4. **Control:** drive `:focus` from the hover path, which was known to work. It painted magenta
   immediately. That proved the cascade, the visual state and the hit-test were all sound and left
   exactly one suspect: whatever runs between setting the state and drawing the frame.

## What I changed

- **`RenderDocument` remembers the state** `apply_visual_state()` was given
  (`m_last_visual_state`) and passes it to `relayout()`.
- **A click focuses before dispatching**, so `:focus` is in the state the repaint uses.
- `HANDOVER.md` gotcha 6 records the trap; the changelog records the fix.

## Evidence

    --click 200 80 on a fixture with #a:focus{background:#ff00ff}
      before: div a = (0, 0, 255)
      after:  div a = (255, 0, 255)

    full suite: 100% tests passed out of 59
    tree: 2ade6788 on main

## What I deliberately did not do

- **Did not wire keys to the focused element.** A click sets `focused`, but key dispatch still goes to
  `document`. That is the remaining half and it is item 1 in `HANDOVER.md`.
- **Did not add a regression test for `:focus`.** The pixel check that proved this is a script in this
  session, not a CTest. It should become one; noted rather than claimed.
- **Did not touch the other three browser repositories.**

## Next

1. Route key dispatch through the focused node, and dispatch `keyup`.
2. Turn the `:focus` pixel check into a CTest, the way `:hover` and `:active` already are.
3. An exact dirty flag from the JS setters, replacing the fingerprint.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.

## The lesson worth keeping

Two entries in this log said "revert, the cause is one print away". They were right about the print and
wrong about the suspect: the print showed the focus path was innocent, and the control experiment
pointed at `relayout()`. A revert plus a sharper question beats a third guess.
