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

---

# Seventh commit, same session — row 3i: the divergence was not there

Commit: `b0c070e3`

The row read: "at an exactly-full line this wraps anyway; upstream overflows. Ours never overflows — the safer
error, recorded not hidden." A probe says both halves are wrong.

| case | measured |
| --- | --- |
| `"aaa"` in a 25 px box | one fragment, 30 px wide — overflows |
| `"aaaaaaaa"` (80 px) in 30 px | one fragment, 80 px wide |
| `"aaa bbb"` in 30 px | two lines, wrapping at the space |
| two 60 px `inline-block`s in 100 px, no whitespace | both at `y=0`; the second at `x=60`, overflowing |
| the same two with a space between | the second at `y=10` |

The engine already behaves as a browser does, so there was nothing to fix. The row is marked `[-]` (out of
scope: no gap) with the numbers in its cell, and five assertions in `AetherisTextLayout` pin the behaviour —
that is the part with value, because a future change to the wrap pass could otherwise start wrapping where it
must overflow.

Suite 65/65 twice, 127.54 s and 125.76 s.

## What this says about the checklist

A row written from a *symptom* can name a fault that is not there. This one survived two sessions because
nobody measured it; the same probe that closed 2h, 2g and 2b would have closed it in ten minutes on the day it
was written. Two rows this session (3i here, and the "not vendored" claim in 2e) turned out to be wrong about
their own premise rather than about the code.

---

# Eighth commit, same session — row 3b: `position: sticky`

Commit: `49f3af69`

## Why paint time

The scroll path is repaint-only by design — "the document is not re-laid out: scrolling repaints, it does not
reflow" (`render_document.hpp`). A sticky offset computed during layout would be stale the first time the page
scrolled, so the render tree carries the geometry (`StickyRegion`) and the paint pass carries the scroll offset
and applies the shift.

## What shipped

| Change | Why |
| --- | --- |
| `StickyRegion` per sticky box: command range, node top/height, containing block top/bottom, `top`/`bottom` | paint needs to know what to move and how far it may move |
| `emit` records it after the subtree is emitted | the range has to cover the box and everything inside it |
| `PaintExecutor` shifts that range: `clamp(scroll + top - node_top, 0, container_bottom - node_bottom)` | the CSS rule, in one expression |
| sticky children sort after in-flow siblings | see below |

## Evidence

200x120 viewport, container spanning rows 60-160, `top: 10px`, magenta box:

| scroll | box at surface y | why |
| --- | --- | --- |
| 0 | 60 | natural |
| 60 | 10 | stuck |
| 100 | 10 | still stuck |
| 140 | 0 | clamped at the container's bottom |

Suite 65/65 twice, 148.98 s and 143.33 s.

## The bug the probe found

The first version shifted the box correctly and painted it **underneath** the sibling that follows it, so at one
scroll offset the magenta was present and invisible — the probe reported "no magenta" at 120 while 0, 30 and 60
were right. `position: sticky` creates a stacking context; sorting sticky children after the in-flow ones fixes
it.

## Named, not done

`bottom` is read and applied symmetrically but only `top` is asserted. Absolute and fixed children still paint in
document order rather than above in-flow content — the same class of bug, a separate row, and changing it would
move pixels this row is not about.

---

# Ninth commit, same session — row 3a3: the generated box paints, both halves of it

Commit: `5d47ff44`

The row said "needs a synthetic text node whose `dom_node` is null". Measured: the **text already painted** — 31
magenta pixels for `::before { content: 'X'; color: #ff00ff }`, 109 at 28 px. What did not paint was the **box**.

| case | before | after |
| --- | --- | --- |
| generated box, background + text | background missing | background, then the glyph over it |
| generated box, border, no text | painted | unchanged |
| generated `inline-block` with text, no width | 200 px — the whole line | 11 px, same as a real span holding "X" |

## Two causes

| # | cause | fix |
| --- | --- | --- |
| 1 | `RenderTree::emit` had background/border/shadow/outline in the `else` of the text branch. A normal element never carries its own fragments (its text is a child node), so only a generated box — the one node kind with both — lost half its paint | a `paint_box` lambda, called before the text (also the CSS order) |
| 2 | `layout_node`'s text branch never set `box.content.width`, so a generated box kept the whole available width; a normal inline-block gets its width from the parent's shrink-to-fit pass, which cannot measure a node with no DOM node | shrink to the text's natural width, never past a specified one |

## Evidence

`AetherisTextLayout` asserts: the background is painted, it is narrower than the line, the glyph is painted over
it, and the generated box is exactly as wide as a real `inline-block` holding the same text. Suite 65/65 twice,
141.62 s and 136.48 s.

