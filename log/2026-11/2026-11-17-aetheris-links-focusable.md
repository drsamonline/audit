# Aetheris — links and form controls are focusable, and a window/render disagreement

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `8ee71471`

## What I looked at

`LibWeb`: `HTMLAnchorElement.h:39` (`is_focusable` = `(Element::is_focusable() || has href) &&
meets_focusable_area_rendering_requirements()`), `HTMLInputElement.h:210` (its own override), and
`Element::is_focusable()` (a tabindex that parses).

## What shipped

`is_focusable`, by tag name, mirroring those clauses:

- a `tabindex` that parses as an integer — as before
- an `a` with an `href`
- `input`/`button`/`select`/`textarea` without `disabled`

The rendering requirement is **not** checked: this layer has no per-node computed style to ask, and the
code says so rather than pretending.

## Evidence

    two anchors, no tabindex, a{display:block;...}, a:focus-visible{background:#ff00ff}
    --key tab, 3 frames

    frame-1: first link (0,0,255)      <- before
    frame-2: first link (255,0,255)    <- :focus-visible painted
    frame-3: first link (255,0,255)

    full suite: 100% tests passed out of 59

## What testing it turned up

The frame showed the two links **side by side**, not stacked — `a{display:block}` was not applied in the
window. The same page through `--render` stacks them correctly:

    --render : (200,50) blue, (600,50) white, (200,150) blue     -> stacked
    --window : (200,50) blue, (600,50) blue                      -> side by side

And `div` is fine both ways: `div{display:inline}` goes side by side, `div{display:block}` stacks, in
`--render`. So the cascade and `LayoutTreeBuilder::display_for` are sound, and the difference is
specific to the window path.

This is **not** the claim retracted earlier today. That one said the user-agent sheet was missing and
every block element laid out inline; this one is narrower and reproducible: author `display` on an
anchor is honoured statically and ignored in the window. Recorded in `HANDOVER.md` with the numbers and
the next probe — print the CSS string `collect_page_style` hands the window and diff it against
`--render`'s — rather than guessed at.

## What I deliberately did not do

- **Did not fix the display discrepancy in this commit.** It is a separate fault in a separate path, and
  mixing it into a focus commit is how a bisect stops being useful.
- **Did not claim the rendering requirement is checked.** It is not; `visibility:hidden` and
  `display:none` elements are focusable here, which upstream would exclude.
- **Did not test `disabled` controls or `select`.** No form control renders yet, so the branch is
  compiled and unproven, as with `:focus-visible`'s text-entry clause.
- **Did not touch the other three browser repositories.**

## Next

1. The `collect_page_style` diff — the window/render `display` disagreement.
2. The rendering requirement for focusability, once computed style is reachable at that layer.
3. Scoped style invalidation from `invalidate_style_after_pseudo_class_state_change`.
4. Family P0 builds still need a machine with dev packages.
