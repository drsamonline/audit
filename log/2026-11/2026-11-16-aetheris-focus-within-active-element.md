# Aetheris — `:focus-within`, `activeElement`, and the event path that stopped at the root

Date: 2026-11-16 (nineteenth session) · Repo `drsamonline/The_Browser`
Commit: `4567af02`

Standing instruction from the owner: read the upstream sources first, because most of what we want to
build is already there. Three features this session, all ported rather than invented.

## What I looked at

Ladybird `Libraries/LibWeb`: `Element::should_indicate_focus()` (the `:focus-visible` heuristic),
`Document::active_element()` and `update_active_element()`, `FocusWithinChain` in
`CSS/SelectorMatching.cpp`, and the pseudo-class table's `ENUMERATE_ELEMENT_STATES`.

## What upstream does

| Feature | Upstream definition |
| --- | --- |
| `:focus-within` | membership in a `FocusWithinChain` built from the focused element — i.e. the focused node and its ancestors |
| `document.activeElement` | `m_active_element` if set, **else `body()`** |
| `:focus-visible` | `is_focused() && should_indicate_focus()`; that function returns true for text-entry controls, and otherwise follows whether the last focus came from a **key** or a **pointer** |
| Event bubbling | one path: target, ancestors, document, window |

## What was wrong in Aetheris

- Neither `:focus-within` nor `activeElement` existed.
- **`dispatch_bubbling` stops at the document element.** It walks `parent`, and the JS `document` and
  `window` objects are not `DomNode`s, so a handler registered on `document` never saw a click or a
  key. Keys were patched last session by calling `js.dispatch_event` afterwards; clicks had the same
  hole and nobody had noticed.

## What I changed

- **`:focus-within`** — walk up from `interaction_state->focused` and match if the element is on that
  chain, the same test `FocusWithinChain::contains` performs.
- **`document.activeElement`** — a host hook on `Interpreter`, answered from the window's interaction
  state, installed as a getter on the document object.
- **Clicks finish with `js.dispatch_event("click")`**, matching what keys already did, so the document
  and window hear the event.

## Evidence

    fixture: #outer > #inner, #outer:focus-within{background:#ff0000},
             document click handler logging document.activeElement.id

    --window <url> 2 /tmp/frames --click 50 50
      |   [js] MARK active inner
      | Window ... relayouts: 1
      outer (below inner): (255, 0, 0)      <- :focus-within matched the ancestor
      inner:               (0, 170, 0)      <- and the child kept its own colour

    full suite: 100% tests passed out of 59
    commit: 4567af02 on main

## What I deliberately did not do

- **Did not implement `:focus-visible`.** It needs two things Aetheris lacks: a focus trigger
  (pointer vs keyboard) on the state, and a notion of which elements take keyboard input. Upstream
  spells both out in `should_indicate_focus`; that function is the checklist for next time.
- **Did not copy upstream's `activeElement` fallback to `body`.** Aetheris returns null when nothing
  is focused. Correct for a page that checks, wrong for a page that assumes `activeElement` is always
  an element — worth doing when forms arrive.
- **Did not unify the two dispatch paths** into one that bubbles through document and window, as
  upstream has. Both now end with the same extra call; a single path would be better and is the
  obvious follow-up.
- **Did not touch the other three browser repositories.**

## Next

1. `:focus-visible` from `should_indicate_focus()`: add a pointer/keyboard focus trigger, and the
   text-entry check when form controls exist.
2. One event path that bubbles target -> ancestors -> document -> window, replacing the two-call
   pattern in `dispatch_bubbling` callers.
3. `keyup`, Tab order, `activeElement` falling back to `body`.
4. Scoped style invalidation (upstream's `invalidate_style_after_pseudo_class_state_change`).
5. Nodus `libcss` wiring — still the family's blocking item.

## The pattern, three sessions running

Every feature attempted by reasoning from the Aetheris tree alone has cost a session and often been
reverted. Every feature ported from `LibWeb` after reading it has landed first time, with a test that
proves it. The tree is derived from upstream; the reading is not optional.
