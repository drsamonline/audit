# The manifest and drift design — the record

**4 November 2026** · `drsamonline` · seven rounds of design and review · status: **ready to ship —
the last defect is closed and verified**

This is the durable record of a design that took seven rounds. It exists so that the next session — human
or agent — does not have to re-derive why the manifest looks the way it does, which of the fourteen
decisions were forced by a defect, and what is deliberately not covered.

The short version: **a per-file provenance manifest that makes "never overwrite a user's edit" true at the
file level, in git, with a diff a reviewer can see** — and six rounds of review that moved the remaining
defect from the centre of the design to a path prefix in a config file.

---

## 1. The problem

Forge's generators rewrite their own artifacts wholesale on a schedule. Four of them, in four
repositories:

| Generator | Writes | How |
|---|---|---|
| `app-builder/drsoam.py` `write()` | `data.json` + 6 siblings in `dashboard` | atomic temp + `os.replace` |
| `registry/refresh.py` `write_json()` | `repos.json`, `catalog.json`, `plan.json` | atomic temp + `os.replace` |
| `control-panel/tools/scan.py` | `docs/inventory.json` | inline `json.dump` — **not atomic** |
| `control-panel/tools/plan.py` | `docs/plan.json` | inline `json.dump` — **not atomic** |

A fifth, `forge/tools/app-deliver.py`, writes into **other** repositories over the GitHub contents API
(`PUT` at lines 758 and 860), never cloning them.

**None of the five compares the file on disk against anything before replacing it.** So a human edit to
`data.json`, `docs/play/index.html` or the README badge block is lost on the next run — silently, with a
green build. The estate's own audit had already recorded the shape of this problem: no artifact anywhere
records *which program wrote it*, and the key `generated` means a date in three files and a list in a
fourth.

---

## 2. The design, as settled

### 2.1 The manifest

`MANIFEST.json` at the repository root, schema 1:

```json
{"schema": 1, "locked": false, "files": {
  "<path>": {"sha": "<git-blob-sha>", "producer": "tool@<sha>",
             "class": "generated|canonical|hand|agent|locked",
             "at": "<ISO8601>"}}}
```

A repo-level `"locked": true` short-circuits every path to `locked`, for repositories that declare
`LOCKED.md`.

### 2.2 The classes

| Class | Meaning | What a generator may do |
|---|---|---|
| `generated` | the tool owns it | rewrite when clean; refuse when drifted |
| `canonical` | a pinned template (`.github/workflows/build-apps.yml`) | same as generated, but `record` will not silently downgrade it |
| `hand` | a human wrote it | never rewrite |
| `agent` | an LLM wrote it for a user | identical to `hand` |
| `locked` | never automated | never rewrite |

### 2.3 The verdict: a three-way blob comparison

`manifest.py check` compares three hashes and needs no history and no author:

```
manifest sha   — what the generator recorded when it wrote the file
HEAD sha       — git rev-parse HEAD:<path>
worktree sha   — git hash-object --path=<path> -- <file>
```

| manifest | HEAD | worktree | status | exit |
|---|---|---|---|---|
| — | — | — | `new` | 0 — safe to create |
| ≠ | = | = | `committed-drift` | 3 — someone committed over us |
| = | ≠ | ≠ | `uncommitted` | 3 — editing before commit |
| = | = | = | `clean` | 0 — safe to rewrite |
| — (no entry) | present | present | `unrecorded` | 3 — bootstrap missed it |
| any | — | absent | `deleted` | 3 — a user deleted it |
| class hand/agent | — | — | `protected` | 4 |
| locked | — | — | `locked` | 4 |

Exit 0 = proceed, 3 = drift (refuse), 4 = protected (refuse), anything else = refuse. **A missing tool is
a hard `SystemExit`, never a silent skip.**

The first design used `git log -1 --format=%an%ae -- path` to ask *who* wrote it. That is unsound here and
the reason is worth keeping: **at `fetch-depth: 1`, `git log -- path` returns the tip commit's author for
every path.** Proven on a three-commit repository — in a shallow clone, `a.txt` (last touched by `human`)
reports `dependabot[bot]`. Every generator checkout in the estate is depth 1, so the author heuristic
would have classified every drift as bot-authored (overwrite) or every drift as human (permanent dead
file), decided by who committed last to the *repository*. The blob comparison replaced it and cannot be
wrong.

