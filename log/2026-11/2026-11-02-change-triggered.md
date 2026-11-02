# 2026-11-02 — Steps 1 and 2 of the new backup plan, live and verified

## Step 1: back up on change, not on a clock

`state.json` records the commit each repository was last backed up at. Each run asks for the
default branch head - two cheap calls - and skips a repository whose commit has not moved.
A new tag forces a snapshot even when the code is identical, because a release is the thing
you would look for later.

Seeded without downloading anything: a repository whose last push is no newer than its newest
stored snapshot cannot have changed since, so its head was recorded. That avoided a first run
that would have re-backed-up all 96.

    seed:  90 recorded as up to date, 8 pending
    run 1: backed up 8 of 98  (skipped 90 unchanged)
    run 2: backed up 3 of 98  (skipped 95 unchanged)

Down from 98 tarballs every six hours to 3-8. The 53% duplication measured earlier stops
being created, so the sweep becomes a safety net rather than a shovel.

### The bug that cost a run

`dump_blob` raises `SystemExit` when a file is absent - correct for a dump it was told to
read, fatal for a probe. The state reader asked all five stores for a `state.json` that only
one of them had, and the first store without one exited the process silently with code 1: no
traceback, no message, just a red run. Added `blob_exists()`, a probe that never raises, and
the restore test's format check now uses it too - it had the same flaw waiting for the first
gzip dump it was asked about.

## Step 2: the restore test can no longer lie

    day 306 of the year -> restore-testing The_Browser
    restore test: dumps-5/.../The_Browser.tar.7z
    unpacks clean, 7z (LZMA2): 28226 files, taken at 35d915c
    PASS  EXACT RESTORE - 28226 files match drsamonline/The_Browser@35d915c file for file

  * `continue-on-error` - it reports as a warning and cannot turn a good backup run red.
    On 1 November a filename bug here made a day of healthy backups look broken.
  * It rotates by day of the year across HCS, ziptastic, The_Browser, forge, app-builder,
    today-card, knowledge and registry. It used to test today-card every time - ten files,
    never the 130 MB repositories where a restore would actually break.

That is the first time a large repository has been restored end to end: 47 MB, 28,226 files,
out of a 7z dump, compared file by file.

## Remaining from the plan

    3. GFS retention instead of --keep 100
    4. sweep without cloning all five stores
    5. 7z dictionary for repos over ~32 MB
    6. concurrency group, job summary, alerting
