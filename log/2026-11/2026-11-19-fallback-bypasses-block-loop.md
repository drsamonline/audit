# The two files that did not move never entered the block loop

Date: 2026-11-19 · Repos `drsamonline/ziptastic`, `audit` · ziptastic PR #67

`2026-11-19-block-size-at-scale.md` left one caveat: `samba` and `sao` were byte-identical at 4 and
16 MiB blocks, "worth a look before trusting the non-text group's +0.31%". Looked, and the answer
was in the archive header.

## They are one whole-stream LZMA2 block

```
$ ziptastic info samba.dr
blocks         1
  0    0x00000016 3737067    21603255   LZMA2_FALLBACK
```

Identical at `-b 4096` and `-b 16384`. The Tier-1 fallback (`FINDINGS.md` §3f) is a whole-stream
LZMA2 pass, not a per-block candidate: when it wins, the block loop's output is discarded and `-b`
has nothing to act on. `sao` is the same, one block, 4,415,013.

## And the fallback was right

Native path (fallback removed), against what shipped:

| file | native 4 MiB | native 16 MiB | fallback | better by |
|---|---:|---:|---:|---:|
| `samba` | 4,009,686 | 3,991,578 | **3,737,179** | 6.4% / 6.8% |
| `sao` | 4,676,756 | 4,679,858 | **4,415,125** | 5.6% / 5.7% |

Bigger blocks move `samba`'s native path 0.45% and `sao`'s 0.07% — and both stay 5–7% behind the
fallback. There is no hidden win, and this is why `HARNESS_MEASURED.md` shows ziptastic within
0.25% of `xz -9e` on both files: on them it *is* an LZMA-class compressor.

## Correction to the previous entry's table

| group | 4 MiB | 16 MiB | change |
|---|---:|---:|---:|
| `samba`, `sao` — fallback, block size inapplicable | 8,152,304 | 8,152,304 | 0.00% |
| `ooffice`, `xml` — block loop | 2,506,387 | 2,538,927 | **+1.30%** |
| non-text as previously reported | 10,658,691 | 10,691,231 | +0.31% |

16 MiB costs **1.30%** on the two non-text files that can respond and nothing on the two that
cannot. The corpus total (−2.70%) is unchanged; the shape of the trade is now honest.

## Trap added to the list

**A corpus table that mixes fallback files with block-loop files measures two different machines.**
One number per file hides which one ran. When a cell does not move, check whether the feature was
reached at all before concluding it did not help — `ziptastic info` prints the mode per block, and
that one command answered a caveat that would otherwise have been re-investigated.

## Still open

- `mozilla` (51 MB) whole-file at any block size — `-9` does not finish in a 300-second step; every
  table in this thread carries it as two halves or not at all.
- 32 MiB measured (−2.66% webster, −5.59% nci against 16 MiB) but not shipped: the population of
  files that can hold a 32 MiB block is three, and one of them is `mozilla`.
