# Apply runbook — the manifest rollout, phase by phase

**Started 4 November 2026.** This is the executable version of the design record beside it. Every phase
has a gate, and no phase starts until the one before it passes.

**How every edit to an existing file is made.** Fetch the current file → apply the change
programmatically with an assertion that the anchor matched → verify (`py_compile` / `bash -n` /
`yaml.safe_load`) → write → read back and compare the sha256 with the tested local copy. **Never retyped.**
A 52 KB file replaced wholesale by hand is how a silent corruption gets in, and this estate has already
lost two apps to a shared block pasted as text.

---

## Phase 0 — Backup (done before any file changed)

| What | How | State |
|---|---|---|
| Whole estate | `dumps/backup-all.yml`, dispatched with `full: true` — every repository, changed or not | **run #62, dispatched 15:41:50Z** |
| The 23 files this rollout touches | `state/pre-manifest-baseline-2026-11-04.json` — repo HEAD + per-file blob sha | **published** |
| Restore one file | `git -C <repo> cat-file blob <blob_sha> > <path>` — exact bytes, from any clone | documented in the baseline |

`backup-all.yml` was re-enabled for this and **should stay enabled for the duration of the rebuild.** It is
the safety net; it was only disabled as part of the 4 November pause.

---

## Phase 1 — The tool and the config (`forge`) — **DONE**

| File | State |
|---|---|
| `tools/manifest.py` | new — verified on all four states, plus `version`, `record`, `claim`, `status` |
| `manifest-paths.json` | new — 19 tracked (16 gated + 3 hand), 16 deferred with their writers, 3 `bot_writable` |
| `tools/manifest-audit.py` | new — declarative; no basename inference |
| `canonical-pins.json` | new — 47 callers, 4 pins, 3 unpinned, target `3c8459e` |

**Gate — passed.** All four read back byte-identical to the tested copies. `python3 tools/manifest.py
version` → `manifest.py schema 1`. `python3 tools/manifest-audit.py` → 16 failures, **every one "does not
call `_manifest_record`", none "not found"** — which is the correct known-good state before the writers are
gated.

---

## Phase 2 — `sweep.py` (`forge`)

The three fixers, in one commit, because they share `SCHEMA` and `now_iso`:

* `SCHEMA = 1` and `now_iso()` at the top, beside `BOT_NAME`. No import from `manifest.py` — the fixer runs
  where the tool may not exist yet.
* `fixer_drift` — **syncs → one write → claims last**, then re-reads and reports only what the on-disk
  check confirms. `committed-drift` → `claim --as hand` unless the path is on `bot_writable`.
* `fixer_bootstrap` — reads `repos.apps` from `manifest-paths.json` (the v7 dict shape), vendors
  `tools/manifest.py`, records each present path with its declared class.
* `fixer_manifest_bump` — declines with a stderr note on a schema mismatch; never raises.
* `choices` grows to `["nojekyll","changelog","kit_bump","drift","bootstrap","manifest_bump"]`.

**Why before the bootstrap:** the rollout's Step 2 runs `sweep --fixer bootstrap`, which does not exist until
this lands. The design's own step order had this backwards.

**Gate:** `python3 tools/sweep.py --fixer drift --dry-run` exits 0; `--fixer bootstrap --dry-run` lists
repos without changing anything; the fixer registry in `choices` matches the dispatch chain.

---

## Phase 3 — Bootstrap

```bash
bash scripts/bootstrap-manifest.sh                      # the four meta repos, direct
python3 tools/sweep.py --fixer bootstrap --cap 20 --dry-run
python3 tools/sweep.py --fixer bootstrap --cap 20       # ~70 app PRs, four runs
```

**Gate — a count, not a sample:** every public app repo has a `MANIFEST.json` or an open bootstrap PR.
Merge in batches after spot-checking three by hand.

---

## Phase 4 — The gates and the test

| File | Change |
|---|---|
| `app-builder/drsoam.py` | `write(path, obj, gated=False)` + `_manifest_check`/`_manifest_record`/`_producer`; `publish_dashboard` checks the **whole artifact once** and routes a refusal into `degraded` |
| `registry/refresh.py` | same shape in `write_json()` |
| `control-panel/tools/scan.py` | gate + atomic write + `return 3` on refusal |
| `control-panel/tools/plan.py` | gate + atomic write + `return 3` on refusal |
| `forge/tools/commit-and-verify.sh` | `git status --porcelain -- MANIFEST.json` (not `git diff` — blind to untracked) |
| `control-panel/tools/fetch.py` | emit `"locked": true` per repo from `LOCK_MARKERS` |
| `control-panel/tools/gaps.py` | skip locked repos in `no-workflows` |
| `forge/tools/adopt.py` | `LOCK_MARKERS` check before `missing_for()` |

**Gate — the five cases.** A, B, C, D, E. **C and E are the ship condition:** C proves the fixer protects
instead of adopting; E proves untracked refuses.

> **The rule, because this class recurred four times:** every gate case asserts from the clone the fixer
> wrote to, after the change is merged and pulled. A test that asserts against a local checkout while the
> fixer has only opened a PR cannot see the state it is testing.

---

## Phase 5 — `app-deliver.py` Option A, then the lint step

API-level manifest gate before each `PUT`; untracked refuses. **Then**, and only then, the lint step in
`forge/lint.yml` with the three extra checkouts — it is a completion check, not a starting gate.

**Gate:** `manifest-audit.py` → `OK: 16 tracked path(s)`, exit 0.

---

## Phase 6 — The four broken schedules, then restore

Fix first, restore second. Starting with `heartbeat` and `backlog-status` for 24 hours.

| Workflow | Fix |
|---|---|
| `forge/new-app.yml` | `FANOUT_TOKEN` cannot `createRepository` — widen it, or move the scaffold to a token that can |
| `forge/health.yml` | the notifier fails on a blank body — an empty report is a skip, not a failure |
| `forge/kit-audit.yml` | `kit-drift` reads with the installation token — point it at a token that can read other repos |
| `audit/licence-check.yml` | `HCS` and `compfactory` have no `LICENSE` file |

Then `bash tools/restore-schedules.sh`, verifying with `--verify`.

---

## Rollback

| Level | Action |
|---|---|
| One file | `git -C <repo> cat-file blob <blob_sha> > <path>` from the baseline, or `git revert <sha>` |
| One phase | `git revert` the phase's commits — each phase is one commit per repository |
| The whole rollout | restore the five repo HEADs from `pre-manifest-baseline-2026-11-04.json` |
| The estate | `dumps` run #62, plus the six-hourly snapshots while `backup-all` stays enabled |

---

## Where it stands

| Phase | Status |
|---|---|
| 0 Backup | **done** — estate run dispatched, baseline published |
| 1 Tool + config | **done and verified** |
| 2 `sweep.py` | next |
| 3 Bootstrap | |
| 4 Gates + the five cases | |
| 5 `app-deliver` + lint | |
| 6 Schedules | |
