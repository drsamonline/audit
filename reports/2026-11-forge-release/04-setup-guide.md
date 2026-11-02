# 04 — The setup guide

**Every step, in the order it must happen.** Written for a person who has never opened the Actions
tab. Roughly 40 minutes, of which 25 is waiting for GitHub.

The order is not a preference. Each step depends on the one before it, and three of the steps are
things that cannot be done from a workflow at all — they need a human in a browser, once.

---

## Step 0 — Account hygiene (10 minutes, once per account)

1. **Two-factor authentication on the account.** Without it, one password is the whole estate.
2. **Recovery codes stored somewhere a second person can reach.** Not in the repository.
3. **Add a trusted second person as admin on the four repositories that cannot be rebuilt** —
   `forge`, `registry`, `dumps`, `app-builder`. They do not need to maintain anything; they need to be
   able to get in. This is the only part of the audit's governance finding worth acting on, and only
   the owner can do it. *Do it after step 2, when the repositories exist.*

The bootstrap checks whether step 3 was done and prints it as a **warning, never as a pass**. A
document that claims continuity is not continuity.

---

## Step 1 — Create the seed repository

**GitHub -> New repository**

| Field | Value | Why |
|---|---|---|
| Name | `forge` | the brain's name; the workflows refer to it by path |
| Visibility | **Private** | the product is the system, not the apps. Apps stay public, where Actions are free |
| Initialise with | **nothing** — no README, no .gitignore, no licence | the seed brings its own; an extra commit makes the first push a merge |

Then, locally:

    tar xzf forge-seed-1.0.0.tar.gz
    cd forge
    sha256sum -c SHA256SUMS          # must print OK for every line
    ./install.sh                     # verifies MANIFEST.json, links `forge`
    forge --version                  # must print 1.0.0

    git init -b main
    git add -A
    git commit -m "chore: forge 1.0.0 seed"
    git remote add origin https://github.com/<owner>/forge.git
    gh auth setup-git                # credential helper; the token never enters the remote URL
    git push -u origin main

**Nothing runs yet.** `bootstrap.yml` is `workflow_dispatch` only, and no other workflow in the seed
has a `push` trigger that writes outside the repository. That is deliberate: the first thing that
happens in a new estate should be a decision, not a cron.

---

## Step 2 — Actions permissions (before anything is dispatched)

**Repository -> Settings -> Actions -> General**

| Setting | Value | What breaks without it |
|---|---|---|
| Actions permissions | **Allow all actions and reusable workflows** | the pinned `uses:` steps cannot resolve |
| Workflow permissions | **Read and write permissions** | every commit step fails at `git push` |
| Allow GitHub Actions to create and approve pull requests | **checked** | `sweep` and `adopt` cannot open a PR — and a cross-repo change that cannot be a PR must not be a push |
| Fork pull request workflows | leave default | this estate takes no fork PRs |

**This must be done before step 5.** A workflow cannot grant itself write access, and the first
failure it produces looks like a permissions error inside a step rather than a missing setting.

---

## Step 3 — The two tokens

Two fine-grained personal access tokens. Nothing else needs a credential: `github.token` covers
everything that happens inside one repository.

**Create a token:** *Personal settings -> Developer settings -> Personal access tokens ->
Fine-grained tokens -> Generate new token.*

### `FANOUT_TOKEN` — the one that writes to other repositories

| Field | Value |
|---|---|
| Token name | `forge-fanout` |
| Expiration | **90 days** — and a calendar reminder for day 80 |
| Resource owner | your account |
| Repository access | **All repositories** (a new app must be reachable the moment it is created) |
| **Contents** | Read and write |
| **Pull requests** | Read and write |
| **Workflows** | Read and write — *without this, writing `.github/workflows/*` into another repository is refused* |
| **Issues** | Read and write — `self-heal` and `self-diagnose` file issues where the failure is |
| **Administration** | Read and write — repository settings and branch protection (step 7) |
| **Pages** | Read and write — enabling Pages on a repository that has none |
| **Metadata** | Read (mandatory, granted automatically) |

