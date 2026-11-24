
---

# Row 0.5 — the engine was downloading the page's link graph

`tools/dep-cost.cpp` prints every discovered dependency with its resolved URL and where it came from.

| before | |
| --- | --- |
| discovered | **1,324** |
| distinct | 927 |
| duplicates | 397 over 140 URLs |
| most repeated | `Google_Chrome` 47x, `Firefox_version_history` 21x, `Pale_Moon` 19x |

Those are article hyperlinks. `discover_dependencies` took every `href`/`src` in the text with one
regex, so `<a href>` was a dependency.

## Fix one: walk tags

Skip `href` on `<a>`/`<area>`; keep `src` anywhere and `href` on `<link>`. **1,324 -> 102**.

## Fix two: what that exposed

With hyperlinks gone, the render loaded **0** resources - every URL was
`load.php?...&amp;...`. Attribute values were never HTML-decoded, so the page's own stylesheets had
never loaded; the old 188 "successes" were the hyperlinks. Decoding the five URL-relevant entities
took it from 0 to **41 real subresources**.

The page still looks unstyled - 41 stylesheets load, but this engine cannot reproduce Vector 2022.
The win is correct fetches, not fidelity.

## Row 0.6

Rendering `file://<path>` resolves every relative URL against `file://`, so the corpus harness has
never fetched a page's subresources. Every corpus measurement before today exercised markup, CSS and
layout with none of the page's own stylesheets, images or scripts.

## The stale pod

Mid-session the checkout was at `fed64d9c` while `origin/main` was `26a4ee55` - four commits behind.
Work saved as a patch, tree reset to `origin/main`, patch re-applied and rebuilt; the suite run
against the stale tree was discarded. Suite 67/67 twice on the correct base, 125.53 s and 125.82 s.
