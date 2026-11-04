# 03 — The one release

**The design.** A single versioned artifact that, extracted into a repository and dispatched once,
stands the whole system up on the account it is pointed at — and carries every one of the audit's
surviving defects already fixed, so a new install does not inherit them.

---

## 1. What ships

    forge-seed-1.0.0.tar.gz
      forge/                    373 files: the complete control plane (see §2)
      bootstrap/                7 files: the remote half (§5)
      MANIFEST.json             every file, its sha256, and the one thing it is for
      SHA256SUMS                the same digests, `sha256sum -c` reads this
      install.sh                the local half: verify the manifest, link the `forge` command
      VERSION                   1.0.0

Cut as a **GitHub Release on `drsamonline/forge`**, tag `v1.0.0`, with the tarball and `SHA256SUMS`
as assets. Two ways to stand up an account from it, and both must work:

**A — as a repository (the primary path).** Create an empty private repository, extract the tarball
into it, push, then run `Actions -> bootstrap -> Run workflow` with `mode: full`. The repository *is*
the control plane from that moment; the bootstrap configures everything around it.

**B — locally.** `tar xzf forge-seed-1.0.0.tar.gz && cd forge && ./install.sh`, which verifies the
manifest, links `forge`, and prints the three things it cannot do from a laptop: create the sibling
repositories, set a secret, and enable Pages.

Both paths end at the same place, and both are checked by the same phase 6.

---

## 2. What is inside — the manifest, by directory

Counts are the tree at `forge@main`, re-measured 4 November 2026: **373 files and 28 workflows**.

| Directory | Files | What it carries | In the seed? |
|---|---|---|---|
| `.github/workflows/` | 28 | the control plane: intake, new-app, adopt, app-deliver, sweep, self-diagnose, self-heal, lint, health, kit-audit, licence, dumps-dedupe, heartbeat, repo-learning, backlog-status, self-update, credential-guard, log-append, `state-set` (sets one dotted key in `STATE.json`, added 3 Nov), plus the reusable audit/docs/pages/release/test/build | yes |
| `tools/` | 34 | `commit-and-verify.sh`, `self-diagnose.py`, `sweep.py`, `kit-audit.py`, `kit-drift.py`, `licence.py`, `policy-guard.py`, `register-check.py`, `spec-guard.py`, `spec-shape.py`, `spec-gap.py`, `demo-drift.py`, `startup-failure-watch.py`, `dumps-dedupe.py`, `dumps-compact.py`, `dumps-consolidate.py`, `dumps-record.py`, `repo-learning.py`, `runlog.py`, `rules.py`, `forge_rules.py`, `shellcheck-runs.py`, `strip-shared-block.py`, `restore-schedules.sh`, `wf-check.py`, `adopt.py`, `app-deliver.py`, `code-compression.py`, `credential-guard.py`, `backlog-status.py`, `licence-headers.py`, `self-update.py`, `spec-audit.py`, `LICENCE.md` | yes |
| `scripts/` | 6 | `intake.py`, `batch.py`, `new-app.py`, `new-kit.py`, `attempts.py`, `forge` (the CLI) | yes |
| `PROMPTS/` | 21 | 20 canonical prompts + `.gitkeep`: `preflight`, `access`, `rules`, `build`, `changelog`, `priority`, `pipeline`, `next-cycle`, `run-log`, `retry`, `refresh`, `topics`, `dataset-licence`, `deck-brief`, `free-ai`, `naughty-inputs`, `shellcheck`, `loop-safety`, `advance`, `retrofit` (retired, kept for the record) | yes |
| `QUEUE/` | 188 | 154 app specs, 5 kit specs, 8 rule specs, 5 system specs, 11 update specs, 3 idea specs, `lan-family`, `lib-van-ui` — one file per work item, each a specification with a failure path | yes |
| `AUDIT/` | 37 | the closed audit: `PHASES.md`, `VERIFIED_FINDINGS.md` (103 findings), nine phase directories, `REMEDIATION_LOG.md`, `REMAINING_WORK.md`, `CLOSEOUT.md`, `schedules-stopped.json` | yes — it is the reasoning, and it is the only place the *why* is written down |
| `registry/` | 15 | the machine-readable state the tools read: `licence-policy.json`, `audit.json`, `delivery.json`, `deps.json`, `diagnose.json`, `drift.json`, `learnings.json`, `lessons.json`, `parity.json`, `size.json`, `spec-mismatch.json`, `startup-failures.json`, `updates.json`, `backlog-done.json`, `false-completions.md` | yes, as **seed** values |
| `templates/` | 4 | `app/` (index.html + README) and `master-list/` (the portfolio page) | yes |
| `docs/` | 2 | `lib-van-ui-decision.md` and `.gitkeep` — the decisions that had no other home | yes |
| `REPORTS/` | 2 | dated reports from scheduled runs | empty seed + `.gitkeep` |
| root | 33 | `README`, `GETTING-STARTED`, `HANDOFF`, `GOVERNANCE`, `STATUS`, `WORKLIST`, `BACKLOG`, `APP_MASTER_LIST`, `LEARNINGS`, `LESSONS`, `PAUSED`, `DIAGNOSE`, `CYCLE-START`, `HEARTBEAT`, `OPEN-SOURCE-POLICY`, `PRIVACY`, `TERMS`, `ROADMAP`, `SIZE`, `SPEC-SHAPE.md`, `SPEC-SHAPE.json`, `REFERENCE-lexora-compression.md`, `STATE.json`, `PROGRESS.log`, `RUNS.jsonl`, `LOCK`, `SIGNATURE.json`, `install.sh`, `LICENSE`, `LICENSE-PERSONAL`, `LICENSE-SUMMARY`, `NOTICE`, `AUTHORS` | yes |

