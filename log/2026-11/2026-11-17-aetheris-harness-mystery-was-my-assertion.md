# Resolved: the harness was right, my assertion was wrong

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `e6c11b6b`

The previous two entries hunted a disagreement between `AetherisWindowScripts` and the CLI. There was no
disagreement. The negative assertion could not pass.

## The bug

```cpp
require(!(off_field[0] > 200 && off_field[2] > 200),
    "a pointer focus elsewhere does not match :focus-visible");
```

White is `(255,255,255)`. `r > 200 && b > 200` is **true for white**. So the assertion meant "the pixel is
neither magenta nor white", and a correct white pixel failed it.

## The measurement that settled it

The harness's exact commands, run by hand, with the frames listed and read:

    --click 60 42    -> frame-1 white, frame-2 magenta, frame-3 magenta
    --click 600 300  -> frame-1 white, frame-2 white,   frame-3 white

Exactly as designed. The binary, the loopback server, the argument splitting and the frame numbering were
all correct, which is what the two earlier probes had already shown one by one.

## The fix

```cpp
auto is_magenta = [](int const (&rgb)[3]) {
    return rgb[0] > 200 && rgb[1] < 100 && rgb[2] > 200;
};
```

Both halves asserted; the comment in the test says why, because this is the **third** time today a colour
check was written as "not white".

## Evidence

    ./build/bin/TestAetherisWindowScripts  -> window scripts: ran, clicked, keyed, hovered, pressed, ticked, laid out, exited cleanly
    ctest -j 8                             -> 100% tests passed out of 59

## The pattern, named properly

| Entry | What was wrong | What was actually wrong |
| --- | --- | --- |
| "the window lays out inline" | the window | my pixel sampling |
| "a :focus-visible rule is the trigger" | the CSS | a verdict my script computed backwards |
| "the harness disagrees with the CLI" | the harness | my assertion matched white |

Three investigations, three times the instrument was at fault and the engine was fine. The engine has not
been wrong once today. Every hour spent reading `style.cpp`, `render_document.cpp` and the test harness was
spent proving code that already worked.

That is worth writing down plainly: **check the instrument before the subject.** A pixel assertion, a
verdict string, a sampling coordinate — these are code too, and they fail silently in the direction that
looks like a product bug.

## What I deliberately did not do

- **Did not delete the three entries.** They are the evidence for the pattern above.
- **Did not add a helper to make colour assertions safer across the suite.** Worth doing, and it is a
  refactor of a test file, not a patch at the end of a session.
- **Did not touch the other three browser repositories.**

## Next

1. A `require_magenta`/`require_not_magenta` helper, so no future case repeats this.
2. Per-node dirty flags, then scoped invalidation.
3. Family P0 builds still need a machine with dev packages.
4. Family docs: the four `HANDOVER`/`AGENTS` files should carry "check the instrument first" next to
   "read upstream first" — they are the same lesson from opposite ends.
