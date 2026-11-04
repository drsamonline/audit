# 2026-11-04 — Check found the skip rate decaying; it was a timestamp format

## What was healthy

Four scheduled backups in a row, all green:

    2026-11-03T00:37  success
    2026-11-03T13:44  success
    2026-11-03T22:57  success
    2026-11-04T05:06  success

The run fixes from 2 November have held. No manual intervention needed for two days.

## What was not

The skip rate was quietly falling:

    2026-11-02T17:06   backed up 27, skipped 73
    2026-11-02T17:17   backed up 19, skipped 81
    2026-11-03T00:37   backed up 24, skipped 76
    2026-11-03T13:44   backed up 50, skipped 51
    2026-11-03T22:57   backed up 88, skipped 13
    2026-11-04T05:06   backed up 87, skipped 14

By the last run it was backing up nearly everything again - the exact waste the change
trigger exists to prevent.

## The cause: two date formats and a string comparison

`state.json` held timestamps in two shapes:

    dumps-3:  "2026-11-03T004109Z"   written by the backup
    dumps-6:  "20261101T215700"      written by --seed-state

`read_state_all` merged the stores by comparing those as STRINGS. `-` sorts below `1`, so
`"20261101T215700"` compared GREATER than `"2026-11-03T004109Z"` - the older, seeded entry
beat the fresh one every time. The state never advanced, so each run re-backed-up whatever
the stale sha said had changed, and wrote a fresh entry that lost the merge again.

That is why the numbers degraded rather than broke: the more repositories that had a seeded
entry, the more of them became permanently stale.

## The fix

  * `read_state_all` compares `_norm_ts()` of each timestamp, not the raw strings.
  * `--seed-state` writes the canonical stamp format instead of its own normalised one.

Verified on the exact pair that failed: raw comparison picks the seeded value, normalised
comparison picks the newer one.

## After

    state: 101 repositories have a recorded commit
    backed up 5 of 101  (skipped 96 unchanged)
    PASS  EXACT RESTORE - 63 files match drsamonline/app-builder@3c8459e
    conclusion: success

Back to skipping 96 of 101.

## Also

Merged the stray `dumps-6#2` removal PR left from the consolidation cycles. `dumps#2` is an
old dependabot bump that nobody needs.

## State of the stores

`dumps-3` is the active store, at about 1.2-1.4 GB of its 2 GB cap. `dumps-4`, `dumps-5` and
`dumps-6` are dormant - emptied by consolidation and receiving nothing.

The API's `size` field still lags and overstates; the tree figure the sweep prints is honest.
