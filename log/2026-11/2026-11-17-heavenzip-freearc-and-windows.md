# heavenzip — FreeArc's own config, ten bundled tools, and Windows actually working

Date: 2026-11-17 · Repos `drsamonline/heavenzip`, `drsamonline/ziptastic`, `drsamonline/HCS`
PRs merged: heavenzip #41–#88 (selected below), ziptastic #20–#21 + issue #22, HCS #14–#15

## What this session set out to do, and what it became

It started as "add more compressors to the bundle" and turned into three separate jobs:
make the orchestrator orchestrate more than one engine, make the Windows side real, and
take FreeArc's configuration seriously instead of guessing at it.

## heavenzip: 9 profiles → 17, 5 binaries → 10

| tool | how it got there |
|---|---|
| `xz` | CMake + zig, static (libc only) |
| `precomp` | CMake + zig, `-include assert.h` for its vendored range coder |
| `7z` | **no make in the container** — `tools/build-7z.py` reads the makefile's object rules |
| `arc` + `unarc` | same approach on `freearc-c-main`; needs **`-DFREEARC_NO_MF_MT`** on `C_LZMA.cpp` |
| `brotli` | CMake, `BUILD_SHARED_LIBS=OFF` |

New profiles: `max-deflate` (precomp→srep→xz), `max-ratio-7z`, `freearc`, `freearc-9b`,
`fa-p`, `fa-precomp-srep-zstd`, `sevenzip`, `audio`.

**`arc` segfaulted on `lzma` until the per-source flag was found.** Nothing fails at build
time — the binary links, runs, prints its version, and dies on the one codec that matters.
The Makefile builds `C_LZMA.o` with `-DFREEARC_NO_MF_MT`; without it the multithreaded
match finder compiles in and the encoder crashes.

## Windows: from "builds" to "works"

| layer | before | after |
|---|---|---|
| `ziptastic.exe` | never built | builds, round-trips, published with its own `SHA256SUMS-windows` |
| `heavenzip.exe` | never built | builds, its tests pass, **drives the engine** |
| `preflate.exe` | "MSVC-only, blocked" | builds, `preflate-wrap.cmd` round-trips |
| bundle | parts only | `heavenzip-1.0.0-windows-x86_64.tar.gz`, config and notices included |

The blocker was `std::system` + cmd.exe quoting: the program never ran and the redirect
files stayed empty, so the failure carried no information. `CreateProcessA` with explicit
`CreateFileA` handles fixed it. The `dlfcn.h` in ziptastic's plugin host was the other one.

## FreeArc's configuration, taken seriously

The 0.67 distribution answered three questions this repo had been guessing at:

- **Licence, verbatim**: free to use, *"File FreeArcCodecs.dll cannot be redistributed
  without my prior written permission."* That DLL is a single file holding **every**
  external codec — srep, precomp, lolz, ecm, jpg. It is why no repository carried
  `srep.dll` or `lolz.dll`.
- **The real method table** (284 definitions) and the `#p` chain:
  `maxprecomp + exe2 + maxsrep + #xb`, `maxprecomp = precomp:intense`,
  `maxsrep = srep:m3f:mem256mb`.
- **`fa.ini`, not `arc.ini`** — from Bulat's posts: *"You can replace any of these
  definitions using 'Compression methods' section in your fa.ini"*, and `-mx` selects
  method `x`, which that section defines.

Captured as data: `config/freearc/{arc.ini,arc-methods.txt,arc-groups.txt,fa.ini,benchmark-baseline.txt}`.

## Measured, on a real corpus

Silesia, 2 MB samples, `tools/sweep.py`:

| file | plain | xz -9 | freearc |
|---|---|---|---|
| dickens | **476,122** | 586,596 | 632,511 |
| ooffice | **744,522** | 893,220 | 904,151 |
| sao | 1,220,380 | **1,220,336** | 1,242,397 |
| xml | **169,242** | 221,232 | 246,212 |

The engine wins three of four by **17–23%**, and is 2–4× slower. On 16-bit PCM audio the
delta filter (`--delta=dist=2`) beats plain LZMA by **38%**.

FreeArc's own baseline, for comparison: `-m5` 7.047×, `-m5p` (precomp+srep) 7.277× —
**3.3% for 30% more compression time and 3× the decompression time**.

## Bugs found by running things rather than reading them

| bug | symptom |
|---|---|
| autotune work dir | `fs::path("s.txt").has_parent_path()` is false — the fix never applied to a bare filename |
| `SIZE_MAX` sentinel through JSON | passed locally, failed CI; 2⁶⁴−1 read back through a double became 0 |
| `tar -a -cf x.zip` in Git Bash | wrote a **tar named .zip**; downloaded, checksummed, then `BadZipFile` |
| precomp's `-oFILE` | the restore path sits inside a token, so the scan recorded "nowhere" and the last step wrote over the input |
| `arc` appends `.arc` | the archive landed at `OUT.arc`; the step's own output never existed |
| 7-Zip `E_NOTIMPL` | a 7-Zip with no 7z format handler compiles, links and runs perfectly |
| `CreateProcess` `started` collision | MSVC refused; GCC never compiles that branch |
| **`ziptastic` segfaults on any valid WAV** | filed as ziptastic#22 with a 2 KB reproducer |

The last one is the only open bug in the fleet. The misleading detail: a WAV **truncated**
mid-stream exits 0, because parsing rejects it and the transform never runs — a corpus of
malformed samples would report the engine as healthy.

## Gates added because prose did not stop the mistakes

`tools/check-pipes.sh` fails any workflow that pipes into `head` under `pipefail`. The trap
cost three CI cycles in one day — `ldd | head -1`, `find | head -1`, `tar -tzf | head -5` —
two of them *after* it was written into `docs/TRAPS.md`. It found two more instances on its
first run, both hidden behind `|| true`.

## The mistake worth recording

I merged a PR **while its checks were failing**: the merge was chained behind a status
query and I did not read the failure. main went red (17 profiles, test asserting 16). Fixed
in #87. Automating the check is not the same as reading it.

## What is left

| # | item |
|---|---|
| 1 | ziptastic#22 — the WAV segfault |
| 2 | `$wav`/`$bmp` detector classes, so `audio` routes without being asked |
| 3 | Media corpus sweep — the three media chains report `n/a` on every corpus tried |
| 4 | `paq8px` on one 2 MB file, once, to know what the ratio ceiling costs |
| 5 | lexora benchmark conflict (0.3352 vs 0.3367), lexora gates |
| 6 | kosh Pages source (API 403), `verify --jobs`, PyPI token |
| 7 | HCS 24 `copy` pins |
