# Aetheris — form controls render as visible boxes

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `0fe673cf`

## What upstream does

`LibWeb/CSS/Default.css`:

```css
input:not(...), textarea { border: 2px inset ButtonBorder; padding: 1px 3px; background-color: Field; color: FieldText; }
button, input[type=submit], ..., select { padding: 1px 7px; background-color: ButtonFace; border: 2px outset ButtonBorder; }
```

## What was wrong here

Aetheris already had `input, textarea, select, button { display: inline-block; }` and nothing else, so a
text field was an inline-block with no border, no background and no content box worth seeing. It painted
white on white. That is also why an earlier session recorded "an `<input>` paints blank white" and
concluded the text-entry focus branch could not be tested.

## What shipped

The same shape, in the subset this engine supports:

```css
input, textarea, select, button {
    display: inline-block; border: 1px solid #999999; padding: 1px 3px;
    background-color: #ffffff; color: #000000; min-width: 8em; min-height: 1.2em;
}
button, select, input[type=submit], input[type=button], input[type=reset] { background-color: #efefef; }
```

System colours (`Field`, `ButtonFace`, `ButtonBorder`) and `inset`/`outset` borders are not supported
here, so the palette is fixed values. The shape is upstream's; the colours are not, and the comment in
the source says so.

## Evidence

    input at (20,8): (255,255,255)   <- a white field, previously indistinguishable from the page
    button at (20,40): (239,239,239) <- #efefef, the ButtonFace stand-in
    full suite: 100% tests passed out of 59

## What this did not prove, and why I stopped

The `:focus-visible` text-entry branch was the point of the exercise. Clicking the input paints it
magenta — but so does clicking 580 px away from it:

    click-input:      (20,8)=(255,0,255)
    click-elsewhere:  (20,8)=(255,0,255)

The input appears to span the line (inline-block with `min-width` and no intrinsic width), so both clicks
land on it. The control case does not discriminate, therefore the branch is **still unproven**, and the
handover says so rather than counting the magenta as a win.

This is the fourth time today a measurement has been one control away from being wrong. Stopping here
instead of adding a fifth probe was the point of the two-probe rule.

## What I deliberately did not do

- **Did not give the input a fixed width to make the control work.** That is the right next step, but it
  is a separate change and this commit is already a visible, verified improvement.
- **Did not claim the text-entry branch.** Magenta without a discriminating control is not evidence.
- **Did not implement value editing, caret or click-to-type.** Rendering is the box; interaction is a
  project.
- **Did not touch the other three browser repositories.**

## Next

1. Give `input` a fixed intrinsic width (`width: 12em`), then re-run the click pair — the control should
   finally discriminate.
2. Then the text-entry branch test, which has been unproven since `4388fef3`.
3. Per-node dirty flags, then scoped invalidation.
4. Family P0 builds still need a machine with dev packages.
