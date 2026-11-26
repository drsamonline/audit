# Aetheris — white space is not an item, and it has no minimum

**Row:** `0.13`'s tail closed. **Date:** 2026-11-26.

The last session ended with `header.vector-header` as the worst overflow on a real page, **422.1px past**
its content box, and the account links still clipped. The next walk needed a number the probe did not
print.

## The probe could not say which number was wrong

`--overflow` gave the header's six children and their widths: two real `div`s and **four anonymous text
runs** at 28.8, 28.8, 38.4 and 19.2px, with six 20px gaps between them - 1,432.9px of items in a 901.3px
content box.

An item that overflows is either **bigger than its base size** or **floored above the space it was given**.
The probe printed only the max-content width, so it could not tell the two apart. `intrinsic_min_width()`
is now public and `tools/article-position.cpp` prints `max=` beside `min=`.

## What the pair said: `min == max`, almost everywhere

```
(anonymous) max=  28.83  min=  28.83  rect.w=  28.83  text
div         max= 439.61  min= 429.20  rect.w= 429.20
```

Two defects, both about white space:

1. **A run of white space was a flex item.** css-flexbox-1 §4: a contiguous sequence of child text runs
   becomes an anonymous item *unless the whole run is white space, in which case it is not rendered at
   all*. Upstream's predicate is `can_skip_is_anonymous_text_run` (`Rust/src/layout/layout_pass.rs:455`),
   used where flex items are generated (`flex_formatting_context.rs:1217`) and again for grid
   (`grid_formatting_context.rs:2180`). Four runs were items here, each with a width and a gap on each
   side: 195.2px belonging to nothing.
2. **Their minimum width was their measured width.** `min_content_width` split a text run on `' '` only,
   so `"\n\t\t\t"` - no space in it - was one unbreakable word measuring 28.83px. A box that renders
   nothing had a 9.61-28.83px floor, and every ancestor inherited it.

## The fixture, because a page cannot say "correct"

Two 50px boxes 10px apart in a 200px row:

| | chromium | engine before | engine after |
| --- | --- | --- | --- |
| first box x | 0 | **19.6** | **0** |
| second box x | 60 | **99.2** | **60** |

`reference-render.sh` scored that fixture **99.7% agreement both ways**. The geometry is the evidence; a
page-sized percentage cannot see a 20px error on a mostly-white page.

## Measured

| instrument | before | after |
| --- | --- | --- |
| overflow count | 141 | **137** |
| `header.vector-header` | worst offender, 422.1px past | **not an offender at all** |
| worst offender | `header.vector-header` | `header.mw-body-header` 252.5 - a different element, deeper in the page |
| pixel agreement | 81.1% | **81.2%** |
| header row | 1,432.9px of items in 901.3px | **932px in 928px** |
| suite | 67/67 | **67/67 twice** |

The account links paint and are legible where they were clipped. Two tests pin it, and **both were proved
to fail on the unfixed engine** by reverting the fix and watching them go red.

## The mistake worth recording

The second test's first version compared `"ab\tcd"` against `"ab"` and **passed on the unfixed engine** -
the tab is not measured either way, so it could not distinguish the bug from its absence. It was replaced,
not kept. An assertion that cannot fail is worse than none, because it looks like proof.

## Left, and named

| row | defect |
| --- | --- |
| 3l | `.vector-header-end` fills 602.7px but does not push its content to the right edge; the links sit at x=386 where chromium puts them at 800-990 |
| 3m | `max_content_width` still measures white space untransformed - a `"\n"` is 9.61px - so every base size carries its markup's indentation |
| 3n | a lone flex item is never shrunk to its automatic minimum: its base is capped at the line width, so free space is exactly zero |
