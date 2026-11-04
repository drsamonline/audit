# 2026-11-04 — Seven rounds on the manifest design: from "the tool cannot know who wrote this" to one path prefix

## What I looked at

A design for a per-file provenance manifest and drift-aware self-healing for the Forge estate, delivered
as seven successive versions (v2 → v7), each reviewed against the code it patches rather than against its
own description.

    generators in scope      drsoam.py, registry/refresh.py, scan.py, plan.py, app-deliver.py
    writers found            14 tools across 4 repositories for the 26 paths first proposed
    paths proposed (v2)      26
    paths tracked (v7)       16, every one with a gated writer; 17 deferred with the writer named
    rounds                   7 — 4 blocking in round 1, 1 blocking in each of rounds 2–5, 1 defect in 6
    executed, not argued     the tool on all four states; the fixer both ways; the batch gate; the auditor

## What was wrong

Not one thing, and the sequence is the useful part: **each round's remaining defect was smaller and
further from the centre.**

**Round 1 — the centre.** The design classified drift by asking git *who* wrote the file
(`git log -1 --format=%an%ae -- path`). At `fetch-depth: 1` — which every generator checkout uses — that
returns the **tip commit's author for every path**. Proven on a three-commit repository: in a shallow
clone, a file last touched by `human` reports `dependabot[bot]`. So the design would have overwritten user
edits or frozen files forever, decided by who committed last to the repository. Also: `app-deliver.py` —
the biggest overwriter of user-editable files — was outside the design entirely; the gate resolved its own
tool to a path that does not exist and failed **silently**; a patch referenced a variable that was not in
scope; and the bootstrap skipped every app repo.

**Round 2 — the promise.** The fixer *adopted* a human's commit, clearing the way for the generator to
overwrite it. Reproduced: the user's line was gone. And per-file gating broke `publish_dashboard`'s
deliberate write ordering, leaving a written index pointing at a stale sibling in a green run.

**Round 3 — the execution order.** The fixer read the manifest, shelled out to a tool that rewrote it, then
wrote its own stale copy — losing the claim it had just made. Reproduced.

**Round 4 — a word and a scope.** `git rm --cached` does not delete the working-tree file, so the untracked
case asserted a status its own setup prevented. And the manifest recorded 26 paths while gating four
writers, which would have started a loop: twelve generated files claimed as `hand`, permanently, with the
drift check reporting them healthy.

**Round 5 — the checker.** The new `manifest-audit.py` failed **16 of 16** on its own config: it scanned
one repository's `tools/` while twelve writers live in four; it matched only *quoted bare* filenames, so
`".github/workflows/build-apps.yml"` was invisible; and it reduced paths to basenames, so
`docs/index.html` and `docs/play/index.html` were indistinguishable.

**Round 6 — a prefix.** The four app paths declare `forge/tools/app-deliver.py`, but `lint.yml` checks
forge out at the workspace root, so that names a directory that does not exist.

## What I changed

Nothing in the estate. This is a review record, not a repair — the design has not been implemented.

    reports/2026-11-manifest-design/README.md   the record: design, seven rounds, verification, scope, rollout
    log/2026-11/2026-11-04-manifest-design-review.md   this entry
    README.md                                   reports/ now has three sets, not two

## Evidence

The measurements the record rests on, all reproducible:

    manifest.py, four states      clean→0 · uncommitted→3 · committed-drift→3 · protected→4
    v3 fixer, user commit         synced → clean → generator wrote → USER_NOTE gone
    v4 fixer, same repo           claimed → protected → refused → edit survived
    v4 fixer, mixed pass          claim executed then overwritten — manifest still "generated"
    reordered fixer               data.json protected · build-apps.yml clean — both correct
    per-file gate                 index written, sibling stale, run green
    git rm --cached               file still on disk → protected, not unrecorded
    manifest-audit (v6)           16 of 16 fail, three independent causes
    manifest-audit (v7)           16/16 resolve; OK on exit 0 once the writers carry the marker

Two cross-checks that came back clean, and are worth recording because they are the failure modes one
would expect: `manifest.py` as specified behaves exactly as documented on all four states, and the v7
declarative auditor reports green the moment the writers are patched — so the gate is real, not
aspirational.

## What I deliberately did not do

- **Did not implement any of it.** Seven rounds of design and review; no file in `forge`, `app-builder`,
  `registry`, `control-panel`, `dashboard` or any app was touched.
- **Did not re-litigate settled decisions.** The three-way comparison, claim-not-adopt, the batch gate and
  the honest scope were fixed by round 3–4 and confirmed in every round after. Re-opening them would have
  cost the rounds that found the real defects.
- **Did not report a defect I had not reproduced.** Every finding marked *reproduced* was executed against
  a real git repository with the plan's own tool. One finding I predicted — a `[ -f ] && cmd` loop failing
  under `set -e` — was **wrong**, and the record says so.
- **Did not take the scope decision for the owner.** Whether to ship 16 honest paths or wait for all 26 is
  a judgement about appetite, not correctness; the record states both and recommends the smaller one.
- **Did not treat the design's own summary as evidence.** Six of the seven rounds found something the
  previous round's "what this gets right" section asserted and the code did not do.

## Next

1. ~~One string, then ship.~~ **DONE.** `manifest-paths.json` → `repos.apps.*.writer` is now
   `"tools/app-deliver.py"` in all four entries, with the layout rule recorded in the file's `why` so the
   next writer added does not rediscover it from an error that blames the wrong file. Verified in the
   `lint.yml` layout: every path resolves, and with the writers carrying the marker the auditor reports
   `OK: 16 tracked path(s), every one declared and recorded by its writer`, exit 0. What is left red is the
   rollout, not the config.
2. **Run the rollout in order**, with Step 4's C and E as the ship conditions — C (the fixer must protect,
   not adopt) and E (untracked must refuse).
3. **Write the rule at the top of Step 4**, because one class recurred four times: *every gate case asserts
   from the clone the fixer wrote to, after the change is merged and pulled.*
4. **Then gate the seventeen deferred paths**, one batch per writer, adding each to `repos` in the same
   commit that gates it — `manifest-audit.py` confirms it.
5. **Open question, unchanged:** `registry/learnings.json` and `registry/startup-failures.json` have no
   writer found by filename. Deferred and harmless either way, but nobody knows what writes them.
