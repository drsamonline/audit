# OpenZL, benchmarked — the blocker was never a compiler

Date: 2026-11-19 · Repos `drsamonline/ziptastic`, `audit` · ziptastic PR #61

Plan item 1, the item that opened this whole thread, is answered. It was blocked twice on "`make`
is not installed in the sandbox", and that diagnosis was wrong in three separate ways.

## What was wrong with the diagnosis

| what the handover said | what is true |
|---|---|
| "`make` is not installed, and it blocks OpenZL" | CMake drives **Ninja**; `make` is not involved |
| "fix that first: `sudo apt install make`, or provide a machine that has it" | the sandbox **can** build it; the cap that kills big builds is `ulimit -v` 1,536,000 KiB with an **unlimited hard limit** — `ulimit -v unlimited` and it runs |
| "the CMake build's unconditional SDDL compilers cost ~1 object per 280-second call" | the SDDL compilers are not the wall; **xgboost** is. `tools/ml_selector` pulls it as an `ExternalProject` — a full xgboost build — and `zli` never links it |

Build that works here, 2 vCPU / 2 GiB / no `make` / no gcc:

- `pip install ninja cmake ziglang`, then `zig cc` / `zig c++` wrappers as `CC`/`CXX`
- comment out `add_subdirectory(ml_selector)` in `tools/CMakeLists.txt` (local patch, not upstream)
- `cmake -G Ninja -B build -DCMAKE_BUILD_TYPE=Release` with tests, benchmarks, examples, python
  extension and install off
- `ninja -C build zli -j2` — 484 objects, ~50 minutes, run in 300-second windows

Result: `zli 0.3.0`, 25 profiles, `list-profiles` and `compress`/`decompress` working.

## The numbers

Silesia, 12 files, 211,938,580 bytes, every archive decompressed and compared byte for byte.

| | ratio of raw | time over corpus |
|---|---:|---:|
| OpenZL `serial -l9` | 29.68% | **18.0 s** |
| ziptastic `-9` | **20.48%** | 622.4 s |
| xz `-9e` | 22.86% | 241.2 s |
| 7z LZMA2 9e | 22.86% | 243.6 s |
| faztest `-q9` | 26.74% | 81.3 s |

Per file, `serial` is between 18.91% (`sao`) and 80.02% (`nci`) larger than ziptastic — never
smaller. ziptastic is **31% smaller and 35× slower**; xz is 24% smaller and 13× slower.

## The result that changes the plan

`sao` is the one file in the corpus OpenZL has a dedicated profile for — the corpus is named
after it. With that profile:

| sao, 7,251,944 bytes | archive | vs ziptastic | vs xz | time |
|---|---:|---:|---:|---:|
| OpenZL `-p sao -l9` | **2,358,130** | **−46.59%** | **−46.72%** | **0.574 s** |
| OpenZL `-p serial -l9` | 5,250,148 | +18.91% | +18.63% | 0.67 s |
| ziptastic `-9` | 4,415,125 | — | −0.24% | 34.26 s |
| xz `-9e` | 4,425,664 | +0.24% | — | 5.66 s |

**46.6% smaller, in one sixtieth of the time.** Level barely matters (`-l6` 5,294,308 vs `-l9`
5,250,148 on `serial`); the profile is the whole difference.

## What it means

1. **The ratio claim survives; the shape claim does not.** "A generic engine beats xz" holds —
   20.48% against 22.86%. "A generic engine is the right shape" does not: on a format with a
   profile, it loses by half.
2. **The next transform is a container, not a codec.** SAO is 3.4% of this corpus and worth 46.6%
   on it. ziptastic's Layer 0 detects PNG, BMP, CSV/TSV, SQLite, WAV, ZIP, gzip and base64; the
   pattern OpenZL demonstrates — identify the format, then delta inside its structure — is what
   the next Layer-0 entry should follow.
3. **18 s against 622 s is a frontier point `PARETO.md` did not have.** Any product shipping `-9`
   as a default is buying ratio with 35× latency, and nothing in the CLI said so.
4. **Trap 8 generalises.** A limit you can raise is not a limit; a missing tool is not a missing
   capability. Two sessions lost to `make` that Ninja replaced, and to a cap that was soft.

## Shipped

| item | where |
|---|---|
| `docs/OPENZL_MEASURED.md` — build recipe, both tables, caveats, what it changes | ziptastic PR #61 |
| `scripts/openzl-bench.sh` — reproduces the table, verifies every round trip, refuses to report a size it could not decode | ziptastic PR #61 |

## Open

- **Format-aware comparison is one file deep.** `sao` is the only corpus file with a profile.
  A CSV, a Parquet and a PyTorch model would each add a row; the corpus has none, and generating
  fixtures for them is the same trap the holdout set exists to avoid.
- **`mozilla` is still measured as two halves for ziptastic** (`docs/FINDINGS.md` §5). OpenZL
  compressed it whole in 3.81 s, so the whole-file number for ziptastic is now the only missing
  cell in the comparison — it needs a machine that can spend more than 300 seconds on 51 MB.
- **lzbench** (plan item 2) is still unbuilt; the same toolchain and the same `ulimit` fix apply.
