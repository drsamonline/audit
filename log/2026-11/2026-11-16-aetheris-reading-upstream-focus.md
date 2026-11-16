# Aetheris — reading Ladybird ended a three-session loop

Date: 2026-11-16 (eighteenth session) · Repo `drsamonline/The_Browser`
Commits: `2ade6788` (relayout keeps state), `36ae19b9` (focus model)

Told to read the upstream sources instead of looping. That was the right instruction: the two
sessions spent on `:focus` were spent re-deriving a design that `Libraries/LibWeb` already states in
a few hundred lines.

## What I looked at

Ladybird `Libraries/LibWeb` (sparse clone, 62 MB): `DOM/Document.h` and `Document.cpp`
(`set_hovered_node`, `set_focused_area`, `active_element`), `DOM/Element.cpp`
(`is_focused`, `is_the_active_element`, `is_being_activated`), `CSS/SelectorMatching.cpp` (the
pseudo-class table), and the invalidation entry points.

## What upstream does, and where Aetheris differed

| Concern | Ladybird | Aetheris before today |
| --- | --- | --- |
| Where state lives | on the `Document`: `m_hovered_node`, `m_focused_area`, `m_active_element` | on a `VisualInteractionState` passed into the style engine |
| How a pseudo-class is answered | `element.is_focused()` → `document().focused_area() == this` | the style engine compares the passed pointer |
| What happens on a focus change | `blur` on the old element → **scoped** invalidation of `:focus`/`:focus-within`/`:focus-visible` → set the pointer → `focus` on the new element → repaint | set the pointer, rebuild the whole layout |
| What happens on a relayout | invalidation marks survive; only dirty subtrees re-resolve | `relayout()` rebuilt with **no** interaction state, discarding `:hover`/`:focus` |
| Key dispatch | to the focused element, bubbling to the document | to the document always |

The third row is the whole bug. Two sessions looked for a fault in the focus *wiring*; the fault was
that `RenderDocument::relayout()` threw the state away, so anything that focused and then relaid out
lost the focus. `dispatch_click_at` does exactly that sequence.

## What I changed

- **`relayout()` keeps the state** (`2ade6788`): `RenderDocument` remembers what
  `apply_visual_state()` was given and passes it back in. This is the minimal version of upstream's
  invalidation: Aetheris still re-resolves everything, but it no longer loses the state.
- **`set_focus` follows `Document::set_focused_area`** (`36ae19b9`): `blur` on the old element,
  re-resolve, set, `focus` on the new element.
- **Keys go to the focused element and bubble to the document**, as `EventHandler` does.
- **Command-line order fixed**: `--click` (which focuses) now runs before `--key`, because a key must
  reach what the click focused. The previous order made the CLI unable to test focus at all.

## Evidence

    fixture: #a:focus{background:#ff00ff}, focus/blur/keydown listeners

    |   [js] MARK focus a
    |   [js] MARK focused key j
    |   [js] MARK doc key j
    | Window ... relayouts: 1
    div a: (255, 0, 255)

    full suite: 100% tests passed out of 59
    commits: 2ade6788, 36ae19b9 on main

## What I deliberately did not do

- **Did not port upstream's scoped invalidation.** `CSS::Invalidation::invalidate_style_after_pseudo_class_state_change`
  re-resolves only elements whose style depends on the pseudo-class; Aetheris still rebuilds the
  whole layout on any state change. Correct, but it is why a pointer move costs a full layout. That is
  the next real optimisation and it should be modelled on that function.
- **Did not add `:focus-visible`, `:focus-within`, `document.activeElement` or Tab order.** All four
  exist upstream and none exists here; each is now a named gap in `HANDOVER.md` rather than a guess.
- **Did not replace the DOM fingerprint** used for timer-driven repaints. Upstream marks nodes dirty
  at the point of mutation (`invalidate_style`), which is exact and O(1); the fingerprint is O(n) per
  frame and heuristic. Same lesson, not yet applied.
- **Did not touch the other three browser repositories.**

## Next

1. `document.activeElement` and `:focus-visible` — small, and they make forms behave.
2. Scoped style invalidation modelled on `invalidate_style_after_pseudo_class_state_change`,
   replacing both the full rebuild on state change and the fingerprint on mutation.
3. `keyup`, `:focus-within`, Tab order.
4. Scrollbar thumb dragging with pointer capture.
5. Nodus `libcss` wiring — still the family's blocking item.

## The lesson

Three sessions of Aetheris work — the page-load duplication, the click path, and `:focus` — were all
cases of re-deriving what `LibWeb` already documents. Reading upstream first is cheaper than
debugging by print, and this repo is derived from it, so the answers are a `git clone` away.
