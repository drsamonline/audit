# Aetheris — a screenshot that was telling the truth, and a block placed at the inline cursor

**Rows:** `0.9` fixed, `0.10` opened. **Date:** 2026-11-24.

## The reading was wrong, not the page

After row 0.8 the page was styled but appeared to show its table of contents where the article should
be. `tools/article-position.cpp` - which prints landmark rects and walks the ancestor chain - said:

| node | where it is |
| --- | --- |
| `mw-content-text` (the article) | y=1578, height 41,297 |
| document | 1024 x **41,297** |
| `h1` | **x=1000**, width 976, on a 1024-wide page |

The article is not missing; the screenshot was the top of a 41,000-pixel page. The real defect was the
`h1`, entirely off the right edge.

## Fixed: block inside inline content

`<div><span>inline text</span><div></div></div>` placed the block on the text's line at the cursor.
`layout_inline_children` now starts a new line at the container's left edge. `AetherisAdvancedLayout`
pins the x and the y.

## Opened: flex items are sized to the container

The `h1` is inside `<header>` with `display: flex; justify-content: flex-end`. The engine honours the
rule *and* gives the item the container's full width, so `flex-end` puts its left edge at 1000 and its
right edge at 1976. A flex item with `flex-basis: auto` should size to its content. Row 0.10, with the
next step named: assert the **width** at all four `justify-content` values - asserting only the position
would have passed.

## The pattern

Three times today a true statement was read as a false one: "188 linked resources" (loaded, not
requested), "the page is unstyled" (its stylesheets were cached as images), and "it shows the contents
instead of the article" (the contents are at the top of a 41,000-pixel page). Each time the fix was to
ask the engine for a number rather than look harder at the picture.

Suite 67/67 twice, 172.79 s and 129.36 s, plus 127.74 s with the new assertion.
