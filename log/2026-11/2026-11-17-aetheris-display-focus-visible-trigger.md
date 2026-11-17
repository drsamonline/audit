# Aetheris — the `display` bug is triggered by a `:focus-visible` rule

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `da0f1ab` (documentation only; tree clean)

Follows `2026-11-17-aetheris-display-bisect-open.md`. That entry left two candidate declarations and no
theory. One rule-count probe and one discriminating run have replaced both with a single trigger.

## What the rule-count probe showed

Both fixtures parse identically and correctly:

    plain:  rules=37   rule[36] sel=a  decls=4
    extra:  rules=38   rule[36] sel=a  decls=5   rule[37] sel=a:focus-visible  decls=1

So the parser is not dropping anything, the UA sheet is present (rules 0-35), and the author rules are
there in order. The CSS string reaching the builder was already known to be identical.

## What the discriminating run showed

Three fixtures, same page, `--render`:

| Author CSS | (600,20) | (200,150) | Reading |
| --- | --- | --- | --- |
| `a{display:block;width:400px;height:100px;background:#00f}` | white | blue | stacked |
| `a{display:block;width:400px;height:100px;background:#00f;color:#fff}` | white | blue | stacked |
| same + `a:focus-visible{background:#f0f}` | **blue** | **white** | side by side |

The declarations are not the trigger. **The presence of an `a:focus-visible` rule is.**

That points at code added this week: the `:focus-visible` branch in `style.cpp` and the `FocusTrigger`
field. The matcher reads correctly in isolation — `if (focused != &node) return false;` then the
text-entry / keyboard-trigger test — so the fault is most likely in how the cascade handles a selector
whose pseudo-class needs interaction state:

1. `if (!interaction_state) return false;` runs **before** the pseudo-class checks. Initial layout has
   no interaction state, so every `:focus-visible` rule is skipped there — which is correct, but worth
   confirming that the skip does not abort the element's cascade.
2. Specificity ordering: a rule that cannot match may still be participating in the sort.

## What I did not do

- **Stopped at two probes.** The rule this project adopted after three retractions: two probes per
  question, then park it with the measurements. This is probe two.
- **Did not guess between the two candidates.** Each is one print away (the resolved specificity list
  for `#l1`, and whether the cascade continues past a non-matching pseudo-class).
- **Did not change code.** `src/rendering/render_document.cpp` was restored after the probe;
  `git status --porcelain` is empty.

## What this is worth

The next session starts from "a `:focus-visible` rule in the sheet stops `a{display:block}` applying",
with the parser and the CSS string eliminated, and two named candidates in a specific function. That is
a two-print fix, not an investigation.

## Next

1. Print the ordered rule list `StyleResolver` applies to `#l1` for both fixtures.
2. Confirm the `!interaction_state` early exit does not abort the cascade for that element.
3. Then the fix, in its own commit, with a fixture that would have caught it.
