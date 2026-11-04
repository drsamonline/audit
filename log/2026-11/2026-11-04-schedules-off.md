# 2026-11-04 — Every scheduled workflow turned off

## What was actually still running

The estate was already quiet. Of 30 workflows in `forge`, 16 were `disabled_manually`; in
`audit`, 2 of 3. Matneo had 3 of 5 off. What remained active with a cron was just two:

    dumps/backup-all.yml       id 395003863   every 12 hours
    forge/dumps-dedupe.yml     id 396710698   weekly, Monday 05:00

Both are now `disabled_manually`.

## Verified, not assumed

Scanned all 109 repositories, read every active workflow file, and looked for a `schedule:`
key:

    repos scanned: 109
    no active workflow anywhere has a cron schedule

## What was deliberately left alone

  * **`forge/f54-probe.yml`** is active but has no cron - its one run was a `push` on 27
    October. Turning it off would not be turning off a schedule.
  * **`dynamic/dependabot/dependabot-updates`** and **`dynamic/pages/pages-build-deployment`**
    are GitHub-managed system workflows. They cannot be disabled through the API and are not
    scheduled jobs in the sense the owner means.

## The crons are still in the files

Disabling is a switch, not a deletion: the `schedule:` blocks are untouched in both YAML
files, so turning either back on restores its old cadence with no edit. That is deliberate -
the audit and replan is still in progress and this is meant to be reversible.

## Consequence, stated plainly

  * no automatic backups from now on
  * no sweep, so no `HISTORY.md` refresh and no duplicate cleanup
  * the last backup was the manual full run on 4 November at 15:41

Nothing is lost. When the forge replan is done, enable `backup-all.yml` and the corpus
resumes where it left off - `state.json` still holds the commit every repository was last
backed up at, so the first run afterwards will only take what changed since.
