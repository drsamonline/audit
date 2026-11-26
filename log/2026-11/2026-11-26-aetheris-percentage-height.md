# Aetheris — a percentage height is not a percentage of the width

**Row:** `0.15` closed, `0.17` opened. **Date:** 2026-11-26.

The row said the block above the table of contents was 156px tall against chromium's ~68, with the failed-logo block
at h=172.9. The probe on `class=mw-logo` put the link itself at **h=140** while its content was 38px — and 140 is
exactly its **width**.

## The line

```cpp
parse_length(style.get("height"), -1, content_width)   // the percentage base for a HEIGHT was the WIDTH
```

css2 §10.5 (and css-flexbox-1 §9.8 for a flex item): a percentage height resolves against the containing block's
**height**, and against an indefinite one it computes to `auto`. This engine has no definite containing-block height
to resolve against, so `parse_height()` returns the fallback for any percentage — honest, where 100% of the width
was merely wrong.

## Four elements of fixture reproduce it

A 38px span inside `<a style='display:flex;height:100%'>` in an auto-height flex row made the row **100px** tall,
which is 100% of the span's 100px width. It is 38px now.

| | before | after |
| --- | --- | --- |
| fixture row height | 100 | **38** |
| `main#content` y | 546.4 | **473.6** (chromium 356) |
| engine text rows vs chromium | 88px below | **15px below** |
| pixel agreement | 88.8% | **84.3%** |

## The percentage went the wrong way and the layout got better

Moving everything up 73px pulled the *next* defect into the viewport: the engine's article **ends** around y=640
where chromium still has paragraphs, so the footer lands on screen. Bands y 640-704 and 704-768 score 65.9% and
39.0% against 94-98% elsewhere. That is row **0.17**, opened with those numbers.

This is the third time in two days that the whole-page percentage and the row positions disagreed. The row positions
were right every time.

## The premise, corrected twice

Row 0.15 was opened saying the table of contents belonged in a column. At 1024px chromium stacks it above the title
too — the grid that would put it in a column is behind `min-width:1120px`. So the row's number was right and its
explanation was wrong, and the explanation is what got fixed first. Both times the *why* had to be measured before
anything could be changed, and both times the measurement was one probe run away.
