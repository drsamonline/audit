# Aetheris — shaping cost, then bidi level 1

Date: 2026-11-22 · Repo `drsamonline/The_Browser`
Commit: `308f1d62` (row 2d4), `85c0b46e` (row 2e)

Row 2d4 was written as "shaping costs 1.043 ms per 24-character run at -O0; measure in a release build
before optimising". Measuring first was the right instruction: the cost was not shaping, and it was not
the build type either.

## What I looked at upstream

| Question | Where | What it said |
| --- | --- | --- |
| Does upstream cache shaped text, and keyed on what? | `Libraries/LibGfx/Font/Font.h:31-45`, `:109-116` | `ShapingCacheKey { Utf16String text; u8 text_type; u32 letter_spacing_bit_pattern; u32 word_spacing_bit_pattern; }`, a `HashMap<ShapingCacheKey, OwnPtr<ShapedGlyphs>>` plus a 128-slot `single_ascii_character_map`, on the `Font` — which already carries its size |
| Where is the hit, and what is stored? | `Libraries/LibGfx/TextLayout.cpp:309-360` (`shape_text`) | lookup by hashed key with a candidate comparison, value built origin-relative and translated per caller; `FIXME: The cache currently grows unbounded` |
| Does the measurement path use the cache? | `Libraries/LibGfx/TextLayout.cpp:363` (`measure_text_width`) | no — it shapes the buffer directly. Their measure is a separate path from their paint path; ours is one `shape_run()` for both, so ours caches under both |
| What does a font cache beyond the face? | `Libraries/LibGfx/Font/Font.h:105` | `harfbuzz_font()` per `Font`, i.e. the scaled `hb_font_t` belongs to the size |

Ported the shape: cache on the identity that owns the data, key on everything that changes the result,
keep the scaled font with the size. Widened where our API forces it — our shaper is a free function, so
the font identity and the size go in the key rather than being implied by `this`.

## What was measured before any code changed

`tools/shaping-bench.cpp`, 2,000 iterations, best of five, DejaVu Sans (756,072 bytes), 24-character run:

| step | -O2 | -O0 |
| --- | --- | --- |
| `shape_run()` as shipped | **1.2571 ms** | ~34 ms |
| HarfBuzz alone, face and font built once | 0.0046 ms | 0.1325 ms |
| `hb_font_create()` per call | 0.0003 ms | 0.0058 ms |
| FNV-1a over the whole font file | **1.2532 ms** | **30.65 ms** |

The face cache added in `18eb91c8` keys on a content hash of the font file, and the hash was taken
**inside** `shape_run` — 756,072 bytes of dependent multiply per shaped run. That is 98% of the -O2 cost
and 90% of the -O0 cost. HarfBuzz was never the problem.

The 1.043 ms in the 11-18 handover was taken before that cache existed. The note beside it — "worth ~7%:
0.075 ms of 1.043 ms" — priced the face creation the cache removed and not the hash it added, so the row
it fed had the wrong shape for two days.

## What shipped

| Change | Why |
| --- | --- |
| `TtfFont::identity()`: FNV-1a over the file, computed once in `load()` | the same content hash, at the frequency that made it free. Still content, not address, because an address is reused when a font reloads into the same buffer |
| `shape_run(data, text, size, font_identity)` | the identity is supplied by whoever owns the bytes; 0 means "no identity", and that path shapes without either cache |
| `SizeCache { hb_font_t* font; map<string, vector<ShapedGlyph>, less<>> runs; }` per (identity, size) | upstream's `ShapingCache` and `harfbuzz_font()` in one place; `std::less<>` so a hit compares a `string_view` and allocates nothing |
| a 4,096-run cap that clears the map | upstream's own FIXME. Bounded, no LRU thread through the hit path, one re-shape per run after a clear |
| identity threaded through `Font::measure` and `draw_text` | one code path; the tests pass an identity too, so the test exercises what the engine runs |

## Evidence

| Case | Result |
| --- | --- |
| `font.identity()` on a loaded font | non-zero |
| two `TtfFont` objects, same bytes | same identity — a reload shares the face |
| same call twice | identical glyphs, clusters and advances |
| same text at 16 px and 32 px | different advances (32 px > 1.5x), so the size is in the key |
| `measure("fi")` vs `measure("f") + measure("i")` | still 10.0781 < 10.0938 — the ligature survives the cache |
| one 24-char run, -O2 | **1.2571 ms -> 0.0001 ms** cached, 0.0086 ms cold |
| one 24-char run, -O0 | ~34 ms -> 0.0027 ms cached, 0.1863 ms cold |
| the suite | 64/64 twice, 126.21 s and 129.14 s at `ctest -j2` (was 210.28 s) |

## What I got wrong on the way

