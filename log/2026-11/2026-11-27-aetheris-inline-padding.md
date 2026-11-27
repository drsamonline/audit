# Aetheris — an inline box's vertical padding does not make the line taller

**Row:** `0.18` closed. **Date:** 2026-11-27.

css2 §8.1 and §10.6.1: the vertical padding, border and margin of an **inline, non-replaced** box start at the top
and bottom of its content area and have nothing to do with the line-height. **Only the line-height is used when
calculating the height of the line box.** The padding paints; it does not advance the next line.

## The line

```cpp
max_bottom = std::max(max_bottom, child->rect.y + child->rect.height);   // the whole border box, padding included
```

A page's table of contents is `<a><div class="vector-toc-text" style="padding:6px 0">`. Every row came out
**28.8px** where a browser gives **16.8**, so the list was 1.7x too tall and pushed the article down.

The line now contributes `max(line_height, content height)` for an inline non-replaced child, and keeps the full
border box for an **inline-block or a replaced element**, which are atomic and do move the line.

## The fixture, measured both ways

Two block `<a>`, each holding a `<span style='padding: 6px 0'>`, `font-size: 14px; line-height: 1.2`:

| | unfixed | fixed | chromium |
| --- | --- | --- | --- |
| gap between the two blocks | **28.80** | **16.80** | 16.8 |
| block height | **57.60** | **33.60** | 33.6 |

With `layout.cpp` reverted to `main` and rebuilt, `AetherisAdvancedLayout` fails with exactly "an inline box's
vertical padding does not push the next line down". Restored, it passes. Suite **67/67 twice** (180.28 s,
152.45 s).

## It moved no page-level number, and that is the correct outcome

| | before | after |
| --- | --- | --- |
| pixel agreement | 84.3% | **84.1%** |
| engine text rows | 11, 44, 150, 179, 207, 236, 265, 293, 306, 323 | **identical** |
| overflow count | 139 | **139** |

This is the fourth row in five days that moved agreement the wrong way while the layout got closer — after 0.11
(90.3 -> 76.9), 0.15 (88.8 -> 84.3) and 3m (81.2 -> 80.4). The whole-page percentage is dominated by whichever
single defect is biggest, so it is read with the per-band table and the row positions or it is not read at all.

The honest reading of this row is that a compatibility fix is worth its commit even when the number does not move.
It makes the engine agree with a browser on a construct the page actually uses, and it removes a 1.7x error from
every padded inline box in the tree.

## A note on the baseline

The reference page is no longer byte-stable: `en.wikipedia.org/wiki/Web_browser` was **416,840 bytes** on
2026-11-26 and **421,819 bytes** on 2026-11-27, while its two stylesheets are byte-identical at 215,770. The
absolute agreement number therefore moved 0.2 points on its own. Only a pair measured on the same HTML in the same
session is comparable, and that is what the row's proof is.
