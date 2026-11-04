# 02 — Every workflow: what runs, when, and what calls what

**Measured 3 November 2026, re-measured 4 November.** A direct parse of every workflow file in the
estate — 186 of them, fetched and read rather than quoted from the panel — gives **97 repositories,
186 workflows, 249 jobs and 990 steps**, with **52 edges** between them: 11 reusable workflows and
175 dispatchable ones. **Thirteen** repositories carry no workflow at all, including two apps
(`repertory-reader`, `corefit-md`) that were delivered without a pipeline.

For comparison, the panel's own inventory said 164 workflows on 1 November and 182 on its next scan;
the difference is four workflows added since (`forge/state-set.yml`, `musicgen/pages.yml`,
`ziptastic/ci.yml`, `conqueror-os/sw-3.2.0.yml`) and a change in what each tool counts. Two tools, two
denominators — the estate's oldest conflict, and [`verify-2026-11-04.md`](verify-2026-11-04.md) records
it as invariant 1 failing.

The 186 divide by job, not by repository:

| Kind | Count | What they are |
|---|---|---|
| Product pipeline | 46 + 5 | the canonical caller into `app-builder/build.yml`, and its `pages.yml` |
| Test / lint / CI | ~60 | each repository proving itself on push |
| Refreshers | 11 | registry, dashboard, knowledge, hub, store, blog, profile, metrics, skills, control panel, audit |
| The control plane | 26 | `forge`'s own workflows — the ones that write to other repositories |
| Kit tests | 1 | `app-builder/kit-tests.yml`, all kits in one matrix |
| Release / packaging | ~20 | per-repository builds that are not web apps (Rust, Python, C++) |

---

## 1. The control plane — `forge`'s 28 workflows

These are the ones that decide what the system does. Grouped by the stage they belong to.

### 1.1 Scratch — an idea becomes a repository

| Workflow | Trigger | Cron | What it does | Token |
|---|---|---|---|---|
| `intake.yml` | `issues: [opened, labeled, edited]`, dispatch | — | an `app-idea` issue becomes a classified queue item: `scripts/intake.py` infers kits and deps, appends to `BACKLOG.md` and `QUEUE/`, comments back on the issue | `github.token` |
| `new-app.yml` | dispatch **and** schedule | `0 7 * * 1` | two jobs. `scaffold` (manual): validates the name, `gh repo create`, copies `templates/app`, writes the canonical `build-apps.yml` **pinned to a SHA**, commits, pushes, then verifies by comparing blob shas in the new repo. `auto` (scheduled): picks the first `QUEUE/app-*.md` whose repo does not exist and which is ≥400 bytes and not DRAFT/PAUSED, then scaffolds it identically | `FANOUT_TOKEN` |
| `adopt.yml` | schedule, dispatch | `0 4 * * 1` | finds repositories with **no workflows** and adds the standard set. A repo with none is committed to directly; a repo that already has some gets a PR, so an existing setup is never changed behind the owner's back. Never overwrites an existing file | `FANOUT_TOKEN` |

`new-app` is the workflow to read if you read only one. Its header records three defects it closed:
it used to only *echo* "Would create …"; it used to be dispatch-only, so 154 specs sat unbuilt; and
its own name-validation step made every Monday's run red on a job with nothing to do.

### 1.2 Deliver — an artefact becomes public

| Workflow | Trigger | Cron | What it does | Token |
|---|---|---|---|---|
| `app-deliver.yml` | schedule, dispatch | `0 5 * * 1` | the delivery sweep. Checks **seven** things on every repository — landing page, live demo, pipeline caller, Pages enabled, README badges, screenshot, release — and applies only what is absent, generating the landing page from the app's own metadata. Idempotent: a landing page means done | `FANOUT_TOKEN` |
| `release.yml` | `workflow_call`, dispatch | — | reusable: changelog from the last tag, version bump, GitHub release | `github.token` |
| `docs.yml` | `workflow_call`, dispatch | — | reusable: README and landing-page regeneration | `github.token` |
| `pages.yml` | `workflow_call`, dispatch | — | reusable: deploy `docs/` to Pages | `github.token` |
| `build.yml` | `workflow_call`, dispatch | — | reusable: EXE + APK + Linux from `forge` (the app-builder one is canonical; this is the older sibling) | `github.token` |
| `test.yml` | `workflow_call`, dispatch | — | reusable: headless tests | `github.token` |
| `health.yml` | push to `RUNS.jsonl` / `APP_MASTER_LIST.md` / `QUEUE/**`, schedule, dispatch | `23 4 * * 1` | copies `SPEC-GAP.json` and `runs.json` into the **public** dashboard repo (a public page cannot read a private repo), and runs the **one central notifier**: a single issue naming what failed, across all seven failure classes | `FANOUT_TOKEN` |

### 1.3 Repair — the system keeps itself honest

