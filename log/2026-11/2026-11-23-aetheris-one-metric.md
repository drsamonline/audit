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

---

# Twelfth commit, same session — row 3d split, and the first half of 3d1

Commit: `617e4204`

Row 3d was "`@font-face`, transitions, animations" — three features that share nothing but a row. Split into
3d1/3d2/3d3; this commit takes the part of 3d1 that stands on its own.

| what | before | after |
| --- | --- | --- |
| `@font-face { ... }` | skipped with every other unknown at-rule | `CssStyleSheet::font_faces` — family plus the url inside `src` |
| `cached_glyph()` key | `(glyph, size)` | `(font identity, glyph, size)` |

The cache key is groundwork, not a fix for today: with one active font the identity never varied. It becomes a
correctness requirement the moment a second font exists — the pattern row 2g asked for, applied again.

## Evidence

| assertion | where |
| --- | --- |
| quoted family keeps its name, `url(...)` yields the source, a block with no family is dropped, the following rule still parses | `AetherisCss` |
| the same glyph id from two fonts is two cache entries — the second font is the embedded one with one padding byte flipped, so the shapes are identical and only the key separates them | `AetherisGlyphRasterizer` |

Suite 65/65 twice, 145.21 s and 137.77 s.

## What 3d1 still needs

1. **Fetch the source**: no `data:` URL support in the loader, and nothing calls it for `@font-face`.
2. **Select the face**: `font-family` is inherited and never read for selection; `Font`, `FontMetrics`, `measure()`
   and `draw_text()` all go through the singleton `active_font()`.

Two files' worth of parsing is done; five files' worth of plumbing is not, and that is written in the row rather
than left to be rediscovered.

---

# Thirteenth commit, same session — row 3d1: `@font-face` end to end, for local files

Commit: `a0f54651`

| what | before | after |
| --- | --- | --- |
| a declared face | nothing loaded it | `RenderDocument` reads a `file://` or plain-path `src` and registers it |
| `font-family` | inherited, never read | `font_for_family()` resolves the list to the first face that exists, else the engine's own |
| `Font`, `FontMetrics` | every path called `active_font()` | carry the resolved face |
| the pen | `draw_text` called `active_font()` | receives the face paint resolved from the command's family |

Six files: `font_library`, `font`, `render_tree`, `paint_executor`, `software_surface`, `render_document`.

## Evidence

| assertion | where |
| --- | --- |
| bytes register as a face; the family finds it; an unknown family has none; a comma list falls through | `AetherisShaping` |
| `Font::from_style` carries the named face; an unknown family falls back to `active_font()` | same |
| a document with `@font-face { src: url(/tmp/…ttf) }` registers the face and puts the family on the text command | same |

Suite 65/65 twice, 141.13 s and 135.05 s.

## Not done, and in the row

`http(s)` and `data:` sources are not fetched — the family falls back to the engine's font, which is what a browser
does for a face that fails to load. `font-weight`/`font-style` do not select among one family's faces: the registry
is keyed on the family name alone.

## Cost of the plumbing

Four compile errors in a row — a member reference (`m_metrics.face` inside a `FontMetrics` member), two missing
includes, an undeclared function. All mechanical. The useful habit is the boring one: add the include when you add
the use, and read the error's first line instead of the flag wall above it.

---

# Fourteenth commit, same session — row 3d2 started: the curve and the arithmetic

Commit: `4e43371d`

A transition is a curve plus a clock. This is the curve and the arithmetic — the half that can be proven without a
clock, a document or a pixel.

| what | where |
| --- | --- |
| `Easing`: `linear`, `ease`, `ease-in`, `ease-out`, `ease-in-out`, `cubic-bezier()`, `steps()` | `src/rendering/easing.{hpp,cpp}` |
| the cubic-bezier solve | ported from `LibWeb/Rust/src/css/animation.rs:217-300`: Newton-Raphson for eight steps at 1e-7, bisection for sixty-four, tangent extension outside [0, 1] |
| `Transition` with `value_at(now)` / `finished_at(now)` | `src/rendering/transition.{hpp,cpp}` |
| the `transition` shorthand in any token order | same |
| 20 assertions | `Tests/AetherisRendering/TestEasing.cpp` — a new binary, so the suite is 66 |

