# 2026-10-31 — 94 of 94: the last three repositories are backed up

## Result

    backed up 94 of 94
    HCS:        133.8 MB in 2 part(s)  -> pushed 3 file(s), every blob sha confirmed on main
    The_Browser: 47.01 MB in 1 file     -> pushed 1 file,    blob sha confirmed on main
    ziptastic:  133.9 MB in 2 part(s)  -> pushed 3 file(s), every blob sha confirmed on main

The run is green. Nothing is outside the backup for the first time today.

## How it got there, including the wrong turns

**The ceiling is on the request body, not the file.** I first set chunks to 90 MB, then
40 MB. Both were refused with "Sorry, the file is too large to be processed". The contents
API counts the *base64* body, which is a third larger than the bytes — a 41.9 MB part was
a ~56 MB request and still too big. The API is simply the wrong transport for anything
large.

**A git push carries up to 100 MB per file**, so parts now travel that way: one clone, one
commit, one push, with every part and the descriptor in the same commit, so a dump is
either wholly there or wholly absent.

**Three bugs of my own, each found by running it rather than reading it:**

1. `write_chunked` passed the whole 133.8 MB blob to `write_via_git` *as well as* the
   parts, so it tried to push the full file and failed the dump. Now `blob=None` means
   "the parts are the payload".
2. `write_via_git` still computed `len(blob)` for its success message and its integrity
   check, and crashed on the chunked path with `TypeError: object of type 'NoneType' has
   no len()`.
3. The integrity check verified only the first file. In chunked mode there are several
   parts plus a descriptor, so a bad part could ride on a good neighbour. It now verifies
   every file it committed.

**And one regression I caused and then fixed:** the 40 MB threshold intercepted
The_Browser, which had been succeeding through the single-file git path, and broke it.
Raising CHUNK to 80 MB put it back on the path that works for a 47 MB tarball.

## What was verified, and how

- Round-trip: a blob split into parts reassembles byte-identically, and flipping one byte
  in a middle part is caught by the descriptor's sha256.
- Descriptor content: part count, total size, whole-file sha256, and per-part blob shas.
- Real code path, no token: `write_chunked` against a public repo ran clone -> read-tree ->
  commit -> verify -> push-attempt and failed only at the push, with no traceback.
- Live: the run above, with every blob sha confirmed on main.

## Also fixed on the way

- `dumps`, `dumps-2`, `dumps-3` ... are excluded from the source list by pattern. The run
  after the first rollover tried to back up `dumps-2` itself.
- The rollover cap now measures the tree (1778 MB) instead of the lagging API size
  (653 MB), which is what let the store grow past its limit in the first place.
- Retention can no longer delete nothing and report success.

## Still open

- Restore has been proven in unit tests but not yet against a live chunked dump. That is
  the one check I would run next: pull HCS back out of dumps-2 and compare it with the
  repository.
