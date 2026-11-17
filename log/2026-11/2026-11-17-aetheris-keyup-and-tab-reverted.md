# Aetheris — `keyup` ships, Tab order reverted with its diagnosis

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `fb956755`

## What I looked at

`LibWeb`: `Element::is_focusable()` (tabindex + focusable-area rendering),
`EventHandler::handle_keyup` (goes through `fire_keyboard_event`, same path as keydown), and the
`Key_Tab` branch in `EventHandler` that consumes Tab for focus navigation.

## What was wrong

`keyup` was never dispatched. A page that pairs keydown with keyup saw only half of every keystroke.

## What shipped

`keyup` now dispatches after `keydown`, on the same chain: focused element, then document and window.

The first attempt logged **`keyup undefined`**: `dispatch_key()` sets the pending key, dispatches its
own keydown, then clears it — so the keyup that followed carried nothing. Both events are now
dispatched explicitly with the key set around them.

    --key j  ->  |   [js] MARK keydown j
                 |   [js] MARK keyup j

    full suite: 100% tests passed out of 59
    commit: fb956755

## What was attempted and reverted

Tab order, ported from `is_focusable()` and the `Key_Tab` branch:

- `is_focusable`: tabindex parses as an integer (exception-free parse — this build has exceptions
  disabled, which is also why upstream's `parse_integer` returns an `Optional`).
- `next_focusable`: document-order walk, wrapping.
- `FocusNext` action in the router; `--key tab` routed to the same path.

**It moved focus and did not visibly work**, and two observations remain unexplained:

| Observation | Expected | Measured |
| --- | --- | --- |
| `:focus-visible` after a Tab focus | magenta | blue — no match |
| Second `tabindex` div in the same fixture | rendered at y 100-200 | white, not painted |

`relayouts` incremented, so `set_focus` ran and the state changed. Something between that and the
pixel is wrong, and a fixture where one of the two elements does not render cannot tell me which.

Reverted rather than shipped: Tab still reaches the page, as it did before.

## What I deliberately did not do

- **Did not ship half-wired Tab.** It would stop Tab reaching pages that handle it, in exchange for a
  focus move that does not paint.
- **Did not claim the keyup fix proves the Tab path.** They share `set_focus` but not the trigger.
- **Did not chase the two observations** with the session's remaining budget. The next move is a
  fixture with a single tabindex element and a print of the computed style's background, not more
  guessing.
- **Did not touch the other three browser repositories.**

## Next

1. Re-attempt Tab with a one-element fixture; if `:focus-visible` still does not paint, compare the
   state the cascade sees against the state the window set — the same control experiment that found
   the `relayout()` bug.
2. Explain why a second `tabindex` div fails to render; it may be a layout bug independent of focus.
3. Scoped style invalidation, replacing the full rebuild and the DOM fingerprint.
4. Family P0 builds still need a machine with dev packages.
