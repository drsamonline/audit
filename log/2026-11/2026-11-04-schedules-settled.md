# 2026-11-04 — Schedules settled, and a finding about what is actually running

## What was changed

    dumps/backup-all.yml     every 6 hours  ->  every 12 hours
    forge/dumps-dedupe.yml   every 4 days   ->  weekly, Monday 05:00
    forge/new-app.yml        weekly cron    -> removed entirely
    forge/health.yml         contents:read  -> + issues:write

**Backups at 12 hours.** Change-triggering made the run cheap, so the only thing the shorter
interval bought was a smaller recovery point: 6h meant a change waited at most 6 hours to be
backed up, 12h means 12. Two runs a day is the honest middle for repositories that change a
handful of times a day, and it halves what the workflow contributes to Actions minutes if
these repos ever stop being public.

**Sweep weekly.** It ran every four days because backups on a clock produced duplicates
constantly. They do not any more. The sweep still earns its run - it writes HISTORY.md,
catches cross-store duplicates a rollover can create, and packs the stores - but it clones
several gigabytes each time, and weekly is enough for that.

**new-app.yml had no business on a timer.** It creates a repository from a name typed into
the dispatch box; a schedule has no name to give it, so the weekly run could only fail. It
did, every Monday, for weeks.

**health.yml was filing an issue with `contents: read`.** That grant cannot create an issue,
so the notify job failed every week while the comment above the block described the grant as
if it were there. Added `issues: write`.

## The finding

Checking why `health.yml` could not be dispatched: it is **disabled**, and so is most of the
estate.

    forge: 16 of 30 workflows disabled_manually
    audit:  2 of 3 disabled_manually  (health.yml, licence-check.yml)
    dumps:  backup-all.yml active

**All four workflows the health page reports as "failing" are disabled, not failing:**

    audit/licence-check.yml   disabled
    forge/health.yml          disabled
    forge/kit-audit.yml       disabled
    forge/new-app.yml         now has no schedule at all

The page judges a workflow by the conclusion of its last run. A workflow that was
deliberately switched off keeps its last red run forever, so it is reported as broken. The
estate looks degraded when it is quiet on purpose.

That is the next thing worth fixing: `audit/tools/fleet_health.py` should read each
workflow's `state` and report `disabled` rather than `failing`. Otherwise the one page that
tells the owner whether anything is wrong is the page that cries wolf.

## Where the backups stand

    dumps    897 snapshots
    dumps-2  545 snapshots
    dumps-3  385 snapshots
    dumps-4, dumps-5, dumps-6   empty

Sweep run after re-enabling: 0 duplicates, 0 moves - converged and clean.
