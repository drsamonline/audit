# Closed: the `display` row is not reproducible

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `22114c30` (documentation only; tree clean)

Three entries and two wrong attributions went into this row. It closes here with measurements and no
theory.

## The measurement

Raw pixels only — no verdict logic, which is what produced the second retraction.

| Fixture / mode | (200,20) | (600,20) | (200,150) | (600,150) |
| --- | --- | --- | --- | --- |
| plain / `--render` | (0,0,255) | (255,255,255) | (0,0,255) | (255,255,255) |
| plain / `--window` | (0,0,255) | (255,255,255) | (0,0,255) | (255,255,255) |
| extra / `--render` | (0,0,255) | (255,255,255) | (0,0,255) | (255,255,255) |
| extra / `--window` | (0,0,255) | (255,255,255) | (0,0,255) | (255,255,255) |

Identical in all four combinations: the first link occupies x 0-400, the second sits on the next row,
and nothing is painted at x 600. That is correct block layout for two `a{display:block;width:400px}`
elements.

With `--key tab`, three frames:

    frame-1: (200,20)=(0,0,255)      frame-2: (200,20)=(255,0,255)      frame-3: (255,0,255)
             everything else unchanged in all three

So Tab moves focus, `:focus-visible` paints, and the layout never becomes side-by-side.

## Conclusion

The side-by-side render that opened this investigation came from a build that no longer exists. Every
component that could be read — parser, resolver, `matches`, `specificity`, `display_for` — was read and
is correct, which is consistent with the behaviour measured now.

## What this cost, and what it taught

| Step | Outcome |
| --- | --- |
| Entry 1 | claimed the window path dropped the user-agent sheet — **wrong**, retracted |
| Entry 2 | narrowed to "the fixture, not the mode" — right question, no answer |
| Entry 3 | claimed a `:focus-visible` rule was the trigger — **wrong**, from an inverted verdict |
| Entry 4 | this: four combinations, identical, row closed |

Three lessons, all about instruments rather than engines:

1. **Print raw values, never a verdict.** The inverted `side[2] > 200` test labelled white and blue alike.
2. **Two probes, then park.** The row survived four entries because I kept probing instead of closing it
   with a measurement that covered every combination at once.
3. **A single table beats a sequence of experiments.** The final measurement — both fixtures × both
   modes in one run — would have closed this on day one for the cost of one script.

## What I deliberately did not do

- **Did not keep a theory in the row.** It now reads as a closed measurement, so nobody spends a session
  re-deriving it.
- **Did not delete the wrong entries.** They are the evidence for the three lessons above.
- **Did not change code.** Nothing needed changing; the engine was correct.

## Next

1. The mutation counter replacing the DOM fingerprint — a full session, every setter wired.
2. Family P0 builds — still need a machine with dev packages.
3. Symmetric-difference invalidation, once subtree relayout exists.
4. Tests for `:focus-visible`'s text-entry branch, once form controls render.
