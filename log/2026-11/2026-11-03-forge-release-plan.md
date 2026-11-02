# 2026-11-03 — The whole system read end to end, and a plan to ship it as one release

## What I looked at

The control plane and everything it governs, read from the repositories rather than from their
descriptions.

    forge        373 files, 27 workflows, 34 tools, 188 queue specs, 37 audit files
    registry      17 files   repos.json, catalog.json, plan.json, deps.json, build-status.json
    knowledge     23 files   the system plan (54 KB), master list, build order, issues
    dumps x6      cap 2 GB    two parts full, two emptied by the 2026-11-02 consolidation
    app-builder   54 files    build.yml (10 jobs), pages.yml, drsoam.py (52 KB), 4 tools
    control-panel 21 files    inventory.json — 97 repos, 164 workflows, 207 jobs, 768 steps, 53 edges

The estate at this date: **100 public repositories and 9 private** — `forge`, `registry`,
`knowledge`, `dumps`, `dumps-2` … `dumps-6`. The private half is invisible to a `gh` token without
the right scope, which is itself the trap the estate has recorded three times: a 404 is a wrong
credential, never an absent repository.

Also read: `HANDOFF.md`, `STATUS.md`, `WORKLIST.md`, `GOVERNANCE.md`, `GETTING-STARTED.md`,
`AUDIT/README.md`, `PHASE-2/ARCHITECTURE_AUDIT.md`, `PHASE-2/SOURCE_OF_TRUTH_MATRIX.md`,
`PHASE-9/REMAINING_WORK.md`, `PHASE-9/CLOSEOUT.md`, `knowledge/docs/drsamonline_system_plan.md`, and
all 27 workflow files in `forge` parsed for triggers, crons, jobs, reusable calls and secrets.

## What was wrong

**1. The system has never been shown to work from nothing.** Every mechanism that runs today depends
on a file in a private repository, a secret on one account, a setting clicked once in a web UI, or a
fact the last session remembered. `GETTING-STARTED.md` promises `./install.sh` then `forge init
my-org` then `forge new app` — and there is no `init`, and no path from a fresh account to a running
system. The install guide describes a product that does not exist yet.

**2. The audit closed on the estate as it is, not on the estate as it would be if rebuilt.** Its
closeout lists what a fresh install would inherit: four discovery paths that each answer "what
repositories exist" differently, a reconcile whose output was computed and never committed, a
`concurrency` group that made one workflow fail 40 times before any job was created, five guards that
did not run themselves, and `builds.json`, which has no producer at all. Each is fixed in the live
estate and none is fixed *structurally* — the next install would reproduce all of them.

**3. The 2026-11 fleet audit measured the consequence.** 18 shared kits, 7 adopted and 11 with zero
consumers; a registry claiming consumers for eight kits that do not import them. A system that cannot
measure itself cannot be re-installed, because there is nothing to check the new install against.

**4. The map and the estate disagree by seven workflows, and the map is right to say so.** The
control panel reports seven `forge` workflows as orphans — `audit`, `docs`, `fanout`, `pages`,
`release`, `self-heal`, `test` — because nothing in the estate calls them. That is not a defect in
the panel. It is the panel doing its job: it says what is connected to nothing, and a reader decides.
Nobody had decided, so it read as a defect for a month.

## What I changed

Nothing outside this repository. This is a plan, and the estate's rule is that a log entry records
verification rather than intention — so the entry says what was written, not what will be.

    reports/2026-11-forge-release/README.md            the plan at a glance, the eight phases, the four decisions
    reports/2026-11-forge-release/01-system-map.md     every repository and its role; what controls what; the token model
    reports/2026-11-forge-release/02-workflows.md      all 164 workflows, the 27 in forge in detail, the timetable, the nine rules
    reports/2026-11-forge-release/03-one-release.md    the seed: contents, manifest, eight phases, the fourteen invariants
    reports/2026-11-forge-release/04-setup-guide.md    every setting, token, secret and click, in order, with the commands to verify
    reports/2026-11-forge-release/05-release-plan.md   six stages, eleven acceptance tests, eight risks, four rollback levels

The design in one line: **`tools/make-seed.py` builds `forge-seed-1.0.0.tar.gz` from the tagged tree,
and `bootstrap/bootstrap.yml` stands the system up in eight idempotent phases** — preflight,
repositories, discovery, settings, pipeline, schedules, guards, report — with `dry_run: true` as the
default and phase 6 running every guard against an *empty* estate before trusting it on a full one.

## Evidence

The measurements the plan rests on, all reproducible from this repository or from the API:

    repositories          100 public + 9 private, read from the API on 2026-11-03
    workflows             164 parsed by control-panel/docs/inventory.json (last scan 2026-11-01)
    callers of the build  46 into app-builder/build.yml, 5 into app-builder/pages.yml
    reusable workflows    11, of which 7 in forge have no caller
    scheduled             30 in the inventory, plus audit/health.yml added since — 31 today
    forge                 27 workflow files, 26 at the last scan
    audit register        103 findings, 0 open, 29 schedules enabled (STATUS, 2026-10-28)

Two cross-checks that came back clean and are worth recording, because they are the failure modes one
would expect:

- **No dangling calls.** All 53 edges resolve to a workflow that exists. The inventory records zero
  `dangling_calls` and zero parse errors across 164 files.
- **Every caller's contract matches.** The audit verified all 46 callers declare no undeclared input,
  no undeclared secret and no unsupported key on the `uses:` job — the one part of the estate that has
  held without exception.

## What I deliberately did not do

- **Did not build the release.** No tag, no tarball, no `make-seed.py`, no bootstrap workflow. The
  plan specifies them; writing them into `forge` without being asked would be a change to the brain
  disguised as documentation.
- **Did not migrate anything.** `mode: verify` is designed to report; the plan says explicitly that a
  migration is a different job with a different risk profile.
- **Did not take the four decisions.** Public or private seed, pruning `dumps`, protecting private
  repositories on the free plan, and adding a second admin are the owner's, and three of them cost
  money or trust.
- **Did not re-open the audit.** It is closed at 0 open and this report adds no finding. Everything
  here is work the audit surfaced, not a claim that something in the estate is currently false.
- **Did not count what I did not read.** The 188 queue specs were counted, not read; the 27 workflow
  files were read. The distinction is in the numbers above.

## Next

Eight batches, in this order, and the fourth one is the one that matters:

1. **R0** — write the fourteen invariants as a file, and make `make-seed.py --check` fail on each one
   when it is removed. Fourteen deliberate breakages, fourteen red runs.
2. **R1** — the bootstrap: one workflow, six helpers, `--dry-run` on everything.
3. **R2** — a fresh free-plan account, run by someone who has not read the design. Every ambiguity
   they hit becomes a fix in the guide. This is the only stage that can prove the release works, and
   it is the one that takes a week of waiting for a Monday.
4. **R3** — cut `v1.0.0`, generate the tarball from the tag, attach `SHA256SUMS`, rewrite
   `GETTING-STARTED.md` around the release instead of the promise of one.
5. **R4** — `mode: verify` against the real estate, and publish the first honest self-portrait against
   a fixed standard: 11 unused kits, 7 orphan workflows, 5 unprotected private repositories.
6. **R5** — handover: the panel gains a fifth route, the dashboard a `seed` row.

**The one thing to watch in week one is the first Monday `new-app` run.** If it scaffolds an app that
has a repository, pipeline, release, landing page and live demo by Monday evening, the release does
what it claims. Everything else in this plan is scaffolding around that one observation.
