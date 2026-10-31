# 2026-10-31 — dumps-4 compacted: 226 commits to 1

## What ran

`tools/dumps-compact.py` on `dumps-4`, dispatched by hand (`compact: dumps-4`). It never
runs on a schedule and refuses to act on a store without `HISTORY.md`.

    226 commits, 24 repository folders, HEAD 3f91c6a80bb5
    new root commit be1df388546a with 32 files
    HISTORY.md is in the new tree
    force-pushed compact to main. Old objects are now unreachable.
    previous HEAD recorded: 3f91c6a80bb5d1c6760368705dc36daba1145513

The guards held: it refused on the fixture when `HISTORY.md` was missing, and it refuses a
dirty working tree.

## The measurement, which is not a saving yet

    pack before compaction:  653.2 MB
    pack after:              700.4 MB

It went UP. The new root commit writes the current tree as fresh objects, and the old
objects are merely UNREACHABLE - not deleted. GitHub collects unreachable objects on its own
schedule, and there is no API to ask it to. Until that collection happens the store is
bigger, not smaller.

Expected once collected: about 336 MB (content 320 MB plus slack), so roughly 317 MB
returned. That is a prediction from the numbers, not a measurement, and it cannot be
confirmed until GitHub runs gc.

## What this means for the plan

The plan was dumps-4 then dumps-5. It should stop here for now. Compacting dumps-5 before
seeing dumps-4 actually shrink would be spending a second irreversible decision on an
unproven one. When dumps-4's pack drops, the approach is confirmed and dumps-5 can follow.

## What was permanently lost

The content of every snapshot removed from dumps-4 before this point. Not the knowledge -
`HISTORY.md` (472 lines) lists each one with the commit it held and the date. The bytes are
gone and there is no undo.

## Still open

1. Confirm dumps-4's pack falls. If it does not within a few days, compaction does not work
   on this host and nothing else should be compacted.
2. `dumps-5` is empty and holds 196 MB; deleting the repository is simpler than compacting it.
3. A 7z dump still has not been restored end to end.
