# 2026-11-04 — Every scheduled workflow paused, on the owner's instruction

## What I looked at

All 74 workflows across the 12 repositories that carry one, and then the subset with a `schedule:`
trigger — **32 workflows in 12 repositories**, from `dumps/backup-all.yml` every six hours to
`audit/health.yml` daily at 03:43.

For each one I recorded the numeric workflow id, the cron, its other triggers, and the state before
and after. The state before, read from the API: **all 74 active, zero already disabled.**

## What was wrong

Nothing, and that is the point of doing it.

The estate is being audited, and **a moving estate cannot be audited**. Yesterday's measurement was
overtaken inside a day: 164 workflows became 186, a repository appeared, four schedules started
failing and one of them — the notifier — began failing *about* the others. Every number in an audit
is a measurement of the moment it was taken, and 32 jobs writing to the same repositories on their own
timetable make that moment very short.

There is also a specific hazard the audit itself surfaced: **`dumps/backup-all` runs every six hours
and `dumps-dedupe` every four days.** A backup taken mid-audit captures a half-measured estate, and a
dedupe during a restore test is the one combination that could turn a measurement into a loss. Pausing
the mutators while reading is not tidiness; it is the difference between an audit and a race.

## What I changed

**32 workflows disabled, by numeric id, through `PUT .../actions/workflows/{id}/disable`** — never by
filename, because a filename resolves against the default branch and a workflow that has been renamed
silently does not match.

    12 repositories:  Matneo(3)  app-builder(1)  audit(2)  control-panel(1)  dashboard(1)
                      drsamonline(2)  drsamonline.github.io(1)  dumps(1)  forge(17)
                      knowledge(1)  registry(1)  skills(1)

**42 workflows left running**, because they are not scheduled: the reusable build and its callers,
`sweep`, `intake`, `state-set`, `backup`, `fanout`, `log-append`, the `drsamonline` one-shot sweeps,
and the GitHub-managed `pages-build-deployment` and `dependabot-updates`.

Recorded in this repository so the pause is reversible by a command rather than by memory:

    state/schedules-paused-2026-11-04.json    every workflow: repo, id, file, cron, other triggers, state
    tools/restore-schedules.sh                re-enable all, or one, or verify without changing anything

**The side effect, stated plainly:** disabling a workflow stops **all** of its triggers, not only the
cron. **15 of the 32 also run on push** and one of those also on `pull_request`, so their CI is paused
too. The list is `paused_with_push_ci` in the manifest, and it includes `forge/lint.yml` (the guards),
`forge/credential-guard.yml`, `forge/health.yml`, `audit/health.yml`, `audit/licence-check.yml`,
`control-panel/scan.yml`, `dashboard/refresh.yml` and the five repository refreshers.

## Evidence

Read back from the API after the pause, not assumed:

    states before:  active 74
    states after:   disabled_manually 32 · active 42
    disabled:       32   failed: 0

And the restore tool run against the live API, on one public and one private repository:

    $ bash tools/restore-schedules.sh --verify --only audit/health.yml
      PAUSED     audit/health.yml  (disabled_manually)
    total=1 enabled=0 already=0 failed=0 mode=verify dry_run=0

    $ bash tools/restore-schedules.sh --verify --only forge/new-app.yml
      CANNOT READ forge/new-app.yml — this token has no Actions:read on it.
      A 403 is a credential, not a missing workflow.
    total=1 enabled=0 already=0 failed=1 mode=verify dry_run=0

That second line is the estate's own rule doing its job: the CLI token reads Actions on public
repositories and gets 403 on private ones. The script says **credential**, not *missing* — the
distinction this estate has confused three times.

## What I deliberately did not do

- **Did not remove the `schedule:` triggers from the files.** That would keep push CI alive, but it is
  32 edits across 12 repositories, it is exactly the kind of bulk edit that ate newlines and broke
  files in batch 128, and re-inserting a cron into YAML is far easier to get wrong than re-enabling a
  workflow. One API call per workflow, one API call back.
- **Did not disable Dependabot's `dependabot-updates`**, which is scheduled on 12 repositories. It is
  GitHub-managed, it opens dependency PRs rather than mutating estate state, and pausing it is a
  separate decision that is yours. Say the word and it goes too.
- **Did not touch the 42 non-scheduled workflows.** `sweep`, `intake` and the one-shot sweeps can only
  be started by hand, so they cannot move anything while nobody is looking.
- **Did not disable the four failing schedules as a "fix".** They are paused with the other 28 and
  they will still be failing when they are switched back on. A pause is not a repair, and this entry
  does not claim one.

## Next

The audit runs against a still estate from now. When it is finished:

    bash tools/restore-schedules.sh              # all 32, read back one at a time
    bash tools/restore-schedules.sh --verify     # change nothing, report state

Then, before the first fire, the four failures want fixing — otherwise the first Monday restores a red
fleet:

1. `forge/new-app.yml` — `FANOUT_TOKEN` cannot create a repository, so the queue has been dead since
   2026-11-02 16:49.
2. `forge/health.yml` — the notifier posts a blank body and fails; a quiet fleet must be green.
3. `forge/kit-audit.yml` — `kit-drift` needs a token that can read the other repositories.
4. `audit/licence-check.yml` — `HCS` and `compfactory` have no LICENSE file.

**A schedule is not a schedule until it has fired once.** After restoring, the first fire is the real
test, and `forge/self-diagnose.yml` is the thing that checks it: a scheduled workflow older than twice
its period is not scheduled, it is broken.
