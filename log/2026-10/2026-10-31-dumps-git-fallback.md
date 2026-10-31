# 2026-10-31 — dumps: a git-push fallback, and the 100 MB wall behind it

## What I changed

`dump_one()` writes each tarball with `PUT /contents`, which refuses large files. It now
falls back to `write_via_git()` when the API answers 422 "too large": clone the dumps repo,
commit the file, push. That is GitHub's own advice in the error message.

Three things the fallback had to get right, because each would have destroyed backups:

1. **`--no-checkout` leaves an EMPTY index.** `git add` + commit would then write a tree
   holding only the new file and delete every other snapshot. `git read-tree HEAD` fills
   the index from the commit first. Verified on a real repo: 26 files in HEAD before,
   27 after, probe present.
2. **The token must not go in the remote URL**, where `git remote -v` would print it. It
   travels in an `http.https://github.com/.extraheader`.
3. **A push that exits 0 is a claim about a command.** The committed blob sha is compared
   with the sha of the intended bytes, then `ls-remote` is asked what main holds. The sha
   function was checked against git's own: both `ce013625...` for the same bytes.

Also fixed: after a successful git push the code went on to run the API-sha check and
printed "integrity NOT verified" about a dump that had just been verified. It now records
that the git path verified it.

## What it achieved

    The_Browser: 47.01 MB pushed, blob 7ce072e10e confirmed on main   ← recovered
    backed up 92 of 94   (was 87 of 91 before the fallback)

The_Browser had no backup at all. It has one now, verified.

## What it did not achieve, and why

    HCS:       push attempt 1..3 rejected: remote: error: ... See https://gh.io/lfs
    ziptastic: same

Both tarballs exceed **GitHub's 100 MB per-file limit**, which applies to a normal push
exactly as it applies to the contents API. This is not a repository-capacity problem, so
`dumps-2` cannot solve it — a single file is too big. The only routes are Git LFS, or
splitting the tarball into parts under 100 MB with a manifest to reassemble.

## State

- 92 of 94 repositories backed up, verified.
- 2 outstanding: HCS, ziptastic. Both need a decision (LFS or chunking), not a bug fix.
- The dumps repo is at 1778 MB — past the 839 MB rollover cap, because `pick_dumps_repo()`
  reads the lagging repository `size` rather than the manifest total it already computes.
  Rollover will happen late. Not changed here; it is a separate, smaller fix.