**`STATE.json` ships empty of history, not empty of shape.** `current`, `doing`, `done`, `blocked`
are reset; `budget`, `decisions`, `attempts` keep their schema and the 41 recorded decisions, because
those decisions are the estate's judgement and a new install should not have to re-litigate them.

**What is deliberately *not* in the seed:** `RUNS.jsonl` history, `PROGRESS.log` history, the six
`dumps` repositories, and every app. They are data, not machinery. A seed that carried the data would
be a backup, and backups have their own repository and their own restore test.

---

## 3. Why it is generated, not copied

`tools/make-seed.py` builds the tarball from the tagged tree. It refuses to run on a dirty tree, it
writes `MANIFEST.json` from the actual files, and it fails if any of the fourteen invariants in §4 is
missing from the tree it just packaged.

The alternative — a second repository that *is* the seed — is the defect this estate already paid for
four times. `drsoam.py` said `# ---- the ONE exclusion list ----` and there were four copies. `web-kit`
was re-vendored into twenty apps and eleven of them drifted. The audit's own closeout says it in one
line: **a sample standing in for the whole**. A maintained second copy of the brain is the largest
possible sample error, so there is one source and one build.

---

## 4. The fourteen fixes baked in

Each one is a defect the audit found, repaired in the live estate, and now made a **property of the
seed** so a fresh install cannot reproduce it. This is the "optimised and tweaked" half of the
release, and it is why the seed is not simply a tarball of today's `forge`.

