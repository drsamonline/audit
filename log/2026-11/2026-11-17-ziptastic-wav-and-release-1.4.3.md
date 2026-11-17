# ziptastic — the WAV segfault, three gates, and 1.4.3 with a Windows asset

Date: 2026-11-17 (second session) · Repos `drsamonline/ziptastic`, `heavenzip`,
`compfactory`, `HCS` · PRs ziptastic #23, #24, #26, #27, #28, #29; heavenzip #89, #91,
#92, #94; issues opened ziptastic #25, heavenzip #90 (closed), #93 (closed), compfactory
#8, HCS #16

## The bug I was sent for

ziptastic#22 — SIGSEGV on any valid 16-bit PCM WAV, mono or stereo, 2 KB up.

**Not the transform.** `wav_pack`/`wav_unpack` round-tripped the 2,044-byte reproducer
standalone before I touched anything. The accept/reject trial measured itself:

```
base64_pays() -> actual_cost() -> compress() -> wav stage -> base64_pays()
```

`actual_cost()` switched off `base64` to stop recursing but left `wav` on, and the wav
stage gates on the same trial. A depth counter in `actual_cost()` climbed 1, 2, 3 …
without bound; at `ulimit -s 512` the same input died with SIGSEGV, which is how the
stack overflow read as a crash in the transform.

The 256-byte boundary in the issue falls out of the code: below it `base64_pays()`
declines at its own floor and never reaches `actual_cost()`. A truncated WAV never
reaches the trial at all — `parse()` rejects it — which is why a corpus of malformed
samples called the engine healthy.

| fixture | before | after | `--no-wav` |
|---|---|---|---|
| 1,000 mono frames, 2,044 B | SIGSEGV | **1,000 B** | 1,355 |
| 1,000 stereo frames, 4,044 B | SIGSEGV | **1,605 B** | 1,877 |
| 8,000 mono frames, 16,044 B | SIGSEGV | **3,276 B** | 4,975 |

Fix: `trial_options()` switches off every stage that gates on `actual_cost()`;
`actual_cost()` returns "no opinion" instead of recursing; `trial_reentries()` counts a
recurrence so a test fails rather than a process dying.

## Three gates, because prose did not stop any of this

| gate | what it catches |
|---|---|
| `tests/unit/test_wav.cpp` (4 new cases) | calls `compress()` — nothing in that file did before, which is why the transform's own tests stayed green while the CLI died |
| `scripts/regression-corpus.sh` | a **valid** WAV: exit 0, byte-exact, smaller than `--no-wav`. Every malformed fixture in that file passes whether or not the bug exists |
| `trial_reentries() == 0` | the recursion class, not the instance |

## heavenzip: the chains that could never run

`$wav`/`$bmp` detector classes (heavenzip#89): content, not extension; narrower than
their containers, because a class is a route. `audio` routes on `detect = wav` now, and
`detect = binary` — documented since the grammar was written and rejected by the parser
— is accepted.

Then the three media chains: they named `bin/srep.exe`, and SREP cannot be shipped in
any form, so they refused on every machine. `BUNDLING.md` had specified the behaviour
("degrade … not fail") since it was written; nothing implemented it.

`optional = true` on a step now drops it with a notice when the tool is absent
(heavenzip#92). Running them for the first time exposed a worse bug: **the verify pass
was vacuous for any chain whose middle step writes to stdout** — `xz -d -c` sent its
payload to the terminal, wrote no file, and the next reverse step read the forward run's
leftover intermediate, so "verified" was printed for an archive that does not decode.

Then `precomp` exit 2 ("nothing to recompress", output still valid) failed every chain
that uses it; `ok_exit = 0,2` per step (heavenzip#94).

## The ceiling, measured

2 MiB of first-party sources, one thread:

| tool | 256 KiB | time | throughput |
|---|---|---|---|
| ziptastic -9 | 27.7% | 1.24 s | 206 KB/s |
| zpaq -m5 | 26.3% | 4.17 s | 61 KB/s |
| paq8px -5 | 22.7% | 207.9 s | **1.2 KB/s** |

−5.1% for 3.4× the time, and −17.9% for **168×**. paq8px is GPL-2+ and can never be
linked in, so the top of the ceiling is unreachable by construction. `FINDINGS.md` §6h.

## vendor/hcs: three wrong answers before the right one

1. `git subtree pull` — the gate's printed remedy — **cannot run**: the directory came in
   as one plain merge commit, no `git-subtree-dir` marker.
2. Forcing it with `-s subtree --allow-unrelated-histories` "merges well" and proposes
   **543 files, −91,112 lines**, deleting `old/zstd/zstd.h`.
3. My own explanation for that — "submodule contents materialised as real files, 247
   mirror-only" — was **wrong**. The files I counted were an untracked clone I had left
   inside an uninitialised gitlink directory: `find` sees it, git does not.

Measured from the index: `vendor/hcs` is HCS's regular files plus **23 gitlinks**, all 23
pins identical to HCS's. A sync is: copy 15 files, record 1 new gitlink
(`old/freearc-067`). Nothing deleted, no submodule fetched.

Applied, and **the build failed**: HCS `main`'s brunsli calls a 3-argument
`BrunsliEncodeJpeg` while its own header declares four. Reverted. `vendor-check` stays
red — correctly, now for a stated reason. HCS#16.

## 1.4.3, and the Windows asset

`ziptastic-1.4.2` published Linux only. The Windows job was added 2026-11-16, five days
after the tag; the 2026-11-16 run was `workflow_dispatch`, so publishing was skipped by
design, and its artifact was built from `main` nine commits past the tag so it cannot be
attached to v1.4.2 honestly.

Cut 1.4.3. The windows job also gained `needs: build-and-publish` — it uploads to a
release the Linux job creates, and nothing declared the dependency.

Published: `ziptastic-1.4.3-linux-x86_64`, `ziptastic-1.4.3-windows-x86_64.exe`,
`SHA256SUMS`, `SHA256SUMS-windows`.

## What I got wrong

- The materialised-mirror claim above, in a merged commit message and a PR body. The
  correction is in ziptastic#25 and in `vendor-sync.sh`'s header.
- Reported `247/262` counts that were artefacts of my own leftover clone, then replaced
  them with a tool — the counts also drift every time HCS moves (374/334 an hour later).
- First fix attempt for the stdout-reverse bug used *this* step's `produced` and
  truncated the archive it was about to read. The round trip caught it in one run.
