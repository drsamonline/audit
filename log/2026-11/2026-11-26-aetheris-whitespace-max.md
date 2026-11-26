# Aetheris — a page's indentation is not its content

**Row:** `3m` closed, and `3l` with it. **Date:** 2026-11-26.

Row 3l said `.vector-header-end` does not push its content to the right edge. It does: the element fills 602.7px
from x=349.3 and its `nav` child reaches x=952, the right edge. What was wrong was one level deeper.

## The number that explained it

`nav.vector-user-links` carries `justify-content: flex-end`, and its content sat at the left edge because there
was **no free space to distribute**: the nav's own base size was **615.42px, of which 423.23px was content**. The
other 192px was six runs of white space at 28.83, 38.44, 28.83, 28.83, 38.44 and 19.22px.

`max_content_width` measured a run of white space at its untransformed text - a `"\n"` is 9.61px, `"\n\t\t\t"`
28.83px - so every container's base size carried its markup's indentation. Row 3l was row 3m.

## The rule, from the spec and from upstream

A run of white space adds **nothing** inside a container that lays out a row of items: it generates no item at
all (css-flexbox-1 §4, the rule the previous commit applied to the minimum), so it adds nothing to the maximum
either. Anywhere else it is **one space**, which is what css-text-3's collapsing leaves; upstream keeps a
collapsed run as a single item and drops it when the line is empty or already ends in white space
(`inline_formatting_context.rs:2931`, `:4546`).

## Measured

| | before | after | chromium |
| --- | --- | --- | --- |
| `nav.vector-user-links` x | 386.3 | **752.2** | links at 800-990 |
| its max-content | 615.42 | **199.84** | — |
| header row | 1,432.9px in 901.3px | **932px in 928px** | — |
| document height | — | **33px shorter** | — |
| fixture: newlines around a 20px box in a flex row | 39.22 | **20.0** | 20 |

Suite **67/67 twice**. The new assertion was proved to fail on the unfixed engine before it was trusted.

## Two numbers moved the wrong way, and they are not wins

Agreement **81.2% → 80.4%**, overflows **137 → 139**. Per band: the header improves (88.0 → 88.7) and the upper
page improves (94.9 → 97.0), while y 512-576 falls 85.1 → 46.4 and y 640-704 rises 46.2 → 67.2. The 33px shift
moved a **pre-existing black title bar** - painted black, and placed ~410px below where chromium puts it - across
a band boundary. That rectangle is now row 0.14 and is the worst band on the page by a factor of two.

**The lesson: a whole-page percentage is dominated by whichever single defect is biggest, so it cannot judge a
row that does not touch that defect.** The numbers that judge this one are the nav's x, its base size, and the
fixture.

## What the environment cost

The pod this was written on filled its process table with 10,084 unreaped zombies under PID 1 and could no longer
spawn `zig` at all - compiles and links both died with `failed to spawn: SystemResources`, and there was no
crt1.o, no compiler and no zig cache on the filesystem to link by hand. Nothing unverified was committed; the
change was delivered as a patch and finished after a recycle, where every number above was reproduced before the
commit. The recycle also **emptied `/scratch/work`**, which the project had assumed survived - worth knowing.
