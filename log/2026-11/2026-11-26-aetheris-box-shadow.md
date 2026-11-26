# Aetheris — a box-shadow is a list, and an outer shadow stays outside its box

**Row:** `0.14` closed. **Date:** 2026-11-26.

The per-band agreement table built for row 3m left one band at 22.9% — a black rectangle about 45px tall across
the page, with the article's own title inside it. It was not a layout defect: `main#content` was at y=546 and so
was the title.

## The instrument that named it

`tools/article-position.cpp` answers "where is this box"; nothing answered "what painted it". A 40-line probe
that prints every paint command landing in a y band did, in one line:

```
DrawShadow  x=24.0 y=546.4 w=976.0 h=40.6  color=black
DrawShadow  x=24.0 y=587.0 w=976.0 h=34.0  color=black
```

Two shadows, black, on boxes whose CSS says `box-shadow: none` and `box-shadow: 0 1px #c8ccd1`.

## Two defects in one feature

| | rule | what the engine did |
| --- | --- | --- |
| the value | css-backgrounds-3 §7.2 — a list; `none` is the empty list; the colour is optional, may appear anywhere in it, and defaults to `currentColor`; two lengths minimum | read positionally as `x y blur colour`, colour defaulting to black, so `none` became an opaque black rectangle and `0 1px #c8ccd1` put the colour in the blur slot |
| the shape | §7.2.1 — an outer shadow is not painted inside its border box | filled the whole offset rectangle, which put a grey band across a toolbar whose box has no background of its own |

Upstream keeps the first shape literally: a list of `ComputedShadow` values each carrying its own colour and
placement, empty for `none` (`Rust/src/css/computed_value_types.rs:1052`, `:1069`).

## Measured

| | before | after |
| --- | --- | --- |
| pixel agreement | 80.4% | **88.8%** (43,623/49,152) |
| title bar | 976x78 black | white, title in black |
| toolbar | black, then a grey band | white with a 1px line |

Suite **67/67 twice** (196.89 s, 186.03 s). Both halves are pinned in `AetherisAdvancedPainting` and each was
proved to fail without its own fix.

## The assertion that could not fail

The clipping case took three attempts. As a document render it passed on the unfixed engine, because a box with
its own background paints over its shadow — the case that separates right from wrong is a box with **no**
background, which is the toolbar's. It now calls `draw_shadow` on a bare surface, where the answer cannot be
confused with "nothing was painted".

## What it cost

Three pods. The first could not spawn a compiler; the second could not fork to push; the third came back with an
empty `/scratch/work` and rebuilt from the patch. The work survived only because it had been delivered as a patch
— the project's assumption that `/scratch/work` survives a recycle is wrong, and now says so in the handoff.

## Left

Row **0.15** — the same page, one level down: the article starts 410px too low because `nav#mw-panel-toc` is laid
out in the content flow. The cause is one declaration, proven with two fixtures: `.mw-page-container-inner`'s
`grid-template` **shorthand** is not parsed (longhand puts two grid children at x=0/100, the shorthand at
x=0/1024), so there are no tracks and no named areas.
