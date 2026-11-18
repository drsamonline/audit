# States that look wrong and are not

Every entry here has been investigated at least once and found to be correct. They are
listed so the next run does not re-open them, and — more importantly — so nobody
"fixes" one by changing something that is right.

Each entry says what you will see, why it is that way, and what would be a real defect.

---

## `NOASSERTION` on a repository whose LICENSE is PolyForm

**You will see:** GitHub's sidebar reports "Unknown license" and the API returns
`license.spdx_id: "NOASSERTION"` for `HCS`, `compfactory`, `lexora` and other
PolyForm repositories, even though each has a `LICENSE` file containing the full
PolyForm Noncommercial 1.0.0 text.

**Why:** GitHub detects licences with Licensee, whose dataset does not include
PolyForm. A file it cannot match is reported as `NOASSERTION` — "I could not classify
this", not "there is no licence".

**What proves it is fine:** `tools/licence_check.py` reads the licence *text* and
classifies it correctly (`PolyForm Noncommercial 1.0.0`), and the README badge says the
same. Badge, text and intent agree; only GitHub's classifier is silent.

**What would be a real defect:** a README claiming MIT while the LICENSE says PolyForm —
that is the `licence-check` gate's job and it fails on it. Or a repository with a
PolyForm badge and no `LICENSE` file.

**Do not fix this by relicensing.** Switching to a licence GitHub recognises, to make a
sidebar look tidier, changes what the software actually grants. `lexora` additionally
declares `license = "PolyForm-Noncommercial-1.0.0"` in `pyproject.toml`, so package
tooling reads it even where GitHub does not.

---

## `state/fleet-audit.json` names fewer repositories than `state/repos.json`

**You will see:** `state/fleet-audit.json` says `repos_count: 100`, dated 2026-11-03,
while `state/repos.json` holds 140.

**Why:** they are different things. `repos.json` is the live snapshot, rewritten by
`tools/collect.py` on every run. `fleet-audit.json` is the capability matrix belonging
to one report, `reports/2026-11-fleet-audit/`, and is dated to the day that report was
written. A historical snapshot is supposed to stop moving.

**What would be a real defect:** `repos.json` older than the last fleet change, or a
report whose matrix disagrees with the state file captured on the same day.

---

## A repository with no `LICENSE` and no badge

**You will see:** the `licence-check` gate reporting "no LICENSE file - a badge here
would claim a licence the repository does not grant".

**Why:** that is the gate working. A badge is a claim; without a licence there is
nothing to claim.

**Do not fix this by adding a badge.** Add the licence, or leave it unbadged.

---

## A fleet repository that is absent from `state/repos.json`

**You will see:** `faztest` (and `dumps`, `dumps-3`, `dumps-4`, `registry`, `forge`,
`knowledge`) is a repository in the fleet and does not appear in `state/repos.json`, which
reports 140 repositories.

**Why:** `tools/collect.py` lists repositories through
`users/{owner}/repos?per_page=100&page=N`, and that endpoint **never returns private
repositories**, even for the owner. Six of the seven absent repositories are private by design
(`dumps*` hold source code; `registry`, `forge` and `knowledge` are the control plane), and
`faztest-fast-file-forge` is private because it was created that way in Lovable. `repos.json`
is a snapshot of the **public** fleet, not of every repository the account owns.

**What proves it is fine:** `gh api repos/drsamonline/faztest-fast-file-forge` returns the
repository, `gh repo list` shows it, and `gh api "users/drsamonline/repos?per_page=100&page=2"`
shows the crawl reaching the last page. The crawl is not truncating — it is answering a
different question.

**What would be a real defect:** a *public* repository missing from the snapshot, or a
`repos.json` older than the last public fleet change. If the owner wants private repositories
in the snapshot, `collect.py` has to move to `user/repos` (which is authenticated and includes
them) — that is a change of scope for the snapshot and a separate subject, not a bug fix.

**Do not fix this by adding the record by hand.** `repos.json` is rewritten by every run of
`tools/collect.py`; a hand-added row is deleted by the next crawl and looks like a regression
when it disappears.
