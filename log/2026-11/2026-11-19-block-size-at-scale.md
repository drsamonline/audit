# Block size, swept where it can matter — 16 MiB is 2.70% smaller

Date: 2026-11-19 · Repos `drsamonline/ziptastic`, `audit` · ziptastic PR #65

The previous entry ended with "full Silesia at 4/8/16/32 MiB, all 12 files — one table decides the
default". Reading the repo's own docs first cut that work in half and changed what the table means.

## What the docs already said

`FINDINGS.md` §3d had already swept block size, 64 KiB → 16 MiB, and concluded **4 MiB stays**:
"it does not move without a reason that is bigger than 0.6%". `BENCHMARKS.md` Phase 12 recorded the
same sweep's first half (256 KiB → 4 MiB on `dickens`, −14.1%).

The hole: **every corpus in §3d was 846 KB to 2.75 MB**, so the 16 MiB column was the same stream as
the 4 MiB column. §3d says it itself — "cells repeat where the block size exceeds the file". The
large-block regime had never been measured on a file large enough to have one.

## The measurement

Silesia (5–51 MB per file), `-9`, `-b` varied, every archive byte-verified:

| group | 4 MiB | 16 MiB | change |
|---|---:|---:|---:|
| text, 7 files | 20,389,315 | 19,518,977 | **−4.27%** |
| non-text, 4 files | 10,658,691 | 10,691,231 | +0.31% |
| **all 11 measured** | **31,048,006** | **30,210,208** | **−2.70%** |

32 MiB keeps going on the biggest text files: `webster` −2.66%, `nci` −5.59% against 16 MiB.
Cost: **+19% time** (470 s vs 395 s on the seven text files). `mozilla` excluded — a whole-file
`-9` does not finish in a 300 s step at either size, which is why §5 records it as two halves.

Against bzip3: `nci` goes −6.28% → **−11.5%**, `webster` +5.23% → +2.42%.

## The decision it supports

| option | verdict |
|---|---|
| keep 4 MiB, document `-b` | leaves 2.70% on the table |
| raise the default to 16 MiB | −2.70% overall, but **+0.31% on non-text**, and every holdout baseline must be re-recorded |
| **size-conditional: inputs above ~8 MiB get 16 MiB blocks** | **recommended** — the gain exists only where a big block can exist, and every `holdout/` file is 21 KB–840 KB, so the cost gate stays valid |

Not shipped yet: the conditional default changes archive bytes for large inputs, so it needs the
holdout re-run and a green CI before it lands. That is the next code change, and it is small.

## Why this was worth reading first

- §3d existed, so re-sweeping 64 KiB–4 MiB would have been wasted work.
- §3d's conclusion was sound for its corpora and wrong as a general claim — the kind of error a
  reader only sees by checking what the corpora *were*, not what the table says.
- The holdout rule (`docs/HOLDOUT.md`) turns "raise the default" from a one-line change into a
  re-baselining exercise, which is why the conditional option is the only cheap one.

## Caveats

Eleven files, one corpus, one run per cell; sizes exact, times not. `samba` and `sao` are
byte-identical at 4 and 16 MiB, which suggests their blocks are dominated by something that does not
scale with block size — worth a look before trusting the non-text group's +0.31%.
