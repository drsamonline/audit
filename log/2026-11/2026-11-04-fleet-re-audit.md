# 2026-11-04 — The fleet re-audited: it is degraded, and the notifier is why nobody knew

## What I looked at

Everything, again, from the API rather than from the last snapshot. 110 repositories, every tree,
every workflow file fetched and parsed, and the four failing runs read down to the step that broke.

    repositories            110        101 public, 9 private (forge, registry, knowledge, dumps x6)
    new since 3 November      1        feather, created 2026-11-03
    workflow files          186        in 97 repositories; 13 carry none
    jobs / steps        249 / 990
    cross-repo edges         52        every one resolves; zero dangling
    scheduled workflows      32
    invalid YAML              0        of 186
    repos publishing a release  59
    activity          74 repos pushed on 2026-11-03, 21 on 2026-11-04

The last committed snapshot said 100 repositories, 164 workflows, 207 jobs, 768 steps, 30 scheduled.
The panel's own scan has since caught up to 110/182; my count is 186 because four workflows have
appeared since that scan, listed below.

## What was wrong

**The fleet is degraded and it says so itself — in a file nobody opens.** `audit/docs/health.json`,
written daily at 03:43, reads `verdict: degraded` and names four failing schedules. Nothing was
raised, because the job whose entire purpose is to raise it fails too.

**1. `forge/new-app.yml` cannot create a repository.** The queue has been unable to build anything
since **2026-11-02 16:49**, and every run since has failed at the same line:

    NAME: accent-oracle
    GraphQL: Resource not accessible by personal access token (createRepository)
    ##[error]Process completed with exit code 1.

`FANOUT_TOKEN` can write contents and open pull requests, but it cannot create a repository. The
queue picked `accent-oracle`, could not create it, and will pick it again next week. **This is the
loop-closing step** — the one the whole system exists to perform — and it has been dead for two days.

**2. `forge/health.yml`'s notifier fails on an empty report.**

    GraphQL: Body cannot be blank (addComment)

The one central notifier, built in batch 121 to cover all seven failure classes, builds a report to
`/tmp/report.md` and posts it with `--body-file`. When the report is empty the body is blank and the
GraphQL call fails — so "nothing to say" is reported as a failure, and the failure that mattered was
never posted. The `publish` job in the same run succeeded, which is why `health.json` is current and
the issue is not.

**3. `forge/kit-audit.yml` can never pass.** The drift step fails after three attempts:

    kit-drift could not read the API after 3 attempts - the drift report is missing,
    and a missing report is not a clean one

It reads with the installation token, which sees only `forge`; the other repositories answer 403.
The refusal to report clean is correct behaviour — it is invariant 14 working — but the job is
structurally unable to succeed, so a real drift would be indistinguishable from this one.

**4. `audit/licence-check.yml` fails on two repositories with no LICENSE.** `HCS` and `compfactory`.
Both were already named in the fleet audit's "add a LICENSE" list on 2026-11-03 and neither has one.
The check is right; the estate has not done the work.

**And the fifth thing, which is not a failure but a measurement error:** the same job printed
`licence badge check - 100 repos`. The account has 110. The audit repository's own collector has the
stale denominator this audit was created to catch, in the tool that is supposed to catch it.

**Six more that the panel's gap rules report, and that I re-measured:**

    no timeout        72 workflow files have none anywhere; 98 individual jobs have none
    no concurrency    42 files (the panel says 40 — it parsed 182 files, I parsed 186)
    no permissions     9 files with no permissions block at any level
    orphan             7 reusable workflows in forge with no caller
    drift              8 workflows that are hand-copied variants
    no workflows      13 repositories, including repertory-reader and corefit-md — two apps
                      delivered without a pipeline
    un-runnable        3

**Two structural regressions since the audit closed:**

- **The build pin is stale everywhere.** 47 callers of `app-builder/build.yml`: 34 on `@246da5d5`,
  8 on `@0464e330`, 1 on `@aa727dee`, 1 on `@fbb5468c`, and **3 still on `@main`**. `app-builder`'s
  main is `3c8459e`. The newest pin is **7 commits behind**, and `build.yml` itself changed (+16
  lines) inside those 7 — so **no caller in the estate is running the current build**. Pinning to a
  SHA was the right fix; without a bumper it became stale-by-default, which is the same outcome as
  `@main` with none of the warnings.
- **Ten workflows now commit or push with no verdict** — the estate closed that as A11 with "zero
  bare commit steps remain". Eight are genuine regressions; `HMS/release.yml` is the known false
  positive (it deletes a tag) and `conqueror-os/repair-src.yml` is the known one-shot.

**Five new credentials since the audit closed**, none of them in the audit's register:

    AUDIT_TOKEN    6 workflows   Contents RW on all repos — used by one-shot repair sweeps
                                 (apply-all, licence-fix, apply-store-fixes, apply-licence-badges,
                                 add-download-blocks) that live in the PROFILE repo, not in forge
    TRAFFIC_TOKEN  1 workflow    dashboard traffic panel
    BILLING_TOKEN  1 workflow    classic PAT with `user` scope, for the Actions-minutes panel
    OVSX_PAT       1 workflow    ai-bridge publishes to Open VSX
    PAT_TOKEN      1 workflow    compfactory dispatches into ziptastic

