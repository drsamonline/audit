# Aetheris — a reference render, because the numbers ran out of expectations

**Row:** `0.11` opened. **Date:** 2026-11-25.

The week of 2026-11-23 found seven defects, every one because a number contradicted an expectation. By
the end the expectations were the scarce thing: the page rendered, and nothing could say whether it
rendered *right*.

## Chromium was already in the sandbox

So the reference is a real browser. `tools/reference-render.sh` builds one self-contained document
(stylesheets inlined, scripts dropped, so neither side needs the network), renders it in chromium and in
the engine at 1024x768, and reports sampled pixel agreement plus where rows of link-coloured text land.

## First result

| | |
| --- | --- |
| pixel agreement, `en.wikipedia.org/wiki/Web_browser` | **44,390/49,152 = 90.3%** |
| contents-list spacing, chromium | **27-28 px** |
| contents-list spacing, engine | **79-80 px** |
| a minimal `<ul><li>` in both | **99.8%**, 19-20px both sides |

The largest visible difference is a spacing rule on the contents list applied at roughly three times its
size - and it is not list layout in general, since the minimal list agrees almost exactly. That 79px is
what pushes the article below the fold, which is what every screenshot this week has been showing.

## What it changes

Each defect so far was found by noticing something odd. From here the question is a number that moves:
90.3% today, and whatever it is after the next fix. One minute per page.

## Next

Extend `tools/article-position.cpp` to report the rules that set margin/padding/line-height for a node
named on the command line, and ask it about a contents item.

---

# Row 0.11 narrowed — an anonymous 16.8px line box

The reference said the contents list sits 79-80px apart where chromium puts it 27-28. The probe now takes
`id=<id>` or `tag=<tag>` and prints the node's box, its children (`display`, `line-height`, height) and
the rules that change it.

## Ruled out

| question | answer |
| --- | --- |
| a margin on the list item? | No - the rules add only `margin: 0.2em 0`, ~3px |
| the anchor inside? | No - `<a>` is 45.6px in a 79.2px item |
| list layout in general? | No - a minimal `<ul><li>` agrees with chromium at 99.8% |
| whitespace text nodes? | No - skipping them changed nothing; reverted |

## Found

A 156-byte fixture reproduces it: `<li>` holding one block `<a>` is **33.6px where chromium gives
16.8** - exactly double. The children print shows the `<li>` has a **second inline child of 16.8px with
no DOM tag at all**: a line box with no node behind it. The suspect is the tail of
`layout_inline_children`, `cursor_y = std::max(max_bottom, cursor_y + line_height)`, which adds a line
whether or not anything was placed on it.

## Reverted

Skipping whitespace-only text nodes did not move the number (33.6 either way), so it was reverted rather
than shipped. A plausible change that leaves the measurement identical is a guess - and this engine has
already been bitten by one (the `reserve(24)` that measured 33% slower).

---

# Row 0.11 closed — the double line, and a metric that went the wrong way

The suspect was the tail of `layout_inline_children`:

```cpp
cursor_y = std::max(max_bottom, cursor_y + line_height);
```

It closed an open line unconditionally. After a block-level child `cursor_y` is already that block's
bottom, so the tail added a second line: every block inside an inline formatting context was counted
twice. A `<li>` holding one block `<a>` measured **33.6px where chromium gives 16.8**. The function now
tracks whether a line is open.

| | before | after | chromium |
| --- | --- | --- | --- |
| `<li>` with one block line | 33.6px | **16.8px** | 16.8px |
| contents-list spacing, real page | 79-80px | **28-29px** | 27-28px |

## The metric went down while the layout got better

Pixel agreement fell **90.3% -> 76.9%**. Not a regression — the earlier score was mostly blank page
matching blank page, and compacting the list moved real text where the reference has the article. A fix
that brings content into view will often lower this number.

The tool prints both, and they must be read together: agreement says "same content in the same place",
row positions say "is the spacing right". A single percentage would have made this commit look like a
regression.

## Left at the top

The header (logo, account links) renders as an empty strip where chromium puts it at y=16-46 — now the
largest remaining difference.

Suite 67/67 twice, 122.29 s and 122.09 s.