| First reading | What was true | What settled it |
| --- | --- | --- |
| "`Font::measure` is faster than `shape_run`, so the shaper is not wired in" | the bench never set `AETHERIS_FONT`, so `measure` used the bitmap fallback | setting the variable: 0.0446 -> 1.4292 ms |
| "the font hash costs nothing (0.0000 ms)" | the loop was dead code; the compiler deleted it | a `volatile` sink |
| "the release build is slower than debug" | the -O0 figure predated the hash | the breakdown |
| "the -O0 bench hangs" | 30 calls at 31 ms each, against a 300 s command cap | a probe that stamps every step |
| "key the cache on a hash memoised by buffer address" — considered, not written | that is precisely the bug `18eb91c8` removed | reading the comment on the code being changed |

---

# Second batch, same session — bidi level 1 (row 2e)

Commit: `85c0b46e`

One audit entry per session, so this is the same entry's second half: two rows, two commits, one day.

## What I looked at upstream

| Question | Where | What it said |
| --- | --- | --- |
| Is there a cheap gate for "does this text need bidi at all"? | `Libraries/LibUnicode/Bidi.cpp` | `may_require_bidi_processing()`: false for ASCII storage, true for R/AL/embedding/isolate/override classes |
| How does the C++ side tell the layout what a code point's direction is? | `Libraries/LibWeb/Layout/TextNode.cpp:556-620` | `text_type_for_code_point()`: a 128-entry ASCII table for the fast path, then `bidirectional_class()` mapped onto `GlyphRun::TextType { Common, Ltr, Rtl, ContextDependent }` |
| How does a run's direction reach HarfBuzz? | `Libraries/LibGfx/TextLayout.cpp:169-190` | `hb_buffer_set_direction()` from the run's text type *before* `hb_buffer_guess_segment_properties()`, which only fills what is unset; ASCII is forced Latin/LTR and skips the guess |
| Where does the reordering happen? | `Rust/src/layout` (not vendored in this tree) | not available here — so level 1 only, and the remaining half is row 2e2 |

## What was measured before writing anything

| case | one guessed buffer | split by direction |
| --- | --- | --- |
| "abc سلام xyz" | 12 glyphs, Arabic in isolated forms, clusters 0-15 ascending | **11 glyphs**, RTL run's clusters 10 6 4 |
| "سلام عليكم" | — | one RTL run, clusters 17 15 13 11 9 8 6 2 0, nine glyphs, lam-alef formed |
| "سلام" shaped LTR vs RTL | LTR: 4 glyphs, isolated | RTL: 3 glyphs, joined |

## What shipped

| Change | Why |
| --- | --- |
| `bidi_class()` — a range table for R, AL and numbers, everything else LTR | the engine is standalone; LibUnicode is not built here, so the table is hand-written and its limits are stated in the header |
| `split_directional_runs()` | cuts where the direction changes; neutrals by N1, then the paragraph direction (LTR, since the engine has none); numbers get their own LTR run so digits are not reversed inside Arabic |
| `may_require_bidi()` | asks the table, not the byte value: "café" and "١٢٣" are non-ASCII and need no split |
| `shape_run()` shapes one buffer per run, direction forced, clusters still absolute byte offsets | one entry point, so measure and paint cannot disagree |

## Evidence

| Case | Result |
| --- | --- |
| ASCII, "café", Arabic-Indic digits alone | no split; the one-run path is kept |
| "abc سلام xyz" | `ltr[abc ] rtl[سلام] ltr[ xyz]` |
| "سلام سلام" | one RTL run: the space between two Arabic words resolves RTL |
| "سلام 123" | `rtl[سلام] ltr[ 123]` |
| shaped mixed string | RTL run's clusters strictly descending; the Latin run still starts at cluster 0 |
| `shape_run` cold, ASCII, -O2 | 0.0086 -> 0.0058 ms: the gate is a byte test per character |
| the suite | 65/65 twice, 125.14 s and 125.28 s |

## The finding this batch is really about

`TextLayout::layout` (`src/rendering/text_layout.cpp:20-22`) tokenises a text node into **one fragment per
word**, and `RenderTree::emit` paints one `DrawText` per fragment. So a shaper fix cannot fix a line: each
word is now shaped in the right direction, and the words are still placed left to right in logical order.

Measured, not assumed: rendering "سلام عليكم" gives ink groups of 30 px on the left and 37 px on the right,
which are the widths of سلام and عليكم rendered alone — the *first* logical word is on the left. Rendering
"عليكم سلام" mirrors it. That is UAX#9 level 2, it lives in layout, and it is row 2e2.

## What I got wrong

| First reading | What was true | What settled it |
| --- | --- | --- |
| "any byte above 0x7F needs bidi" | "café" needs none | the test failed on it; the gate now asks the class table |
| "a neutral takes the direction before it" | that is N1's same-direction case; N2 gives the paragraph direction | the split assertion failed: `rtl[سلام ]` where `rtl[سلام] ltr[ xyz]` was expected |
| "the render is broken: سلام is on the left" | the render is right for a shaper and wrong for a line | ink widths of each word alone, then of the phrase |
| "`--render file:///...` will show me the page" | the CLI registers only the HTTP backend | `no backend supports the URL`; a 40-line harness on `RenderDocument::create()` instead |
