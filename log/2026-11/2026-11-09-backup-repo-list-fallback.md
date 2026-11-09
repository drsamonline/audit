# backup — the public-list fallback restarted mid-pagination

Date: 2026-11-09 · Repo `drsamonline/backup` · PR #2 (open, not merged)
Links taken: none

## What I looked at
`backup.py` (1,443 lines) — `all_repos`, `dumps_to_delete`, the change-detection
block — and `tests/test_backup.py`.

## What was wrong
`all_repos` fell back to the public repository list per page. A private-list
failure on page 2 left page 1 (private) in `out` and took page 2 from the public
list: a mixed set, and a repository missing from it quietly stops being backed
up. The file's own doctrine below says a failed lookup is not evidence of no
change; the same applies to a failed listing.

## What I changed
Endpoint chosen once. Failure on page one restarts on the public list from page
one; failure after that raises instead of returning a partial list.

## Evidence — and its limit
    python3 tests/test_backup.py        57 passed, 0 failed (with the change)
    targeted probe                      NOT RUN — sandbox raises MemoryError at
                                        `out += batch` (in-place list extend)
The suite stubs `all_repos` wholesale, so this path had no test before. Recorded
as inspected rather than tested; the probe is a minute's work on a normal machine.

## What I deliberately did not do
- No change to the private-first policy, the SKIP/dump-store filters or the sort.
- No link work: borg/restic/Keka/rustic are backup engines with their own storage
  formats; this is a GitHub-releases snapshot tool.
- No version bump, no merge.

## Next
Decide on PR #2, and add the pagination probe to `tests/test_backup.py`.
