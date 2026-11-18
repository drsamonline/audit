# ziptastic — PNG: the pixels, not the deltas; and three numbers that corrected themselves

Date: 2026-11-18 · Repos `drsamonline/ziptastic`, `audit` · PRs #31–#40, issues 0

Continues `2026-11-17-ziptastic-wav-and-release-1.4.3.md`. The plan's A1 was "re-choose the PNG
per-row filter" — the optipng/ECT objective, a smaller *deflate* stream.

## What the measurement said instead

| image | filtered (as stored) | true pixels + filter map | change |
|---|---|---|---|
| 1,280×900 UI screenshot | 60,678 | **44,694** | **−26.3%** |
| 320×320 photograph as PNG | **65,152** | 97,556 | **+49.7%** |

Both directions, by a lot. A context-mixing model predicts a screenshot's rows once the deltas
are gone; a photograph's deltas are already small and *are* what compresses. So A1 was redefined
from "search filters" to **choose per file by measurement** — and shipped as #34, with the
payload carrying a version marker so older archives still decode.

End to end, `-9`, `docs/shot.png`: **67,217 → 51,822 bytes (−22.9%)**, byte-exact. A photograph
is unchanged at 70,308 because the trial keeps the filtered form for it.

## The trial cost, and what fixed it

Two payloads are built and compared. The comparison first coded both 3.4 MB payloads in full
(25 s of a 44 s run). A 256 KiB sample of the whole payload resolved it correctly; **64 KiB of
the whole payload chose wrong**.

The fix was the one `PRECOMP_GATE.md` already prescribed — compare the actual encodings on a
sample — applied where the candidates differ: `png_pixel_span()` finds the stored pixel stream,
and 64 KiB is sampled from *inside* it. Interleaved with 1.4.3, three runs each:

| build | bytes | runs |
|---|---|---|
| 1.4.3 | 67,217 | 20.5, 20.5, 23.7 s |
| now | **51,822** | 18.8, 19.1, 19.9 s |

Every new run beat every old one. The lesson is the sample's **location**, not its size.

## Three numbers that corrected themselves

1. **64 KiB chose wrong** — the same ~6% error `FINDINGS` §3g records for a 64 KiB sample.
   Re-learned by measurement because §3 was not read first.
2. **The timing claim.** #39 recorded "17.4 s"; re-checking minutes later gave 20.8 s. The docs
   now carry the interleaved spread, not a favourable pair (#40).
3. **The `--no-parse --no-lzma2` collapse** (92,930 bytes on a 92,822-byte input) is the framing
   overhead, measured at exactly 108 bytes on `/dev/urandom` — the engine storing the file, not
   a regression.

## Docs audited, all 71 of them

Three of the four things "discovered" this week were already written down: the 64 KiB error
(§3g), why oxipng does not transfer (§3), and the better gate as the known fix
(`PRECOMP_GATE.md`). Fixed: §2's PNG row, §3's oxipng row, a new §6i, `PRECOMP_GATE.md`'s
"not attempted", `PNG_NESTED.md`'s pre-change numbers, and `SESSION_HANDOFF.md` (format v5 → v8,
28 → 37 suites, "heavenzip: docs only" → shipped).

## What is left

The measured frontier has no point that is fast *and* small: `--no-precomp` is 0.5 s and +67%
size, the default is 17–20 s, and `--no-parse` is the only middle (+2.1% for −27%). Speed needs
a fast deflate re-encode of the IDAT — S1 — which is a second code path.
