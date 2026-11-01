# 2026-11-01 — Backups were red for a day. Found it, fixed it, and 7z restore is proven.

## What the check found

The stores were fine, the sweep was fine, and the backups were being MADE - every failing
run said `backed up 96 of 96`. But three scheduled runs in a row were red:

    2026-11-01T12:46  failure
    2026-11-01T04:43  failure
    2026-10-31T21:05  failure

## The cause

The restore-test step I added on 31 October builds the path to the dump file. It assumed:

    {repo}/{stamp}/{name}.tar.gz

The moment new dumps started being written as `.tar.7z`, that path stopped existing. Every
store returned 404, the step could not prove recoverability, and it failed the whole run -
with a message blaming the backups rather than the filename.

    could not read dumps-5/.../today-card.tar.gz: 404 Not Found

The backups were never at risk. A verification step was lying about them.

## The fix

`restore_test` now looks for `.tar.7z` and then `.tar.gz`, and reports plainly if neither is
there. The message also stopped claiming "gzip CRC verified" when it had just read LZMA2.

## The run after the fix

    backed up 96 of 96
    restore test: dumps-5/drsamonline__today-card/2026-11-01T193619Z/today-card.tar.7z
    unpacks clean, 7z (LZMA2): 10 files, taken at 086a8fc
    PASS  EXACT RESTORE - 10 files match drsamonline/today-card@086a8fc file for file
    restore verified from dumps-5
    conclusion: success

**This closes the last unproven link.** A 7z dump has now been written, stored, read back
out of a store, decompressed, and compared file by file with the commit it names.

## Where the estate stands

    store       content      pack     waste
    dumps        941.0M    896.0M     +0.0M
    dumps-2      922.0M    688.2M     +0.0M
    dumps-3      968.0M    921.7M     +0.0M
    dumps-4      840.0M    976.3M   +136.3M
    dumps-5      136.0M    264.8M    +60.5M (grown since - it is the active store)

    96 of 96 repositories backed up
    restore proven, 7z and gzip
    sweep green, three phases, every 4 days
    1048 redundant snapshots removed
    ~197 MB of history reclaimed on dumps-4
