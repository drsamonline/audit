# 2026-10-31 — The health check's first real catch: three red jobs, diagnosed

## How I got here

The health page reported 27 ok / 3 failing once AUDIT_TOKEN was in place. My sandbox token
cannot read private repos, but the GitHub connector can, so the logs were readable after all.

## 1. forge / new-app.yml — red every Monday, for nothing

**Symptom:** `scaffold` job failed at "Refuse a bad name"; `auto` job failed at "Scaffold it".

**Cause (scaffold):** the job had no `if:` guard, so it also ran on the weekly schedule.
On a schedule `inputs.name` is empty, so `NAME=""` matched the step's own `case` guard and
failed. The job that only makes sense when a human supplies a name was failing the run
every Monday since 27 October — which is why the failure is 93 hours old.

**Fixed:** `if: github.event_name == 'workflow_dispatch'`.

**Cause (auto):** `Resource not accessible by personal access token (createRepository)`.
The queue correctly picked `accent-oracle`, then `gh repo create` was refused. So automated
scaffolding cannot create a repository at all — `FANOUT_TOKEN` lacks **Administration: write**.
Not fixed: that is a token permission, not code.

**Also found:** the scaffold template wrote `build.yml@34fa725` — the 26 October commit,
before the icon work and before the pinned-kit fix. Every app Forge created would have
shipped without its own icon. **Fixed:** both occurrences now pin the current head.

## 2. forge / repo-learning.yml — a push race

**Symptom:** "could not push after 6 attempts", then "NOT on origin/main with the bytes this
run computed".

**Likely cause (inference, not proven):** the run was dispatched on branch
`fix/workflow-audit-and-kit-learning` while the helper was told to commit to `main`. The
helper rebases onto `origin/main` from a checkout of a different branch, which can conflict
on every attempt. Not fixed — `tools/commit-and-verify.sh` is shared by many jobs and
changing it blind is exactly the retrofit risk this estate keeps getting bitten by.

## 3. dumps / backup-all.yml — the backup repository is nearly full

**Symptom:** exit 1 with `backed up 87 of 91` and `NOT BACKED UP (4): HCS, The_Browser,
game-kit, ziptastic`.

**Cause:** `ziptastic: could not write (422)` — a 422 from the contents API. The dumps repo
is at **653.3 MB of 839 MB**, so the writes are hitting the size ceiling. Four repositories
are silently outside the backup.

Not fixed: resolving it means deleting old snapshots, which is destructive and the owner's
call.

## Evidence

- Logs pulled through the connector (the sandbox token cannot see private repos).
- `new-app.yml` read in full; the missing `if:` and the stale pin are both visible at
  lines 38-45 and in the generated `build-apps.yaml` heredoc.
- Fix committed to forge as `7dbc8150`.

## Next

1. `FANOUT_TOKEN` needs Administration: write, or automated scaffolding stays dead.
2. dumps needs pruning or a larger store; 4 repos are currently unbacked.
3. repo-learning needs the branch/target mismatch resolved.
