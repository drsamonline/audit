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

---

# An experiment that was reverted

The menu items overflowed because the container allocated 54.1px. The container is `.vector-user-links`,
`display: flex` - and the engine measured a flex row as its **widest child** instead of the **sum**.

Summing is what css-flexbox-1 says, and it worked:

| | before | with the row-sum |
| --- | --- | --- |
| container intrinsic | 54.1 | **423.23** |
| container actual | 54.1 | **389.55** |

The box was right and the page looked **worse**: links pushed further off the right edge ("Don" where
"Donate" had been), agreement unmoved at 81.1%.

Reverted. The parent still places the child at x=766 using the size it had *before* layout; giving the
child its correct width without fixing that placement just moves the overflow. A spec-correct change that
makes the page worse is not a fix - this engine has now had two (the `reserve(24)` that measured slower,
and this).

## Next

In `layout_flex_children`, place each item from the width it ends up with rather than its base size.

No engine source changed: the tree is at HEAD and check-build is clean.

---

# Three variants, three regressions, and a stop

I proposed going after the pattern - a box sized or placed from a value computed before the thing it
depends on was known - rather than the symptom. The attempt was worth making; it failed; the record
matters more than the result.

## Tried

1. **The row-sum** - a flex row's intrinsic width is the sum of its items, not the widest. Correct per
   css-flexbox-1, and it worked: 54.1px → **423.23 intrinsic / 389.55 actual**. The page looked
   **worse**.
2. **`translate_subtree` + re-placement** - a new helper so a flex container can move an item after its
   layout reveals its width. The container went from x=766 to **x=919.1, w=389.6** - right edge **1308
   on a 1024px page**. Worse again.
3. **Both together** - worse still: only a fragment of "D" visible.

All reverted. Pixel agreement never left 81.0-81.1% for any of them - its own signal that none of these
touched what is actually wrong.

## What the measurement says

The box is sized correctly and positioned wrongly, and the position is decided **above** it: the parent
places it using the width it had before layout, and my re-placement did not reach that level. The defect
is in the header chain, not the menu.

## Why stop here

Four sessions have produced one reliable rule: the defect is one layer below where the symptom appears.
This time I guessed the layer and was wrong twice. The instrument that settles it - the ancestor walk -
already exists; pointing it at the right node is deliberate work, not a patch.

Suite 67/67 on the reverted tree, 128.05 s. Tree green, `check-build` clean.

---

# The mechanism, measured at last

The previous entry stopped with "walk the ancestor chain before touching code". This one did it.

## The chain, from the menu container upward

| node | x | width | ends at | parent's right edge |
| --- | --- | --- | --- | --- |
| `nav` (`justify-content: flex-end`) | 678.7 | 192.2 | 870.9 | — |
| its child | **697.9** | 192.2 | 890.1 | 870.9 — **19px past** |
| `p-vector-user-menu-overflow` | **861.2** | 117.7 | 978.9 | 890.1 — **89px past** |

Every level overflows by the gap between the size the parent handed its child and the size the child
ended up with, and the overflow accumulates.

## The fourth variant, measured not eyeballed

Re-placement alone (`translate_subtree` + repositioning from real widths) moved the menu
**861.2 → 884.2** - 23px further right. Earlier variants were judged from a crop; this one from a number,
and the number said no. All four reverted; agreement never left 81.0-81.1%.

## What it rules out

The fix is not in how one flex container places its own items. Each container places correctly given the
size its parent handed it; the parent hands it a stale size. A re-placement pass inside one container
cannot fix that - which is why all four attempts failed the same way.

## What it means

A restructure: a container can place its children only once its own width is final - two-pass layout
(measure top-down, place bottom-up) or a parent re-placing after its children settle. Not a patch.

Tree green at HEAD: 67/67 (128.05 s), check-build clean.

---

# An instrument for the restructure, and a variant rejected by it

The previous entry ended with "the work is a restructure, not a patch". A restructure needs a number, so
this one built the number first.

## `--overflow`

`tools/article-position.cpp --overflow` counts containers whose children reach past their own content
box, worst first. **Baseline: 165 containers** on `en.wikipedia.org/wiki/Web_browser`.

| container | children past its content box |
| --- | --- |
| `header.mw-body-header` | **347.7px** |
| `div.vector-header-start` | **321.2px** (in a 188px box) |
| `div#p-lang-btn` | 232.0px |
| `div#right-navigation` | 218.8px |

The header is where the page breaks; the account menu is a symptom of it, not the cause. First time this
has been a number rather than an inference from a screenshot.

## The fifth variant, rejected by the number

Re-placement (`translate_subtree` + repositioning a flex line from the widths its items actually got) was
tried again and judged by the count: **165 → 164**. Noise. Reverted.

