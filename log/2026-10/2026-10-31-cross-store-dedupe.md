# 2026-10-31 — Cross-store dedupe and consolidation

## What was asked

    "check cross dumps if same remove them"
    "condense dumps so if one has space move the half used dumps from new ones to old ones"
    "keep record of everything"

## What already existed

`forge/tools/dumps-dedupe.py` plus `.github/workflows/dumps-dedupe.yml` — weekly Monday
05:00, keeps one copy of each identical snapshot per repo, PR-only, with nine self-tests.
It compared git TREE SHAS, which is exact: same content, same tree sha, no hashing by hand.

**Its gap, created by today's rollover:** it hardcoded `drsamonline/dumps`. Backups now roll
into dumps-2 and dumps-3, so every store after the first would have grown forever with
nothing deduping it. Fixed: it derives owner/name from its own checkout, and the workflow
walks every store matching `^dumps(-[0-9]+)?$`.

## What I added

`forge/tools/dumps-consolidate.py` — the cross-store half.

**Rule 1, cross-store duplicates.** Same repo, same tree sha, in more than one store: keep
the copy in the OLDEST store, remove the newer ones. Within one store is left to
dumps-dedupe, which keeps the NEWEST — and the keeper rule here matches that, so the two
tools cannot disagree about which copy survives.

**Rule 2, consolidation.** Move snapshots out of newer stores into older ones that still
have room. Never into a newer store.

**The dangerous part.** Moving between two repositories is a two-repository write. Delete
here and add there in one step, and a half-merged pair loses the backup. So every move is
two phases:

    phase 1  COPY into the older store, open a PR there
    phase 2  on a LATER run, once the copy is confirmed on the older store's main,
             remove the original and open a PR there

Between the phases the snapshot exists twice, which wastes a little space and loses
nothing. `already_present()` is the gate, and it asks the branch, not the plan.

**The record.** Every decision is written to `--record` JSON, into the run summary, and
into the pull-request body — a run summary expires, a merged commit does not.

## Two bugs of mine, caught by running it

1. The first run reported **1273 cross-store duplicates**, and the sample read
   `dumps/... (same content already in dumps)` — it was counting WITHIN-store copies, which
   belong to the other tool and follow a different rule. Only a copy in a DIFFERENT store
   counts now. The honest number is **452**.
2. Its "moves" went into `dumps-3`, a NEWER store. Now only stores with a lower index are
   candidates.

## Current state, measured

    snapshots:  dumps=1441, dumps-2=378, dumps-3=90
    sizes:      dumps 1779 MB / 880 cap,  dumps-2 898 MB / 880,  dumps-3 301 MB / 880
    cross-store duplicates: 452
    moves into older stores: 0

Zero moves is the correct answer today, and worth understanding: dumps and dumps-2 are both
OVER their cap, so there is nowhere older with room. Consolidation is blocked behind
dedupe — run the dedupe, free the space, and the moves appear on the next pass.

## Not applied

Everything above is report-only. Applying opens PRs: 452 removals from the newer stores,
then, once those merge, the moves. Nothing merges itself and nothing is deleted on the
strength of a plan.
