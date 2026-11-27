# Aetheris — floats leave the flow, and content flows beside them

**Row:** `0.20` closed. **Date:** 2026-11-27.

## The bug

`figure.mw-halign-right` laid out **953.6px wide on a 976px content column**, at **x=46.4**, covering the article and
pushing the lead paragraph below it. `float` was never read by layout at all: `COVERAGE.md` listed it as absent, and the
figure took the whole column as an ordinary block. Chromium floats it at ~255 wide with the text flowing beside it.

The cost was visible in the bands and not in the cause: band 576-640 fell **87.1% → 27.7%** once row 0.17's 150px shift
pulled the figure into the viewport. That was the single largest difference on the page, and it was a missing property
rather than a mis-measured one.

## The fix

css2 §9.5: a floated box is **taken out of the normal flow**, shifted to the left or right edge of the line box, and the
content that follows **flows beside it** rather than below.

In `src/rendering/layout.cpp`:

- `struct FloatBox { float top, bottom, left, right; }` and `static void float_intrusion(...)`, placed just above
  `LayoutEngine::layout_inline_children`. A `FloatBox` is a placed float's **margin box**; `float_intrusion` reports,
  for every box overlapping `[y, y + height)`, how far it insets the line from whichever container edge it touches.
- `layout_inline_children` keeps a `std::vector<FloatBox> floats` and a `float const content_right = x + available_width`
  before the child loop. A child whose `float` is `left`/`right`/`inline-start`/`inline-end` is laid out at
  `min(max_content_width, available_width)`, re-laid at `content_right - outer` when floated right, its margin box
  pushed into `floats`, and the loop `continue`s **without advancing the flow**.
- Both the block-level child path and the text-run path call `float_intrusion(...)` and start beside the float:
  `x + block_left` with width `available_width - block_left - block_right`; for text, `cursor_x` is raised to
  `x + run_left` and the run limit becomes `content_right - run_right`.
- `layout_node` scans its children for a float into `has_float` and dispatches
  `else if (has_inline || has_float) layout_inline_children(...)`. Without this the mechanism is dead on exactly the
  containers that need it: a block container holding only blocks plus one float would take the plain block-stack path
  and place the float as an ordinary block.

**The branch had never been compiled before this session.** The build is the first thing that could fail, and it did
not: **68/68** binaries current under `-Werror`, no warnings-as-errors.

## Before and after

| | before | after |
| --- | --- | --- |
| pixel agreement | 84.1% | **84.8%** |
| `figure.mw-halign-right` | x=46.4 w=**953.6** h=175.4 | x=**772.4** w=**227.6** h=**179.6**, right edge **1000.0** |
| band 576-640 | 27.7% | **80.4%** |
| band 704-768 | 49.3% | **82.2%** |
| worst band | 576-640 at 27.7% | 640-704 at **50.5%** |

Agreement is 41672/49152 exact-match samples, every 4px over 1024x768. The figure's right edge sits on **1000.0**,
which is chromium's own edge; chromium's width is near 255 against the engine's 227.6. A second `mw-halign-right`
figure is floated to the same 1000.0 edge at **x=756.8 y=4897.2 w=243.2 h=145.8**.

Per-band agreement, 64px bands over y 0..768, 4096 samples each:

| band | agree | band | agree |
| --- | --- | --- | --- |
| 0-64 | 88.7% | 384-448 | 92.3% |
| 64-128 | 97.4% | 448-512 | 82.5% |
| 128-192 | 92.6% | 512-576 | 77.8% |
| 192-256 | 98.0% | 576-640 | **80.4%** |
| 256-320 | 94.7% | 640-704 | **50.5%** |
| 320-384 | 80.3% | 704-768 | 82.2% |

Engine `text rows at [11, 44, 150, 179, 207, 236, 265, 293, 306, 325]`.

This is the first fix on this page that moved the whole-page percentage the **right** way — after 0.11 (90.3 → 76.9),
0.15 (88.8 → 84.3), 3m (81.2 → 80.4), 0.18 (84.3 → 84.1) and 0.17 (84.1 → 77.6), each of which traded the number for a
better layout. 0.20 pays one of those debts back: **77.6% → 84.8%** against the pre-0.17 best of 84.1%.

## Verification

| check | result |
| --- | --- |
| `tools/check-build.py` | all **68** binaries current |
| `TestAetherisAdvancedLayout` | exit **0** |
| `TestAetherisCss` | exit **0** |
| `ctest --test-dir build -j 2` (pass 1) | **100% out of 67**, 128.93 s |
| `ctest --test-dir build -j 2` (pass 2) | **100% out of 67**, 130.53 s |

The two passes are the same work twice — `WindowGeometry` alone is 128.91 s and 130.49 s of them. The float assertions
were already proved to fail when float placement is disabled, in the previous session; that was not re-proved here.

## The three gaps, stated plainly

1. **`clear` is not implemented.** Nothing reads `clear: left | right | both`; a box that should be pushed below a float
   is placed beside it instead.
2. **Floats do not stack.** `float_intrusion` takes an inset from a box only when it touches the container's left or
   right edge, and every float is placed at the current `cursor_y` against that edge. Two floats on one line both claim
   the full band, and a second float does not drop below the first.
3. **Intrusion is per-block, not per-line.** The inset is computed once when the block or text run begins and applies to
   all of it, so a `<p>` that starts beside a float has **every** line shortened — including the lines below where the
   float has already ended. css2 §9.5 asks for the inset to be recomputed per line box.

The worst band, 640-704 at **50.5%**, is most likely these three rather than anything this row left half-done. That is
the next measurement, not a claim.
