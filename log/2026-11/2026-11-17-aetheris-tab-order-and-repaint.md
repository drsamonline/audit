# Aetheris — Tab order, and the one line that hid `:focus-visible` for two sessions

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `3193327f`

## What I looked at

`LibWeb`: `Element::is_focusable()` (tabindex + focusable-area rendering), the `Key_Tab` branch in
`EventHandler`, and the document-order walk behind sequential focus navigation.

## What shipped

- **`is_focusable`**: a `tabindex` that parses as an integer. Exception-free parse — this build disables
  exceptions, which is also why upstream's `HTML::parse_integer` returns an `Optional`.
- **`next_focusable`**: document order, wrapping.
- **Tab** in the router becomes a `FocusNext` action; the focus it sets is keyboard-driven, so
  `:focus-visible` matches.
- **`need_render`** is set by the focus path itself.

## The bug that cost two sessions

> A focus change alters the cascade but not the DOM. The window only redrew when the document
> fingerprint moved.

So Tab relaid out the page with the correct focus state and then never drew it. `:focus-visible` was
"broken" twice while the state, the layout and the matcher were all correct.

## How it was finally found

Four probes, each eliminating a candidate:

| Probe | Result | Ruled out |
| --- | --- | --- |
| `--key tab` prints the node it focuses | a valid pointer | "the walk finds nothing" |
| one-element fixture, frame inspected | blue in every frame | "the wrong element is focused" |
| `--focus-key` (hit-test) vs `--key tab` (DOM walk) | both paint the same element when hit-testing | "the matcher is wrong" |
| **same process**: `dom-walk == hit-test`, `same=1` | identical pointers | "duplicate DOM trees" |

With the node identity proven and the matcher proven, only "nothing asks for a frame" was left. One
line.

## Evidence

    one-element fixture, #a:focus-visible{background:#ff00ff}, --key tab, 3 frames

    frame-1.ppm: pixel(200,84)=(0, 0, 255)
    frame-2.ppm: pixel(200,84)=(255, 0, 255)
    frame-3.ppm: pixel(200,84)=(255, 0, 255)

    full suite: 100% tests passed out of 59
    commit: 3193327f

## What this corrects

The previous entry retracted a wrong claim about layout. This one explains the failure that started
that investigation: it was never layout and never the cascade. The handover now carries gotcha 9 —
"a focus change does not change the DOM" — so the next state-driven feature sets its own `need_render`.

## What I deliberately did not do

- **Did not make every `set_focus` call set `need_render`.** Only the paths that own the frame loop
  should; a helper that repaints would hide the same bug elsewhere.
- **Did not add links and form controls as focusable.** Upstream gives them their own clauses
  (`HTMLAnchorElement` with href, form controls, editable hosts); Tab here sees `tabindex` only, and
  that limit is stated in the handover rather than discovered later.
- **Did not re-verify `:focus-within` and `activeElement` against the new Tab path.** They were proven
  with clicks; a Tab-focused child should also match `:focus-within` and is untested.
- **Did not touch the other three browser repositories.**

## Next

1. Links and form controls as focusable; `:focus-within`/`:focus-visible` for those kinds.
2. Scoped style invalidation from `invalidate_style_after_pseudo_class_state_change` — the same
   "repaint only what changed" concern, done properly.
3. A CTest for Tab order and for `:focus-visible`, which currently exist only as session scripts.
4. Family P0 builds still need a machine with dev packages.
