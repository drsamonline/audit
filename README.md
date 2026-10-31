# audit

The change log for the drsamonline fleet — **78 repositories, 105 workflow files, 10 scheduled jobs**.

Every audit, fix and correction lands here, with the evidence. Nothing in this repo is a plan for
later; if it says a thing was done, the `log/` entry that claims it carries the before-and-after.

## Why this exists

The fleet grew faster than its bookkeeping. Licence badges drifted from their LICENSE files, new
repos fell into an "Other / New" bucket, landing pages stopped offering downloads, and the audit
files that documented all of it were scattered across five unrelated repos. This repo is the single
place where the state of the fleet is measured, the change is recorded, and the next run can prove
what moved.

## Layout

    log/YYYY-MM/YYYY-MM-DD-<slug>.md   one file per session
    state/                             machine-readable snapshots, refreshed by tools/collect.py
    tools/collect.py                   read every repo into state/
    tools/diff.py                      compare two snapshots, print only what changed
    tools/licence_check.py             licence badge vs LICENSE file, all repos
    tools/fix_licence_badges.py        make a badge say what its LICENSE grants

## The rule

**A change is not done when it is pushed. It is done when it is read back from the API and the
batch's verification passes.** The log entry records the verification, not the intention.

Every log entry uses the same six headings, in this order:

    ## What I looked at
    ## What was wrong
    ## What I changed
    ## Evidence
    ## What I deliberately did not do
    ## Next

The fifth one matters most. A log that only records what changed hides the decisions that were
made by *not* changing something, and those are the ones that get re-litigated later.

## Read state through the API, never through raw

`raw.githubusercontent.com` serves a cached copy that lags minutes to hours behind a commit. In this
fleet it has twice made finished work look broken:

- a `build.yml` that already contained the icon wiring was served without it
- 14 landing pages that had just been repaired were served in their old, broken form

Both times the API (`GET /repos/{owner}/{repo}/contents/{path}`) showed the truth immediately.
**Use the API to decide whether something worked.** Use raw only for bulk reading of files that
have not changed in the last hour. Where a URL matters, fetch actual bytes and check the status.

## Running it

    gh auth login                      # or GH_TOKEN in the environment
    python3 tools/collect.py           # ~5 minutes for 78 repos
    python3 tools/licence_check.py     # exits 1 if any badge is wrong

`licence_check.py` runs weekly on a Monday at 03:31 UTC and commits the fresh snapshot. That cron is
deliberately clear of every other job in the fleet — the current set is:

    Mon 03:17  update-profile        Mon 03:23  skills/refresh
    Mon 03:31  licence-check (this)  Tue 03:47  dashboard/refresh
    Tue 04:00  metrics               Tue 04:12  Matneo/blog
    Tue 04:22  Matneo/store          Tue 06:00  control-panel/scan
    Wed 05:00  app-builder/kit-tests 1st+16th 03:00 store-images, 03:37 refresh-hub

## Conventions

- **One commit per repo.** Repos are independent; there is no shared release train, and a
  cross-repo change cannot be reverted per repo.
- **A script fixes a class of defect; a human decides a class of question.** Encoding a space is
  a script. "Is this repo MIT or PolyForm?" is not.
- **Never let a sweep invent a licence.** If a badge and its LICENSE disagree, the sweep stops
  and the repo goes to the decision batch.
- **Test against the real response shape and the broken state.** Two repairs in this log failed
  because they were tested against cached data and against a clean page instead of the damaged one.

Licence: PolyForm Noncommercial 1.0.0 — see LICENSE.
