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

---

# Second row, same session — 2e3: `text-align: start`/`end` follow `direction`

Commit: `3f00eaaa`

## What I looked at upstream

| Question | Where | What it said |
| --- | --- | --- |
| What do `start` and `end` mean? | `Libraries/LibWeb/HTML/Canvas/Canvas2DContextBase.cpp:445-470` | "In RTL, `start` means right-aligned"; "In RTL, `end` means left-aligned"; "Explicit `left` and `right` alignments ignore direction"; `center` is the same either way |
| What is the initial value? | `Libraries/LibWeb/CSS/ComputedValues.h:447` | `TextAlign::Start` — so an unset `text-align` is `start`, not `left` |

## What shipped

| Change | Why |
| --- | --- |
| `TextLayout::layout` resolves alignment against `direction` | `start`/`end` were being treated as `left`/`right`, so an RTL block stayed left-aligned |
| eight assertions on exact fragment positions | the bitmap fallback makes them exact: 10 px per character at 16 px |

## Evidence

| text-align | direction | fragment x, "abc" in a 200 px line |
| --- | --- | --- |
| unset | ltr | 0 |
| unset | rtl | 170 |
| `start` | rtl | 170 |
| `end` | rtl | 0 |
| `end` | ltr | 170 |
| `left` | rtl | 0 |
| `right` | ltr | 170 |
| `center` | rtl | 85 |

Rendered: the `direction: rtl` paragraphs of the bidi fixture moved from the left margin to the right one;
the LTR paragraphs did not move. Suite 65/65 twice, 131.36 s and 126.43 s.

## What is left

`text-align: justify` is treated as `start`. It is the only part of the property not implemented.

---

# Third row, same session — 2f: line breaking by cluster

Commit: `5a8a5d7a`

## What I looked at upstream

| Question | Where | What it said |
| --- | --- | --- |
| How does upstream find break opportunities? | `Libraries/LibWeb/Rust/src/layout/text_chunker.rs` | an ICU `LineSegmenter` (UAX#14) and a `GraphemeSegmenter` (UAX#29), both held by the chunker; `can_break_after` is per chunk |
| How is a chunk's text type decided? | `text_chunker.rs:238-245` | `unidirectional_ltr` short-circuits to LTR, otherwise a per-code-point FFI call into `TextNode::text_type_for_code_point` |
| Is `HB_GLYPH_FLAG_UNSAFE_TO_BREAK` used anywhere in the tree? | grep over `Libraries` and `Rust` | no — it exists only in HarfBuzz itself. It is what this engine uses, because neither segmenter is available without ICU |

## What was measured before writing it

`hb_glyph_info_get_glyph_flags()` after a plain `hb_shape`, embedded font, 16 px. `!` marks a cluster where a
break would change the shaped result:

| text | clusters | safe offsets |
| --- | --- | --- |
| `office` | `0 1 4 5` — the ffi ligature covers bytes 1-3 | 1, 4, 5, 6; never 2 or 3 |
| `To` | `0 1!` — kerned | 2 |
| `AV` | `0 1!` | 2 |
| `fi` | `0` | 2 |
| `e` + U+0301 + `x` | `0 0 3` | 4; never 1 |

Control, so the assertions cannot pass vacuously: `ox`, `To` and `AV` carry the flag; `ll`, `ab` and `of` do
not.

## What shipped

| Change | Why |
| --- | --- |
| `ShapedGlyph::flags`, filled from `hb_glyph_info_get_glyph_flags()` | the shaped run already had the answer; it was being thrown away |
| `safe_break_offsets()` | cluster starts not flagged unsafe, ascending (a `std::map` gives that for free, which matters because an RTL run arrives descending), end of text last |
| `break_word()` in the wrap pass, gated on `overflow-wrap: break-word\|anywhere` or `word-break: break-all` | browsers overflow a long word unless asked; the default path is unchanged and asserted |

## Evidence

| Case | Result |
| --- | --- |
| `AetherisShaping` | green; the eight new assertion strings are in the built binary |
| `office` / `To` / combining mark | no offset inside the ligature, the kerned pair or the cluster |
| long word, no property | one fragment — it overflows |
| long word, `overflow-wrap: break-word` | several fragments, each within the line, bytes summing to the word |
| the suite | 65/65 twice, 122.91 s and 123.00 s here; 65/65 twice, 123.48 s and 128.74 s in the separate sandbox |

## What went wrong, and what it cost

While linking, the session's environment exhausted its process table: **17,879 zombies** parented to PID 1
against `ulimit -u 4096`, after which every `zig` invocation failed with `failed to spawn: SystemResources`,
including a one-line `int main(){}`. `git diff` failed on its threaded lstat; `git -c core.preloadIndex=false`
worked and was used to save the patch and revert the tree to `3f00eaaa`.

| First reading | What was true | What settled it |
| --- | --- | --- |
| "the link step is failing" | nothing could spawn; the compiler was fine | `ps` and a one-line test program |
| "the patch is lost with the tree" | `git diff` had already saved it to `/scratch/work` | applying it again, cleanly, in two different environments |

The row was then verified twice — in a fresh sandbox with the patch applied to `3f00eaaa`, and again on a new
environment with the same patch and the same result. A row is not verified because one environment said so.

## Correction to the 2e and 2e2 entries above

Those said the reordering lives in `Rust/src/layout`, "which this tree does not vendor". The Rust layout **is**
vendored, at `Libraries/LibWeb/Rust/src/layout/` — I looked at the repo root instead of inside `Libraries/LibWeb`.
What it does not contain is a bidi reordering pass: `text_chunker.rs` splits chunks by `text_type` and
`inline_level_iterator.rs:168` only decides whether a block is unidirectional LTR. The conclusion held; the
reason given for it did not.
