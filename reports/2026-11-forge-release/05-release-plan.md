# 05 — The release plan

**How this ships, in what order, and how each stage is judged.** Six stages. Nothing is called done
until the acceptance test for its stage passes on a real account, not on a scratch copy.

The estate's own rule applies unchanged: **a change is not done when it is pushed. It is done when it
is read back from the API and the batch's verification passes.**

---

## The stages

### R0 — Freeze the invariants (in `forge`, 1 batch)

Write `bootstrap/INVARIANTS.md`: the fourteen fixes from `03-one-release.md` §4, each with the check
that proves it and the finding it closes. Then write `tools/make-seed.py` and `tools/wf-check.py`'s
nine-property rule, and make `make-seed.py` **fail** if any invariant is missing from the tree it is
packaging.

*Acceptance:* `python3 tools/make-seed.py --check` exits 0 on `forge@main` today, and exits 1 when any
one of the fourteen is removed from a scratch copy. Fourteen deliberate breakages, fourteen red runs.
A check that has never failed has not been tested.

### R1 — Build the bootstrap (in `forge`, 3 batches)

`bootstrap/bootstrap.yml` and six small Python helpers, one per phase that needs logic
(`preflight.py`, `discover.py`, `settings.py`, `pipeline.py`, `schedules.py`, `verify.py`). Each helper
takes `--dry-run`, prints `{done, skipped, failed}`, and writes `bootstrap/last-run.json`.

*Acceptance:* a full dry run against the **current** estate reports what already exists and changes
nothing — `git status` clean afterwards, zero API writes in the run log. Then a real run against a
throwaway account creates the four sibling repositories, sets their visibility, writes one caller into
one app and verifies it by blob sha.

### R2 — Prove it on a fresh account (1 batch + 1 week of waiting)

The stage that cannot be skipped. A second GitHub account, free plan, no repositories. Run the guide
in `04-setup-guide.md` verbatim, with a person who has not read the other four documents.

*Acceptance:* the "Forge is live" issue appears with every phase green; the three published pages
return 200; `new-app` scaffolds one app on the first Monday and that app has a repository, a pipeline,
a release, a landing page, a live demo and a screenshot by Monday evening.

**Every ambiguity found by the person running it becomes a fix in the guide, not a note in a report.**
That is the whole point of using someone who has not read the design.

### R3 — Cut the release (1 batch)

`forge@v1.0.0`, `tools/make-seed.py` builds `forge-seed-1.0.0.tar.gz` from the tagged tree,
`SHA256SUMS` written, `MANIFEST.json` generated, assets attached to the GitHub Release. `GETTING-
STARTED.md` rewritten around the release instead of the promise of one. `README.md` gains the
download line and the two-minute path.

*Acceptance:* download the asset on a machine that has never seen the repository, verify the
checksums, run `./install.sh`, `forge --version` prints `1.0.0`, and `install.sh` exits non-zero when
one file in the extracted tree is altered.

### R4 — Point it at the real estate, in verify mode (1 batch)

`mode: verify` against the current account. It creates nothing and reports, per phase, what differs
from the release's expectation. This is the estate's first honest self-portrait against a fixed
standard, and it is where the eleven unused kits, the seven orphan workflows and the five unprotected
private repositories appear as a list rather than as background knowledge.

*Acceptance:* a report in `audit/reports/2026-11-forge-release/verify-<date>.md` with one row per
repository and one column per invariant, and a diff against the previous run.

### R5 — Handover (1 batch)

`audit` gains the log entry and this report; `control-panel` gains the bootstrap as a fifth route
("stand up an account"); the dashboard gains a `seed` row showing the release version and the last
verify date.

*Acceptance:* a reader who has never seen the estate can go from the dashboard to the release to a
working account without asking a question. If they have to ask, the handover is not done.

---

## Definition of done

The release is done when all eleven are true, each with a command behind it.

1. `forge-seed-1.0.0.tar.gz` downloads, and `sha256sum -c SHA256SUMS` prints OK for every file.
2. `MANIFEST.json` lists every file with a sha256 and a one-line purpose, and `install.sh` refuses a
   tree that does not match it.
3. A fresh free-plan account reaches "Forge is live" with all eight phases green, following only
   `04-setup-guide.md`.
4. `tools/make-seed.py --check` fails on each of the fourteen invariants when it is removed.
5. Every workflow in the seed parses, carries the nine properties, and is pinned to the release SHA.
6. The first Monday `new-app` scaffolds one app, fully delivered.
7. `backup --restore-test` passes on a dump written by the new install.
8. The three published pages return 200 with a body.
9. `mode: verify` against the real estate produces a report, and the report is reproducible.
10. `GETTING-STARTED.md` no longer promises anything the release does not do.
11. Nothing in the release writes to another repository without a PR, except `new-app` (which creates
    a repository) and the four `self-*` workflows (which file issues and re-run runs).

