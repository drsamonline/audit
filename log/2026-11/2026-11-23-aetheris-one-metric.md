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

---

# Fourth row, same session — 2g: letter- and word-spacing

Commit: `82bbec03`

## What I looked at upstream

| Question | Where | What it said |
| --- | --- | --- |
| Where is spacing applied? | `Libraries/LibGfx/TextLayout.cpp:283-292` | while building the glyphs: `extra_advance = letter_spacing`, plus `word_spacing` when the glyph's cluster starts at `is_word_separator()`; the advance is `x_advance + extra_advance` |
| What counts as a word separator? | `LibGfx/TextLayout.cpp:207-216` | space, no-break space, and the line feed (AD-HOC, matching other engines) |
| Does the cache key carry them? | `Libraries/LibGfx/Font/Font.h:31-45` | yes, as `u32` bit patterns in `ShapingCacheKey` |
| Is the trailing edge spaced? | `LibGfx/TextLayout.cpp:296-298` | yes, deliberately: "the spec says that we 'really should not' apply letter-spacing to the trailing edge of a line but other browsers do so we will as well" |

## What was wrong before

`TextLayout::measure_text` added letter-spacing per code point and word-spacing per space; `draw_text` added
neither. A page with `letter-spacing: 8px` and eight characters was laid out 64 px wider than it painted.

## What shipped

| Change | Why |
| --- | --- |
| `shape_run(font, text, size, identity, letter_spacing, word_spacing)` | spacing is part of the shaped result, so it is applied once, where the advances are made |
| cache key `(identity, size, letter bits, word bits)` | widened in the same commit as the property, which is what the row asked for |
| `Font::measure(text, letter, word)`; `measure_text` adds nothing itself | one number for layout and paint |
| `PaintCommand::letter_spacing`/`word_spacing` → `draw_text` → `shape_run` | the pen advances by what layout measured |

## Evidence

| Case | Result |
| --- | --- |
| `"abc"`, `letter-spacing: 2px` | +6.0 px through layout (3 glyphs) |
| `"a b"`, `word-spacing: 5px` | +5.0 px, once, at the space |
| spaced then unspaced, both ways round | each returns its own width — the cache does not collide |
| fragment width vs shaped run | equal within 0.01 px |
| rendered, 32 px, `letter-spacing: 8px`, centred in 400 px | ink 79-309, centre 194; the 6 px offset is the trailing spacing, as upstream documents |
| the suite | 65/65 twice, 129.99 s and 135.76 s |

## What I got wrong

| First reading | What was true | What settled it |
| --- | --- | --- |
| "`css_length_px(value, 0, size)` — the last argument is the size" | the signature is `(value, reference, fallback)`; I passed them swapped, so a *missing* `letter-spacing` resolved to 16 px | the 2h assertion failed: `measure_text("To")` stopped matching the shaped width |
| "the build is clean" | `ninja` was not installed in the new environment; the command's empty output, filtered through `grep`, read as success | `ninja: command not found` on the next call |

The second is row 4d's hazard — a missing artefact and a successful one look the same through a filter.

---

# Fifth commit, same session — rows 2b and 2c: status drift

Commit: `580f366e`

Both rows were `[ ]` and both were true in the code. The checklist says a wrong status is fixed in the next
commit with the message saying so, so this one ticks them and supplies the proof each was missing.

| row | already true | proof added |
| --- | --- | --- |
| 2b | `draw_text` → `cached_glyph()` → `rasterize_glyph()` | `AetherisGlyphRasterizer` asserts the cached bitmap equals the rasterised one, value for value (24x26 for 'A' at 32 px, 221 inked, 115 partial) |
| 2c | GPOS for shaped runs, the embedded pair table for the fallback | `AetherisShaping` asserts A+T = -159 from the table and a shaped "AT" narrower than "A" + "T" |

## The fixture, again

| First attempt | What was true | What settled it |
| --- | --- | --- |
| `kerning_adjustment(local_font, T, o)` | returns 0 for every pair unless the font *is* `active_font()` — the table holds the embedded subset's glyph ids | a probe over all ASCII pairs: zero pairs from a local `TtfFont`, twelve from the active font |
| `T + o` | not in the table; `A + T` is | the same probe |

## Found and not fixed

`cached_glyph()` keys on `(glyph, size)`, not on the font. Correct while `active_font()` is the only font
paint can reach; wrong the day `@font-face` lands (row 3d). Recorded in the handover, not ticked anywhere.

---

# Sixth commit, same session — row 3a6: `content` as a list, with alt text

Commit: `13aac19b`

## What I looked at upstream

| Question | Where | What it said |
| --- | --- | --- |
| How is `content` modelled? | `Libraries/LibWeb/CSS/StyleValues/ContentStyleValue.h:16-45` | `ContentStyleValue` holds a `StyleValueList content` and an optional `StyleValueList alt_text` |
| What does the tree builder ask it? | `Libraries/LibWeb/Rust/src/layout/tree_builder.rs:1714-1800` | `FfiComputedContentType` — Normal, None or List; a List generates a box even when its text is empty |
| Where does the alt text come from? | the declaration's `/` (css-content-3) | the part after the slash is alternative text, not page text |

## What was wrong before

The parser wrapped the **whole** declaration in quotes so `content: ''` could be told apart from no
declaration. Everything between those quotes then rendered as page text, so `content: 'C' / 'alt text'` put
`/ alt text` on the page and `content: 'a' 'b'` rendered "a b" — a space that the declaration does not contain.

## What shipped

| Change | Why |
| --- | --- |
| `ContentValue` (kind, items, alt-text items, unsupported count) | the property is a list; three kinds are what the tree builder needs |
| the parser quotes **each** string item | item boundaries survive into the declaration string; `content: ''` is still a one-item list |
| `make_generated_box` asks `ContentValue` | the hand-stripped quotes are gone |
| `LayoutNode::generated_alt_text` | the alt text stops at the parser otherwise |

## Evidence

| Declaration | Before | After |
| --- | --- | --- |
| `content: 'a' 'b'` | "a b", two fragments | "ab", one fragment |
| `content: 'a b'` | "a b" | unchanged |
| `content: 'C' / 'alt text'` | "'C' / 'alt text'" on the page | "C", alt "alt text" on the node |
| `content: ''` | empty box | empty box |
| `content: attr(title)` | the literal text "attr(title)" | nothing, counted unsupported |

Probe over the layout tree printed `[ab]`, `[a b]`, `[C] alt=[alt text]`, and an empty box with no
fragments. Suite 65/65 twice, 125.10 s and 125.36 s.

## What I got wrong

| First reading | What was true | What settled it |
| --- | --- | --- |
| "trim the value, then quote it" | the trimmed value was thrown away; the quoted string was built from the untrimmed tokens, so `content: 'C'` came back as ` 'C'` | the existing CSS test failed on a leading space |

Nothing reads `generated_alt_text` yet — no accessibility tree, tier 4. Recorded rather than dressed up as
complete.
