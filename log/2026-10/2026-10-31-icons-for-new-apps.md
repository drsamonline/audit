# 2026-10-31 — Icons for apps that do not exist yet

## What was wrong

The 36 drawn icons fixed today's fleet. They did not fix tomorrow's: a new app scaffolded by Forge
has no `docs/icon.png`, so `make_icons.py` fell back to a monogram - two initials on a coloured
square. The same defect, waiting to reappear on every new repo.

## What I changed

`tools/make_icons.py` now carries a glyph library and a keyword matcher:

    pick_glyph(name, description)  ->  (glyph, colour) or (None, stable colour)

It reads the app's own words - the repo name, plus the `<title>` and
`<meta name="description">` of its landing page - and matches them against ordered keywords:

    invoice/billing/gst      -> receipt     calendar/today/streak -> calendar
    seal/vault/passphrase    -> envelope    encrypt/lock/pin      -> lock
    pdf/document             -> book        repertory/rubric      -> search
    health/bmi/clinical      -> pulse       first aid/triage      -> cross
    sound/audio/mixer        -> wave        dance/rhythm/song     -> note
    poet/rhyme/verse         -> quill       game/arcade/rpg       -> joystick
    shooter/fight/arena      -> crosshair   runner/fast/blink     -> bolt
    city/build/idle          -> city        transfer/share/send   -> transfer
    camera/scan/qr/optical   -> camera      lan/room/wifi/board   -> network
    base/unit/convert        -> grid        memory/flash/revise   -> brain
    skin/derma/track         -> hand        console/cli/forge     -> terminal

Order matters: the specific words are matched before the generic ones, so
`invoice-maker` is a receipt rather than a generic tool. If nothing matches, it returns no glyph and
the monogram still applies - a deliberate floor, not an accident.

Because the match uses the landing page, a Forge-scaffolded app that has a title needs no extra
input and no hand-drawn file. Nothing about Forge itself was touched: this is in the shared kit, so
any app that calls the shared build workflow inherits it.

## Evidence

- `tests/test_glyph_pick.py` added, written as `unittest` so the kit's CI (`unittest discover -s
  tests`) actually finds it - my first version used bare functions and would never have run.
- Four tests: obvious names map to obvious glyphs; an unknown app returns no glyph but a stable
  colour; every glyph draws at 48/64/192; the description alone is enough when the name is generic.
- `python3 -m unittest discover -s tests -v` -> 4 tests, OK.
- Kit CI (`tests.yml`) ran green on the commits that carried the change.
- End-to-end: a fake app with only a landing page title ("Invoice Maker - GST billing") and no
  artwork produced a green receipt icon through the normal `--ico` / `--res` path.

## What I deliberately did not do

- **Did not invent a glyph for an app whose words match nothing.** Falling back to a monogram is
  honest; guessing a picture is not.
- **Did not add a dependency.** Primitives drawn with Pillow, no SVG renderer, no cairosvg, no
  system graphics library in CI.

## Next

1. **The pin.** The generator lives at `a17fc371` and later. Apps pinned below that - all 35 that
   are not `today-card` - will not see it until their pin moves. New apps must pin at or after it to
   inherit the behaviour.
2. Bump the fleet to the current head, which delivers both the glyph generator and the pinned-kit
   fix in one move.
3. Item 9 of the original requirements list - still unknown.