### 2.4 The gates

* **Single-file generators** — `write(path, obj)` calls `_manifest_check([path])` first, then writes
  atomically, then records **outside** the try (a record failure must not undo a successful write).
* **Multi-file artifacts** — `publish_dashboard` checks the **whole artifact once** and writes
  all-or-nothing. This matters because `data.json` is written last *on purpose* (it is the index that
  names its six siblings); a per-file gate that skipped `forks.json` but wrote `data.json` would leave the
  page pointing at stale data in a green run. Verified by reproducing that exact state, then fixing it.
* **A refusal is not success** — `plan.py` and `scan.py` return 3, not 0. `drsoam` routes the refusal into
  its existing `degraded` list, which `main()` already turns into `sys.exit(3)`.
* **`app-deliver.py` Option A** — an API-level gate before each `PUT`: fetch `MANIFEST.json` from the
  target repo, refuse if locked, refuse if `class` is hand/agent/locked, refuse if the current content sha
  differs from the manifest's, **refuse if untracked**. Option B (convert to a clone-and-PR flow, like
  `sweep`) remains the target, not the blocker.

### 2.5 The fixer

`sweep --fixer drift` resolves drift **by protecting it, not by adopting it**:

```
committed-drift  → claim --as hand        (a commit is a human decision until proven otherwise)
bot_writable     → sync the manifest to HEAD   (a three-path allowlist, not a heuristic)
uncommitted      → claim --as hand        (unreachable in a --depth 1 clone, kept for depth N)
```

`bot_writable` is `.github/workflows/build-apps.yml`, `package.json`, `package-lock.json` — the paths where
adopting a bot's commit is the correct policy. It is **path-based, not author-based**: any commit on those
paths is adopted, whoever made it, because a shallow clone cannot tell them apart. That is the one place
the design gives up the distinction, which is why the list is three entries. `pin_check` still reports the
pin against `canonical-pins.json` after adoption, so an adopted bump does not become the new target.

**The ordering is the whole design:** syncs → one write → claims last. A claim is a subprocess that
re-reads the file, so a sync write afterwards would overwrite it. Reproduced both ways.

The fixer re-reads after acting and reports only what the on-disk check confirms, so a failed claim cannot
be counted as a protection.

### 2.6 The scope, stated honestly

Release 1 tracks **16 paths, every one of which names its writer, and every one of whose writers calls
`_manifest_record`**:

| Repository | Paths | Writer |
|---|---|---|
| `dashboard` | `data.json`, `history.json`, `changes.json`, `feed.xml`, `forks.json`, `community.json`, `traffic.json` | `app-builder/drsoam.py` |
| `registry` | `repos.json`, `catalog.json`, `plan.json` | `registry/refresh.py` |
| `control-panel` | `docs/inventory.json`, `docs/plan.json` | `control-panel/tools/scan.py`, `plan.py` |
| every app | `README.md`, `docs/index.html`, `docs/play/index.html`, `.github/workflows/build-apps.yml` | `tools/app-deliver.py` |
| `forge` | `registry/deps.json`, `registry/licence-policy.json`, `SPEC-SHAPE.json` | `hand` — a decision, not a generator |

**Sixteen paths are deferred, with the writer that must be gated before each is added** — a work list,
not an excuse:

| Repository | Deferred path | Writer to gate |
|---|---|---|
| `forge` | `registry/diagnose.json` | `self-diagnose.py` |
| `forge` | `registry/drift.json` | `kit-drift.py` |
| `forge` | `registry/audit.json` | `kit-audit.py`, `repo-learning.py`, `code-compression.py` (three) |
| `forge` | `registry/parity.json` | `kit-audit.py` |
| `forge` | `registry/updates.json` | `self-update.py`, `kit-audit.py` (two) |
| `forge` | `registry/lessons.json` | `repo-learning.py` |
| `forge` | `registry/size.json` | `code-compression.py` |
| `forge` | `registry/spec-mismatch.json` | `spec-audit.py` |
| `forge` | `registry/backlog-done.json` | `backlog-status.py` |
| `forge` | `registry/delivery.json` | `app-deliver.py`, local mode |
| `forge` | `registry/learnings.json` | **no writer found — open** |
| `forge` | `registry/startup-failures.json` | **no writer found — open** |
| `registry` | `build-status.json` | `registry/tools/build-status.py:121` |
| `control-panel` | `docs/gaps.json` | `control-panel/tools/gaps.py:166` |
| apps | `VERSION` | `app-builder/build.yml` version job (a workflow, not a tool) |
| apps | `CHANGELOG.md` | same |

