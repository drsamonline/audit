# CLDR — conventional commits as a CI gate (cocogitto)

Date: 2026-11-09
Repo: `drsamonline/CLDR` · branch `ci/conventional-commits` · PR #18 (open, not merged)
Reference link taken: `cocogitto/cocogitto`
Same session: `2026-11-09-cldr-units-ten-dimensions.md` (PR #17),
`2026-11-09-feather-router-signatures.md` (feather PR #1)

## What I looked at

`.github/workflows/build-release.yml`, `CONTRIBUTING.md`, and 82 commit subjects
on `main`.

## What was wrong

Conventional commits are written by hand across this fleet, and drift is silent
— nothing checks a subject before it lands. The proposal was cocogitto; the
question was whether a gate would be red on arrival.

It would have been. Of the 82 commits on `main`, 52 use a type outside the
standard set: `licence:` (12 commits), `sweep:`, `release:`, and title-cased
subjects such as `Fix ...`. A gate over history would have failed immediately
and been ignored from then on.

## What I changed

1. `cog.toml` declaring the types this repo actually uses — `licence` and
   `sweep` alongside the standard set, with `ignore_merge_commits = true`.
2. A `commits` job in the existing workflow, `pull_request` only, running
   `cog check <base.sha>..<head.sha>` — the commits the PR adds, never the
   history. Advisory (`continue-on-error: true`), matching how `rustfmt` and
   `clippy` are already gated here; promote it once a few PRs pass clean.
3. cocogitto 7.0.0 pinned and downloaded from its GitHub release (musl x86_64)
   into the runner. Nothing added to `Cargo.toml`; the shipped binary is
   untouched.
4. `CONTRIBUTING.md` now says to write conventional subjects and gives
   `cog check main..HEAD` as the local equivalent.

## Evidence

The job ran on PR #18 in 6s, the first PR it has ever seen:

    cog 7.0.0
    cog check "aea2963..7960e89"
    No errored commits

A gate that only passes proves nothing, so the same pinned binary and this
`cog.toml` were run against a throwaway repo with a deliberately bad subject:

    $ cog check $BASE..HEAD
    Found 1 non compliant commits in 73ad6bf..HEAD:
    Errored commit: ce25c76 <t>
    	Commit message: 'Fix the thing'
    	Error: Missing commit type separator `:`
    exit=1

In the same range `feat(units): a conforming subject` and
`licence: PolyForm Noncommercial 1.0.0 (docs/index.html)` both pass — which is
the point of declaring `licence` rather than letting the standard set reject the
repo's own vocabulary.

## What I deliberately did not do

- **No history rewrite.** 52 non-conforming commits stay as they are. Rewriting
  the history of a shipped repo to satisfy a linter is not a change I would
  make.
- **Not blocking yet.** Advisory first, for the same reason rustfmt and clippy
  are.
- **No `cog bump` / changelog generation.** CLDR already has `changes/` and a
  `VERSION`; a second release mechanism would fight the first.
- **No version bump, no merge.**

## Next

Promote `commits` to blocking after a few clean PRs. Decide on PR #17 and #18.