| Workflow | Trigger | Cron | What it does | Token |
|---|---|---|---|---|
| `self-diagnose.yml` | schedule, dispatch | `0 8 * * 3` | checks the **machinery**, not the code: every workflow parses, its cron is real, it **actually fires** (a scheduled workflow older than twice its period is not scheduled, it is broken), and every local file a `run:` block names exists. Also detects a startup failure — a run with 0 jobs — which is otherwise unobservable | `FANOUT_TOKEN`, `github.token` |
| `self-heal.yml` | `workflow_call`, schedule, dispatch | `30 20 * * 3` | re-runs a failed run **once**; escalates the rest as an issue. Never pushes, never force-pushes, never merges. Carries a **killswitch** input, which was unreachable until the inputs were declared | `FANOUT_TOKEN` |
| `audit.yml` | `workflow_call`, schedule, dispatch | `0 4 * * 1` | reusable conformance audit: README, LICENSE, description, landing page, resolving homepage — `total` counted from the checks that actually ran | `github.token` |
| `licence.yml` | schedule, dispatch | `0 4 * * 3` | licence badge vs `LICENSE` vs the policy file, across the estate | `FANOUT_TOKEN` |
| `kit-audit.yml` | schedule, dispatch | `0 6 * * 1` | which vendored kits are dead, and the harvest signals — reading `index.html`, `docs/index.html` **and** `docs/play/index.html`, which was the bug that made every kit look dead | `github.token` |
| `lint.yml` | push, schedule, dispatch | `0 6 * * 2` | four jobs. One is `guards`: `register-check`, `policy-guard`, `spec-guard`, `demo-drift` self-tests — so five guards that used to run by hand now run on every push | `github.token` |
| `sweep.yml` | dispatch only | — | **the ONE cross-repo mechanism.** One PR per repository, one fixer per rule (`nojekyll`, `changelog`, `kit_bump`), `--cap` bounds the blast radius, every change leaves as a PR. Supersedes `fanout.yml` | `FANOUT_TOKEN` |
| `fanout.yml` | `workflow_call`, dispatch | — | superseded by `sweep`'s `kit_bump`; kept because its PRs are open. Cannot run on its own | `FANOUT_TOKEN` |
| `credential-guard.yml` | push, PR, schedule, dispatch | `20 6 * * 2` | fails the build if the preflight pointer in the README breaks — the guard against three cycles in a row reporting the system blocked on a 404 from the wrong credential | `github.token` |
| `backup.yml` | `pull_request`, dispatch | — | calls `backup/backup.yml` for a pre-merge snapshot | `BACKUP_TOKEN` |
| `dumps-dedupe.yml` | schedule, dispatch | `0 5 */4 * *` | byte-identical dedupe across the dumps corpus, grouped by `(repository, tree sha)` | `FANOUT_TOKEN` |
| `code-compression.yml` | schedule, dispatch | `0 7 * * 2` | the compression pipeline check | `github.token` |
| `heartbeat.yml` | schedule, dispatch | `0 6 * * *` | stamps `HEARTBEAT.md` daily. A heartbeat must beat — it is the cheapest proof the control plane is alive | `github.token` |
| `repo-learning.yml` | schedule, dispatch | `0 7 * * 1` | turns the run history into `registry/learnings.json` and `lessons.json` | `github.token` |
| `backlog-status.yml` | schedule, push, dispatch | `0 5 * * 1` | the backlog's own status file | `github.token` |
| `self-update.yml` | schedule, dispatch | `0 9 * * 1` | reports which pinned action SHAs are behind. It does **not** bump them — a major bump can be breaking, so a human sees the diff | `github.token` |
| `log-append.yml` | dispatch | — | appends a run record | `github.token` |

### 1.4 The seven that nothing calls

`audit`, `docs`, `fanout`, `pages`, `release`, `self-heal` and `test` are `workflow_call`-able and
have **no caller** in the estate. That is not a defect and it is worth stating plainly: they are the
public interface of the control plane, available to any repository that wants to adopt them, and the
estate's own copies of `docs`/`pages`/`release`/`test` were superseded by `app-builder`'s versions.
The inventory reports them as orphans every week, which is the correct behaviour for a map — it says
what is connected to nothing, and a reader decides.

---

## 2. The pipeline — one push, end to end

This is the path that runs ~46 times per change in the estate, and the one a new install must
reproduce exactly.

    push to main
      -> <app>/.github/workflows/build-apps.yml          12 lines, the canonical caller
      -> uses: drsamonline/app-builder/.github/workflows/build.yml@<sha>
         with: app_name, app_src, deploy_path
         |
         +- exe      windows-latest  PyInstaller -> portable .exe, icon generated, icon verified
         +- apk      ubuntu-latest   Gradle -> signed .apk, launcher icons generated and verified
         +- linux    ubuntu-latest   a binary that must SERVE the app in a smoke test
         +- version  consume change files -> commit VERSION + CHANGELOG -> versioned release
         +- kit-guard  refuse a kit added to a page that already existed
         +- parity     compare the app against its base
         +- demo       docs/play/index.html must equal the app + an SEO block
         |
         +- release  collect the three artifacts -> rolling tag `app-latest`
         +- pages    enable Pages if off -> upload -> deploy
         +- shot     headless Chromium -> screenshot -> written back into the README

