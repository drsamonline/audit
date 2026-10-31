# 2026-10-31 — Applied: dedupe and consolidation, as pull requests

## What ran

`forge/dumps-dedupe.yml`, dispatched with `apply: true`. It dedupes each store internally,
then consolidates across stores, and every change left as a pull request.

## The pull requests

| Repo | PR | What it does |
|---|---|---|
| dumps | [#3](https://github.com/drsamonline/dumps/pull/3) | remove 200 identical snapshots |
| dumps-2 | [#1](https://github.com/drsamonline/dumps-2/pull/1) | remove 200 identical snapshots |
| dumps-2 | [#3](https://github.com/drsamonline/dumps-2/pull/3) | remove 126 snapshots duplicated in an older store |
| dumps-2 | [#2](https://github.com/drsamonline/dumps-2/pull/2) | absorb 2 snapshots from a newer store (phase 1 of a move) |
| dumps-3 | [#1](https://github.com/drsamonline/dumps-3/pull/1) | remove 74 snapshots duplicated in an older store |

**600 snapshots queued for removal**, all of them byte-identical to a copy that stays.
Nothing merges itself.

## Three bugs found by applying rather than reading

1. **The keeper was matched by PATH, not content.** The first apply run removed **zero**
   duplicates and printed `SKIP ... not yet confirmed on dumps's main` 200 times. The
   keeper holds the same content under a *different timestamp*, so asking for the same path
   was always false. `already_present()` now walks the repo folder on the keeper's main and
   compares tree shas. Verified on a fixture where the copy sits at S0 and the duplicate at
   S1: removed from dumps-2, dumps keeps its copy.
2. **Removals span stores but the commit was made in one.** Cross-store duplicates come
   from dumps-2 *and* dumps-3; committing in `cross_dupes[0]`'s checkout meant the other
   store's deletions were staged and then thrown away with no PR. Now grouped per store,
   one commit and one PR each — which is why there are two removal PRs, not one.
3. **A second run found its own PR already open** and `gh pr create` failed, which would
   have taken down the whole sweep. Both tools now treat an existing PR as success and
   update the branch instead.

Also fixed before applying: each store is reset to `origin/main` before consolidation
starts, so the dedupe branch's commits do not ride along into the consolidation PR.

## Numbers

    snapshots:  dumps=1441, dumps-2=378, dumps-3=90
    sizes:      dumps 1779 MB / 880 cap, dumps-2 898 MB / 880, dumps-3 301 MB / 880
    cross-store duplicates found this run: 262  (452 before the 200-removal cap ran)
    moves absorbed: 2

`dumps-2` PR #2 is **phase 1** of a move: the snapshots are copied in and NOT yet removed
from their origin. The removal happens on a later run, once that copy is confirmed on
main. A half-merged move wastes space; it can never lose a backup.

## Next

1. Review and merge the five PRs. Removal is safe by construction - every one is identical
   to a copy that stays - but 600 deletions deserve a look before they land.
2. After they merge, run the sweep again: space frees up, and the consolidation moves that
   are currently blocked (both dumps and dumps-2 are over cap) become possible.
3. Restore has still not been exercised against a live chunked dump. That is the last
   unproven link in the backup chain.