| curve at 0.5 | value |
| --- | --- |
| `linear` | 0.5 |
| `ease` | **0.802403** (standard 0.8024) |
| `cubic-bezier(0,0,1,1)` at 0.3 | 0.3 — the solve agreeing with the identity |
| `steps(2)` at 0.4 / 0.6 | 0.0 / 0.5 |

Suite 66/66 twice, 136.06 s and 146.45 s.

## What is left, and why it is the awkward part

1. **A clock**: `render_to_surface` is static; the window loop has frames, so the clock belongs there and on
   `RenderDocument`, with paint reading it.
2. **The trigger**: a transition starts when a property's computed value changes. The style cache records which
   nodes are dirty, not which property moved — that is the piece with no test yet because it has no code yet.

One expectation was wrong on the first run and the code was right: `ease` is *flat* past input 1.0, because its
second control point is (0.25, 1) and the tangent is horizontal; `ease-in` is the curve that keeps climbing. The
assertion now says both.

---

# Fifteenth and sixteenth commits, same session — row 4d (the guard) and row 3d2 (transitions run)

Commits: `e600da2a`, `c4b69410`

## Row 4d — a guard against trusting a stale binary

Twice in one session a build was killed by the sandbox's time limit, ninja printed nothing anyone read, and the next
`ctest` passed on the *previous* binary. `tools/check-build.py` asks the two questions that went unasked: does ninja
have pending steps, and did anything get linked after the last source edit. Verified on three cases in an environment
that could not compile at all (stale tree → 57 pending steps, exit 1; missing build directory → 2; never-linked
binary → 1). One process, no subprocesses for the source check, because the environment that needed it allowed
exactly one level of process creation.

Two false positives surfaced the day it was used, both fixed: `tools/*.py` counted as a compiled source, and
comparing against the *oldest* binary made a test-only edit report `aetheris` as stale. It now compares the newest
source with the newest binary.

## Row 3d2 — transitions run

| part | where |
| --- | --- |
| the curve (`ease(0.5) = 0.802403`, ported from `Rust/src/css/animation.rs:217-300`) | `easing.cpp` |
| the arithmetic (`Transition::value_at`) and the shorthand | `transition.cpp` |
| the clock (`set_time`, `start_opacity_transition`) | `render_document.cpp` |
| paint: opacity overrides, tree rebuilt from the existing layout | `render_tree.cpp`, `render_document.cpp` |

| t | pixel at (20, 20) | rect |
| --- | --- | --- |
| 0.00 | rgba(255, 0, 0) | x=10 y=10 50x50 |
| 0.50 | rgba(255, 128, 128) | unchanged |
| 1.00 | rgba(255, 255, 255) | unchanged |

`layout_passes()` 1 before, 1 after — a transition repaints, it does not reflow. Suite 66/66 twice, 211.64 s and
185.69 s.

Still open: the trigger (a style change starting a transition — the cache records dirty nodes, not which property
moved), properties other than `opacity`, and comma lists in the shorthand.

## The guard's first day

When this session resumed, `tools/check-build.py` reported **57 pending steps** — the exact state that had made a
green suite meaningless twice. That is the whole justification for the row: thirty lines, written in the environment
that motivated it, and used before it was trusted.

---

# Seventeenth commit, same session — row 1g4c: `scrollRestoration`

Commit: `5b0974a2`

Upstream first: the mode belongs to the **session history entry**, not the document —
`History.scrollRestoration` reads and writes `active_session_history_entry()->scroll_restoration_mode()`
(`HTML/History.cpp:229-242`). That is the shape ported here.

| what | before | after |
| --- | --- | --- |
| history entries | `vector<string>` of URLs | `vector<HistoryEntry>`: url, offset, mode |
| traversal | URL changed, scroll jumped to 0 | destination entry decides: `Auto` restores, `Manual` leaves it to the page |
| the app | `scroll_to(0, 0)` after every load | `take_scroll_restore()` first |

| assertion | `AetherisBrowserSession` |
| --- | --- |
| a new entry defaults to `Auto` | ✓ |
| a forward navigation restores nothing | ✓ |
| back to an `Auto` entry restores **its own** offset — 320, not the other page's 40 | ✓ |
| the restore is answered once | ✓ |
| a `Manual` destination restores nothing | ✓ |
| the mode is per entry | ✓ |

