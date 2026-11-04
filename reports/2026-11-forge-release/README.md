# Forge 1.0 — one release, and the whole system stands up

**3 November 2026** · a release plan for `drsamonline/forge` · nothing in any other repository is
changed by this document

This is the plan to ship Forge as **one downloadable release that becomes the whole system**. Upload
it as a repository, press one button, and the control plane, the registry, the archive, the build
pipeline, the schedules, the guards and the public pages stand themselves up — on the account it is
pointed at, with no hand-copied file and no second maintainer.

Five documents. Read them in this order.

| # | File | What it answers |
|---|---|---|
| 1 | [`01-system-map.md`](01-system-map.md) | What every repository is for, what actually controls what, and where the truth lives |
| 2 | [`02-workflows.md`](02-workflows.md) | All 186 workflows: what runs, when, what calls what, and what each one needs |
| 3 | [`03-one-release.md`](03-one-release.md) | The design of the release: contents, manifest, the eight bootstrap phases, the fourteen fixes baked in |
| 4 | [`04-setup-guide.md`](04-setup-guide.md) | Every setting, token, secret and click, in the order they must happen |
| 5 | [`05-release-plan.md`](05-release-plan.md) | Phases, acceptance tests, risks, rollback, and what is deliberately out of scope |
| — | [`verify-2026-11-04.md`](verify-2026-11-04.md) | Stage R4, run early: the fourteen invariants measured against the live estate — 5 pass, 1 part, 4 fail, 4 unverified |

---

## The system in one paragraph

**Forge is the brain, the registry is the database, knowledge is the black box, app-builder is the
factory, the kits are the shared parts, the apps are the products, and the control panel and
dashboard are the two pages that make it checkable.** Forge holds the queue, the rules, the prompts,
the templates and the workflows that write to every other repository. It scaffolds an app from a
spec, wires the pipeline, builds a Windows EXE, a Linux binary and a signed Android APK, publishes a
rolling release, deploys the live demo, screenshots it, writes the landing page, and keeps the
registry, the dashboard and the archive current — then audits itself, heals what is transient, and
records what it could not fix.

**The whole thing is one direction of flow:**

    Forge writes the memory  ->  the tools derive the facts  ->  the panel and the dashboard publish them

Three layers, three jobs, and no arrow pointing back. That is the design; the audit's
`PHASE-2/ARCHITECTURE_AUDIT.md` (in `forge`) traced it end to end and found the direction right and
several of the claims false. This release is where the claims become true.

---

## What is being released, in one line

    forge-seed-1.0.0.tar.gz   the complete control plane, built from forge@v1.0.0 by tools/make-seed.py
    MANIFEST.json             every file, its sha256, and the one thing it is for
    SHA256SUMS                the same digests, in the format `sha256sum -c` reads
    install.sh                the local half: link the `forge` command, check the manifest
    .github/workflows/bootstrap.yml   the remote half: eight idempotent phases, one dispatch

The tarball is **generated from the tagged tree**, never maintained as a second copy. A seed that is
a copy of the brain drifts from the brain — the audit found four copies of the exclusion list and
counted it as a finding. There is one source and one build.

---

## Why now, and why this shape

The audit closed on 2026-10-28 with 103 findings, 0 open, and 29 schedules re-enabled. That is a
system that works *on this account, in this state, with these tokens in place*. It has never been
shown to work from nothing. Everything that makes it work today is either a file in a private
repository, a secret on one account, a setting clicked once in a web UI, or a fact the last session
remembered.

Three things in the estate say so directly:

1. **`GETTING-STARTED.md` promises an install that does not exist yet.** It says `./install.sh` then
   `forge init my-org` then `forge new app`. `install.sh` is 1,244 bytes that fetch and link; there is
   no `init`, and no path from a fresh account to a running system.
2. **The audit's own closeout lists what a fresh install would inherit**: five guards that did not
   run themselves (fixed in batch 129), a `concurrency` group that made one workflow fail 40 times
   before any job was created, a reconcile whose output was computed and never committed, and four
   independent code paths that each answer "what repositories exist?" differently.
