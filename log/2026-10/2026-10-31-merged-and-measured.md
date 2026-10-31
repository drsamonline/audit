# 2026-10-31 — Merged, measured, and the restore test finally works

## Merged

| Repo | PR | Result |
|---|---|---|
| dumps | #3 | merged `1b677e9f` |
| dumps-2 | #1 | merged `1d64ab3c` |
| dumps-2 | #3 | merged `8aced2ca` |
| dumps-3 | #1 | merged `977b7271` |
| dumps-2 | #2 | merged `41458101` |

600 snapshot directories removed: 200 + 200 + 126 + 74.

## The honest measurement, which is not what was hoped

    disk (API) before the merge:  2301.4 MB across 4 stores
    disk (API) after:             2497.9 MB across 5 stores

**Disk did not go down, and dedupe is not why it should have.** Git stores a blob once per
CONTENT. Every snapshot the sweep removed was byte-identical to one that stays, so it was
never occupying separate space - the merge deleted references, not bytes. The blob stays
because the keeper still points at it. Meanwhile the test runs kept adding snapshots and a
fifth store appeared, so the total grew.

What dedupe actually buys is a smaller TREE: fewer directories to walk, faster clones, and a
history a person can read. That is worth having; it is not space.

**Where space actually came from is 7z**, and that is real:

    HCS        133.78 -> 109.08 MB   18%
    ziptastic  133.92 -> 109.18 MB   18%
    HMS          0.67 ->  0.48 MB    28%
    BLINKTRANSFER 0.18 -> 0.14 MB    23%

Those are new snapshots. The older gzip ones keep their size until they age out.

## The restore test was broken, and had been all along

I added a step that proves one dump restores on every run. It failed immediately:

    FAIL  this dump holds drsamonline-today/card, not drsamonline/today-card

The dump was fine. `parse_tarball_root` split GitHub's `<owner>-<repo>-<sha>` directory on
the last TWO hyphens, so `drsamonline-today-card-<sha>` became owner `drsamonline-today`,
repo `card`. **Every repository with a hyphen in its name failed the restore test** - and
that is most of them - with a message blaming the dump.

Fixed: split off the sha (which never contains a hyphen), then match the known owner prefix
rather than guessing where the boundary is. Verified against `today-card`, `forge` and
`MATERIA-MEDICA-BUILDER`.

## Restore is now proven

    --- restore test against dumps-4 ---
    unpacks clean (gzip CRC verified): 10 files, taken at 086a8fc
    PASS  EXACT RESTORE - 10 files match drsamonline/today-card@086a8fc file for file
    restore verified from dumps-4

That is the last link in the chain that was unproven: a dump written weeks ago, read back
out of a store, compared file by file with the commit it names.

## Still to prove

The restore above was a gzip dump. No 7z dump has been read back out of a store yet - the
round trip is verified at write time, but an end-to-end restore of a `.tar.7z` has not been
run. The restore-test step now starts at the newest store, so the next few runs will hit one.
