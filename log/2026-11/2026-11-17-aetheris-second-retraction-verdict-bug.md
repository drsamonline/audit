# Second retraction: my own script's verdict logic was inverted

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `8e7596d5` (documentation only; tree clean)

The previous entry concluded that "the presence of an `a:focus-visible` rule is what stops `a{display:block}`
applying". That is wrong. It came from a script that printed a verdict rather than the values.

## The bug in my instrument

```python
side = im.getpixel((600,20))
print(f"... -> {'SIDE-BY-SIDE' if side[2]>200 else 'stacked'}")
```

`side[2]` is the blue channel. White is `(255,255,255)` — blue 255 — so the test is true for **white**
and for **blue** alike. Every fixture was labelled "SIDE-BY-SIDE". The raw pixels in the same output
said otherwise:

| Fixture | (600,20) | (200,150) | What it actually is |
| --- | --- | --- | --- |
| `a{display:block;width:400px;height:100px;background:#00f}` | white | blue | stacked |
| `a{display:block;background:#00f;color:#fff}` | blue | white | full-width block, auto height — stacked |
| same + `width`/`height` + `color` | white | blue | stacked |

Two of the three are stacked. The third is a block that fills the width, which is correct block
behaviour, not a side-by-side row.

So the discriminating experiment did not discriminate anything, and the conclusion built on it was
fiction. The only real observation remains the original one: one window fixture renders two
`display:block` anchors side by side, and a very similar one does not.

## What has actually been eliminated

| Candidate | How |
| --- | --- |
| the CSS string reaching the builder | probe: identical on both paths |
| the parser dropping rules | rule-count probe: `a` = 4 decls plain, 5 with colour; UA rules present |
| `display_for` | reads `style.get("display")`, maps "block" to Block, default Block |
| `StyleResolver::resolve` | collects, sorts by specificity then source order, applies — no early exit |
| `matches` / `specificity` | no caching, no shared state; `a` = 1, `a:focus-visible` = 101 |
| the `:focus-visible` matcher | correct in isolation |

Everything readable has been read and is correct. What remains is a difference I have not isolated.

## The rule this adds

**Print raw values, never a derived verdict.** Every retraction today has the same root: I let a script
decide what the pixels meant. A verdict hides the evidence it was computed from; the numbers do not.

    print(pixel)            # yes
    print("SIDE-BY-SIDE")   # no

## What I deliberately did not do

- **Did not run a third attribution attempt.** Two have been wrong; the row now forbids a third without a
  raw-value print.
- **Did not delete the row.** It stays, with the eliminations listed, so the next session does not redo
  six checks that are already done.
- **Did not change code.** Tree clean at `8e7596d5`.

## Next

1. Print raw pixels from **both** fixtures in **both** modes, side by side, before forming any view.
2. If they genuinely differ, print the resolved `display` for `#l1` in each.
3. Otherwise close the row as "not reproducible" and move on — this has now cost more than it is worth.
4. The mutation counter, and the family P0 builds, both remain more valuable than this.