| # | Invariant | What it prevents | Enforced by |
|---|---|---|---|
| 1 | **One discovery path.** Every "what repositories exist" call goes through `drsoam.repos()` and emits `{seen, skipped}` | four code paths answering 74 / 69 / 78 / 30, none recording what it could not see | `register-check.py` asserts `seen + skipped` equals the account's own count |
| 2 | **One exclusion list**, in one module, imported by every generator | four copies that had already diverged; the published product list was a function of which script ran last | `policy-guard.py` |
| 3 | **A producer publishes what it computes.** `registry/refresh.yml` stages `plan.json` | a reconcile written and never committed, so the dashboard computed its own answer against a different denominator | the commit's own file list, asserted in the workflow |
| 4 | **A label matches its formula.** `score` is renamed `metadata_completeness`; `build_health` comes from the latest run per repository | eight of nine repositories with a failing build presented at 5/5 | `register-check.py` |
| 5 | **No artifact without a producer or a consumer.** `builds.json` is gone; `gaps.json` and `routes.json` are produced and rendered or removed | three artifacts written by nothing and read by nothing | `wf-check.py` over the inventory |
| 6 | **Every commit step carries a verdict** — "did it land", read back by blob sha | a commit step reporting `git`'s exit code instead of the data | `commit-and-verify.sh`, vendored into the seed and called by 11 workflows |
| 7 | **A reusable workflow suffixes its `concurrency` group** with a literal | 40 failed runs before any job was created, and nothing able to report it | `lint.yml` parses every workflow and fails on an unsuffixed group |
| 8 | **Reusable workflows are pinned to a SHA**, never `@main` — **and a fixer bumps them** | one edit reaching 47 builds with no staging and no tag; and, once pinned, a pin nobody bumps, which is a slower `@main` | `make-seed.py` rewrites every `uses:` to the release SHA; `sweep.py` gains a `build_pin` fixer, and `mode: verify` re-checks the pin on every run |
| 9 | **A secret that may be absent is `required: false`**, checked in the first step | a `required: true` secret rejecting the call before validation, so the workflow's own guard could never run | `self-diagnose.py` cross-checks declared inputs and secrets against every caller |
| 10 | **A startup failure is detectable** — 0 jobs, or a run named after its own path | the one failure class with 0 jobs, 0 checks, 0 annotations and a 22-byte log | `startup-failure-watch.py`, wired into `self-diagnose` |
| 11 | **A backup proves itself.** `--restore-test` runs on the newest dump; dedupe groups by `(repository, tree sha)` | 349-file restores verified by hand and never again; a dedupe that compared the wrong level and always said "nothing duplicated" | `backup.py --restore-test` in `bootstrap` phase 6, and monthly |
| 12 | **Every documented rule has a guard, and the guards run in CI** | five rules that were prose, and five guards that ran when someone remembered | `lint.yml` `guards` job on every push |
| 13 | **Exactly one cross-repo mechanism.** `sweep.yml`, one PR per repository, `--cap` bounded | two mechanisms that both open cross-repo PRs, and can cross | `fanout.yml` ships dispatch-only and is documented as retired |
| 14 | **A failed read is not an empty result.** Refuse to publish; keep the previous artifact byte-for-byte; exit non-zero | a failed fetch producing an empty graph, a 74-row reset to `role: product, score: 0`, and a green run | the `drsoam.py` degradation pattern, copied outward |

---

## 5. The bootstrap — eight phases, one dispatch

`bootstrap/bootstrap.yml`, `workflow_dispatch` only, **`dry_run` defaults to `true`**. Every phase is
idempotent, prints `{done, skipped, failed}`, and writes its verdict to the run summary *and* to
`bootstrap/last-run.json`. No phase proceeds if the previous one failed.

**Inputs:** `mode` (`full` | `verify`), `dry_run` (bool, default true), `owner` (default: the
repository owner), `visibility` (`private` | `public`, default private), `app_globs` (default: every
repository that has a `docs/play/index.html`).

### Phase 0 — Preflight
Who am I; what can `FANOUT_TOKEN` see; what plan is this account on. Prints the repository count with
`{seen, skipped}`, the plan tier, and therefore **which of the protections in phase 3 are possible**.
On the free plan: branch protection on a private repo is not possible, the audit-log API is
Enterprise-only, and 2,000 Actions minutes a month is the ceiling for private CI. Says so, once, at
the top of the run, rather than letting a later phase look like a failure.

### Phase 1 — Repositories
Create or verify `registry`, `knowledge`, `dumps`, `backup`. Never overwrites; a repository that
exists is verified and left alone. Verifies `dumps` is **private** — a public dumps repository would
publish any private repository it backs up, which is why the real one is private on purpose.

