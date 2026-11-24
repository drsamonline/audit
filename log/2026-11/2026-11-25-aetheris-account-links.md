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
