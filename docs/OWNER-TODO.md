# Owner TODO — the things only you can do

Written 2026-11-19. Everything here needs a human: a token, a dashboard click, or a file that does
not exist in the sandbox. Everything **not** listed here is done and merged.

Six steps, in the order they unblock the most. Each one says what to click, what "done" looks like,
and what happens if you skip it.

---

## 1. Disconnect the old app-builder project for faztest (5 minutes)

**Why:** faztest was scaffolded by a hosted builder (Lovable). Its files are gone from the repo, but
the project is still connected on their side, so a push from their editor can put the scaffolding
back.

**Steps:**
1. Open <https://lovable.dev> and sign in with the same account that created `faztest-fast-file-forge`.
2. Open the project for **Faztest Fast File Forge** (the repo README used to link it as
   `lovable.dev/projects/9ddecf34-…`).
3. Go to the project **Settings** → **GitHub** (or "Connected repository") → **Disconnect**.
4. If you want it gone entirely, choose **Delete project**. The GitHub repo stays; only the link
   between them is removed.

**Done when:** the Lovable project no longer lists the GitHub repo as connected.

**If you skip it:** nothing breaks today, but a future edit in that editor will re-add `.lovable/`
and the old AGENTS block, and the next session will spend time removing them again.

---

## 2. Publish `zipkosh` to PyPI (10 minutes)

**Why:** the wheel is built, tested on three platforms, `twine check` passes, and `kosh doctor`
returns ready from a clean venv. The only missing piece is the token.

**Steps:**
1. Open <https://pypi.org/manage/account/token/>.
2. Click **Add API token**. Name it `zipkosh`, scope it to the project `zipkosh` (create the project
   first if PyPI asks — uploading the first time creates it).
3. Copy the token (`pypi-AgEIcHlwaS5vcmc…`). It is shown **once**.
4. Give it to the next session as an environment variable named `PYPI_API_TOKEN`, or run the upload
   yourself:
   ```bash
   cd kosh && python -m twine upload --username __token__ --password "$PYPI_API_TOKEN" dist/*
   ```
5. Check it landed: <https://pypi.org/project/zipkosh/>.

**Done when:** the project page loads and `pip install zipkosh` works in a fresh venv.

**If you skip it:** `zipkosh` stays built-but-unpublished. Nothing else depends on it.

---

## 3. Grant the GitHub connector Actions read access (2 minutes)

**Why:** the agent cannot read CI results. It gets `403 Resource not accessible by integration` on
`actions/runs` and `check-runs`, so it has been merging PRs **blind** — twice today it said so in the
PR body. One wrong merge and the branch is red with nobody watching.

**Steps:**
1. Open <https://github.com/settings/installations>.
2. Find the **Sarvam** app (the one the agent uses) → **Configure**.
3. Under **Permissions**, set **Actions: Read-only** and **Checks: Read-only**.
   Under **Repository access**, make sure the repos you want checked are selected.
4. Save. The next session will see the change; nothing needs reinstalling.

**Done when:** a session can run `gh run list` without a 403.

**If you skip it:** every merge stays blind, and "the tests pass" remains something nobody verified.

---

## 4. Give the SQLite column transform a real database (15 minutes, one file)

**Why:** the transform's probe (`ziptastic/scripts/column_filter_probe.py`) is the gate, and it has
never run on a real database — the sandbox has none. A synthetic one would only prove the code agrees
with itself.

**Steps:**
1. Find any real SQLite file on your machine — a browser history, an app's local DB, a phone backup,
   anything with numeric columns. **Do not send anything private**; a small one is enough (a few MB).
2. Copy it into the session's upload area, or attach it in the chat.
3. Say: "run the column filter probe on this database".

**Done when:** the probe has printed a per-column saving table and the numbers are in
`docs/SQLITE_MEASUREMENT.md`.

**If you skip it:** the transform stays unimplemented. It is a measured 27.8% on a 6.9 MB indexed
database — the largest unclaimed win after ECM.

---

## 5. `corpus-extendum`: decide on the `resvg` swap (5 minutes)

**Why:** PyMuPDF is AGPL — the last AGPL dependency in the fleet. `resvg` (MPL-2.0) would replace it
for SVG plates, but the decision needs the plates rendered correctly, and the sandbox has no traced
plates to compare.

**Steps:**
1. Pick 2–3 of the traced SVG plates the site actually serves (the ones with the most paths).
2. Attach them, or say where they are.
3. Say: "render these with resvg and compare against the PyMuPDF output".

**Done when:** either the swap ships or it is rejected with a measurement, and the AGPL dependency is
either gone or explicitly accepted.

**If you skip it:** the fleet keeps one AGPL dependency, which matters if you ever distribute binaries.

---

## 6. Optional: a machine without the 300-second call limit (no action if you don't care)

**Why:** `mozilla` (51 MB) is the one file in every table that is measured as two halves or not at
all — `-9` needs about 315 s and the sandbox kills a call at 300 s. Everything else is measured.

**Steps:** nothing, unless you want that last cell. Any Linux box with 4 GB RAM and a shell would do;
the build recipe is in `docs/HANDOVER-2026-11-19.md` §5 and takes about five minutes.

**Done when:** `ziptastic -9 mozilla` prints a size in one run.

---

## What you do **not** need to do

- **Nothing needs installing in the sandbox.** There is no `make` and nothing requires one; the
  toolchain is `pip install ziglang cmake ninja` plus a `ulimit -v unlimited`.
- **No secrets in the repo.** The `PYPI_API_TOKEN` above goes into the session environment, never
  into a file.
- **No manual merging.** All PRs from today are merged; the repos are at 0 open PRs and 0 open
  issues.
- **No re-running of measurements.** Every number in today's documents came from a command whose
  output was read, and the holdout gate is green at the new block-size policy.