3. **The 2026-11 fleet audit measured the result**: 18 shared kits, 7 adopted and 11 with zero
   consumers; a registry that claims consumers for eight kits that do not import them. A system that
   cannot measure itself cannot be re-installed, because there is nothing to check the new install
   against.

So the release is not a repackaging. It is the estate's own findings turned into **bootstrap
invariants** — fourteen of them, listed in `03-one-release.md` §4 — each one a defect that a fresh
install would otherwise reproduce.

---

## The eight phases, in one table

Every phase is idempotent, every phase reports `{done, skipped, failed}`, and no phase proceeds if
the previous one failed. `bootstrap.yml` takes `dry_run: true` by default.

| Phase | What it does | Needs | Proves |
|---|---|---|---|
| 0 | **Preflight** — who am I, what can this token see, what plan is this account on | `GITHUB_TOKEN` | the plan tier, and therefore which protections are possible |
| 1 | **Repos** — create or verify `registry`, `knowledge`, `dumps`, `backup` | `FANOUT_TOKEN` | each exists, is private, and is empty-or-mine |
| 2 | **Discovery** — the one measured census, with `{seen, skipped}` | `FANOUT_TOKEN` | `seen + skipped` equals the account's own repo count |
| 3 | **Settings** — Actions permissions, Pages source, topics, description, licence, branch protection where the plan allows | `FANOUT_TOKEN` | read back from the API, not assumed |
| 4 | **Pipeline** — write the canonical caller into every app repo that lacks it | `FANOUT_TOKEN` | the file lands in the *new* repo, by blob sha |
| 5 | **Schedules** — register the timetable | the files themselves | no two crons that share state collide |
| 6 | **Guards** — health, licence, kit-audit, demo-drift, spec-guard, register-check | nothing | every guard passes on the empty estate, so a later failure is real |
| 7 | **Publish** — dashboard, control panel, hub | Pages | three URLs return 200 with a body |
| 8 | **Report** — one issue: "Forge is live", with the verification table | `issues: write` | the next reader starts from evidence |

Phase 6 is the one that matters most, and it is the one no current install has: **the guards must
pass on an empty estate before they are trusted on a full one.** A guard that has never seen a clean
run cannot distinguish "nothing is wrong" from "I am not looking".

---

## The four decisions this plan asks for

Recorded here because the agent should not take them.

1. **Public or private seed.** Private keeps the product yours and costs 2,000 Actions minutes a
   month on the seed's own CI. Public makes the release a shop window and makes every build free.
   The estate's existing choice — apps public, control plane private — is what the numbers assume.
2. **`dumps` retention.** Six dumps repositories exist, but since 2026-11-02 the cap is 2 GB rather
   than 800 MB and the parts were consolidated — `dumps` and `dumps-2` are full, `dumps-4` and
   `dumps-5` are empty. Keeping all six costs nothing; retiring the empty ones needs a restore test
   first. The plan does not prune.
3. **Branch protection on private repos.** Free plan cannot protect a private repository's default
   branch. 78 of 82 are protected; the remainder needs Pro/Team or an accepted gap. The bootstrap
   reports which it was, rather than pretending.
4. **Continuity.** Admin on the four repositories that cannot be rebuilt — `forge`, `registry`,
   `dumps`, `app-builder` — for a second trusted person. Only the owner can do this; the bootstrap
   checks whether it was done and prints it as a warning, never as a pass.

---

## What this document is not

It is a **plan**. It changes nothing in any repository except this one. No release has been cut, no
tarball built, no bootstrap run. Where a number appears it is dated, because in this estate a count
is a measurement of the day it was taken — five findings' stated sizes did not survive being read.

The companion entry in `log/2026-11/2026-11-03-forge-release-plan.md` records what was read to write
this, what was wrong with the previous answer to the same question, and what was deliberately left
undone.