This scoping is the most important correction in the whole sequence. An earlier version recorded all 26
paths while gating four writers. The consequence would have been a loop: bootstrap records twelve
`forge/registry/*.json` as `generated` → their ungated tools rewrite them → `check` reports
`committed-drift` → the fixer claims them all as `hand` → the tools keep writing → twelve generated files
are permanently `hand`, and the weekly drift check reports them **protected**, a clean bill of health on
files whose provenance record is a lie. **A manifest that claims more than the gates cover is worse than a
smaller honest one.**

---

## 3. The seven rounds

Every finding below was checked against the code, and the ones marked *reproduced* were executed.

| Round | Findings | What was wrong | What closed it |
|---|---|---|---|
| **1** (v2) | **5 blocking**, 8 serious, 6 minor | `last_author` unsound at depth 1 · `app-deliver.py` outside the design entirely · the gate resolved the tool to a path that does not exist and failed **silently** · the `scan.py` patch referenced a variable not in scope · the bootstrap skipped every app repo | three-way blob comparison · Option A · `_find_manifest_tool` with `SystemExit` · lock discovery moved to `fetch.py` · meta-only bootstrap + `sweep --fixer bootstrap` |
| **2** (v3) | **4 blocking**, 9 serious, 5 minor | the fixer **adopted** a human's commit, destroying the protection it exists to create (*reproduced*) · per-file gating broke `publish_dashboard`'s deliberate write ordering (*reproduced*) · `plan.py` returned `0` on refusal · `scan.py`'s write still ungated | `committed-drift` → claim · batch gate + `degraded` · `return 3` · the scan.py patch |
| **3** (v4) | **1 blocking**, 6 serious, 3 minor | the fixer's read-modify-write **lost the claim it had just made** when a `bot_writable` sync ran in the same pass (*reproduced*) · `fixer_manifest_bump` raised `SystemExit`, aborting the whole sweep · `SCHEMA`/`now_iso` undefined · Step 4 Cases C/D/E could not see what they tested | syncs → one write → claims last · decline instead of raise · the two constants · the test corrections |
| **4** (v5) | **2 blocking**, 2 minor | `git rm --cached` does not delete the working-tree file, so Case E asserted a status its own setup prevented · the gate covered about **half** the paths the manifest recorded, which would have started the claim-as-hand loop | `git rm` · scope to gated writers + defer the rest |
| **5** (v6) | **1 blocking**, 1 serious, 2 notes | the new `manifest-audit.py` failed **16 of 16** on its own config — it scanned one repo's `tools/` while 12 of 16 writers live in four, matched only *quoted bare* filenames (so `".github/workflows/build-apps.yml"` was invisible), and reduced paths to basenames so `docs/index.html` and `docs/play/index.html` were indistinguishable · Case D asserted against a stale local clone | declarative `writer` per path · four-repo checkout · merge + pull before asserting · don't vendor the auditor · `hand` restored |
| **6** (v7) | **1 defect** | the four app paths declare `forge/tools/app-deliver.py`, but `lint.yml` checks forge out at the workspace **root**, so that resolves to a directory that does not exist (*reproduced*) | change the prefix to `tools/app-deliver.py` |

**Verified at the end:** with the prefix fixed and the writers patched, the auditor reports
`OK: 16 tracked path(s), every one declared and recorded by its writer` and exits 0.

### The last item, closed

`manifest-paths.json` → `repos.apps.*.writer` was `"forge/tools/app-deliver.py"`. In the `lint.yml` layout
forge's files are at the workspace root (`actions/checkout` with no `path:`), so that named a directory
that does not exist — and the error it produced blamed the other checkouts rather than the prefix.

