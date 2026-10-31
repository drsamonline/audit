# 2026-10-31 — Three phases, every four days, and 7z

## What was asked

    "first deduplicate each dump separately, detect remove, then deduplicate cross dump
     and remove, then consolidate to dum0 as per space"
    "schedule should run every 4 days"
    "dumps should be 7z ultra rather than zip to save more space"

## The sweep, in that order

    phase 1  dedupe each store against itself        dumps-dedupe.py
    phase 2  remove duplicates present in another store   dumps-consolidate.py --only cross
    phase 3  consolidate into the oldest store with room  dumps-consolidate.py --only consolidate

`--only` filters before the REPORT as well as before the apply, so each phase prints only
its own work — the first version filtered at the apply step and every phase reported
everything.

Schedule: `0 5 */4 * *`. GitHub has no "every N days" cron, so this fires on days 1, 5, 9,
13 ... of each month and the gap across a month boundary is 1-3 days. Close enough for a
sweep whose job is to keep the store tidy, and far more often than the weekly it replaced.

## 7z -mx=9, measured

    BLINKTRANSFER  0.18 -> 0.14 MB   23% smaller
    HMS            0.67 -> 0.48 MB   28% smaller
    HCS          133.78 -> 109.08 MB  18% smaller
    ziptastic    133.92 -> 109.18 MB  18% smaller
    whispering     0.96 -> 0.79 MB   17% smaller
    All4ONE        0.84 -> 0.77 MB    8% smaller

94 of 94 backed up, every one round-trip verified.

### Three wrong turns before it worked, each caught by measuring

1. **`7z a -si -so` does not work for creating an archive** in p7zip. Every repository
   fell back to gzip and the run still said "backed up 94 of 94" — the fallback did its
   job and hid the failure. Now creation goes through a temp file; extraction still streams.
2. **It compressed the already-gzipped stream.** Gain: 0-2%. Gzipping gzip is pointless.
   It now gunzips to the raw tar first, and the same data saves 8-28%.
3. **A rename left a stale variable name** (`gz_bytes`) and the whole run died with
   `NameError`. Fixed, and the round trip was then proven with a stand-in 7z before another
   ten-minute run.

### The safety rule that made all of this survivable

A dump is only stored as 7z if it is **decompressed again and compared byte-for-byte with
the tar it came from**, and only if the result is actually smaller. If 7z is missing, the
round trip differs, or the gain is nil, GitHub's gzip tarball is stored instead. That is why
the first two failures cost nothing: the backups were still made, in the older format.

Restore reads both: a 7z dump decompresses to the raw tar, a gzip dump opens as before.

## State

- `dumps-4` now exists — the store rolled over again during the 7z runs.
- Five pull requests from the previous sweep are still open and unmerged.
- Restore has still not been exercised against a live 7z dump. The round trip at write
  time is verified; reading one back out of a store is the last unproven step.
