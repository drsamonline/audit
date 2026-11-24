# Aetheris — the account links are zero width

**Row:** `0.13` opened. **Date:** 2026-11-25.

With the header fixed, the next difference the reference shows is the account links: chromium puts
"Donate / Create account / Log in" at the top right; the engine puts nothing there.

Not a missing element — `tools/article-position.cpp` finds `p-vector-user-menu-overflow` in the layout
tree at x=766.5 y=8 w=54.1, with its flex `ul` beside it. The items fail:

| node | width | height |
| --- | --- | --- |
| `p-vector-user-menu-overflow` | 54.1 | 33.6 |
| `pt-sitesupport-2` (Donate) | **0.0** | 33.6 |
| its `<a>` | — | 16.8 |
| its `<span>` holding the word | — | **0.0** |

No rule sets a width (only `margin: 0.2em 0` and `margin: 0 4px` apply), so the zero comes from the flex
base size: `max_content_width()` returns 0 for these items.

## The fixture does not reproduce it

`<ul display:flex><li><a><span>Donate</span></a></li></ul>` gives the item **50.9px**, which is correct.
So the trigger is in this page's markup. Leading candidate: an anonymous box — the `<span>`'s text is a
child with no DOM node behind it, the same class of thing row 0.11 found, and `max_content_width()`
measures text only when the node has a DOM text node.

## Next

Expose `max_content_width()` to the probe (private static) or replicate it, and print what it returns at
each level of one item next to the text's measured width. That turns "0" into "0 because this box has no
DOM node", and the fix follows.

No engine source changed this turn beyond row 0.12's alt text, which is its own commit.

---

# Row 0.13 closed — the flex shrink had no floor

The row's next step was to expose the sizing and see what it returns, and that **falsified the
hypothesis**. I expected `max_content_width()` to return 0 (an anonymous box it could not measure):

```
li       intrinsic=  59.30  rect.w=   0.00
  a        intrinsic=  50.89  rect.w=   0.00
    span     intrinsic=  50.89  rect.w=   0.00
```

The base size was right. The item was **shrunk** to zero: the flex line had 54.1px and the items
totalled ~180. css-flexbox-1 floors an item's shrink at its automatic minimum size (`min-width: auto`,
min-content) and the engine had no floor.

`min_content_width()` now answers it - a text run's widest word, the widest of a block's children, or the
sum of a row of inline ones - and the shrink pass floors there.

| | before | after | chromium |
| --- | --- | --- | --- |
| menu item width | 0.0 | **43.3** | ~43 |
| "Donate" painted | no | yes | yes |
| pixel agreement | 76.6% | **81.1%** | — |

First fix today that moved agreement in the right direction — the double-line fix lowered it while
improving the layout; this one raised it.

## Left, one level up

Items no longer collapse but now **overflow** right: the outer container still allocates 54.1px. Next
question: what sizes that box.

Suite 67/67 twice, 122.64 s and 121.94 s, plus 122.37 s with the assertion.