---

## Risks

| # | Risk | Likelihood | Consequence | Mitigation |
|---|---|---|---|---|
| 1 | **The seed drifts from `forge`** | high if maintained by hand | two brains, and the estate's four-copies-of-the-exclusion-list defect returns at the largest scale | `make-seed.py` builds it from a tag; there is no second tree. `--check` fails if the artifact's manifest and the tag disagree |
| 2 | **`FANOUT_TOKEN` is too broad, or leaks** | medium | write access to every repository the account owns | 90-day expiry; `AUTHORITY:` comment in every consumer; never in a remote URL; the bootstrap prints the token's scope in phase 0 so it is seen, not assumed |
| 3 | **A phase half-succeeds** | medium | an estate that is partly configured and looks configured | every phase is idempotent and reports `{done, skipped, failed}`; phase 8 fails the run on any failure; `mode: verify` re-checks without changing |
| 4 | **The free plan cannot do what the design assumes** | certain, in three places | branch protection on private repos, the audit-log API, 2,000 private minutes | phase 0 states the tier; phase 3 reports which protections it could apply; the guide names all three as gaps rather than passing over them |
| 5 | **A guard passes because it is not looking** | medium — four recorded instances | a green run that means nothing | phase 6 runs every guard against an *empty* estate first, and `make-seed.py --check` proves each guard can fail |
| 6 | **The first week's cron collides with something** | low | a run refused at startup, invisible | the timetable is in the files, `self-diagnose` checks every cron is real and fires, and phase 5 asserts that no two crons sharing state collide |
| 7 | **A person following the guide hits an undocumented step** | high on the first run | the release looks unfinished | R2 exists for exactly this, with a reader who has not seen the design |
| 8 | **The bootstrap is run against an estate with real data** | medium | a settings sweep could change something the owner wanted | `dry_run` defaults to true; `mode: verify` is the only mode that touches the real account, and it writes nothing outside `bootstrap/last-run.json` |

---

## Rollback

Four levels, and every one of them is a thing the estate can already do.

1. **One repository, one batch:** `git revert <sha>`. This is why the estate keeps one commit per
   repository per batch.
2. **A bad settings sweep:** phase 3 records every value it *changed* (old -> new) in
   `bootstrap/last-run.json`. Re-running with `--revert` applies the old values. Anything it cannot
   revert is listed as such.
3. **A bad release:** the previous tag still exists. `git checkout v0.9.x` on the seed, or re-run
   `make-seed.py` at the older tag. The release is a build artifact, so rolling back is a rebuild.
4. **A damaged estate:** `backup/backup.py --restore-test` proves the newest dump restores; the
   restore procedure is documented in `backup/README.md`. `dumps` has never had an unrecoverable
   failure, and the reason is that the restore test is not optional.

**What cannot be rolled back:** a `git push --force` to a default branch, a deleted repository, and a
rotated token whose old value was not recorded. The first two are blocked by branch protection on 78
of 82; the third is why the expiry is 90 days and the reminder is day 80.

---

## Effort, honestly

| Stage | Batches | Wall clock |
|---|---|---|
| R0 invariants | 1 | 1 session |
| R1 bootstrap | 3 | 3 sessions |
| R2 fresh account | 1 + a week | a week of waiting, one session of work |
| R3 cut the release | 1 | 1 session |
| R4 verify the estate | 1 | 1 session |
| R5 handover | 1 | 1 session |
| **Total** | **8 batches** | **about two weeks, mostly R2's waiting** |

The week in R2 is not slack. It is the only way to observe the first Monday, and the first Monday is
the only proof that the loop closes.

---

## Out of scope, deliberately

- **Migrating the existing estate into the seed.** `mode: verify` reports; it does not migrate. A
  migration is a different job with a different risk profile, and it should be its own plan.
- **The agent's judgement loop.** The "Forge cycle" that builds, retrofits, refreshes and reports in
  one bounded run is the agent's work, not a workflow's. The seed ships the queue, the prompts and the
  state that loop reads. Installing the loop itself is a scheduling decision on the account, and it is
  the owner's.
- **Notification outside GitHub.** Slack was specified and is not wired. One issue per failure class
  is the current, honest state; wiring a webhook is a half-batch and should be its own change with its
  own secret.
- **Deleting the eleven unused kits**, pruning `dumps`, or relitensing anything. All three are
  decisions with a cost and none of them is a prerequisite for standing the system up.
- **`The_Browser`.** A 165 MB C++ codebase that is not finished and whose build fails by design. It
  is in the estate; it is not in the release's acceptance criteria, and pretending otherwise would
  make the first Monday red for a reason that has nothing to do with the release.
