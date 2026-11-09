# compfactory — the sync put the workspace where nothing else looked

Date: 2026-11-09
Repo: `drsamonline/compfactory` · branch `fix/sync-workspace-path` · PR #1
(open, not merged)
Reference links taken: none
Same session: `2026-11-09-hcs-sources-crosscheck.md`,
`2026-11-09-heavenzip-badges.md`, `2026-11-09-ttb-title-case.md`,
`2026-11-09-neo-string-literal-escapes.md`,
`2026-11-09-lumen-capture-date-and-badge.md`,
`2026-11-09-app-image-toolkit-badges.md`,
`2026-11-09-offline-pdf-toolkit-cli-refusals.md`,
`2026-11-09-feather-router-signatures.md`,
`2026-11-09-cldr-conventional-commits.md`

## What I looked at

All 24 tracked files. There is no source code: four scripts (`sync.ps1`,
`sync.sh`, `build-all.ps1`, `bump-hcs.ps1`), `.gitignore`, `dispatch-sync.yml`,
docs and badges. The scripts *are* the repository.

## What was wrong

The four scripts disagreed about where the workspace is. `$root` is the scripts
directory in all of them:

    sync.ps1       Join-Path $root "workspace"          -> scripts/workspace
    build-all.ps1  Join-Path $root "..\workspace\ziptastic" -> workspace/ziptastic
    bump-hcs.ps1   Join-Path $root "..\workspace\ziptastic" -> workspace/ziptastic
    sync.sh        "$(dirname "$0")/../workspace"       -> workspace

So on Windows the first step of the documented flow cloned into
`scripts/workspace` and the second step said "workspace/ziptastic not found. Run
scripts/sync.ps1 first." — after running exactly that.

Second symptom, same cause: `.gitignore` ignores `/workspace/`, anchored to the
repository root, so the misplaced tree was not ignored. A PowerShell sync left an
untracked checkout one `git add -A` from being committed.

## What I changed

`sync.ps1` resolves `..\workspace` like the other three, with a comment saying
why. `tests/check-scripts.sh` reads all four and fails if they disagree or if the
path they agree on is not ignored; `tests.yml` runs it. The repository had no test
job at all, so the guard would otherwise have been a file nobody ran.

## Evidence

    $ bash tests/check-scripts.sh
    scripts agree: workspace at ../workspace, ignored by .gitignore     exit 0

    $ git stash push scripts/sync.ps1 && bash tests/check-scripts.sh
    FAIL: sync.ps1 resolves the workspace to 'workspace', expected ../workspace from scripts/
    1 problem(s) found.                                                 exit 1

CI run 42644341281, job `scripts`: success, log line `scripts agree: workspace at
../workspace, ignored by .gitignore`.

## What I deliberately did not do

- **`badge-build.svg` still says "build: green"** and nothing here builds in CI:
  `build-all.ps1` builds *ziptastic*, in a workspace this repository does not
  contain. That is the same class of false claim as heavenzip's, and it needs its
  own change; folding it in would have made this PR two ideas.
- **No link work.** `awesome-compopt` and `awesome-oss` are indexes;
  `7-Zip-zstd`, `PeaZip`, `zpaqfranz`, `CompactGUI`, `crabz` are compressors this
  workspace does not contain; `hyperfine` and `criterion.rs` benchmark a codebase
  that is not here.
- **No version bump, no merge.**

## Next

Decide on PR #1. Then the build badge, which is the only remaining claim in this
repository that is not true.