`AUDIT_TOKEN` is the one that matters. It is a fourth cross-repo writer — after `sweep.yml`,
`fanout.yml` and `new-app` — and it lives outside the control plane, in the repository whose job is
to be a profile page. The invariant "exactly one cross-repo mechanism" is now false.

**What genuinely improved, and should be said:**

- Zero invalid YAML across 186 files; zero dangling calls across 52 edges.
- All 11 reusable workflows have a correctly suffixed `concurrency` group — the defect that failed
  `backup.yml` 40 times is gone, and stayed gone.
- Zero `workflow_call` secrets declared `required: true` — invariant 9 holds everywhere.
- Four new workflows landed, all of them real: `forge/state-set.yml` (sets one dotted key in
  `STATE.json` so a cycle whose credential cannot rewrite a 30 KB file can still record state),
  `musicgen/pages.yml`, `ziptastic/ci.yml`, `conqueror-os/sw-3.2.0.yml`.
- 59 repositories publish a release; the delivery sweep is holding.

## What I changed

Nothing outside this repository, and inside it only additions. This is a measurement, not a repair.

    log/2026-11/2026-11-04-fleet-re-audit.md              this entry
    reports/2026-11-forge-release/verify-2026-11-04.md   the fourteen release invariants against the live estate
    state/re-audit-2026-11-04.json                       the census and the workflow inventory, diffable

I did **not** overwrite `state/repos.json`. Its producer, `tools/collect.py`, is the tool that
reported 100 repositories against an account with 110, and replacing its output with a differently
shaped file would break `tools/diff.py` while hiding the reason. The fresh census is a separate file
with its own schema and its own stated denominator.

## Evidence

Every claim above is a log line, an API answer or a count that can be re-run:

    new-app failure        forge run 41485228285, step "Scaffold it, exactly as the manual path does"
                           "GraphQL: Resource not accessible by personal access token (createRepository)"
    notifier failure       forge run 41508261810, step "Open or update the estate-failure issue"
                           "GraphQL: Body cannot be blank (addComment)"
    kit-audit failure      forge run 41463858933, step "Drift - is a vendored copy actually out of date..."
                           "kit-drift could not read the API after 3 attempts"
    licence failure        audit run 41438236873, step "Check licence badges"
                           "licence badge check - 100 repos" ... HCS, compfactory: no LICENSE file
    pin drift              gh api repos/drsamonline/app-builder/compare/<pin>...main -> 1, 3, 7, 15 ahead
    build.yml change       compare 246da5d5...main: ".github/workflows/build.yml modified +16 -0"
    fleet health           audit/docs/health.json, checked_at 2026-11-04T01:39Z, verdict "degraded"
    panel gaps             control-panel/docs/gaps.json: 72 / 40 / 9 / 7 / 8 / 13 / 3

Three things I could not verify from outside and am not asserting: whether the registry now stages
`plan.json` (invariant 3), whether `score` has been renamed to match its formula (invariant 4), and
whether `demo-drift --check` runs anywhere but its self-test. They are marked UNVERIFIED in the
verify report rather than passed.

## What I deliberately did not do

- **Did not fix any of the four.** Each needs a change to a workflow in `forge` or to a token's
  scope, and the token change is an account action. They are specified in the verify report, with
  the one-line fix for each.
- **Did not re-run the checks that are failing.** Re-running a job that fails for a scope reason
  produces a second identical red run and tells you nothing.
- **Did not re-do the 61-page fleet audit.** That report's findings were about capability, overlap
  and licence feasibility across 1.4M lines; none of today's measurements contradicts it. What
  changed is the machinery, and that is what this entry covers.
- **Did not touch `state/repos.json`** — see above.
- **Did not call the fleet "healthy" because 28 of 32 schedules pass.** Four of the four that matter
  — the queue, the notifier, the drift audit and the licence check — are exactly the ones that keep
  the other 28 honest.

## Next

In this order, because each one unblocks the next:

1. **Give `FANOUT_TOKEN` the ability to create repositories** (or move `new-app` onto a token that
   has it). Nothing in the estate builds until this is done, and `accent-oracle` will be picked first.
2. **Make the notifier treat an empty report as a skip.** One guard: if the report is empty, exit 0
   with a notice. Until that is done, every "nothing is wrong" run is red and every real one is lost.
3. **Point `kit-drift` at `FANOUT_TOKEN`**, so the drift report can be produced instead of refused.
4. **Add a LICENSE to `HCS` and `compfactory`** — the two-line fix the fleet audit asked for a day ago.
5. **Bump the 47 build pins in one sweep, and add the bumper to `sweep.py` as a fixer** so the pin
   cannot go stale again. Three callers are still on `@main`; they go first.
6. **Retire or adopt `AUDIT_TOKEN`.** Either the one-shot sweeps move into `sweep.yml` where the one
   cross-repo mechanism lives, or the token is revoked once the sweeps are done. A credential with
   write on every repository, held by a profile page, is the largest unowned authority in the estate.
7. **Fix the collector's denominator** — `{seen, skipped}` in `tools/collect.py` and
   `tools/licence_check.py`, so the audit stops reporting 100 of 110.
