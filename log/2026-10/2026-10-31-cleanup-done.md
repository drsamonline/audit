# 2026-10-31 — Cleanup done: 1048 snapshots removed, 988 MB off the tree

## The policy, as instructed

    old dumps keep their format (gzip)
    new dumps are 7z -mx=9
    then dedupe, and delete what is not needed

No conversion pass was run. Re-compressing old dumps would commit new blobs while git keeps
the gzip originals in history, so the pack would grow. Measured, rejected, not built.

## What was removed

Two rounds, 14 pull requests, all merged:

    round 1: 513 snapshots   (200 + 36 + 16 + 66 internal, 12 + 94 + 89 cross-store)
    round 2: 535 snapshots   (411 + 2 internal, 39 + 83 cross-store)
    ---------------------------------------------
    total:  1048 snapshots, plus 126 copied between stores as phase-1 moves

## The measurement

    store      start tree   now tree    saved     pack
    dumps         1290.0M     788.0M   +502.0M   748.1M
    dumps-2        939.0M     922.0M    +17.0M   688.1M
    dumps-3        712.0M     968.0M   -256.0M   545.4M
    dumps-4        839.0M     320.0M   +519.0M   653.2M
    dumps-5        206.0M       0.0M   +206.0M   196.5M
    TOTAL         3986.0M    2998.0M   +988.0M  2831.4M

**988 MB off the tree, a quarter of it.** The pack did not move, for the reason measured
earlier: git stores identical blobs once, and history keeps every blob ever committed. The
tree is what a clone checks out and what the sweep walks, and that is now 25% smaller.

`dumps-3` grew by 256 MB because 126 snapshots were moved INTO it by consolidation - the
packing step doing its job. `dumps-5` is now empty: everything in it was duplicated in an
older store.

## A bug the run exposed

Phase 3 failed with `cp: cannot stat ... No such file or directory`: phase 2 deletes
duplicates out of the same checkouts, so a snapshot planned for a move was already gone by
the time the copy ran. It also copied every item in a group from the FIRST item's source
store rather than each item's own. Both fixed; the re-run completed clean.

## Still open

1. `dumps-5` is an empty store holding 196 MB of history. Deleting the repository would
   reclaim that; it is destructive and the owner's call.
2. The pack can only shrink by rewriting history - an orphan branch holding current
   snapshots, force-pushed. That is the last real disk win available and it is a decision,
   not a task.
3. A 7z dump still has not been restored end to end. The restore step starts at the newest
   store, so it will be exercised soon.