### Phase 2 — Discovery
The one measured census. Writes `registry/repos.json` from `drsoam.repos()` with `{seen, skipped}`,
and asserts `seen + skipped` equals phase 0's own count. **This phase is the one that must pass
before any other number is trusted**, because every derived figure in the estate is downstream of it.

### Phase 3 — Settings
Per repository, applied through the API and read back: description, topics, licence label, homepage,
Actions workflow permissions (`Read and write`, and allow Actions to create and approve PRs), Pages
source (`GitHub Actions`), delete-branch-on-merge, and branch protection where the plan allows —
block force-push and deletion, admins included. Read back, never assumed: the estate's rule is that a
change is not done when it is pushed, it is done when it is read back from the API.

### Phase 4 — Pipeline
For every app repository: does `.github/workflows/build-apps.yml` exist? If not, write the canonical
caller, pinned to the release SHA, and **verify it landed by comparing blob shas in that repository**
— the `new-app` verdict pattern, applied outward. If it exists, leave it alone and report the diff.

### Phase 5 — Schedules
The timetable from `02-workflows.md` §4, written into the workflow files themselves (crons are code,
not settings). Asserts that no two crons that share state collide, and that the two Chromium jobs
run twice a month.
A scheduled workflow is not a schedule until it has fired once; phase 8 records the first fire.

### Phase 6 — Guards
The phase no current install has. Runs, against the *new* estate:

    register-check.py      the register is internally consistent
    policy-guard.py        every licence claim matches the registry
    spec-guard.py          every spec has a runnable home
    demo-drift.py          (self-test only — no app is checked out yet)
    wf-check.py            every workflow parses, and has the nine properties
    backup --restore-test  the newest dump restores, file for file
    kit-audit.py           every vendored kit is either used or absent

**A guard must pass on an empty estate before it is trusted on a full one.** A guard that has never
seen a clean run cannot tell "nothing is wrong" from "I am not looking", and this estate has four
recorded instances of exactly that.

### Phase 7 — Publish
Enable Pages and deploy: the dashboard, the control panel, the hub. Asserts three URLs return 200
with a body. A 404 on Pages takes a minute after the first deploy, so this phase waits and re-checks
rather than failing on the first attempt.

### Phase 8 — Report
Opens **one** issue: *"Forge is live"*, carrying the verification table — phase, done, skipped,
failed, and the evidence line for each. The next reader, human or agent, starts from evidence rather
than from a claim. If anything failed, the issue is labelled `needs-you` and the run fails, so the
failure is visible on the repository and not only in a log.

**Total runtime:** roughly 12–20 minutes, most of it Pages propagation and the restore test.

---

## 6. What it does after the bootstrap

The bootstrap stands the system up. This is what then runs, with no further input.

**Hour 1.** `heartbeat` stamps. `self-diagnose` parses all 28 workflows and checks each cron is real.
`register-check` passes. The dashboard is live and lists what exists.

**Day 1.** `dumps/backup-all` snapshots the estate (every 6 hours). `audit/health` writes the health
file. `intake` is listening: an issue labelled `app-idea` becomes a queue item within a minute, with
its kits inferred and its deps recorded.

**Week 1 — the first Monday.** `adopt` (04:00) finds any repository with no workflows. `audit` (04:00)
scores every repository. `app-deliver` (05:00) checks the seven delivery facts on every app and applies
what is missing. `backlog-status` and `dumps-dedupe` (05:00). `new-app` (07:00) **scaffolds the first
spec whose repository does not exist**, writes the canonical caller pinned to the release SHA, and
verifies by blob sha. `repo-learning` (07:00) writes the lessons. `kit-audit` (06:00) says which kits
are dead. `self-update` (09:00) says which pins are behind.

**Wednesday.** `kit-tests` runs every kit's suite in one matrix. `lint` runs the guards. `self-diagnose`
checks the machinery. `self-heal` re-runs what is transient and files an issue for what is not.

