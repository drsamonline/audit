# The block-size policy ships — 16 MiB above 8 MiB

Date: 2026-11-19 · Repos `drsamonline/ziptastic`, `audit` · ziptastic PR #66

Follows `2026-11-19-block-size-at-scale.md`, which measured the gap and recommended a
size-conditional default. It is now in the engine.

## What changed

```cpp
// include/chimera/format.hpp
inline constexpr size_t kLargeInputThreshold = 8u * 1024u * 1024u;
inline constexpr size_t kLargeBlockSize      = 16u * 1024u * 1024u;

// src/engine/compressor.hpp
inline size_t default_block_size_for(size_t input_size) {
  return input_size > kLargeInputThreshold ? kLargeBlockSize : kDefaultBlockSize;
}
```

The policy lives in the library, so every `compress()` caller gets the same answer; the CLI
passes `-b` through untouched and an explicit `-b` always wins. Files at or below 8 MiB keep
4 MiB, which is what every holdout baseline was recorded at.

## Verification

| check | result |
|---|---|
| `xml` (5.3 MB, under threshold) | 374,814 — the 4 MiB result, unchanged |
| `dickens` (10.2 MB, over threshold) | 2,260,672 — exactly the `-b 16384` result |
| `dickens -b 4096` | 2,355,685 — explicit flag wins |
| holdout (`scripts/holdout.py --check`) | 4 files, **+0 bytes each**, "hashes match and nothing grew" |
| `ctest` | **38/38 suites**, 217 s |
| new unit case | `block_size_policy`: threshold/above/zero, plus a 16 MiB block round-trip on a small input |

## Cost, stated in the PR

+19% time at 16 MiB on the seven text files (470 s vs 395 s). Ratio is bought with latency,
on large inputs only.

## Two things worth recording

1. **A test fixture that lies.** The first version of the CLI assertion used 9 MiB of
   repetitive text and got **one block at `-b 4096`** — because dedup collapses the repetition
   before the block loop, so the fixture never exercised block splitting. Incompressible data
   gave the right counts but took 35 s per run. The assertion moved to a unit test on the pure
   function instead: 3 lines, milliseconds, and it tests the thing that was actually wrong
   (the default), not the thing that was already right (the flag).
2. **The sandbox filled `/tmp`.** `/tmp` is a 64 MB tmpfs; a 9 MB fixture plus archives hit
   "No space left on device" mid-test. Everything now writes under `/scratch/work`.

## What is still open

- **`samba` and `sao` are byte-identical at 4 and 16 MiB** — their blocks are dominated by
  something that does not scale with block size. Worth one look before trusting the non-text
  group's +0.31%.
- **`mozilla` (51 MB) is unmeasured whole** at any block size: `-9` does not finish in a
  300-second step. It is the largest binary in the corpus and the one number missing from
  every table in this thread.
- **32 MiB is measured but not shipped.** It continued to help on the two largest text files
  (−2.66%, −5.59% against 16 MiB); the threshold policy could be extended to a second tier,
  but the time cost was not measured at that size.
