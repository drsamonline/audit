# 2026-11-01 — Compaction checked: it worked, and the store grew for a different reason

## The check

Yesterday `dumps-4` was compacted: 226 commits to 1. The pack went 653.2 -> 700.4 MB, which
looked like a failure. A day later it reads 929.8 MB, which looks worse.

It is not. The right measure is not the pack on its own, it is the pack against the content
it holds - the difference is waste, the history that has not been collected.

    at compaction:   content 320.0M   pack 653.2M   waste 333.2M
    now:             content 840.0M   pack 976.3M   waste 136.3M

**Waste fell by 197 MB.** GitHub collected most of the unreachable objects. The store grew
because it took on 520 MB of NEW snapshots in the meantime - it is the active store, and the
backup workflow has been writing to it all day.

## Every store, now

    store       content      pack     waste
    dumps        941.0M    896.0M     +0.0M
    dumps-2      922.0M    688.2M     +0.0M
    dumps-3      968.0M    921.7M     +0.0M
    dumps-4      840.0M    976.3M   +136.3M
    dumps-5      136.0M    196.5M    +60.5M
    TOTAL       3807.0M   3678.6M

Three stores have NO waste at all: their pack is smaller than the content they hold, because
git packs and deduplicates better than a rewrite would. Compacting them would gain nothing
and would destroy history for free.

## The store survived

  * `HISTORY.md` is on main, 38,381 bytes
  * main is taking new `backup:` commits normally - the force-push broke nothing
  * 24 repository folders and 32 files in the root commit, as reported at compaction

## Correction to yesterday's plan

I said `dumps-5` was empty and should be deleted for 196 MB. **It is not empty any more** -
it holds 136 MB of snapshots, because the stores roll over and it is in use. Deleting it
would have destroyed live backups. It has 60.5 MB of waste and is the only other candidate
for compaction, and that is worth far less than the risk of getting it wrong.

## Verdict

    compaction: works. ~197 MB returned on dumps-4, measured, not predicted.
    further:    not worth it. Only 60.5 MB of waste remains anywhere.
    dumps-5:    NOT to be deleted. It is live.