**Steady state.** One app per week appears from the queue, fully delivered: repository, pipeline,
EXE, APK, Linux binary, release, landing page, live demo, screenshot, README badges. The registry,
the dashboard, the control panel, the hub, the store and the skills catalogue refresh themselves.
Anything that breaks opens exactly one issue naming it.

---

## 7. Does it do everything we envisioned?

The system plan (§4, §5, §8.1, §8.2, §9) asked for twelve capabilities. This is where each one
actually lives after the release, and the honest status of each.

| # | The capability | Where it lives | Status |
|---|---|---|---|
| 1 | **Feed an idea, get an app** | `issues: [app-idea]` -> `intake.py` -> `QUEUE/` -> `new-app.yml` auto | **live** — proved end to end with a real issue |
| 2 | **The same twelve steps every time** | `PROMPTS/` + the canonical caller + the reusable build | **live** — 47 callers, contract verified |
| 3 | **Every app delivered, not just built** | `app-deliver.yml`, seven checks | **live** |
| 4 | **Three platforms from one commit** | `app-builder/build.yml`: EXE, APK, Linux | **live** |
| 5 | **A spec before a scaffold** | `spec-guard.py` + the 400-byte and DRAFT checks in `new-app` | **live** — Rule 0 in executable form |
| 6 | **Budget-aware batching** | `STATE.json.budget`, `scripts/batch.py`, `LOCK` + `concurrency` | **partly live** — the machinery exists and is honoured by the agent's runs; it is not yet a scheduled GitHub job |
| 7 | **Self-troubleshooting** | `self-diagnose.yml` (parses, crons, fires, files exist, startup failures) | **live** |
| 8 | **Self-repairing, safely** | `self-heal.yml` — re-run once, escalate the rest, never push/force/merge | **live**, scope `forge` only by decision (F-57) |
| 9 | **Self-learning** | `repo-learning.yml` -> `registry/learnings.json`, `lessons.json` | **live** |
| 10 | **Nothing runs itself into a loop** | dispatch-only sweep, `[skip ci]`, bot-actor guard, `--cap`, DAG check, attempt cap, lock + watchdog | **live** — §8.2's ten rules map to these |
| 11 | **One dashboard, always current** | `dashboard` + `control-panel` + `hub`, each on its own cron | **live** |
| 12 | **The system can prove it** | the audit register, the guards, `audit` (this repo) | **live** |

Two things the vision asked for that are **not** built, and should be stated rather than implied:

- **The agent's judgement loop** — the "Forge cycle" that builds one item, retrofits one kit, refreshes
  four outputs and reports, in one bounded run. The GitHub half exists; the judgement half is the
  agent's, and it is not a workflow. The bootstrap cannot install a person or an agent, so the seed
  ships the queue, the prompts and the state that the agent reads, and the agent still has to be
  scheduled by whoever owns the account.
- **Notification to a human outside GitHub.** `health.yml` opens one issue. There is no Slack, no
  email, no push. The system plan specified Slack delivery; it is not wired. One issue per failure
  class is the honest current state.

---

## 8. What the release deliberately does not do

- **It does not migrate an existing estate.** It stands a new one up. Pointing it at the current
  account is `mode: verify`, which reports what differs and changes nothing.
- **It does not restore data.** `dumps` restores with `backup.py --restore-test` and a documented
  procedure; the seed does not touch it.
- **It does not delete anything.** No prune, no archive, no cleanup of the eleven unused kits. A sweep
  that deletes a kit while its successor is unwritten is how a consolidation becomes a regression.
- **It does not decide the licence.** The policy file ships as it is; the four decisions in the
  README's §"The four decisions" are the owner's.
- **It does not claim to work on a plan it has not been tested on.** Phase 0 prints the plan tier and
  phase 3 reports which protections it could apply. Anything unavailable is reported as unavailable,
  not as passed.
