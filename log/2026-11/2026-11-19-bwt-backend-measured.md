# The BWT candidate — it fires, it pays, and it is 7% behind bzip3

Date: 2026-11-19 · Repos `drsamonline/ziptastic`, `audit` · ziptastic PR #63

Follows `2026-11-19-openzl-benchmarked.md`. `HARNESS_MEASURED.md` showed bzip3 beating ziptastic on
all seven text files of Silesia. This answers why: **the selector is fine, the backend is behind.**

## Method

`-9` against `-9 --no-bwt` on the same file — the difference is exactly what the BWT candidate
(libbsc) contributes, every other candidate untouched. Both arms decompressed and byte-compared.

| file | `-9` | `--no-bwt` | BWT saves | bzip3 -10 | `-9` vs bzip3 |
|---|---:|---:|---:|---:|---:|
| `dickens` | 2,355,685 | 2,360,448 | 4,763 (0.20%) | 2,233,938 | +5.45% |
| `mr` | 2,249,704 | 2,365,814 | 116,110 (4.91%) | 2,119,994 | +6.12% |
| `nci` | 1,434,131 | 1,829,641 | **395,510 (21.62%)** | 1,366,367 | +4.96% |
| `osdb` | 2,368,404 | 2,495,870 | 127,466 (5.11%) | 2,261,858 | +4.71% |
| `reymont` | 1,024,711 | 1,156,716 | 132,005 (11.41%) | 980,463 | +4.51% |
| `webster` | 7,158,216 | 7,158,216 | 0 (0.00%) | 6,448,837 | **+11.00%** |
| `x-ray` | 3,798,464 | 4,056,779 | 258,315 (6.37%) | 3,657,087 | +3.87% |
| **total** | **20,389,315** | **21,423,484** | **1,034,169 (4.83%)** | **19,068,544** | **+6.93%** |

## What it means

1. **The per-block selector works.** BWT is chosen wherever it wins; removing it costs 4.83% over
   these seven files and 21.62% on `nci`.
2. **The BWT implementation is the gap.** ziptastic's BWT candidate is libbsc — BWT + QLFC. bzip3
   pairs the same transform with arithmetic coding over context models, and wins 3.87–11.00% on
   every file, including those where BWT carries the block.
3. **`webster` is the outlier.** BWT contributes exactly zero bytes there and the gap is the worst
   on the list (11.00%) — whatever owns its blocks is worth profiling next.

## Next, cheapest first

| # | experiment | cost |
|---|---|---|
| 1 | run libbsc output through the existing rANS/range stage — both coders are already in the tree | small |
| 2 | a bzip3-class BWT + arithmetic block format behind a new mode value | medium, format bump |
| 3 | profile `webster`'s chosen backends | small |

Do 1 before 2: if a second pass recovers most of the 7%, the transform is fine and only the coder
changes.

## Caveat

Seven files, chosen because they are the seven bzip3 wins. This is a targeted comparison, not a
corpus-wide effect: on the five files ziptastic already wins, BWT is not the deciding backend.
