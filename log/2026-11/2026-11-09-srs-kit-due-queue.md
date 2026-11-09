# srs-kit — the due queue was storage order, and the cap took whatever was first

Date: 2026-11-09 · Repo `drsamonline/srs-kit` · PR #6 (open, not merged)
Links taken: none

## What I looked at
`srs-kit.js` (85 lines: SM-2 review, due queue, stats), `test-node.js` (23 assertions).

## What was wrong
`dueCards` filtered the due set and capped it in **storage order**. A card due today
came before one thirty days overdue, and a cap of 20 took whichever cards sat first
in the array. The function's own comment says the cap stops a backlog becoming a
wall; taking the wrong twenty of it is the wall.

    cards due 1d, 30d, 2d   ->  queue 1, 30, 2   ·   cap 2 takes 1, 30

## What I changed
Sorted by `due` ascending before the cap.

## Evidence
    node test-node.js     25 passed (2 new assertions)
    before                23 passed, 2 failed
                            FAIL the queue leads with the most overdue (1,30,2)
                            FAIL the cap takes the most overdue (1,30)
CI: success.

## What I deliberately did not do
- SM-2 maths untouched: interval uses the previous ease then ease updates, lapse
  resets reps and interval, 1.3 floor — read and consistent with SM-2.
- No tie-break beyond `due`; sort is stable, so it is deterministic.
- No link work: fsrs4anki is a different scheduler model (FSRS, not SM-2) and
  clanki wraps Anki's engine; either changes what a review means for existing decks.
- No version bump, no merge.

## Next
Decide on PR #6.
