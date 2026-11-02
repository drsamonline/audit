# 2026-11-02 (later) — Check found a red run; three fixes

## What the check found

The 14:55 scheduled backup had failed. Everything before it was green, and nothing was
missing from the stores - the run died mid-way:

    http.client.RemoteDisconnected: Remote end closed connection without response

One dropped socket, while checking which store to roll over to, ended a run that had already
written twenty repositories. Nothing was wrong with the backup or with GitHub's data.

## 1. Retries on transient failures

`call()` now retries network errors and 5xx responses with backoff, four attempts. A 4xx is
NOT retried - it is an answer, and retrying it only wastes the run.

Proven on a stub: two drops then a success returns the answer on the third attempt; a 404
still returns immediately on the first.

## 2. Rollover survives a blip

`pick_dumps_repo` used to raise `SystemExit` on any non-404 error, so a dropped connection
mid-rollover killed the run. A network error now keeps the store it was about to use and
carries on: if that store turns out to be full the write fails and is reported as a failed
repository, which is visible - unlike a dead run.

## 3. The rollover check was doing six times the work

It always began at `dumps` and walked every store, measuring each tree, to arrive back at the
one already in use - once per repository. The log was a wall of "dumps-2 is full ... rolling
over" for stores nobody was going to touch.

It now starts from the store in use. Measured on the next run:

    rolling-over lines in the log: 5   (was one set of five per repository)

## Also fixed

`(kept 0)` in the log line, left over from count-based retention, now reads
`retention 7d/8w/12m, N snapshot(s) now`.

## State

    backed up 19 of 100  (skipped 81 unchanged)
    PASS  EXACT RESTORE - 28226 files match drsamonline/The_Browser@35d915c
    conclusion: success

    stores: dumps 896M, dumps-2 688M, dumps-3 922M, dumps-4 976M, dumps-5 585M, dumps-6 146M

`dumps-6` was created by a rollover during this work. `state.json` lives in dumps-5 and
dumps-6, and is read across all stores, so a rollover never loses the record of what has
already been backed up.
