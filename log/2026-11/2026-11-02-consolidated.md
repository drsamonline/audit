# 2026-11-02 — Cap raised to 2 GB, and the six stores consolidated

## The limit question

Checked rather than recalled. GitHub's current documented figures:

  * per file: 100 MB, **enforced** (50 MB warns; browser uploads cap at 25 MB)
  * per repository on disk: 10 GB recommended maximum
  * per push: 2 GB, enforced
  * directory width: 3,000 entries; depth 50; branches 5,000

The 800 MB cap was my choice, not GitHub's - about 8% of what is allowed. It predated 7z and
change-triggered backups, and it was the main thing forcing rollovers.

**Both copies of it are now 2 GB.** The consolidation tool had its own hardcoded
`CAP_BYTES = 839 MB`; raising only the backup side would have left consolidation convinced
every store was full, which is exactly why it had been reporting "0 moves" for days.

## What that unlocked

With 800 MB caps, every older store was full and consolidation could move nothing. At 2 GB:

    moves into older stores: 817

## Four cycles, twelve pull requests

Each move is two phases - copy in, then remove the original on a later run once the copy is
confirmed on main - so it took four sweeps:

    cycle 1: 400 copied (218 into dumps, 182 into dumps-2)
    cycle 2: 400 originals removed; 400 more copied
    cycle 3: 400 more removed; 17 left
    cycle 4: 17 removed; 0 moves, 0 duplicates - converged

`dumps` and `dumps-2` are now at the 2 GB cap. `dumps-4` and `dumps-5` are empty: everything
in them had a copy elsewhere.

## What this bought

Six stores became two full ones plus leftovers, so the sweep clones far less and there are
far fewer state files to merge. Total bytes barely moved - consolidation is about shape, not
size - but the estate is now a shape that does not grow a store every day.

## Worth noting

The API's `size` field lags badly: it still reports the pre-consolidation figures. The
tree-based measurement the sweep prints is the honest one.

`dumps-4` and `dumps-5` are empty and could be deleted to reclaim their history. That is
destructive and not done.
