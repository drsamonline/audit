# 2026-10-31 — dumps: rollover now measures the store, and cleanup can fail loudly

## 1. The rollover cap was reading a stale number

`pick_dumps_repo()` decided whether a dumps repo was full from `info["size"]` — the
repository API's size field. That field lags badly: the API said **653 MB** while the
manifest said **1778 MB**. So the cap was checked against a figure days out of date, the
store sailed past its own 839 MB limit, and rollover never happened.

Now it sums the `.tar.gz` blobs in the repository tree — the same source the manifest is
derived from. Verified against a fake tree: counts 350 bytes from two tarballs while
ignoring a 9999-byte README and a tree entry, and returns None when the tree is
unreadable so the caller can fall back.

**Confirmed live.** The next run said:

    drsamonline/dumps is full (1778.3 MB) - rolling over
    creating drsamonline/dumps-2 ...
    could not create drsamonline/dumps-2: 403 Resource not accessible by personal access token

So the measurement is fixed and the rollover now fires. It stops at creation because
`BACKUP_TOKEN` has no **Administration: write** — which the workflow's own header already
warned about ("administration: write - ONLY if you want it to create dumps-2 when this one
fills up; otherwise create that by hand").

## 2. There is no cleanup workflow — the cleanup is `--keep`

I searched every workflow in the fleet for anything named clean/prune/purge/gc/trim/
retention/rotate/archive. The only match is `forge/sweep.yml`, which opens cross-repo pull
requests and has nothing to do with backups.

Retention lives in `backup.py`, driven by the `keep` input both backup workflows pass:
`dumps_to_delete()` keeps the newest N folders per repository, and `delete_folder()`
removes the rest. The logic is sound — it sorts by the timestamp in the folder name and
deletes oldest first — and the logs show it working ("kept 15", "kept 16").

**But it could not fail.** `delete_folder()` returned silently whenever the listing was
not a list, and never checked that a DELETE had actually worked. A rotation that deleted
nothing looked exactly like one that worked, and the store kept growing. It now:

- treats 404 as success (already gone is the end state we want),
- reports a failed listing and a failed DELETE by name,
- re-reads the folder afterwards and returns False if it is still there,
- and the caller logs "rotation could NOT delete X - the store will keep growing".

Tested three ways with a fake API: delete works -> True; delete silently no-ops -> False;
listing forbidden -> False.

## State

- 92 of 94 repositories backed up and verified.
- HCS and ziptastic still unbacked: both tarballs exceed GitHub's 100 MB per-file limit,
  so neither the contents API nor a push will take them. Needs LFS or chunking.
- Rollover is correct but blocked on the token's Administration permission.
