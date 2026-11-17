# Aetheris — the five attribute selector operators

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `261feebe`

## What upstream supports

`[a]`, `[a=v]`, `[a~=v]`, `[a|=v]`, `[a^=v]`, `[a$=v]`, `[a*=v]`, plus a case-sensitivity flag and
namespaces.

## What shipped

All six forms without the flag or namespaces. The requirement became a small struct with an operator
rather than a name/value pair, so matching is a `switch` and each operator's rule is one readable case:

| Operator | Meaning |
| --- | --- |
| `~=` | a whitespace-separated word equals the value |
| `\|=` | equals, or starts with the value followed by `-` |
| `^=` | prefix |
| `$=` | suffix |
| `*=` | substring |

## Evidence — both directions for each

Ten rows on one page, 60 px each:

    [class~=note]  note   -> magenta      noted  -> blue
    [lang|=en]     en-GB  -> magenta      eng    -> blue
    [href^=https]  https  -> magenta      http   -> blue
    [href$=.png]   .png   -> magenta      .pngz  -> blue
    [href*=mid]    a-mid  -> magenta      a-b    -> blue

    ctest -j 8  ->  100% tests passed out of 59

## The failure on the way

The fixture first used 100 px rows: ten of them are 1000 px tall, the frame is 768, and the last rows fell
outside it, so `frame_pixel` refused to read and the assertion said "operator row readable". The fix was to
shrink the rows, not to skip the rows that did not fit — a test that quietly checks eight of ten cases is
the kind of thing this project has already been burned by.

## What I deliberately did not do

- **Did not implement `[a=v i]`.** One flag, no page in the fixtures needs it, recorded as a limit.
- **Did not implement namespaces.** No XML in this engine.
- **Did not start incremental layout.** It was the other candidate for this pass and it is a
  multi-session project; the operators finish a story instead of opening one.

## Next

1. Per-node dirty flags **with** incremental layout — a session of its own.
2. Family P0 builds, on a machine with dev packages.
3. `[a=v i]`, if a page needs it.
