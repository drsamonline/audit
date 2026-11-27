# Aetheris — a `calc()` media query, and the space it loses

**Rows:** `0.17` and `0.19` closed, `0.20` opened. **Date:** 2026-11-27.

Two fixes in one batch, because either alone makes the render worse: the media query exposes a dropped space, and the
space fix has nothing to fix until the query matches.

## Row 0.17 — a query that was silently false

```cpp
auto px = value.find("px");
if (px != std::string::npos) value = value.substr(0, px);   // "calc(1120px - 1px)" -> "calc(1120"
```

`strtof` failed on `"calc(1120"`, the query returned false, and **29 rules never applied — with nothing anywhere to
say so.** The feature's close paren was also `rfind(')')`, the last one in the string, which on a `calc()` value is the
wrong one.

**The measurement that matters is the scope**, and it was taken without a compiler: both evaluators were ported to
Python and run over the real 215,770-byte stylesheet.

| | |
| --- | --- |
| `@media` blocks | 76 |
| distinct preludes | 17 |
| blocks that change state | **13** |
| rules inside them | **29** |
| of which `calc()` preludes | **13 of 13** |

63 of 76 evaluate identically before and after. That is what makes the fix narrow, and it is the number the row had
never had — the row had carried three wrong explanations before this one.

One finding was new: `min-width: calc(640px - 1px)` = 639 **matches at 1024**. So this was never only a cap on the
table of contents; a block of "desktop-and-up" rules had never applied either.

## Row 0.19 — the space at a text run's edge

`TextLayout::layout` emits a space only between two words of its own run (`text_layout.cpp:116` discards it, `:137`
puts it back). A run that starts or ends in a space loses it, and the next inline box is placed flush against the last
word: `"often abbreviated as"` + `<a>browser</a>` read **"asbrowser"**.

It is symmetric — **424** boundaries of whitespace before an inline start tag, **316** after an inline close tag. A
trailing-only fix leaves 316 wrong.

## Both assertions were proved to fail, separately

| assertion | how it was proved |
| --- | --- |
| trailing space | whole fix reverted → `"the space before a link occupies width, so 'a b' is not 'ab'"` |
| leading space | only the leading advance disabled → `"the space after a link occupies width too"` |

The second one matters because it sits *behind* the first: with the fix reverted it is never reached, so it had not
been shown to fail at all. A test behind another failing assertion is not evidence.

## The page

| | before | after |
| --- | --- | --- |
| pixel agreement | 84.1% | **77.6%** |
| overflow count | 139 | **148** |
| `"often abbreviated as"` y | **900.0** (off screen) | **749.6** (on screen) |
| site subtitle y | 669.9 | **519.4** |

The article moves up **150.4px** and real article text enters the first screen. That is row 0.17's stated goal,
measured rather than inferred — and it is the part the whole-page percentage cannot see.

The percentage fell because the shift pulls a `figure.mw-default-size mw-halign-right` into the viewport at
**x=46.4 w=953.6 h=175.4**, where chromium floats it at ~255 wide with the text flowing beside it. `float` is absent,
so the figure takes the whole content column: band 576-640 falls **87.1% → 27.7%**.

That is row **0.20**. It is the fifth time a fix has moved the whole-page percentage the wrong way while the layout
got closer — after 0.11 (90.3 → 76.9), 0.15 (88.8 → 84.3), 3m (81.2 → 80.4) and 0.18 (84.3 → 84.1).

## And a documentation defect the batch found

Row 0.18's checklist row was never a row. The previous batch's insertion matched an anchor whose preceding line did
not end in a newline, so the row was concatenated onto row 0.17's line — `... line box || 0.18 | ...`. The table still
rendered, the commit message claimed the tick, and `grep 0.18` found it.

The check that would have caught it is one line: every table row must start with `|` and contain exactly five pipes.
It is in the commit, and the tier-0 table now validates at 22 rows of four columns each.

**The lesson is the one this project keeps relearning: check the artefact, not the intention.**
