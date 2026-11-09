# art-kit — a filled circle was a plus sign

Date: 2026-11-09 · Repo `drsamonline/art-kit` · PR #4 (open, not merged)
Links taken: none

## What I looked at
`art-kit.js` (552 lines) — palette, canvas primitives, dither, quantise — and
`test-node.js` (86 assertions).

## What was wrong
`api.ellipse` rounded the per-row half-width, so the rasterisation was too fat: a
radius-2 filled circle was `1,5,5,5,1` pixels wide instead of `1,3,5,3,1`. In a
pixel-art kit the ellipse is the shape that has to be right. The existing test
only asserted "has a centre and no corners", which the fat version passes.

## What I changed
`Math.floor` in both passes — a pixel whose centre falls outside the half-width is
outside the ellipse. The r=4 outline tightens with it.

## Evidence
    node test-node.js                        87 passed (new shape assertion included)
    git show HEAD:art-kit.js > art-kit.js    FAIL "a radius-2 filled ellipse is
                                             1,3,5,3,1 wide", 86 passed 1 failed
CI: success.

## What I deliberately did not do
- No change to the two-pass outline union (thicker on the diagonals — separate
  question).
- dither/quantise read and correct as far as I could check; untouched.
- No link work: RgbQuant/quantize/atcq/colorquant/nQuantCpp/hitherdither/dither/
  floyd-steinberg/zimg/matugen are libraries in four languages for what this
  dependency-free kit already does.
- No version bump, no merge.

## Next
Decide on PR #4.
