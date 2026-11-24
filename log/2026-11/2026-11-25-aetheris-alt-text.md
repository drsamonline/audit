# Aetheris — an image that fails to load now paints its alt text

**Row:** `0.12`. **Date:** 2026-11-25.

The reference render left one large difference: the header. Chromium puts the Wikipedia wordmark and
account links in the top 46px; the engine painted an empty strip.

`tools/article-position.cpp --top` (new) lists every layout node starting above a given y, in document
order, and settled it in one run:

- the header **is** laid out — `div` flex at y=0 h=66, `header` at y=0 h=66 w=949;
- the logo images **are** laid out — `img y=14 h=22 w=140`, `img y=41 h=11 w=140`;
- they are never painted, because their URLs (`/w/skins/...`) do not resolve when the page renders from
  a local file.

Chromium, in the same situation, draws the **alt text** — which is why the reference shows "Wikipedia"
and "The Free" where the logo would be. The engine drew an empty box.

`RenderTree` now emits a `DrawText` with the `alt` attribute when an `<img>` has no loaded image, using
the element's own font size and colour, and nothing when there is no `alt`.

| | before | after | chromium |
| --- | --- | --- | --- |
| failed logo | empty box | "Wikipedia" / "The Free Encyclopedia" | "Wikipedia" / "The Free" (clipped) |

## A note on the metric

Pixel agreement barely moved: 76.9% → 76.6%. The header is a small area, so a whole-viewport percentage
cannot see it. The picture is the better evidence here — the metric is a guide, not a verdict.

Suite 67/67 twice, 122.48 s and 122.69 s.
