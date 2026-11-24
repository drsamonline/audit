# Aetheris — 22 pixels, bounded, and deliberately left

**Row:** `0.10`'s tail. **Date:** 2026-11-25.

The real page's `h1` sits at x=487 with width 534.84 in a container ending at 1000, so its right edge
lands at 1021.84 — a 21.84px overshoot.

What this session added is a bound, not a fix:

- It is **not** padding or border. Those were fixed on 2026-11-24 and the fixture proves it:
  `padding: 0 10px` at `flex-end` went from 260-319 to 240-299.
- The flex free space comes from a base of **513**; the placed box ends **534.84** wide. The difference
  is exactly the overshoot.
- `tools/article-position.cpp` now prints text-fragment counts: the `h1` has **0 fragments of its own**,
  so its text is in a child, and `max_content_width()` (which measures text) is not the same number the
  child's layout produces.

Next question: which of the two measurements is wrong. The way to answer it is a fixture with one text
item in a flex row comparing `rect.width` against `measure_text` of the same string.

## Why it was stopped

Three attempts, 22 pixels, one heading. The engine's real gap is not this: it is that no one can say
whether a render *matches* anything, because there is no reference to compare against. Every defect
found this week came from a number contradicting an expectation, and those numbers are running out of
expectations to contradict. A reference render is the next instrument worth building.