The rejection cost one measurement instead of a session of squinting at pixels — the earlier two were
rejected by eye and by x-coordinate.

## What this leaves

A bounded, measurable job: a container can place its children only once its own width is final, so
layout needs a measure pass and a place pass. **165 is the number to bring down.** Whoever picks it up
has a baseline, the worst offenders, and four documented dead ends.

Tree green: 67/67 (130.55 s), check-build clean.

---

# Upstream says the engine is already right, so the metric must be wrong

The instruction was to check upstream first. The reference tree was re-cloned (it does not survive a pod
recycle) and read.

## What upstream does

`Libraries/LibWeb/Rust/src/layout/flex_formatting_context.rs`:

- **:4299** — hypothetical main size = `clamp(flex_base_size, clamp_min, clamp_max)`, `clamp_min`
  defaulting to `automatic_minimum_size_for_clamping` (the automatic minimum size).
- **:4318** — `resolve_flexible_lengths()` runs in `run()` **before** any placement, so every item's used
  main size is fixed before the line is positioned.
- **:4304** — `run()`: prepare items, collect lines, resolve flexible lengths, cross sizes, place.

The engine already has both halves — `min_content_width()` is the automatic minimum (row 0.13), and the
flex pass computes widths before placing. The port found nothing to port, which was the answer.

## Enforcing the second half changed nothing

Adding the resolved-size discipline (the item keeps the size the algorithm resolved; content overflows
inside the box) moved the count by **zero: 164 → 164**. Reverted.

## The finding: the metric counts design as defect

| container | x | note |
| --- | --- | --- |
| `div#p-lang-btn` | **1069.9** | beyond a 1024px viewport |
| `span#mwBEg` | **1009.4** | beyond a 1024px viewport |

Hidden menus and off-canvas UI, positioned outside the viewport on purpose — correct CSS, not overflow.
The counter treated "child reaches past its parent" as a defect without asking whether the child was
meant to be there. Six variants failed against it because it could not tell a bug from a design.

## Next

Make `--overflow` ignore children whose box lies wholly outside the document's viewport, then
re-baseline. The real number is lower, and what remains is worth chasing.

Tree green: 67/67, check-build clean, tree at HEAD.

---

# Fix the instrument, then a real defect falls out of it

## The instrument

`--overflow` now ignores children whose box lies **wholly outside the viewport** — hidden menus and
off-canvas UI are placed there on purpose, which is correct CSS, not overflow. Corrected baseline:
**164 → 150**.

## Upstream had answered the layout question

`Rust/src/layout/flex_formatting_context.rs:4318` resolves every item's used main size before placement;
`:4299` clamps the hypothetical main size at the automatic minimum. The engine already did both, so
there was nothing to port — which is why six variants moved nothing.

## The first real offender

`div.vector-header-start` is 188px wide with children **321px** past. Cause: **an `<img>` contributed no
width at all** to the intrinsic sizing — no children, no `width` style — so a link wrapping a 140px logo
was measured as if it held nothing.

Upstream takes a replaced element's contribution from its natural size (`replaced_sizing.rs:85-100`); the
engine now uses the `width` attribute or the loaded image's width, for max- and min-content both.

| | before | after |
| --- | --- | --- |
| overflow count | 150 | **147** |
| pixel agreement | 81.1% | 81.1% |

`AetherisAdvancedLayout` pins it. Suite 67/67 twice, 128.20 s and 127.81 s.

## Left

`div.vector-header-start` still the worst at 321px — the logo's container is the next walk.

---

# Two elements with the same class, and a probe bug of my own

Chasing `div.vector-header-start`, the worst offender at 321px. Three things came out; none was the fix
I expected.

## A probe bug: an empty tag matched the document root

`find_layout` returned the first node whose `dom_node->name == tag`; with `tag` empty that matched the
synthetic root, whose name is also empty — so `class=...` searches silently reported the root. One line:
`!tag.empty()`.

## The probe finds elements by class and prints widths now

Without widths, "which child is 321px past" was unanswerable.

## The namesake

The walk says this instance overflows by **54.7px**, not 321.2:

| child | x | width | right edge |
| --- | --- | --- | --- |
| anonymous inline | 88.0 | 38.4 | 126.4 |
| `nav` | 146.5 | 116.2 | 262.7 |
| anonymous inline | **282.7** | 48.0 | **330.7** |

Content box ends at 276. Wikipedia ships **two** elements with that class (normal and sticky header); the
scan reports the worst across both. A class name is not an identity.

## Next

`--overflow` should print an element's position and its parent's, so the worst offender can be told from
its namesake. Third time in this row that the instrument, not the layout, was what was wrong.

Tree green: 67/67, check-build clean.