**This is the highest-value credential in the estate and it should be treated as such.** It can write
to every repository the account owns. Three mitigations, all cheap: the 90-day expiry, the
`AUTHORITY:` comment at the top of every workflow that uses it (so a reader of the file knows what it
can do even though the `permissions:` block says otherwise), and a rule that it never appears in a
remote URL, a log line, or an error message.

### `BACKUP_TOKEN` — the one that writes dumps

| Field | Value |
|---|---|
| Token name | `forge-backup` |
| Expiration | 90 days |
| Repository access | **Only select repositories:** `dumps`, `dumps-2` … (add each new part when it rolls over) |
| **Contents** | Read and write |

Narrow on purpose: it writes snapshots and can do nothing else.

**Add both:** *Repository -> Settings -> Secrets and variables -> Actions -> New repository secret.*
Names must be exactly `FANOUT_TOKEN` and `BACKUP_TOKEN` — they are referenced by name in the workflows
and a typo reads as "the secret is absent", which the estate has already mistaken for "the repository
is absent" three times.

---

## Step 4 — Pages (optional, phase 7 does it)

Per repository: *Settings -> Pages -> Build and deployment -> Source: **GitHub Actions***.

The `pages` job in `build.yml` and in `app-builder/pages.yml` enables Pages itself when it is off, so
this is a convenience, not a requirement. Set it by hand for the three publishing repositories —
`dashboard`, `control-panel`, `drsamonline.github.io` — because those deploy from their own workflows
and a first 404 is otherwise confusing.

---

## Step 5 — The first dispatch, dry

**Repository -> Actions -> bootstrap -> Run workflow**

    mode:     full
    dry_run:  true          <- the default, and it stays true the first time
    owner:    <your account>
    visibility: private

Read the run summary. It prints, phase by phase, `{done, skipped, failed}` and one evidence line each.
A dry run creates nothing, sets nothing and writes nothing outside the repository.

**What a clean dry run looks like:** phase 0 prints the plan tier and the repository count with
`{seen, skipped}`; phases 1 and 3 print what they *would* create and change; phases 2 and 6 print the
numbers they would write. If phase 0 reports `seen + skipped` that does not match your own repository
count, **stop** — the token cannot see everything it needs to, and every number downstream of it will
be wrong.

---

## Step 6 — The real dispatch

Same screen, `dry_run: false`. Twelve to twenty minutes. Phase 8 opens one issue titled **"Forge is
live"** with the verification table. If it is labelled `needs-you`, a phase failed and the run is red.

Then, in order — each one dispatch-only, each one safe to run twice:

    Actions -> self-diagnose   -> Run workflow    (parses all 27 workflows, checks every cron is real)
    Actions -> lint            -> Run workflow    (the guards)
    Actions -> audit           -> Run workflow    (score every repository)
    Actions -> app-deliver     -> Run workflow    (dry_run: true first — it reports what is undelivered)
    Actions -> heartbeat       -> Run workflow    (proves the loop closes)

---

## Step 7 — The settings the API can set, and the one it cannot

Phase 3 applies these through the API and reads each one back. Listed so you can verify them by hand:

| Setting | Where | Value |
|---|---|---|
| Description, topics, homepage | repo -> About | so the dashboard and the hub have something to show |
| Delete head branches on merge | Settings -> General | on — a stale branch is a future merge conflict |
| Branch protection on `main` | Settings -> Branches -> Add rule | **block force pushes**, **block deletions** — 78 of 82 in the current estate |
| Required status checks | same page | optional for a single maintainer; it blocks your own work, so the estate's decision was to skip it |

**The one the API cannot set on the free plan:** branch protection on a **private** repository.
78 of 82 are protected; the remainder needs Pro/Team. Phase 3 reports which it was. A gap that is
named is a decision; a gap that is assumed is a defect.

---

## Step 8 — Verify, with commands

