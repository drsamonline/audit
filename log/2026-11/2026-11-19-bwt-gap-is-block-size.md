# The BWT gap is the block size, not the coder

Date: 2026-11-19 · Repos `drsamonline/ziptastic`, `audit` · ziptastic PR #64 · probes in `2026-11-19-probes/`

Follows `2026-11-19-bwt-backend-measured.md`, which proposed three experiments and said do the
cheap one first: push libbsc output through the rANS/range stage. Done. **It cannot work, twice
over** — and the experiment that does work was not on the list.

## The coder hypothesis, refuted twice

| test | result |
|---|---|
| residual redundancy in libbsc output | **none** — zstd -22 adds 22 bytes to 374,656 (`xml`), 73 to 2,565,414 (`ooffice`) |
| a stronger coder on the same BWT | **worse than QLFC** — xz -9e +17.70% / zstd -22 +25.67% on `xml`; +8.32% / +14.82% on `ooffice` |

A second pass has nothing to find; replacing QLFC makes it bigger. The coder was never the gap, and
the bzip3-class block format the previous entry proposed would have bought almost nothing.

## The block size, which is the gap

ziptastic's default block is **4 MiB**. bzip3's is far larger, and BWT is a whole-block transform.
`-9` at the default against `-9 -b 16384`, seven text files, every archive byte-verified:

| file | `-9` (4 MiB) | `-9` (16 MiB) | change | bzip3 -10 | 16 MiB vs bzip3 |
|---|---:|---:|---:|---:|---:|
| `dickens` | 2,355,685 | 2,260,672 | −4.03% | 2,233,938 | +1.20% |
| `mr` | 2,249,704 | 2,205,432 | −1.97% | 2,119,994 | +4.03% |
| `nci` | 1,434,131 | 1,280,531 | **−10.71%** | 1,366,367 | **−6.28%** |
| `osdb` | 2,368,404 | 2,247,164 | −5.12% | 2,261,858 | **−0.65%** |
| `reymont` | 1,024,711 | 982,707 | −4.10% | 980,463 | +0.23% |
| `webster` | 7,158,216 | 6,785,793 | −5.20% | 6,448,837 | +5.23% |
| `x-ray` | 3,798,464 | 3,756,678 | −1.10% | 3,657,087 | +2.72% |
| **total** | **20,389,315** | **19,518,977** | **−4.27%** | **19,068,544** | **+2.36%** |

Gap to bzip3: **+6.93% → +2.36%**. ziptastic now beats bzip3 on `nci` (−6.28%) and `osdb`
(−0.65%). Cost: **+19% time** (470 s against 395 s).

## Why this matters beyond the number

- **A default is a claim.** 4 MiB has been the block size since the format was written, and no
  document justified it. It costs 4.27% on text against 16 MiB. Same defect class as a README claim
  nobody measured.
- **Two experiments were spent on the wrong hypothesis.** "The coder is weaker" was plausible, was
  written down as the next step, and is false. What settled it was a 60-line probe against the
  vendored libbsc, not another argument.
- **`webster` remains the outlier**: 5.20% better at 16 MiB, still 5.23% behind bzip3, and the one
  file where the BWT candidate is never selected at 4 MiB.

## Next

1. Full Silesia at 4 / 8 / 16 / 32 MiB, all 12 files — one table decides the default. Text gains
   4.27%; binary and container files may not, and the time cost is +19%.
2. Then either move the default or document `-b` as the ratio lever.
3. Re-run the `PARETO.md` frontier with block size as a third axis — it is a ratio/time dial the
   frontier does not currently show.

## Probe harnesses

`2026-11-19-probes/probe_bwt.cpp` reproduces the engine's exact libbsc settings (BWT + adaptive
QLFC, no LZP, 4 MiB blocks, block size as an optional third argument);
`2026-11-19-probes/probe_bwt2.cpp` emits the BWT transform alone so an external coder can be
measured on the same bytes.