Suite 66/66 twice, 135.91 s and 131.35 s.

## Two corrections

1. My expectation was wrong, not the code: the **destination** entry's mode decides, not the page being left. The
   test now sets `Manual` on the page being navigated *to*.
2. `viewport` was declared below the history hooks that need it; the declaration moved above them. A lambda cannot
   capture what does not exist yet.

## Not done

`history.state`/`pushState` remain row 1g4b. `scrollRestoration` has an API but no `window.history` binding — that
belongs with 1g4b.

---

# Eighteenth commit, same session — row 5c: mixed content, measured rather than assumed

Commit: `ec883b38`

The row said only "Mixed-content blocking". The code was already there — `SecurityPolicy::allows_resource()` behind
`SecureResourceLoader`, which every fetch goes through — so the work was to measure it against upstream's rule and
fix what the measurement found.

| upstream asks | we asked |
| --- | --- |
| is the origin *potentially trustworthy*? https, wss, file, loopback (`SecureContexts/AbstractOperations.cpp:15-57`) | is the scheme https — **only that** |
| optionally-blockable allowed, blockable refused | images allowed, the rest refused — correct |

## Two faults, both real

| # | fault | consequence |
| --- | --- | --- |
| 1 | trustworthiness was https-only | `http://localhost:3000/app.js` was blocked as mixed content on an https page; an `http://localhost` document was never secure at all |
| 2 | the test used `assert` | under NDEBUG the entire security test compiles to `main() { return 0; }` and passes forever |

Fixed: `is_potentially_trustworthy()` covers https, wss, file, `localhost`, `*.localhost`, 127.0.0.0/8, with four
numeric labels parsed so `127.0.0.1.evil.test` is not loopback. My first version got that case wrong; the test caught
it in one run.

## Evidence — `AetherisSecurityPolicy`, 18 assertions

| group | cases |
| --- | --- |
| trustworthiness | 6 trusted (https, file, localhost:8080, 127.0.0.1, 127.5.6.7, a.localhost), 2 near-misses refused |
| blockable | script, stylesheet, document, form submission refused |
| optionally-blockable | image allowed |
| schemes | `data:` refused |
| other direction | http-over-http allowed, loopback script on https allowed |
| enforcement | the loader itself both ways |

Suite 66/66 twice, 135.20 s and 144.22 s.

## Not done

Audio and video are optionally-blockable per spec; this engine fetches neither, so there is no context to classify
them with — recorded in the row rather than invented.

---

# Nineteenth commit, same session — row 5a: CSP fetch directives

Commit: `d77d56bc`

The policy lived in `main.cpp` as one function answering one question — may inline scripts run? — and the seam for the
other half already existed: `SecureResourceLoader`, which every fetch passes through.

| upstream | here |
| --- | --- |
| a class per directive with `pre_request_check`: effective directive → should it execute (`default-src` fallback) → match the source list (`ContentSecurityPolicy/Directives/ImageSourceDirective.cpp:27-43`) | one matcher, same two steps, for an engine that fetches four kinds of thing |

| request context | directive |
| --- | --- |
| image / stylesheet / script / document / form / other | `img-src` / `style-src` / `script-src` / `frame-src` / `form-action` / `connect-src` |

Sources matched: `'none'`, `*`, `'self'`, scheme, host, subdomain, optional port. Inline gating moved onto the same
object; `csp_allows_inline_scripts()` is gone from `main.cpp`.

## Evidence — 22 further assertions in `AetherisSecurityPolicy`

| group | cases |
| --- | --- |
| empty policy | allows all, inline included |
| `'self'` | own origin yes; another host no; another scheme on the same host no |
| `default-src` | stands in for an absent directive, never overrides a present one |
| wildcards | `*` allows any host; `'none'` refuses even the origin |
| subdomains | `*.example.test` matches `cdn.example.test`, not the bare domain |
| scheme source | `https:` matches any host on https, refuses http |
| inline | `'unsafe-inline'` both ways |
| enforcement | loader allows a matching image, refuses a foreign one, allows a script from the named host, refuses one from the document's own host |

Suite 66/66 twice, 148.83 s and 160.37 s. The build guard reported 67/67 binaries current before both runs.

## Not done

Nonces, hashes, `report-uri`/`report-to`, header delivery (no response headers in this engine), and a path inside a
source expression is not matched.

