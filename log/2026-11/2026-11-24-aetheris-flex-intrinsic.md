# Aetheris — flex items had no width at all

**Row:** `0.10`. **Date:** 2026-11-24.

The row said a flex item is sized to its container so `justify-content` overflows. The fixture it asked
for - one item, four `justify-content` values, asserting the **width** as well as the position - found
something worse: four rows painted their background and **no item appeared**. An item with no basis and
no width was laid out at **zero width**.

That limitation was already recorded, as a parenthetical in row 3c1: "`flex-basis: auto` with no width
starts at 0 - no intrinsic-width pass". It had been a footnote for two days.

The row's own case was the same defect the other way round: the real page's `h1` was given the
container's full width and pushed off the edge by `justify-content: flex-end`.

## Fix

`LayoutEngine::max_content_width()` - a text run's measured width, the widest of a block's children, or
the sum of a row of inline ones - now supplies the base size for an auto-basis item, capped at the row.

| fixture | before | after |
| --- | --- | --- |
| text item, auto width | 0px, invisible | **29px** |
| two 40px items, flex-start | 0-79 | 0-79 |
| one 40px item, flex-end | 260-299 | 260-299 |
| the real page's `h1` | x=1000, w=976 | **x=487, w=535** |

## Why the width assertion mattered

The `flex-end` item was in the right *place* before and after; only its width told the truth. Asserting
position alone would have passed while the bug was live - which is exactly how it survived.

## Still open

The `h1`'s right edge lands at 1022 in a container ending at 1000: a 22px overshoot, so the flex-end
arithmetic is not exact. Suite 67/67 twice, 128.19 s and 133.82 s, plus 128.98 s with the assertion.
