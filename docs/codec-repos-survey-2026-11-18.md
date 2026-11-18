# Fifty codec and archive repositories, checked against this project

2026-11-18. Every repo queried for licence, stars and last push; the ones that could change a
decision were read. Findings are ordered by what they mean for **CHCE first**, then lexora and kosh.

Method note: stars and dates are from the GitHub API on this date; the DwarFS numbers are its own
README's claims, not my measurements.

---

## The three that change a decision

### 1. liblz4 **1.11.0** exists — and we vendor 1.10.1

`lzbench`'s bundled-version table lists **lz4/lz4hc/lz4frame v1.11.0, updated 2026-11-04**. The
fleet's LZ4 transform is built against **1.10.1**, and its open question was whether to widen support
to 1.9.4 frames.

That question just got bigger. There are now **at least three matcher generations** in the wild
(≤1.9.4, 1.10.x, 1.11.x), and our transform reproduces exactly one of them. The decision the owner
was holding — "widen to 1.9.4 or not" — is now "which single version do we match, and do we track
upstream as it moves".

**Recommendation:** before widening backwards, check whether **1.11.0 changed the matcher again**.
If it did, a transform pinned to 1.10.1 is already stale for newly produced frames, and the more
valuable move is forward-tracking, not backward.

### 2. c-blosc2 — BSD, and it is the column-encoding layer as a library

Blosc2 describes itself as "a flexible framework of **codecs and filters**", where the filters are
shuffle, bitshuffle and delta applied **before** the codec. That is precisely the ClickHouse
two-stage stack from the earlier survey, shipped as a C library under a **BSD** licence.

Plan item 6 is "a column-aware encoding under the SQLite transform (delta / RLE /
frame-of-reference)". Writing that by hand is a week; Blosc2's filter set is the delta and shuffle
half of it already, and BSD means it can be linked.

**Recommendation:** read Blosc2's filter implementations before designing the SQLite column
transform. Not necessarily to link it — the CHCE format wants its own byte-exact inverse — but the
filter design and its measured effect on numeric data are exactly the reference we lack.

### 3. DwarFS — the closest thing to what ziptastic is trying to be

A read-only filesystem, **MIT and GPL-3.0 mixed**, 2.6k stars, active. Its distinct features, in its
own words:

- **clustering of files by similarity using a similarity hash** — exploits redundancy *across* file
  boundaries;
- **segmentation analysis** across filesystem blocks;
- a **categorisation framework** that processes categories differently — "not waste time trying to
  compress incompressible files", or "compress PCM audio data using FLAC compression".

That last one is ziptastic's entire Layer 0 dispatch, arrived at independently, plus a similarity
hash we do not have. Its README's comparison on 1139 Perl installations (47.49 GiB):

| | compressed | ratio |
|---|---|---|
| `.tar.zst` (long mode, ultra 22) | 0.387 GiB | 122.7 |
| **DwarFS (lzma)** | **0.310 GiB** | **153.2** |
| 7zip `-mx=7` | 1.219 GiB | 38.96 |

**Recommendation:** the similarity hash is the idea worth taking — ziptastic compresses one file at a
time and cannot see that a corpus is 1139 near-copies of the same tree. That is a **heavenzip-level**
feature (it sees the whole directory), and DwarFS is prior art for it. Licence is mixed MIT/GPL-3.0,
so read it, do not link it.

---

## The harness we should be using

**`inikep/lzbench`** compiles every supported compressor into one binary, so all of them are built
with the same compiler and flags — the fair comparison the fleet has never done. It already bundles
**brotli 1.2.0, bzip3 1.5.4, libdeflate 1.26, lizard 2.1, lzham 1.0, lz4 1.11.0** and dozens more.

```
lzbench -eALL -t8,8 -o1c4 silesia.tar
```

**Caveat that matters here:** it is built with `make`, which this sandbox does not have — the same
blocker as the OpenZL build. Both need one environment change, not two projects.

---

## What the vault already carries, and what it does not

Of the fifty, **twelve are already tracked in `HCS/SOURCES`**: zstd, lz4, brotli, snappy, zlib,
libdeflate, zopfli, xz, bzip3, lizard, lzham, zpaq.

**Not tracked, and worth considering:**

| repo | licence | why it might matter |
|---|---|---|
| **c-blosc2** | **BSD** | the filter layer for plan item 6 |
| **lrzip** | GPL-2.0 | long-range matching — the thing ziptastic's fixed block size cannot do on large files |
| **libarchive** | BSD-2 | the canonical multi-format reader; the format-coverage reference for kosh |
| **7zip** | LGPL-2.1 + unRAR restriction | the reference implementation for the formats heavenzip shells out to |
| **bzip2** | (untracked) | tracked upstream copy exists (`libarchive/bzip2`) but the vault has no entry |

---

## Corrections to the list as given

Two of the fifty **do not exist**:

- `ncruces/go-zstd` → 404
- `ncruces/go-brotli` → 404

And one is under a different owner: **`facebook/zstd-jni` → `luben/zstd-jni`** (BSD-2-Clause, 1,080
stars, active).

---

## The rest, briefly

| repo | verdict |
|---|---|
| `mholt/archiver` | **archived** (MIT, 4.4k stars) — superseded by its own v4; not a source to adopt |
| `sharpcompress` | MIT, active — the C# archive library; no fit here |
| `sanjay7178/filecompressor` | MIT, 0 stars, one-person — not a reference |
| `espadrine/compressor-benchmark` | no licence, last push 2019 — do not use |
| `ning/jvm-compressor-benchmark` | no licence file — the JVM benchmark; no fit |
| `sfu-compbio/compression-benchmark-tools` | no licence, 2016 — dead |
| `mbhall88/compression_benchmark` | MIT, FASTQ-specific — already assessed, no fit |
| `MartinEesmaa/awesome-compopt` | **CC-BY-4.0**, a curated list — a good source of *ideas*, not code |
| `jermp/data_compression_course` | no licence, educational — useful reading on techniques |
| `klauspost/compress`, `pierrec/lz4`, `golang/snappy`, `ulikunitz/xz`, `dsnet/compress` | Go implementations, permissive — no fit for a C++ engine; relevant only if a Go component ever appears |
| `airlift/aircompressor`, `commons-compress`, `hadoop`, `parquet-java`, `arrow`, `avro`, `kafka`, `orc` | Java/Apache — no fit; `parquet`/`orc`/`arrow` are columnar formats worth remembering for the *SQLite column* idea, not for code |
| `python-zstandard` | **BSD-3, and it is lexora's actual dependency** — confirmed current |
| `python-lz4`, `snappy-java`, `lz4-java`, `zstd-jni` | bindings — no fit |
| `Blosc/c-blosc`, `python-blosc`, `python-blosc2` | the Blosc1 line and Python wrappers; **c-blosc2 is the one that matters** |
| `google/zopfli` | Apache-2.0, tracked — already measured and rejected for the PNG fast form |
| `libarchive/bzip2` | the maintained bzip2 mirror, 2022 — the vault has no bzip2 entry at all |

---

## What I would do with this

1. **Check whether liblz4 1.11.0 changed the matcher** — it decides the LZ4 transform's future, and
   it is a ten-minute check once a compiler exists.
2. **Read Blosc2's filters** before designing the SQLite column transform (plan item 6).
3. **Read DwarFS's similarity hashing** as prior art for a corpus-level feature in heavenzip.
4. **Install `make`** — it unblocks OpenZL, lzbench, and any future build, all at once.
