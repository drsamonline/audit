# Aetheris — the window lays block elements out inline

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `26e4f145` (documentation only — no code changed)

Chasing why Tab focus did not paint turned up something larger: **the window path renders pages with
the author stylesheet but without the user-agent stylesheet**, so every block element is laid out
inline. `--render` is correct; `--window` is not.

## What I looked at

`RenderDocument::create_from_document` (which prepends `user_agent_stylesheet()` to the author CSS),
`create_scripted_document`, and both callers' arguments in `src/main.cpp`.

## The experiments, in order

| # | Fixture | `--render` | `--window` |
| --- | --- | --- | --- |
| 1 | two `div`s, `div{width:400px;height:100px;background:#00f}` | stacked, y50 and y150 blue | **one row**: blue spans x 0-800 at y 60, nothing at y 150 |
| 2 | same, with `tabindex="0"` on both | stacked | same one-row result |
| 3 | same, plus `div:focus-visible{...}` | stacked | same |
| 4 | same, with `display:block` added to the author rule | stacked | **stacked** |

Experiment 4 is the one that matters: the only change is an explicit `display:block`, and the window
becomes correct. So the author sheet applies (the blue background comes from it) and the UA default
does not.

A horizontal scan confirmed the reading rather than assuming it:

    y=60 : x10 blue, x100 blue, x300 blue, x420 blue, x600 blue, x900 white
    y=150: all white

Two 400px boxes side by side, no height — inline boxes with a background, exactly what a `div`
without a UA `display:block` produces.

## Why this matters beyond the layout

It explains a day of confusion. Hover, `:active`, `:focus` and click dispatch were all verified with
coordinates computed on the assumption that the page was laid out as blocks. On any page whose layout
was inline, the point that hit the intended element was a coincidence — and the Tab attempt's
`:focus-visible` failure is very likely this, not a focus bug.

## What I did not find

`create_from_document` demonstrably prepends the UA sheet, and both callers pass the same
`viewport_width` and the same `css` string. So the sheet is being lost somewhere between that call and
the first frame — or the window's page is re-laid out by something that rebuilds with a different
sheet. That is the next probe, and it is a print, not a guess:

1. Print the parsed rule count of `m_stylesheet` in the window's first frame, and the same in
   `--render`. If they differ, find what re-parses.
2. If they match, print the resolved `display` of `#a` from both paths.

## What I deliberately did not do

- **Did not guess a fix.** Every plausible cause here (missing UA sheet, a second parse, `relayout()`
  with a different sheet) is one print away, and the last three sessions' lesson is that guessing costs
  more than measuring.
- **Did not change code.** Documentation only; the tree is at `fb956755` plus a handover row.
- **Did not re-attempt Tab.** It would be measuring the same broken surface.
- **Did not touch the other three browser repositories.**

## Next

1. The two prints above; then fix the sheet on the window path.
2. Re-attempt Tab order afterwards — the `:focus-visible` failure is probably downstream of this.
3. Scoped style invalidation from `invalidate_style_after_pseudo_class_state_change`.
4. Family P0 builds still need a machine with dev packages.
