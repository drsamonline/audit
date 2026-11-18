# Thirty-two compression links, triaged

2026-11-18. Every link opened or classified by source and content. Six have something the fleet can
use; the rest are background, tutorials, vendor pages or noise. One (the Facebook engineering post)
could not be fetched — the site refuses automated requests — so its subject was read from
`openzl.org` and the `facebook/openzl` repository instead.

## The six worth acting on

### 1. OpenZL — BSD, and the same thesis as Layer 0

`facebook/openzl`, BSD-licensed, used in production at Meta. It builds a **specialised compressor
from a description of the data**, and ships **one universal decompressor that decodes anything the
compressor produced, whatever graph it used**.

That is ziptastic's architecture arrived at independently: parse the container, split it into
homogeneous streams, transform each, store a recipe, and let one decoder read any recipe. The
differences are the interesting part:

| | OpenZL | ziptastic |
|---|---|---|
| how a format is described | **Simple Data Description Language** — a declarative syntax that splits input into streams | hand-written C++ per format (`png_wrap`, `sqlite_wrap`, …) |
| codec choice | a DAG of primitive codecs, with **user-defined control flow that can change the DAG mid-compression** based on the data | fixed stage order, one gate per stage |
| decoder | one universal decoder, graph-independent | one decoder, driven by the layer bits |
| licence | BSD | own |

Three things to take, in order of cost:

1. **The idea of a declarative split description.** Every new format here costs a C++ transform.
   If a format's split can be *described* rather than coded, the marginal format gets much cheaper.
   Not a rewrite — a study of whether their SDL covers what `png_wrap` and `sqlite_wrap` do by hand.
2. **Control flow inside the graph**, not just at stage boundaries. ziptastic decides "unfilter or
   not" *before* the encode, by a trial; OpenZL can branch mid-DAG on the data.
3. **It is a fair external yardstick.** A BSD, production, format-aware compressor is the honest
   comparison for "is our Layer 0 actually good", and the fleet has never benchmarked against one.

### 2. ClickHouse's two-stage stack — the transform ziptastic is missing

The article's core claim: columnar engines stack a **column-aware encoding** (dictionary, RLE, delta,
delta-of-delta, Gorilla, frame-of-reference) *under* a general-purpose codec, and get 5–10× where
row-based engines get 1.5–3×. Both stages are needed — "encodings know patterns codecs cannot see,
and codecs catch entropy encodings leave behind".

ziptastic's SQLite transform does stage one only in the weakest sense: it **groups pages by B-tree
kind** (measured 27.8% on a 6.9 MB indexed database) and then hands the bytes to the block loop. It
does not delta-encode integers, does not run-length encode repeated values, does not dictionary-code
strings. That is a named, measured, unexplored transform with an external taxonomy to work from.

### 3. The 2026 AIT Data Compression Challenge — the methodology the fleet keeps relearning

117 submitted compressors, sixteen heterogeneous files, **public training set and hidden test set**,
ranked on ratio, speed, **Weissman score** and a **Pareto frontier**.

Two things worth copying, and one worth noting:

- **The Pareto frontier as the headline, not a single number.** This is what the PNG frontier table
  arrived at by hand today (51,822 at 17 s · 62,618 at 1.3 s · 86,626 at 0.5 s). Reporting a ratio
  without its speed is reporting half a result.
- **A hidden test set.** Every single-fixture mistake this week — the 64 KiB sample, the formula
  PNG, the gzip XML decline, the LZ4 synthetic frame — was the same failure: measuring on the files
  I chose. Their answer is a split nobody optimises against.
- Note: their finding that "no single compressor dominates across all criteria" is the same
  conclusion, from 117 entrants.

### 4. lzbench-web — where ziptastic actually sits

36 datasets × 40 codecs × every level = 7,200 datapoints, and a decomposition worth keeping: **a
compressor is an algorithm, an archive format, and an implementation** — the same three-way split
ziptastic makes between its block codec, the CHCE container and its CLI.

Its speed tiers are a useful, unflattering yardstick:

| tier | throughput | algorithms |
|---|---|---|
| fast | ~1 GB/s | lzo, lz4, snappy |
| medium | 10–500 MB/s | deflate, zstd |
| slow | 0–10 MB/s | lzma, bzip2, brotli |

ziptastic's measured 0.3–0.6 MB/s is **below the slow tier** — two orders of magnitude under
brotli's floor. The ratio buys that, and `--png-fast` (62,618 bytes in 1.3 s) is the first attempt to
offer anything above it. Worth stating plainly in the README rather than leaving a reader to find it.

### 5. Matt Mahoney's Large Text Compression Benchmark — the CM reference

enwik9, ranked by compressed size **plus the decompressor's own size**. Still updated (Nov 2026). It
is the canonical table for context-mixing compressors, which is what ziptastic's `--max-ratio` path
is. If the CM backend is ever compared to anything, this is the table, and the decompressor-size rule
is a discipline worth adopting: a 4 MB binary is not free when you are comparing 1 GB outputs.

### 6. "Data Compression with a Time Limit" (Carpentieri, Algorithms 2025)

The problem: given a **time budget** and a set of files, assign files to compressors so the budget is
used well. Their result is that an optimised assignment eliminates idle time versus a fixed choice.

That is heavenzip's orchestration problem stated formally. heavenzip currently picks a profile per
file from its config; this is the scheduling layer above it — *which* profile for *this* file given
how long we have. The paper is about images and lossy codecs, so the transfer is the framework, not
the numbers.

## The rest, classified

| # | link | what it is | verdict |
|---|---|---|---|
| 8 | PeaZip maximum compression benchmark | 303 MB corpus, 7z/zpaq/RAR at max settings: zpaq 19.01%, 7z 23.50%, RAR 25.78% | **useful reference numbers** for any ziptastic claim against those tools |
| 24 | SPEC CPU 2026 801.xz_s | xz 5.8.1 as a CPU benchmark: in-memory, no I/O, SHA-512 verification of the round trip, buffer and level as parameters | **methodology** — the verification shape is the one the fleet already uses |
| 26 | go-compression-benchmark results | per-library ratio/time/memory, pure Go | corroborates the tiers; no action |
| 3 | mbhall88/compression_benchmark | FASTQ-specific, MIT, mature-tool-only | niche; no action |
| 18 | Gregory Szorc, "Better Compression with Zstandard" (2017) | Mercurial's zlib→zstd migration: clone 1184 MB → 1052 MB, 60% of the CPU | historical; the argument is settled |
| 14 | code.kx.com file compression | kdb+ on-disk compression | niche columnar reference |
| 13, 16, 17, 22, 31 | journal/ACM/MDPI papers | 22 read (item 6 above); 16, 17, 31 not opened — ACM and a university PDF, titles not compression-strategy material | low priority |
| 1, 2, 6, 11, 15, 19, 28 | scribd, dev.to ×4, medium, wearecommunity, speedvitals | tutorials and blog comparisons | background only |
| 7, 12, 20, 30 | reddit, HN, quora, superuser | discussions | noise |
| 25, 32 | fast.io listicle, cast-inc whitepaper | vendor marketing | noise |
| 27 | researchgate | the same AIT challenge paper as #23 | duplicate |

## What to do

| # | action | effort |
|---|---|---|
| 1 | **Study OpenZL's SDL** against `png_wrap`/`sqlite_wrap`: is a declarative split description feasible, and what would it save per new format? | medium |
| 2 | **Benchmark against OpenZL** on the fleet's own corpus — the first external, BSD, format-aware comparison | small |
| 3 | **A column-aware encoding under the SQLite transform** (delta / RLE / frame-of-reference), per the ClickHouse taxonomy | medium |
| 4 | **Report the Pareto frontier, not single numbers**, in BENCHMARKS.md — and add a hidden test set so measurements stop being on chosen files | small |
| 5 | State ziptastic's throughput tier honestly in the README (0.3–0.6 MB/s, below brotli's floor) | trivial |
| 6 | Read Carpentieri's scheduling framework for heavenzip's profile choice under a time budget | small |
