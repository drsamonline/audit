# Aetheris — the focus model, attempted and reverted

Date: 2026-11-16 (fifteenth session) · Repo `drsamonline/The_Browser`
Commit: none. Tree left at `8b03b68d`, clean.

Fifteenth entry today. Follows `2026-11-16-aetheris-css-active.md`, whose "Next" item 1 was a focus
model. It was built, it compiled, the suite went green, and it did not work — so it was reverted.

## What I looked at

`The_Browser`: `VisualInteractionState` and its `set_node` transition, `style.cpp`'s pseudo-class
matcher, `RenderDocument::apply_visual_state`'s relayout guard, the window's key dispatch, and the
`--click` / `--key` command-line paths.

## What was wrong

`:focus` never painted. The plan was: a click sets `focused`, `apply_visual_state` rebuilds layout,
the cascade matches `#a:focus`, the frame changes. Three of those four happened.

Measured after the change:

    --window <fixture> 2 /tmp/frames --click 200 80 --key j
      |   [js] MARK doc key j
      | Window ... relayouts: 1
      focused div pixel: (0, 0, 255)   <- still blue, not the #ff00ff the rule asks for

So the state changed and a relayout ran, and the pixel did not.

Two concrete defects, both found by that measurement rather than by reading:

1. **The `--key` path bypasses focus entirely.** The router's `Key` action dispatches to the focused
   element, but the command-line `--key` flag calls `Interpreter::dispatch_key` directly, which fires
   at document. The fixture logged `MARK doc key j` and never `MARK focused key j`.
2. **The `--click` path never set focus.** Only the router's `PageClick` case did. Adding it there
   moved `relayouts` from 0 to 1 and still did not change the pixel.

## What I changed

Nothing. The work was reverted: `git checkout -- src/main.cpp src/js/js.hpp`, tree clean at
`8b03b68d`, suite 59/59 as it was before.

## Evidence

    suite with the change:    100% tests passed out of 59
    suite after the revert:   100% tests passed out of 59
    git status --porcelain:   0 lines

A green suite proved nothing here: no test covers `:focus`, so the suite was green both with the
feature and without it.

The mechanism itself checks out on inspection, which is why this is worth recording:

    visual_state.cpp:  set_node() bumps generation and sets paint_dirty on every change
    style.cpp:292:     if (pseudo == "focus" && interaction_state->focused != &node) return false;
    render_document.cpp:106: relayouts unless generation matches and nothing is dirty

Every link looks correct, so the fault is in a pointer identity or in which node the hit actually
returns - not in the wiring's shape.

## What I deliberately did not do

- **Did not ship it.** `HANDOVER.md` says to leave the tree building and green and to revert what
  cannot be finished. A half-wired `:focus` that silently does nothing is worse than no `:focus`,
  because the next session would assume it works.
- **Did not add a test that passes either way.** A `relayouts: 1` assertion would have been green
  with the broken feature; that is the mistake the hover work avoided by checking pixels.
- **Did not keep chasing the pointer identity** with the session's remaining budget. Instrumenting
  the `:focus` branch to print the compared pointers is the first move next time, not the last.

## Next

1. Instrument `style.cpp`'s `:focus` branch: print `interaction_state->focused` and `&node` for a
   clicked div, and see whether they differ.
2. Route `--key` through the router's `Key` path, so the command line and a real keypress take the
   same route.
3. Then re-attempt the focus model with a pixel assertion that fails without it.