## Cost

Three compile errors, all mine and all ordering: the fetcher out of scope where the policy is installed, a default
argument on both declaration and definition, and the superseded helper turning into an unused function under
`-Werror`. None was a design problem; all three were caught by the compiler before the suite ran.

---

# Twentieth commit — row 1g4b: `pushState`, `replaceState`, `history.state`

Commit: `0f361020`

Upstream's shape (`HTML/History.cpp:169-223`): one shared path for push and replace that serialises the state,
resolves an optional URL against the document, refuses a URL the document cannot be rewritten to, and updates the
session history entry **without loading anything**.

| what | before | after |
| --- | --- | --- |
| `history.pushState` / `replaceState` | did not exist | on `window.history`, wired to the session |
| `history.state` | did not exist | the current entry's state, parsed back, `null` when none |
| `history.scrollRestoration` | C++ API only | on `window.history` — the half row 1g4c owed |
| a history entry | url, scroll, mode | plus the serialised state |

## Evidence

| test | assertions |
| --- | --- |
| `AetherisBrowserSession` | push grows and moves the URL; empty url keeps it; cross-origin refused and changes nothing; replace overwrites; back reads **that entry's own** state; the first entry has none; no load is started |
| `AetherisJs` | `null` for no state; `{n:2}` round-trips; a string state; **a function becomes null rather than throwing**; a cross-origin push throws where a script can catch it; `scrollRestoration` reads `auto` and writes `manual` |

Suite 66/66 twice, 135.25 s and 131.69 s.

## The limit, stated in the row

The state is **JSON, not a structured clone** — `Map`, `Set`, `Date`, typed arrays and cycles collapse or become
`null`. Upstream substitutes `null` itself when its serialiser refuses (`History.cpp:177`), so the failure mode
matches a browser's; only the set of clonable values is smaller.

## Two test bugs, both mine

1. `open()` leaves `loading` true until a page reports back, so `pushState` looked like it started a navigation.
2. I expected the entry *below* a `replaceState` to carry the replaced state. It carries its own — that is what
   replace means.

## One flake named

`WindowGeometry` failed once under a loaded `-j2` run, then passed alone (81 s) and in the two reported runs
(77 s). Long test, busy pod; both suite times above are clean.

---

# Twenty-first commit — row 3d3: `@keyframes` animations

Commit: `456a8962`

Upstream's shape: a named rule holding keyframes, each with an offset and a declaration block
(`CSS/CSSKeyframesRule.h`, `CSSKeyframeRule.h`), sampled between the frames that mention the property.

| piece | where |
| --- | --- |
| `@keyframes` parsing (block of blocks, `from`/`to`/`50%`/`0.5`, sorted) | `css_parser.cpp` → `CssStyleSheet::keyframes` |
| the `animation` shorthand | `animation_spec_from_style()` |
| sampling a numeric property at a time | `Animation::value_at` |
| starting them | `RenderDocument::start_stylesheet_animations()`, once at build |
| applying them | the opacity override map row 3d2 built |

**Why this row was cheaper than transitions:** a transition needs a *trigger* (a computed value changing), which the
style cache does not record. An animation needs none — the declaration is in the stylesheet at load time.

| t | pixel at (20, 20), red box fading over 1 s |
| --- | --- |
| 0.00 | rgba(255, 0, 0) |
| 0.50 | rgba(255, 128, 128) |
| 1.00 | rgba(255, 255, 255) |
| 1.50 | rgba(255, 255, 255) — last keyframe holds |

`layout_passes()` unchanged. Suite 66/66 twice, 138.02 s and 149.24 s.

## Three bugs, all found by running it

| bug | how it showed | fix |
| --- | --- | --- |
| parser looked for an opening brace the caller had consumed | rule parsed with **zero frames** | start reading at the first keyframe's offset |
| `strtod("infinite")` returns infinity | the iteration keyword landed in the **delay** as `inf` | check the keyword before anything numeric; reject non-finite times |
| duplicate offset helper | `-Wunused-function` under `-Werror` | one owner for offset parsing |

## Not done

Numeric properties only (`opacity`); no `animation-direction`, `fill-mode`, `play-state`, comma lists; colour and
transform keyframes need a value type this engine lacks.

---

