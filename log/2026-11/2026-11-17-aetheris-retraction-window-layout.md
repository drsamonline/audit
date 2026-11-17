# Retraction: the window does not lay block elements out inline

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commits: `26e4f145` (the wrong claim), `a269bf59` (this retraction)

The previous entry, `2026-11-17-aetheris-window-lays-out-inline.md`, claimed the window path renders
pages without the user-agent stylesheet, so block elements lay out inline. **That claim is wrong.** It
is retracted here, in the handover, and in the commit history.

## What I actually measured this time

I rendered the window frame to PNG and looked at it, which the handover has asked for since the first
session and which I had been skipping in favour of sampling pixels.

The frame shows **two divs stacked correctly**: "A" at the top, "B" below, each 400 px wide and 100 px
tall. Their backgrounds are the same colour and there is no margin between them, so the two rectangles
merge into one visually continuous blue block 400 x 200.

And the probe that the previous entry said was "next" was run:

    --render : [probe] sheet: css=63 combined=1729
    --window : [probe] sheet: css=63 combined=1729      <- same page build
               [probe] sheet: css=0  combined=1666      <- the chrome document

The page is built with the same sheet on both paths, user-agent stylesheet included. The second build
is the chrome, which legitimately has no author CSS.

## How the wrong conclusion was reached

| Step | What happened |
| --- | --- |
| Fixture | two 400x100 divs, identical background, no margin |
| Sampling | I read single pixels at (200,50), (200,150), and a horizontal row at y=60 |
| Misreading | the merged block made "blue at x=420" look like two boxes side by side, and the second div's text at y~140 with blue behind it was read as "nothing at y=150" |
| Leap | from two misread samples to "the UA stylesheet is missing", then to a confident handover row |

The experiment that "confirmed" it — adding `display:block` and seeing the window become correct — was
not a control at all: with `display:block` the divs also had **different** geometry in my sampling, and
I attributed the change to the property rather than to my own sampling.

## What survives from that session

Nothing about layout. The `keyup` fix from `fb956755` is unaffected and still verified. The Tab order
revert stands, but its cause is **not** the layout: Tab moved focus (`relayouts` changed) and
`:focus-visible` did not paint, and that remains unexplained and unexplained by this.

## What I changed

- `docs/HANDOVER.md`: the wrong row is replaced with a corrected note that says the claim was wrong and
  points at this entry, rather than deleted. A question that was asked and answered should stay answered.
- No code changed. `src/rendering/render_document.cpp` was restored to `HEAD` after the probe.

## The rule this adds

**Look at the frame before concluding from pixels.** Three of this project's investigations have now
gone wrong the same way: a numeric sample was treated as a picture. `--render-window` and the frame
directory exist precisely so a human (or a model) can see the page; sampling three coordinates is not
seeing it.

## Next

1. Re-attempt Tab with a **one-element** fixture, and look at the frame rather than sampling it.
2. If `:focus-visible` still does not paint, print the state the cascade receives against the state the
   window set — the control experiment that found the `relayout()` bug.
3. Scoped style invalidation from `invalidate_style_after_pseudo_class_state_change`.
4. Family P0 builds still need a machine with dev packages.
