# `webster` profiled — PPMd owns it, and the knobs are dead ends

Date: 2026-11-19 · Repos `drsamonline/ziptastic`, `audit` · ziptastic PR #70

The worst remaining gap to bzip3 sits on one file, and it is the file where the BWT candidate never
fires. Two turns of measurement had left "why" as an open question; it is now a closed one.

## The profile

`-9` at the 4 MiB default: **10 of 10 blocks are PPMD**, archive 7,158,216. BWT contributes exactly
zero (`-9` and `-9 --no-bwt` are byte-identical), and BWT *alone* is worth **7,259,207** — measured
for free when a worse PPMd made the selector fall back to it. So BWT is 1.4% behind PPMd on this
content, not ahead.

## Both knobs, measured

| variant | webster @4 MiB | vs default | blocks chosen |
|---|---:|---:|---|
| order 6, 16 MiB (default) | **7,158,216** | — | 10 × PPMD |
| order **8**, 16 MiB | 7,259,207 | **+1.41% worse** | 10 × BWT |
| order 6, **128 MiB** | 7,158,216 | **identical** | 10 × PPMD |

Order 8 dilutes the statistics, so PPMd loses to BWT on every block and the archive is worse than the
order-6 result it replaced. A 128 MiB model is byte-identical to 16 MiB — the model is not the
constraint on a 4 MiB block.

That retires a stale comment: `ppmd.cpp` says "16 MiB of model, ample for 256 KiB blocks", written
when blocks were 256 KiB and never revisited when the default moved to 4 MiB. The comment is out of
date; the constant, measured, is not wrong.

## Why the gap survives

| at | ziptastic | bzip3 -10 | gap |
|---|---:|---:|---:|
| 4 MiB | 7,158,216 | 6,448,837 | +11.0% |
| 16 MiB | 6,785,793 | 6,448,837 | +5.23% |
| 32 MiB | 6,605,132 | 6,448,837 | +2.42% |

bzip3 pairs BWT with **arithmetic coding over context models**; ziptastic's BWT is libbsc (BWT +
QLFC) and loses to its own PPMd here. Re-coding libbsc's BWT output with a general-purpose coder is
already measured **worse** than QLFC (`2026-11-19-block-size-at-scale.md`: xz +17.70%, zstd +25.67%
on the same transform), so the entropy stage is not the constraint either.

## Decision

Closing this means implementing **bzip3's coder family** — a new backend and a format change — for
2.42% on one file of twelve. Recorded as not worth it, so the question is not reopened as a tuning
problem. If a second file ever shows the same shape (PPMd-owned, BWT never fires, bzip3 ahead), that
is a content class rather than one file, and a class is worth a backend.

## Note on the sandbox

The order-8 build and measurement exceeded one 290-second call and had to be split; the rebuild after
restoring the defaults was three targets and 20 seconds. Nothing was lost — the CSV-free, one-shot
nature of these runs is why.