# Twenty-second commit — row 5b: same-origin, measured before it was enforced

Commit: `83d52d57`

The row said "Same-origin enforcement in the bindings". The measurement found there is **nothing to enforce**: no
`fetch`, no `XMLHttpRequest`, no frames — no binding can reach across an origin. Same shape as row 3i, except the
measurement turned up a real bug underneath.

| what | before | after |
| --- | --- | --- |
| storage keyed per origin | yes, on a hand-computed key | on `SecurityPolicy::origin()` |
| `https://A.test` vs `https://a.test` | **two buckets** | one; `set_storage_origin()` lowercases |
| definitions of "origin" | two | one |

| assertion in `AetherisJs` |
| --- |
| a second origin sees neither store |
| its writes do not reach back |
| the first origin's data survives the visit |
| `https://A.TEST` is the same origin as `https://a.test` |
| `http://a.test` is not — the scheme is part of the origin |

Probe before: `b sees: null`, `a sees: from-a`, **`A.test sees: null`**. After: `A.test sees: from-a`.

Suite 66/66 twice, 125.93 s and 128.85 s.

## Not invented

Nothing enforces an origin across documents because there is only ever one document. When a `fetch` or an iframe
arrives, the check belongs in that binding; these assertions are what would catch it going wrong.

## Trap hit again

The first re-run of the probe printed the **old** numbers — a probe links the static library, and it had not been
relinked. The trap is documented and still caught me; relinking is not optional.

---

# Twenty-third commit — row 4.1: the tab strip

Commit: `1f980a7e`

The chrome had one hardcoded tab box, and the input router kept **its own copy** of every chrome coordinate
(`tab_width() 190`, `back_x() 230`, …) with the comment `activating a tab needs the tab list; not yet`. Two
computations of one layout is the bug the row was really about.

| piece | where |
| --- | --- |
| one layout: tab boxes, close buttons, `+`, back/forward/reload, address bar | `src/ui/chrome_layout.{hpp,cpp}` |
| drawing | `chrome_document()` — one box per session tab |
| hit-testing | `InputRouter::set_chrome_layout()` → `ChromeLayout::hit_test()` |
| actions | `ActivateTab` (with index), `CloseTab` (that tab), `NewTab`, `Back`/`Forward`/`Reload`, `FocusAddress` |

Tabs shrink from 190 px toward a 56 px minimum, so twelve fit and the strip never runs under the `+`.

## Evidence — `AetherisInputRouter`

| assertion |
| --- |
| a click in the second tab names **index 1** |
| a click on its close button closes rather than switches |
| `+` opens a tab |
| one tab keeps the 190 px maximum; twelve shrink but stay ≥ 56 px |
| the strip ends before the `+`; the address bar stays inside the window |
| zero tabs still shows one box |

Suite 66/66 twice, 136.09 s and 131.10 s.

## Not done

No drag-reorder, no middle-click close, no overflow menu below the minimum width; the close button is a text glyph.

## The useful signal

Deleting the duplicated coordinates broke the test that had been written against them. That is exactly what a shared
layout is supposed to do — the duplication had been pinned in place by a test that believed in it.

---

# Twenty-fourth commit — row 4.2: history and bookmarks

Commit: `8dd7dbd4`

| piece | where |
| --- | --- |
| `HistoryEntry` keeps the title it had while current | `browser_session.{hpp,cpp}` |
| bookmarks: add, remove, `is_bookmarked`, `toggle_bookmark` — no duplicates, first title wins | same |
| panels as ordinary documents of real `<a href>` links | `src/ui/library_page.{hpp,cpp}` |
| Ctrl+H / Ctrl+B / Ctrl+D | `input_router.cpp` |

**The design decision:** the panel is a *document*, not an overlay. Its rows are real links, so a click goes through
the navigation path a page's own links already use — no second hit-testing path, no second set of coordinates to
drift, which is exactly what row 4.1 was about.

## Evidence — `AetherisBrowserSession`

| assertion |
| --- |
| each entry kept its own title |
| a bookmark cannot be added twice; the first title is kept |
| `toggle_bookmark` adds then removes |
| the history panel is titled, entries are `<a href>` links, **newest first**, current page marked, bookmarked entries starred |
| the bookmarks panel lists only bookmarks |
| an empty panel says "No bookmarks yet" |

