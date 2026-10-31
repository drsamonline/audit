# 2026-10-31 — dumps: the split is fine, the write path is the wall

## What the owner said

"Dumps are automated to split when full and clean themselves."

That is true, and I checked it: `backup.py` has `pick_dumps_repo()`, which walks
`dumps`, `dumps-2`, `dumps-3`... and creates the next one when the current is over the
cap, and `dumps_to_delete()` applies `--keep`. Neither is the failure.

## What the run actually said

I made the write-failure log print the API's own words instead of just the status code
(`288d1146`), then ran a backup. It failed again, and now it said why:

    HCS:         could not write (422) "Sorry, the file is too large to be processed.
                 Consider creating/updating the file in a local clone and pushing it."
    The_Browser: could not write (422) same
    ziptastic:   could not write (504) "We couldn't respond to your request in time."

    backed up 91 of 94 — NOT BACKED UP (3): HCS, The_Browser, ziptastic

So there are two unrelated causes:

1. **HCS (125 MB) and The_Browser (165 MB) exceed what the contents API will accept.**
   `dump_one()` writes with `PUT /repos/.../contents/<path>`, and that endpoint has a
   per-file ceiling. Splitting into dumps-2 does not help: the problem is the size of ONE
   file, not the size of the dump repository. GitHub's own advice is in the message —
   commit it in a local clone and push.
2. **ziptastic was a 504 gateway timeout** — transient. `game-kit`, which failed the
   previous run, succeeded this time, which confirms the transient class.

## A second thing worth knowing

The run reported `93 repositories, 1348 snapshots, 1610.1 MB` — the dumps repository is
now well past the 839 MB cap the script rolls over at. It did not roll over because
`pick_dumps_repo()` reads `size` from the repository API, and that figure lags the real
contents. So the cap check can be behind by a lot, and rollover happens later than
intended — or not at all while the number catches up.

## What I changed

Only the error message (`288d1146`). No behaviour change: a write that fails still fails
the same way, it is just no longer silent about why.

## What I did not change, and why

The fix for the two large repos is a git-push path in `dump_one()` as a fallback when the
API refuses the file. That is the right fix, but it rewrites the one function that
actually stores every backup, in a session that has already found three ways a confident
change can be wrong. It deserves its own pass with a restore test, not the tail of this one.

## Next

1. Add a git-push fallback for tarballs the contents API refuses.
2. Make the rollover check use the manifest total (which the script already computes)
   rather than the lagging repository `size`.
3. ziptastic needs nothing — it timed out.