**Fixed:** four entries, one string each, now `"tools/app-deliver.py"`. Verified in the layout the
workflow creates:

```
$ python3 tools/manifest-audit.py          # writers not yet patched
16 failure(s) across 16 tracked non-hand path(s)   # every one "exists but does not call _manifest_record"

$ python3 tools/manifest-audit.py          # writers carrying the marker
OK: 16 tracked path(s), every one declared and recorded by its writer
exit=0
```

So the config is correct and the gate is real: what remains red is the rollout — the five writers gaining
`_manifest_record` — not the configuration. That is the order v7 §3 already specifies: the audit step lands
at the end of Step 3 (four generators) and Step 6 (`app-deliver.py`).

---

## 4. The verification record

What was executed rather than argued, so the next session can trust the claims:

| What | Result |
|---|---|
| `manifest.py check` on the four states | `clean` → 0 · `uncommitted` → 3 · `committed-drift` → 3 · `protected` → 4 — all as specified |
| The v3 fixer on a committed user edit | synced → `clean` → the generator wrote → **`USER_NOTE` gone** |
| The v4 fixer on the same repo | claimed → `protected` → refused → **the edit survived** |
| The v4 fixer with one sync + one claim in a pass | claim **lost** (manifest still `generated`) |
| The reordered fixer, same fixture | `data.json` → `protected`, `build-apps.yml` → `clean` — both correct |
| Per-file gate with a protected sibling | index written, sibling stale, **run green** |
| Batch gate | whole artifact refused, `degraded` set, exit 3 |
| `git rm --cached MANIFEST.json` | file still on disk → `protected`, not `unrecorded` |
| `manifest-audit.py` (v6, heuristic) on its own config | **16 of 16 fail**, three independent causes |
| `manifest-audit.py` (v7, declarative) | 16/16 resolve; green once the writers carry the marker |

---

## 5. The rollout

Eight steps, each with a gate, and the gates are the point:

| Step | What lands | Gate |
|---|---|---|
| 0 | Confirm the paused set (`state/schedules-paused-2026-11-04.json`) | the nine named workflows are disabled |
| 1 | `tools/manifest.py` + `manifest-paths.json` in the four meta repos | identical sha256 everywhere; `_find_manifest_tool()` resolves from `.drsoam/` |
| 2 | Bootstrap: meta repos direct, apps via `sweep --fixer bootstrap` | **a count**, not a sample: every public app repo has a `MANIFEST.json` or an open bootstrap PR |
| 3 | Gate the four generators; `commit-and-verify.sh`; `fetch.py` emits `locked`; `gaps.py` reads it | in a scratch clone: first run writes and records, second run is a no-op diff |
| 4 | **The three-way test — A, B, C, D, E** | C (the fixer must **protect**, not adopt) and E (untracked must refuse) are the ship conditions |
| 5 | `adopt.py`'s `LOCK_MARKERS`, then restore schedules | `adopt.py --dry-run` shows zero changes to `repertory-reader`; then heartbeat + backlog-status for 24 h, then the rest |
| 6 | `sweep --fixer drift` weekly, `app-deliver.py` Option A, `new-app.yml` scaffold record | no PRs on a stable fleet; a test scaffold has 5+ manifest entries |
| 7 | `canonical-pins.json` + `pin_check` | reports **47 callers, 4 distinct pins, 3 unpinned, target `3c8459e`** |

**The rule to write at the top of Step 4, because one class recurred four times:** *every gate case
asserts from the clone the fixer wrote to, after the change is merged and pulled. A test that asserts
against a local checkout while the fixer has only opened a PR cannot see the state it is testing.*

---

## 6. What release 1 promises

* A human-drifted or uncommitted file is **refused by its generator** and never overwritten.
* A committed-drift file is **claimed as hand** by the fixer unless it is on the three-path `bot_writable`
  allowlist.
* A protected sibling in a multi-file artifact **blocks the whole artifact**, all-or-nothing.
* An **untracked file is refused**, not adopted.
* A **missing `manifest.py` is a hard failure**, not a silent skip.
* A **fixer's summary reports only what the on-disk check confirms.**
* Adding a path to `manifest-paths.json` without gating its writer **fails lint immediately.**