## Process note

The first probe run after the fix printed the old numbers: the probe is statically linked against
`libAetherisRendering.a`, and only the library had been rebuilt. That is the stale-artefact trap from the 11-18
handover, one link further down the chain — the binary in your hand is not always the code in the tree.

---

# Tenth commit, same session — row 3c1: flex completeness

Commit: `30fca7d3`

Row 3c was "complete flex and grid", which is two algorithms in one row. Split: 3c1 flex (this commit), 3c2 grid
areas and named lines.

| what | before | after |
| --- | --- | --- |
| `flex: 1` | ignored — the shorthand was never parsed, so the commonest flex declaration in the wild did nothing | `1 1 0%` |
| `flex-basis` | ignored | the base size, ahead of `width` |
| overflow in a row | free space clamped at 0, items overflowed | shrink proportional to `flex-shrink × base` |

| 300 px row | widths |
| --- | --- |
| three `flex: 1` | 100 100 100 |
| `width: 100px` + two `flex: 1` | 100 100 100 |
| `flex: 2` vs `flex: 1` | 200 100 0 |
| two `flex-basis: 200px` | 150 150 0 |
| the same with `flex-shrink: 0` | 200 200 0, overflowing |
| three `flex: 0 0 150px` | 150 150 150 |

Upstream: `Rust/src/layout/flex_formatting_context.rs:797` (`used_flex_basis_for_item`) and `:1022`
(`determine_flex_base_size`). Suite 65/65 twice, 135.15 s and 141.02 s.

## The environment trap, recorded because it nearly shipped

This environment's working copy had been restored from a snapshot **older than the pushed history**: `HEAD` at
`5a8a5d7a` while `origin/main` was at `5d47ff44`, with the working tree matching the older state. The flex work was
therefore committed on the wrong base, in a commit that would have reverted rows 3a6, 3i, 3b and 3a3.

| what caught it | what it showed |
| --- | --- |
| `git push` rejected as non-fast-forward | the remote had four commits this tree did not |
| `git diff --stat origin/main HEAD~1` | 25 files, **909 deletions** — a "single feature" commit deleting 900 lines |

The commit was preserved on a branch (`flex-work-preserved`), the branch reset to `origin/main`, and only the flex
hunks re-applied: `style.cpp` (pure addition), `layout.cpp` (the flex function only), `TestLayout.cpp` (additive),
three doc edits. Rebuilt and re-ran the suite, because the sources had changed under the build tree. The final diff
against `origin/main` is **213 insertions, 20 deletions**.

Rule for the next session: compare `git log --oneline -1` with `git fetch && git log --oneline -1 origin/main`
*before* the first commit, not after the first rejected push.

---

# Eleventh commit, same session — row 3c2: grid placement

Commit: `7d90d8e6`

`grid-template-areas` was not parsed and `grid-area` was ignored, so a grid laid out exactly like a row-major
list — the one thing a page writes a grid for had no effect.

| what | before | after |
| --- | --- | --- |
| `grid-template-areas` | not parsed | a name grid, `.` empty |
| `grid-area: <name>` | ignored | that name's bounding box, spans included |
| `grid-column` / `grid-row` | ignored | 1-based line, or `start / end` |
| auto-placed items | index ÷ columns | the first free cell |

| 300 px container, three 100 px columns | result |
| --- | --- |
| `'h h h' / 'l . r'`, `grid-area: h` | x=0 y=0 **w=300** |
| `grid-area: l` / `r` | x=0 y=20 / x=200 y=20, skipping the `.` |
| `grid-column: 2 / 4` | x=100 **w=200** |
| explicit column 2, then two auto items | x=100, x=0, x=200 |

Upstream: `Rust/src/layout/grid_formatting_context.rs:746` (`find_unoccupied_grid_area`) — an occupation grid
scanned along the auto-flow axis. Suite 65/65 twice, 154.66 s and 159.66 s.

## Two faults, both invisible from outside

| # | fault | fix |
| --- | --- | --- |
| 1 | the tokenizer strips quotes, so `grid-template-areas: 'h h h'` arrived as `h h h` and the parser found no rows | re-quote it in the parser exactly as `content` is re-quoted (row 3a6) |
| 2 | the areas parser looked for **double** quotes, and the re-quoting writes **single** ones | accept either |

The grid looked like it ignored areas; it was ignoring the property's syntax, twice.

## Still not read

Named lines (`[name]`), `span n`, `auto-fit`/`minmax`, `grid-auto-flow: column`; `grid-template-rows` understands
pixel tracks only.
