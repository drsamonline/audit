# Aetheris — the focus model, second attempt: the evidence got sharper, the bug did not fall

Date: 2026-11-16 (sixteenth session) · Repo `drsamonline/The_Browser`
Commit: none. Tree left at `8b03b68d`, clean.

Follows `2026-11-16-aetheris-focus-attempt-reverted.md`. That entry said the first move next time was
to instrument the `:focus` branch. That was done, and it moved the diagnosis a long way without
reaching a fix. Reverted again rather than shipping a half-wired feature.

## What I looked at

`The_Browser`: `style.cpp`'s pseudo-class matcher (instrumented with a `fprintf` on a `:focus`
mismatch), the window's `--click`, `--move` and `--key` paths, `node_at`, and
`apply_focus_visual_state`.

## What was wrong

`:focus` still does not paint, and the instrumentation narrowed it to one question.

Three measurements, all on the same fixture and the same coordinates:

| Run | div `#a` pixel | `:focus` branch evaluated? |
| --- | --- | --- |
| `--move 200 80` (`#a:hover` green, `#a:focus` magenta) | **(0,255,0)** — hover painted | **yes**, once, and missed (nothing focused) |
| `--click 200 80` | (0,0,255) — unchanged | **no, never** |
| `--render` with `#a{background}` and `div:focus` | id selectors and layout both correct | n/a |

That pair of rows is the whole finding: **hover evaluates the pseudo-class branch and focus never
reaches it.** Since `apply_focus_visual_state` is called on the click path and the branch is never
evaluated, `set_focused(target)` must be returning false — which it does when the value is unchanged,
i.e. when `target` is null.

So `node_at` returns null on the click path at the same coordinates where `hover_at` — which calls the
same `node_at` — returns the div. That is the next thing to look at, and it is one `fprintf` away.

## What I changed

Nothing. Reverted: `git checkout -- src/main.cpp src/js/js.hpp src/rendering/style.cpp`. Tree clean at
`8b03b68d`; suite unchanged at 59/59.

## Evidence

    hover:  y84=(0, 255, 0)  y184=(0, 0, 255)  focus-diag=1
    click:  y84=(0, 0, 255)  y184=(0, 0, 255)  focus-diag=0

    --render probes:  plain: y50=blue y150=blue     id-selector: y50=magenta
                      (so #a resolves, and both divs lay out where expected)

    git status --porcelain -> 0 lines

## What I deliberately did not do

- **Did not ship.** Third rule in `HANDOVER.md`: leave the tree green, revert what cannot be finished.
  A `:focus` that silently does nothing is worse than none.
- **Did not assert on `relayouts`.** It was 1 with the broken feature; only the pixel and the
  diagnostic told the truth.
- **Did not guess at the fix.** The remaining candidates are (a) `node_at` returning null on that
  path, (b) `relayout()` wiping the interaction state after `dispatch_click_at`, (c) hit-testing
  before layout exists. Each is one print away and guessing between them is how a session gets spent.

## Next

1. Print `target` inside the click block. If it is null, print the hit-test result for the same
   coordinates in both the hover and click paths and diff them.
2. Check whether `RenderDocument::relayout()` passes the interaction state; if it does not, a click
   that both focuses and dispatches will always discard the focus styling.
3. Then re-attempt, with the pixel assertion that has now failed twice.