### What it does not promise

* **`app-deliver.py` Option B** — the clone-and-PR refactor. Option A protects user edits today; the
  estate's rule ("a cross-repo change that cannot be a PR must not be a push") is still violated in
  principle until B lands. A second PR, not a blocker.
* **`learnings.json` and `startup-failures.json`** — no writer found by filename. Under `deferred`. If
  nothing regenerates them they sit clean and harmless; if a generator later writes one under another name,
  the first run trips `unrecorded` and forces a decision.
* **The 70-copy vendoring of `manifest.py`** — accepted as a stated decision, with two guardrails: `load()`
  refuses a stale schema (a repo with an old copy raises, it does not silently write), and
  `fixer_manifest_bump` opens one PR per repo when the schema bumps. The `lint.yml` sha256 check keeps the
  four meta copies identical.

---

## 7. The five recurring classes

The most reusable part of seven rounds, because each one recurred:

1. **A test that cannot see the state it tests** — four times. v2's passed *because* of the shallow-clone
   bug; v3's Case D blessed the wrong fixer behaviour; v5's Case E could not delete the manifest; v6's Case
   D could not see the merged fix. *Every gate case asserts from the clone the fixer wrote to, after merge
   and pull.*
2. **An inference where a declaration was needed** — twice. Asking git *who* wrote a file (unsound at
   depth 1), and inferring *which* tool writes a path from a grep of its basename. Both replaced by an
   explicit statement: three blob shas, and a `writer` field.
3. **A gate that fails open on the one case that matters** — twice. An untracked file allowed through
   ("bootstrap will catch up"), and a missing tool returning `False`. Both now fail closed, because the
   first run after a bootstrap miss is exactly the window the design exists for.
4. **A promise wider than the mechanism** — once, and it was the most dangerous. "Every write is gated"
   covered about half the recorded surface, and would have permanently mislabelled twelve generated files
   as human. Scope the promise to the mechanism, and make the gap a named work list.
5. **Ordering in a read-modify-write** — once. The fixer read the manifest, shelled out to a tool that
   rewrote it, then wrote its own stale copy. When two things write one file, the subprocess must go last.

6. **A config whose paths are relative to a layout nobody wrote down** — once. `"forge/tools/app-deliver.py"`
   in a config, when forge *is* the checkout root. Found only by running the check in the layout the
   workflow actually creates, never by reading it. The durable rule, now a comment at the top of the file:

   > A writer path in `manifest-paths.json` is relative to the `manifest-audit.py` checkout root — the
   > repository whose `lint.yml` runs the audit. Paths to that repository's own tools have no prefix; paths
   > to another repository's tools begin with that repository's checkout subdirectory, which is what
   > `actions/checkout`'s `path:` parameter names.

---

## 8. Files this touches

| Repository | Files |
|---|---|
| `forge` | `tools/manifest.py` (new), `tools/manifest-audit.py` (new), `manifest-paths.json` (new), `canonical-pins.json` (new), `scripts/bootstrap-manifest.sh` (new), `tools/sweep.py`, `tools/adopt.py`, `tools/app-deliver.py`, `tools/commit-and-verify.sh`, `tools/fetch.py`, `.github/workflows/new-app.yml`, `.github/workflows/lint.yml`, `scripts/new-app.py` |
| `app-builder` | `drsoam.py`, `tools/manifest.py` (vendored) |
| `registry` | `refresh.py`, `.github/workflows/refresh.yml`, `tools/manifest.py` (vendored) |
| `control-panel` | `tools/scan.py`, `tools/plan.py`, `.github/workflows/scan.yml`, `tools/manifest.py` (vendored) |
| `dashboard` | `tools/manifest.py` (vendored) |
| every app | `MANIFEST.json`, `tools/manifest.py` (vendored by the bootstrap, via a PR) |

---

## 9. One line to end on

The design was right from round 3. Every defect after that was in the code that checks the design — a
tool that could not see its own inputs, a test that could not see its own result, a config that named a
directory that does not exist. All three are closed, and the last one is verified by running the check
rather than by reading it.

The idea no longer has anything left to fix. What remains is work, not design: five writers gaining
`_manifest_record`, and sixteen deferred paths gaining a gate each.
