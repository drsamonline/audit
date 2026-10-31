# 2026-10-31 — The history is now written down as markdown

## The idea, and what is right about it

    "can we not store history in md files and then delete the record history so it takes
     less space"

Yes for the first half, and it is the right half to do first. A store's git history holds two
different things: the snapshots that are current, and the account of every snapshot ever
taken. The account is worth keeping; it is also most of the weight, because git never
forgets a blob.

## What was built

`forge/tools/dumps-record.py` walks `git log --diff-filter=AD` and writes `HISTORY.md`:

  * every snapshot ever taken, with the commit it held and the date
  * every snapshot ever removed, and when
  * what the store holds right now

It runs inside the sweep, immediately after each store is cloned and BEFORE anything is
removed, and pushes the result to a `history-record` branch so the record survives even if
`main` is later rewritten.

    dumps     HISTORY.md: 3990 lines
    dumps-2   HISTORY.md: 1166 lines
    dumps-3   HISTORY.md:  666 lines
    dumps-4   HISTORY.md:  472 lines
    dumps-5   HISTORY.md:  195 lines

It says plainly in the file what it is not: a record, not a backup. It knows a snapshot
existed and which commit it held; it does not hold the bytes.

## The second half, and why it is only worth doing twice

Compaction means rewriting history to a single commit holding the current tree, then
force-pushing. Old objects become unreachable and the pack collapses. What it would return:

    store      content     pack   after compact   saved
    dumps       788.0M   748.1M         748.1M    +0.0M
    dumps-2     922.0M   688.1M         688.1M    +0.0M
    dumps-3     968.0M   545.4M         545.4M    +0.0M
    dumps-4     320.0M   653.2M         336.0M  +317.2M
    dumps-5       0.0M   196.5M           0.0M  +196.5M

**Three of the five stores are already tighter than a rewrite would make them.** Where the
pack is smaller than the content it holds, git's packing and deduplication are doing better
than a fresh single commit would. Only dumps-4 is history-heavy, and dumps-5 is empty.

So the plan is two stores, not five:

  * **dumps-4** - compact. Returns about 317 MB, the only real win.
  * **dumps-5** - it holds nothing at all. Deleting the repository is simpler than
    compacting it and returns 196 MB.

Both are irreversible: the old objects are gone, and with them the content of every deleted
snapshot. The record survives, the bytes do not. That is the trade, and it needs an explicit
yes.
