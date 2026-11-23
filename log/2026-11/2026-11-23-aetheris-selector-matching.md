# Aetheris — the style pass was re-parsing every selector for every node

**Row:** `3j` in `drsamonline/The_Browser` `docs/CHECKLIST.md`.
**Date:** 2026-11-23. **Commit:** the one that carries this entry.

## What was claimed, and what was measured

Row 3j said layout costs "~0.8 ms per element, and far worse on real markup", and told the next session to
profile before touching anything. Profiling split the three stages of building a document:

| document | parse | style | layout |
| --- | --- | --- | --- |
| 400 empty divs | 15.5 ms | **392 ms** | 34 ms |
| 800 empty divs | 19.6 ms | **514 ms** | 49 ms |
| 800 divs with text | 37.4 ms | **1089 ms** | 333 ms |

The row's premise held, but its label was wrong: this was never a layout cost. Style resolution was 10-20x
geometry at every size. A second sweep varied only the number of author rules, and style cost tracked
**rules x nodes** - 445 ms at 0 rules, 3862 ms at 800 rules, a slope of 10.6 us per (rule x node).

## The cause

`StyleResolver::matches_simple` took the selector as text and re-parsed it on every call, allocating five
containers and re-scanning the characters into them - work that depends only on the selector, redone once per
node. `matches()` additionally scanned for a combinator with a lambda that re-walked the selector from index 0
for every character: O(n^2) in selector length, per node per rule. Specificity was re-scored from the same
text on every match.

Upstream parses a selector into an object once (`LibWeb/CSS/Selector.h`) and matches that object
(`LibWeb/Rust/src/css/dom_selector_matching.rs:1262`). The fix ports that shape rather than inventing one.

## What was fixed

1. Selectors are parsed once, when the stylesheet is parsed (`src/rendering/selector.cpp`,
   `CssRule::compiled`). Matching walks the parsed compound; specificity comes with it.
2. `StyleProperties::fingerprint()` was rebuilt per node - a string per property, sorted, joined - because
   layout asks every node for its parent's digest. It is cached now, invalidated by `set()`.
3. The class test built an `istringstream` and a `vector<string>` from the `class` attribute per rule x node.
   It scans for word boundaries in place instead. `[a~=v]` likewise.

Fixes 2 and 3 were found by re-running the probe after fix 1 and noticing the per-node cost had barely moved.

## Result

| case | before | after |
| --- | --- | --- |
| 400 empty divs, style | 392 ms | **98 ms** |
| 800 empty divs, style | 514 ms | **201 ms** |
| 800 divs with text, style | 1089 ms | **446 ms** |
| 800 author rules, style | 3862 ms | **933 ms** |

0.8 ms per element became 0.24 ms. The suite's own wall clock fell from ~400 s to **141.52 s / 139.62 s**,
`WindowGeometry` from 177 s to 81 s, with 66/66 green twice.

## What is not fixed

The per-node `StyleProperties`: an `unordered_map<string, string>` filled by ~80 string insertions for every
node. It is now most of what remains of the style pass. Row 3j stays `[~]` in progress rather than `[x]`.

## The mistake

The refactor was first assembled by slicing the original file with hand-computed line ranges; two were off by
one, and regenerating from `git show HEAD:` silently reverted two earlier edits. Both were re-applied and
grepped before building. Print and read the boundary before slicing source by line number.

---

# Addendum — the second term, and a fix that measurement rejected

Row 3j stayed `[~]` after the selector work, naming the per-node `StyleProperties`. This addendum
measures that term. **No engine code changed**: the fix that looked obvious measured worse.

## What a style is

`tools/style-cost.cpp` counts what a resolved style holds and splits the resolve.

| measurement | value |
| --- | --- |
| properties in a resolved style | **17** (the previous entry's "~80" was a guess) |
| resolve, full sheet | 0.114 ms per element |
| resolve, sheet with no rules at all | 0.074 ms per element — **65%** |
| so selector matching | 0.040 ms per element — 35% |

The property work is not a remainder; it is the larger half of what is left.

## The rejected fix

The map rehashes as it grows, so reserve it. Priced alone: 0.039 ms per style, 0.005 ms with
`reserve(24)` — 8x on the component that is 65% of the cost.

Built alternately, five runs each, on the targeted measure:

| build | runs | median |
| --- | --- | --- |
| with `reserve(24)` | 0.068 / 0.063 / 0.069 / 0.064 / 0.059 ms | 0.064 ms |
| without (HEAD) | 0.048 / 0.048 / 0.075 / 0.047 / 0.048 ms | **0.048 ms** |

The reserve is **33% slower**. `StyleProperties` is not one object per element: text nodes, generated
boxes, pseudo-element styles and the temporaries inside `apply_declaration` all construct one, and
most hold a property or two. Reserving 24 buckets makes every one of them pay for a table it never
fills, which costs more than the rehashes it saves on the styles that reach seventeen.

Reverted; `git status` clean before the commit.

## What is left

Structural, not tuning: a style is seventeen string-keyed inserts into a hash map. The honest fix is
a typed property set or interned property ids, touching every consumer of `StyleProperties`.

## The measurement discipline this bought

Identical suite runs: 126.97 s and 164.79 s back to back. One probe line: 0.047 to 0.075 ms across
five runs. Anything smaller than ~20% is not measurable on this box — which is why the decision came
from an alternating build rather than a single before/after pair, and why it went against the
prediction.
