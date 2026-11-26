# Aetheris — a grid written with the `grid-template` shorthand had no tracks

**Row:** `0.16` closed, `0.15` corrected. **Date:** 2026-11-26.

## The shorthand

`.mw-page-container-inner` sets its grid only through the `grid-template` **shorthand**. The engine did not read it,
so a container reporting `display=grid` had no tracks and no named areas and every child stacked in one column.

css-grid-1 §7.3: `grid-template` is a shorthand for `grid-template-rows`, `grid-template-columns` and
`grid-template-areas` — the row list, with any quoted area strings interleaved, before a `/`, the columns after.
Upstream states exactly those three longhands (`CSS/Properties.json:3282-3297`).

This engine has no shorthand-expansion layer — a shorthand is read where it is used, the way `resolve_edges`
splits `margin` — so `layout_grid_children` falls back to the shorthand for whichever longhand is absent, splitting
on the **top-level** `/` (never one inside `minmax(...)`), and `parse_tracks` now reads `minmax(a, b)`.

| fixture, two `grid-area` children | before | after |
| --- | --- | --- |
| `grid-template-columns: 100px 1fr` | x=0 w=100, x=100 w=924 | same |
| `grid-template: 1fr / 100px 1fr` | x=0 w=1024, x=1024 w=0 | x=0 w=100, x=100 w=924 |

Suite **67/67 twice** (130.72 s, 129.65 s), assertion proved to fail without the change.

**Agreement on the reference page: 88.8% before and after.** The rule that needs the shorthand is behind
`@media screen and (min-width:1120px)` and the reference render is 1024px wide, so this closes a compatibility gap
and does not move this page. That is why it is its own row.

## The premise that did not survive the render

Row 0.15 was opened saying the table of contents was wrongly laid out in the content flow. **It is not.** At 1024px
chromium stacks the Contents list above the title too — its heading at y=98, the engine's at y=186, same order —
because the grid that would put the TOC in a column is behind the same `min-width:1120px`.

The row's number was right and its explanation was wrong. `main#content` starts at **y=546.4** against chromium's
**356**, and the 190px is:

| | engine | chromium |
| --- | --- | --- |
| block above the Contents heading | header 156px tall, failed-logo block h=172.9 | ~68px |
| the Contents box | y=180.1 h=350.4 | y=98, h≈247 |

So +88px above and +103px in the box. Row 0.15 now says that, and names `class=vector-header-start` as the next
probe question.

## The lesson

A number with the wrong explanation attached is worse than an open row, because the explanation is what the next
person builds on. The reference render was already in the tree; comparing it cost nothing, and it took one crop to
disprove a story that had already been written into the plan.