Not "does the page look right". Each line below answers one question and prints one answer.

    # 1. Can the token see everything?
    gh api "user/repos?affiliation=owner&per_page=100&page=1" --jq 'length'
    # must match the {seen, skipped} in the bootstrap summary

    # 2. Do the four sibling repositories exist and are they private?
    for r in registry knowledge dumps backup; do
      gh api repos/<owner>/$r --jq '"\(.full_name) private=\(.private)"'
    done

    # 3. Is the register consistent?
    python3 tools/register-check.py AUDIT/VERIFIED_FINDINGS.md ; echo "exit=$?"

    # 4. Does every licence claim match the policy?
    python3 tools/policy-guard.py --check ; echo "exit=$?"

    # 5. Do all workflows parse, and do they carry the nine properties?
    python3 tools/wf-check.py --dir .github/workflows

    # 6. Did the first snapshot land, and does it restore?
    gh api repos/<owner>/dumps/contents --jq 'length'

    # 7. Do the three published pages answer?
    for u in https://<owner>.github.io/dashboard/ https://<owner>.github.io/control-panel/ \
             https://<owner>.github.io/<owner>.github.io/; do
      curl -s -o /dev/null -w "%{http_code} %{size_download}  $u\n" "$u"
    done

**Read state through the API, never through raw.** `raw.githubusercontent.com` serves a cached copy
that lags minutes to hours behind a commit; in this estate it has twice made finished work look
broken. `GET /repos/{owner}/{repo}/contents/{path}` shows the truth immediately.

---

## Step 9 — The first week

Do not touch anything for seven days. The schedules are in the files and start firing as soon as the
seed is on `main`. What to expect, and what each one proves:

| When | What fires | What it proves |
|---|---|---|
| within an hour | `heartbeat` (06:00), `audit/health` (03:43) | the control plane is alive |
| every 6 hours | `dumps/backup-all` | the safety net works before it is needed |
| Mon 04:00 | `adopt`, `audit` | every repository is guarded and scored |
| Mon 05:00 | `app-deliver`, `backlog-status`, `dumps-dedupe` | every app is delivered, not just built |
| Mon 07:00 | **`new-app`** | the queue builds itself: one app appears, fully delivered |
| Wed 05:00–20:30 | `kit-tests`, `lint`, `code-compression`, `self-diagnose`, `self-heal` | the system checks and repairs itself |

**The single most important observation of week one is the Monday `new-app` run.** If it scaffolds an
app that has a repository, pipeline, release, landing page and live demo by Monday evening, the
release does what it claims. If it does not, the failure is in the caller it wrote or the secret it
used — and phase 6 already proved the caller's shape, so it is the secret.

---

## Troubleshooting — the eight failures this estate actually had

| Symptom | Cause | Fix |
|---|---|---|
| A workflow shows a run with **0 jobs, no log, a 22-byte archive** | a reusable workflow declared a secret `required: true` that the caller does not hold; or an unsuffixed `concurrency` group collided with its caller | make the secret `required: false` and check it in the first step; suffix the group with a literal |
| Every commit step fails with **permission denied** | Actions workflow permissions are read-only | step 2 |
| A commit step is **green but nothing landed** | the step reports `git`'s exit code, not the data | `tools/commit-and-verify.sh` |
| **Pages 404** | Pages source is not "GitHub Actions", or the first deploy is still propagating | wait a minute and re-check; then step 4 |
| `gh api repos/<owner>/forge` returns **404** | the token cannot see a private repository — this is a **wrong credential, never an absent repository** | re-check the token's repository access. This mistake was made three cycles in a row |
| The dashboard shows **no projects** | the refresh has not run | dispatch `dashboard/refresh.yml` once |
| A **schedule never fires** | an invalid cron, or GitHub's 60-day inactivity disable on a repository with no commits | `self-diagnose` checks "actually fires" — a scheduled workflow older than twice its period is not scheduled, it is broken |
| The **APK build fails** | `app_src` does not point at the folder holding `index.html` | fix the input in the caller, not the workflow |

---

## What the guide cannot give you

- **A second maintainer.** The estate is deliberately single-maintainer; `GOVERNANCE.md` records the
  decision and the one continuity action that follows from it.
- **Slack or email notification.** `health.yml` opens one issue. That is the whole notification
  system, and it is honest about being pull-only.
- **Protection on private repositories on the free plan.** Named, not hidden.
- **A restore of your data.** `backup.py --restore-test` verifies a dump; restoring an estate is a
  documented procedure, not a button, and it should stay that way.
