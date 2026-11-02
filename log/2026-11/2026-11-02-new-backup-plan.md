# 2026-11-02 — The new backup plan, implemented and verified

## 1. Back up on change, not on a clock — DONE

`state.json` holds the commit each repository was last backed up at. Each run compares the
default-branch head; unchanged means skip. A new tag forces a snapshot anyway.

    seed:   90 recorded up to date, 8 pending
    run 1:  backed up 8 of 98   (skipped 90)
    run 2:  backed up 3 of 98   (skipped 95)
    run 3:  backed up 7 of 98   (skipped 91)
    run 4:  backed up 2 of 98   (skipped 96)

98 tarballs every six hours became 2-8. The 53% duplication stops being created, so the
sweep is now a safety net rather than a shovel.

Seeding matters: the first run would otherwise have re-backed-up everything, which is the
duplication this change exists to stop. A repository whose last push is no newer than its
newest stored snapshot cannot have changed since, so its head was recorded without
downloading anything.

## 2. A restore test that cannot lie — DONE

    day 306 of the year -> restore-testing The_Browser
    PASS  EXACT RESTORE - 28226 files match drsamonline/The_Browser@35d915c file for file

  * `continue-on-error`: a verification bug can no longer paint good backups red. It did
    exactly that for a day on 1 November.
  * It rotates by day of the year across HCS, ziptastic, The_Browser, forge, app-builder,
    today-card, knowledge, registry. First time a 47 MB, 28,226-file repository has been
    restored end to end.

## 3. Retention by age — DONE

`--keep 100` replaced by: every snapshot for 7 days, then one per week for 8 weeks, then one
per month for 12 months. `--keep` survives as an optional hard cap, default off.

Verified against realistic histories: 40 daily snapshots keep 14; 3 snapshots delete nothing;
72 hourly inside three days delete nothing; 24 monthly over two years keep 12.

## 5. Compression — DONE

`-mx=9` was already the top preset. The only headroom was the dictionary, now 256 MB for
inputs over 32 MB and default below that. Measured on the small repositories this run: 14%
and 22% smaller. It will matter on HCS, ziptastic and The_Browser.

## 6. Summary and concurrency — DONE

`concurrency: backup-all` was already there; a job summary now states what the run did and
makes clear that a restore failure is a warning, not a backup failure.

## 4. Sweep without cloning every store — NOT DONE, deliberately

It would save cloning ~3.7 GB every four days. But with change-triggered backups no new
duplicates are being created, so the sweep will usually find nothing to do. Re-engineering
the comparison to work through the API is real complexity for a cost that is now small. The
honest move is to leave it, watch whether the sweep ever finds anything again, and relax the
schedule if it does not. Doing it now would be optimising the quietest job in the system.

## The bugs this work found

  * `dump_blob` raises `SystemExit` on a missing file - right for a dump, fatal for a probe.
    The state reader asked five stores for a file only one had, and the first miss killed the
    run with no traceback. Added `blob_exists()`; the restore test's format probe had the
    same flaw waiting for the first gzip dump it was asked about.
  * `--seed-state` was dispatched after the source repository was split, so it died on
    `a.repo.split("/")` before reaching its own code.
