# UniRep — two files, no app

Date: 2026-11-09 · Repo `drsamonline/UniRep` · no branch, no PR
Links taken: none

## What I looked at
`git ls-files`: `PRIVACY.md` and `SECURITY.md`. That is the whole repository
(GitHub reports 2 KB). No README, no LICENSE, no app, no tests, no workflow.

## What was wrong
Nothing to fix and nothing to verify. "Universal Index Repertory" is a name and two
policy files.

## What I changed
Nothing.

## Evidence
    $ git ls-files
    PRIVACY.md
    SECURITY.md

## What I deliberately did not do
- **Did not start the app.** A universal repertory index is a data project plus a
  reader; the reader pattern already exists (`repertory-reader`, `Repertorium-Publicum`)
  and the data lives in `homoeopathic-materia-medica-repertory-json`. Building it
  blind, with no data checkout and no specification in the repo, is not a slice —
  it is a guess about what the app should be.
- **No link work.** `oorep` and `OpenRep-Deutsch` are the two data projects the
  repertory apps in this fleet already read.

## Next
Decide what UniRep is meant to be — a reader over the same JSON, or an index across
several. Then it is a build, not an improvement pass.
