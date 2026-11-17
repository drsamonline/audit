# Plan review — 2026-11-17

Checked against `analysis-validation` (the four rounds) and filled against upstream.
The plan is the "Next" table in `handoff-2026-11-17.md`; this is the critique of it, not
a replacement for the fleet state.

## Round 1 — logic

| plan item | the claim it rests on | verdict |
|---|---|---|
| 1. PNG: 22.4% for 25 s | measured on one file, one thread | **holds, and is now decomposed** (#31). But it is a *trade*, not a defect — the plan called it a product decision and that is right |
| 2b. `--no-bwt` never wins, `--no-lzma2` saves 7% | one file | **weak** — one file cannot say "never". Reword to "on inflated pixels in one screenshot", or measure a second |
| 2. `check-sources.py` cannot see a broken copied tree | one incident (brunsli) | **holds**; the incident is the evidence |
| 3. Real PDF with embedded JPEGs | none — the fixture is synthetic | **holds**, and it is the only item that is pure gap |
| 4. lexora / kosh | untouched for four sessions | **holds**; no claim, just neglect |

Nothing in the table was stated as cause when it was correlation. Two items overreach on
n=1 and are reworded below.

## Round 2 — data handling

- **Same grain throughout?** Yes for the engine numbers (bytes in, bytes out, one thread),
  but the PNG claim compares a 93 KB file to a "24.5 s" figure measured in `heavenzip`
  (sweep) and a "25.7 s" figure measured in `ziptastic` (direct). Two harnesses, 5% apart.
  Not a problem, but the doc should say which harness each number came from.
- **Missing:** there is no second PNG in the fleet's reach. Every PNG claim is one file,
  one screenshot. That is the plan's real gap, not the PDF.

## Round 3 — uncertainty

Every number in the handoff carries n and a window except the two PNG claims, which carry
a file but not a corpus. Fix: name the file and say "one screenshot".

## Round 4 — cross-result

Cross-checked the PNG claim against a second harness (the sweep) and against upstream
benchmarks (below). The engine's 22.4% is inside the range lossless PNG optimisers report,
so the claim is not an outlier. It is **not** a head-to-head: different corpora, different
metrics (percent of one file vs megabytes saved across 30 image sets).

## Gaps filled from upstream

What the field actually does for lossless PNG, and where this engine sits:

| upstream fact | consequence for the plan |
|---|---|
| **oxipng** is "the usual choice: multithreaded, fast"; `oxipng -ao6` + `ect` is the strongest pairing measured — 67.05 MB saved in 483 s, against oxipng alone 66.14 MB in 255 s | the fast path in the field is **filter-strategy search + a zopfli-class deflate**, not a context-mixing model. Our 25 s buys a comparable ratio by a much slower route |
| **ECT** is a modified zopfli, "about 3× faster than Zopfli and now also has more compression"; `ect -9` recompresses IDAT in 257 s **for a whole corpus of 30 image sets** | our 25 s is for **one** 93 KB file. On time-per-byte we are one to two orders of magnitude behind the field's fast tools |
| oxipng's advantage over ECT is attributed to **better reductions and filter strategies**, not to the deflate | the ratio gap we could still close is **filter choice**, which we do not touch: `png_wrap` inflates the filters the file already chose |
| ECT multithreads (`--mt-file`, ~40% on 4 cores) | we measured `-9 --parallel -T 2` on the PNG: **30.2 s, same bytes**. No gain — the inflated payload is one block, so there is nothing to spread |

## Two measurements that change the plan

Made while checking the above, both on `docs/shot.png`:

| run | bytes | time |
|---|---|---|
| `-9` | 67,217 | 29.4 s |
| `-9 --parallel -T 2` | 67,217 | 30.2 s |
| `-9 --parallel -T 2 -b 256` | 74,478 | 23.6 s |

1. **Parallelism does not help the PNG path.** The 3.4 MB payload fits one block, so the
   work is single-threaded however many cores are offered. Anything that promises speed
   from threads here is wrong until blocks are split, and splitting costs ratio.
2. **Smaller blocks buy 20% time for 10.8% size.** That is a worse trade than the two
   existing knobs, so it does not belong in a default — it belongs in the record.

## The plan, re-ordered for speed and accuracy

Two axes, kept apart because they trade against each other.

**Accuracy (ratio), highest value first:**

| # | item | why it beats the current list |
|---|---|---|
| A1 | **PNG filter-strategy search** — re-choose the per-row filter before compressing, instead of compressing the filters the file already had | upstream's measured ratio advantage comes from here, not from the deflate; it is the one accuracy gap we can name |
| A2 | A real PDF with embedded JPEGs | closes the only pure gap; brunsli is untested on PDF-embedded JPEGs |
| A3 | Second PNG and a second screenshot class (photo-ish vs UI) | every PNG claim is n=1; two more files make the plan's numbers defensible |

**Speed, highest value first:**

| # | item | why |
|---|---|---|
| S1 | A **fast PNG mode**: skip the CM pass, recompress IDAT with a stronger deflate and a filter search | this is what the field does for speed; it is a different code path, not a flag on the current one |
| S2 | Do not promise threads for PNG until blocks are split | measured: `--parallel` is a no-op here, and the block split that would enable it costs 10.8% |

**Housekeeping, unchanged:** `check-sources.py` compile check; lexora / kosh.

## What this review changes in the plan

- Item 1 stays but is **reworded as a trade with a named file**, not a defect.
- Item 2b is **downgraded to n=1** until a second file is measured.
- **New A1** (filter search) leads the accuracy list: it is the one gap upstream names
  explicitly, and we do not touch filters at all.
- **New S1** (a fast deflate path) replaces "make the PNG path faster", which the
  measurements show is not a matter of turning a knob.
- **A3** added because every PNG number in the fleet is one file.