Suite 66/66 twice, 138.26 s and 136.71 s.

## Not done

No delete-one-entry or clear-all, no folders or editing, no search box, and **nothing is persisted** — history and
bookmarks end with the process. Persistence needs a store on disk and a decision about where it lives: a row of its
own, not a corner of this one.

## Cost

Three compile errors, all includes or namespaces. The codebase's tests include by angle-bracket path, and every new
module costs one of those.

---

# Twenty-fifth commit — row 1g2: realm isolation, and the checklist closes

Commit: `cf1d6394`

The probe confirmed the row's premise before any code was written.

| after a "navigation" | before | after |
| --- | --- | --- |
| `var leaked` from page one | still a `string` | `undefined` |
| `window.onPageOne` | still a `function` | `undefined` |
| a listener from page one | still fired | does not fire |
| `has_timers` | 1 | 0 |
| `localStorage` | survives | survives — correct |

## The fix, and the approach that failed

`reset_realm()` **replaces the context**. The first attempt emptied the global object and could not work: a top-level
`var` creates a **non-configurable** property, so it cannot be deleted. Replacing the realm that owns the names is the
only honest answer — and it is what upstream does by building a new `Window` and `Realm` per document.

## Two leaks the runtime found

| leak | surfaced as |
| --- | --- |
| timer callbacks dropped without `JS_FreeValue` | `JS_FreeRuntime: Assertion 'list_empty(&rt->gc_obj_list)' failed` |
| `m_window` / `m_document` overwritten without being freed | the same assertion, after the first fix |

A leak checker finds these; a reader does not. The assertion is why the reset is believed rather than assumed.

Suite 66/66 twice, 140.19 s and 161.79 s.

## The checklist

| | count |
| --- | --- |
| done | **66** |
| blocked | 1 — `0.1`, needs open internet |
| out of scope | 2 — `3i` non-divergence, `5d` process isolation |
| open | **0** |

Twenty-five commits, every one with its suite run twice, its four docs updated, an audit entry, and a verified push.

---

# Twenty-sixth commit — row 0.1: the corpus, and the finding that pays for it

Commit: `0ca65f04`

Row 0.1 was blocked as "no open internet". **It was wrong about itself** — the network is reachable through an HTTP
proxy; the precise blocker is a short egress allowlist. One call found that out.

| what | state |
| --- | --- |
| `tools/run-corpus.sh` + `tools/corpus-urls.txt` (20 sites) | built, runs, records a TSV |
| `--render file:///…` | works now — the CLI registers `FileResourceBackend`; before this a local file could not render at all |
| fetching | curl's job: the engine's client has no proxy support (new row **0.3**) |
| the 20-site list | blocked: `example.com` and `en.wikipedia.org` answer, seven others measured at 502 |

## Two reachable sites were enough

| site | bytes | result |
| --- | --- | --- |
| `example.com` | 577 | rendered |
| `en.wikipedia.org/wiki/Web_browser` | 416,975 | **did not finish in 280 s**, with scripts and without |

| document | parse | style + layout |
| --- | --- | --- |
| wikipedia, 8,339 bytes | 10 ms | 13 ms |
| wikipedia, 20,848 bytes | 25 ms | **121,972 ms** |

| elements | empty divs | divs with text | inline spans |
| --- | --- | --- | --- |
| 100 | 78 ms | 161 ms | 170 ms |
| 200 | 144 ms | 299 ms | 291 ms |
| 400 | 316 ms | 636 ms | 544 ms |

Parse is linear; layout is linear on synthetic pages but at **~0.8 ms per element** — three orders of magnitude slower
than a browser — and real markup is worse than the synthetic shapes predict. Row **3j** carries it; the report is
`docs/COVERAGE-CORPUS.md`.

## Why the row existed

First time the engine was pointed at a real page, and it produced the largest performance problem in the project —
one no unit test could have found, because every test page is small.

## Two process notes

1. The commit was written **before** the suite ran and its message claimed the suite was unchanged. It was run
   afterwards — 66/66 twice, 142.22 s and 164.02 s — and the message amended with the real times. A claim that happens
   to be right is not the same as a check.
2. The new rows were first written as `3e` and `0.2`, both already taken. The checklist has no uniqueness check; the
   collision was caught by grepping the file before committing.