**Four gates, all of them real:** `kit-guard` (the one-way rule), `parity` (no capability lost),
`demo` (the demo is the app), and the Linux smoke test (the binary must actually serve). The audit
called this the strongest part of the estate and found the input contract clean in every caller.

**Two weaknesses, unchanged and recorded rather than hidden:** no staging — a push to `app-builder`
reaches all 47 callers at once — and failure is local: a red build notifies nobody, because no
workflow in the estate uses `workflow_run`.

---

## 3. The refreshers — eleven workflows that keep the pages true

| Repository | Workflow | Cron (UTC) | Writes |
|---|---|---|---|
| `registry` | `refresh.yml` | `42 4 * * 1` | `repos.json`, `catalog.json`, `plan.json` |
| `dashboard` | `refresh.yml` | `47 3 * * 2` | `data.json`, forks, community, traffic, changes, `feed.xml` |
| `knowledge` | `refresh.yml` | `32 4 * * 2` | the plan-status block inside the system plan |
| `drsamonline.github.io` | `refresh-hub.yml` | `37 3 1,16 * *` | the project index |
| `drsamonline` | `update-profile.yml` | `17 3 * * 1` | README + metric cards |
| `drsamonline` | `metrics.yml` | `0 4 * * 2` | metrics |
| `Matneo` | `store.yml` | `22 4 * * 2` | the storefront catalogue |
| `Matneo` | `store-images.yml` | `0 3 1,16 * *` | card images (installs Chromium) |
| `Matneo` | `blog.yml` | `12 4 * * 2` | `posts.json` |
| `skills` | `refresh.yml` | `23 3 * * 1` | the skills catalogue + `validate` job |
| `control-panel` | `scan.yml` | `0 6 * * 2` | `inventory.json`, `plan.json`, the page |
| `audit` | `licence-check.yml` | `31 3 * * 1` | the licence snapshot |
| `audit` | `health.yml` | `43 3 * * *` | `docs/health.json`, the page |
| `app-builder` | `kit-tests.yml` | `0 5 * * 3` | all-kit test matrix |
| `dumps` | `backup-all.yml` | `0 */6 * * *` | the estate snapshot |

Four of these read the same module: `registry`, `dashboard`, `knowledge` and the store all check out
`app-builder` and run `drsoam.py` in a mode. One shared client, four outputs — which is why the
numbers can be compared, and why the day one of them gains its own copy is the day they stop being
comparable.

---

## 4. The timetable

**32 scheduled workflows.** Two things are true of the timetable and only one of them was ever the
rule. The two jobs that install a Chromium browser run twice a month rather than weekly, because that
is the expensive step. And same-minute groups **do** exist — `adopt` and `audit` both fire Monday
04:00, `new-app` and `repo-learning` both Monday 07:00 — because those pairs share no state. The
invariant that actually matters is the `concurrency` group, not the minute; "no two crons share a
minute" was a description that read like a rule, and a fresh install should not be built on it.

    daily      03:17  profile        03:37  hub (1st/16th)   03:43  audit health
               06:00  heartbeat      every 6h  dumps/backup-all
    Monday     03:23  skills        03:31  audit licence     04:00  audit+adopt
               04:05  app-deliver   04:05  backlog-status    04:05  dumps-dedupe
               04:23  forge health  04:42  registry          05:00  new-app
               05:00  repo-learning 06:00  kit-audit         09:00  self-update
    Tuesday    03:47  dashboard     04:00  metrics           04:12  Matneo blog
               04:22  Matneo store  04:32  knowledge         06:00  control-panel
               06:20  credential-guard
    Wednesday  05:00  kit-tests     06:00  lint              07:00  code-compression
               08:00  self-diagnose 20:30  self-heal
    1st+16th   03:00  store-images  03:37  hub

Every job carries a `timeout-minutes` (four did not — the default is six hours) and every checkout is
`fetch-depth: 1`. Both were swept in one batch and both are bootstrap invariants now.

---

## 5. What a workflow in this estate must always have

Earned by failure, one line each. The bootstrap enforces all nine on every file it installs.

1. **A `concurrency` group with a literal suffix** if it is reusable. In a called workflow
   `github.workflow` is the *caller's* name, so an unsuffixed group collides with the caller and
   GitHub refuses to schedule the run: 0 jobs, no log, no check run. This is how `backup.yml` failed
   40 times.
2. **`timeout-minutes` on every job.**
3. **`fetch-depth: 1`** unless the job needs history.
4. **A pinned SHA** for every `uses:`, including reusable workflows. `@main` means an edit to one file
   reaches 47 builds immediately.
5. **`permissions:` scoped to the job**, and an `AUTHORITY:` comment when the file writes to another
   repository — because the `permissions:` block does not describe what a PAT can do.
6. **No token in a remote URL.** `gh auth setup-git`.
7. **A verdict, not an exit code,** on every commit: `tools/commit-and-verify.sh` compares blob shas
   after the push, so "did it land" is answered by the branch and not by `git`.
8. **A secret that may be absent is `required: false`**, and checked in the first step of the job.
9. **No step that can swallow a failure.** `set -o pipefail`, and `::notice::` where a soft failure is
   deliberate — the estate had 42 silent swallows and 14 unpiped pipelines at the last census.
