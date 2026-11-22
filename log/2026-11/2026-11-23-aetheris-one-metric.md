# Aetheris — one metric for layout and paint

Date: 2026-11-23 · Repo `drsamonline/The_Browser`
Commit: `15c0e11f`

Row 2h, written down on 2026-11-22 while bidi work was in progress and closed the next morning. Fragments
were being *placed* by one metric and *drawn* by another: layout summed code point advances, the pen
advanced by shaped glyph advances.

## What I looked at upstream

| Question | Where | What it said |
| --- | --- | --- |
| How does upstream measure a string for layout? | `Libraries/LibGfx/TextLayout.cpp:363` (`measure_text_width`) | it shapes the buffer, sums `x_advance` over the glyphs, and adds `glyph_count * letter_spacing` — the shaped width, spacing per cluster |
| Does their paint path use a different number? | `LibGfx/TextLayout.cpp:309` (`shape_text`) | no: the glyph run carries the same `width` the measurement produced, so the box and the ink come from one call |

So the fix is the one the upstream shape implies: measure by shaping, and add spacing per character.

## What was measured before the change

A probe comparing the old sum of per-code-point advances against `Font::measure()`, both at 16 px with the
engine's embedded font:

| text | sum of advances | shaped | delta |
| --- | --- | --- | --- |
| `"To"` | 19.5625 | 16.8594 | −2.7031 |
| `"AV"` | 21.8906 | 20.8906 | −1.0000 |
| `"office"` | 44.1406 | 43.9062 | −0.2344 |
| `"The quick brown fox jump"` | 207.8750 | 207.1406 | −0.7344 |
| `"ToToToTo"` at 40 px | 195.6250 | 168.4375 | −27.1875 |

Kerning, not ligatures: `"To"` has no ligature and loses 2.7 px. The old measurement applied no kerning at
all — the fallback in `Font::measure` did, which is why the two paths disagreed.

## What shipped

| Change | Why |
| --- | --- |
| `TextLayout::measure_text` returns `Font::measure(text)` plus letter-spacing per code point and word-spacing per word separator | one metric; the shaped width is what the pen advances by |
| two assertions in `AetherisShaping` | layout width equals the shaped width of a kerned pair, and is narrower than the two characters measured separately — so dropping kerning again fails the suite |

The no-font build keeps per-code-point advances on both sides, because both sides then take the bitmap
fallback. Nothing else moved: one function, one call site.

## Evidence

| Case | Result |
| --- | --- |
| `"To"` through `TextLayout::measure_text` vs `Font::measure` | equal within 0.01 px |
| `"To"` vs `measure_text("T") + measure_text("o")` | narrower by more than 0.5 px — the kerning is in the width |
| centred `"ToToToTo"`, 40 px, 400 px page, rendered | ink centre **199.0** against a page centre of 200 (the old box puts it at 186.4) |
| the suite, `ctest -j2` | 65/65 twice, 127.55 s and 126.95 s — the pixel tests did not move |

## What I got wrong

| First reading | What was true | What settled it |
| --- | --- | --- |
| "layout and paint already agree: every delta is 0.0000" | the probe set `AETHERIS_FONT` after the first `active_font()` call, so all four tables measured the bitmap fallback | one font per process; the deltas appeared |
| "the difference is the ligature" | kerning is the whole story; `"To"` has no ligature | the per-string table |

Third appearance of the `active_font()` trap in this repo. It is now in the probe's comment and in the
handover's build facts.
