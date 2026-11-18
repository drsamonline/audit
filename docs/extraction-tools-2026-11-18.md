# Eight extraction tools, read at source level

2026-11-18. Asked to check these deeply and not reject superficially. Each was cloned and its
source tree read — handlers, detector tables, dispatch logic, licences — rather than its README.

The fleet's constraint that decides most of this: **ziptastic links permissive-only** (LGPL at most,
via a plugin ABI), **heavenzip spawns processes** (much higher licence ceiling), and **the HCS vault
records a licence and a pin for everything it carries**. An unverified licence is a "do not use",
which is what happened to `parmar-main`.

| repo | what it is | licence | verdict |
|---|---|---|---|
| **magic-extractor** | Python + bundled Windows detectors; 21 format handlers, a 5-detector cascade, a PE-installer fallback list | **MIT** | **take: the handler interface and the fallback list** |
| **extractcode** | ScanCode's extraction library; libarchive + 7z, handler scoring, two-extractor fallback | **Apache-2.0** | **take: the scoring algorithm** |
| **bannsec/extractor** | 14 MIME-keyed handler modules, small and clean | **MIT** | **take: the MIME-dispatch shape, and the formats we lack** |
| **uniextract2** | AutoIt GUI over ~50 external extractors; a 19-file format→plugin map | **GPL-2.0** | **reference only** — spawnable by heavenzip, not linkable |
| **UniPyX** | 1,109 formats; **777 signature rules** in `lib/ddb.json` | **none found** | **cannot use** — no licence in the tree |
| **ZipXtract** | Android app; commons-compress + zip4j + 7-Zip-JBinding + libarchive | **GPL-3.0** | reference only — the library combination is evidence |
| **ComfyUI-Universal-Extractor** | ComfyUI node that extracts **AI-model metadata** (artists/tags), not archives | MIT | not applicable — it is not an archive extractor |
| **mixpeek-extractors** | Hosted multimodal extractors (Gemini embeddings) | MIT | not applicable — a SaaS cookbook, not file extraction |

---

## 1. magic-extractor — MIT, and the most directly reusable

`src/cli/` is a real program, not a wrapper script: 21 `format_*.py` handler modules under `formats/`, a detector
cascade in `detection.py`, and a PE fallback list that names the formats to try on an unrecognised
executable.

**The handler interface** (`formats/base_extractor.py`) is one class per format with
`detection_names()` — the strings a detector must produce to select it — and `extract()`. Two ideas
worth taking as they are:

- **`extract_atomically()`** stages into a per-attempt directory (`.mx_staging_*`) and moves on
  success. A failed extraction leaves nothing half-written. That is the failure mode heavenzip's
  multi-binary extraction has today.
- **`merge_move()` with the `--merge-output` contract**: the archive's version wins on collision,
  with an explicit `protect` set. Small, and it is the kind of decision that otherwise gets made
  silently per handler.

**The PE installer fallback list** (`detection.py`) is the single most useful constant in these eight
repos for us:

```
FormatRarHandler, FormatAceHandler, FormatArcHandler, FormatKgbHandler, FormatUharcHandler,
FormatInnoSetupHandler, FormatBitrockHandler, FormatCicdecHandler
```

An unknown `.exe` is the hardest case in extraction — self-extracting installers of a dozen formats,
all `application/octet-stream`. That list is somebody else's answer to "what do we try first", and
it is worth adopting as heavenzip's fallback order before we invent our own.

**The detector cascade**, cheapest first: `magic` → `puremagic` → `signatures` → `binwalk` →
`magika` → `DIE` (Detect It Easy). Bundled DIE signature databases live in
`src/cli/bin/detectors/die/db/Binary/*.sg` — a corpus of binary signatures, though in DIE's own
format and therefore only readable by DIE.

## 2. extractcode — Apache-2.0, and the algorithm worth copying

`src/extractcode/archive.py` has the piece no other repo here has: **a scoring function that ranks
extraction handlers instead of taking the first match**.

```
score  = handler.kind                 # higher kinds are more specific by design
score += 10 if type and mime and extension all matched
score += 8  if type matched
score += 6  if mime matched
score += 2  if extension matched
score -= 100 if extension matched ALONE
score += len(handler.extractors)      # prefer one-pass nested (tgz over gunzip-then-untar)
```

That `-100` is our own rule — *classification by content, never by extension* — implemented as a
scoring penalty rather than a sentence in a style guide. It is the cleanest expression of it I have
seen, and heavenzip's router should use the same shape.

Also here: `extract_with_fallback()` and `extract_twice()` — run a second extractor and compare,
rather than trusting one. That is the same instinct as the engine's accept/reject trials, applied to
extraction.

## 3. bannsec/extractor — MIT, small enough to read in full

14 handler modules, one per MIME type: `x_7z_compressed`, `x_arj`, `x_bzip2`, `x_compress`,
`x_cpio`, `x_lrzip`, `x_lzma`, `x_rar`, `x_tar`, `x_xz`, `x_zoo`, `zip`, `gzip`, `octet_stream`.
The dispatch is a MIME→module map, which is the simplest thing that works and is a good contrast to
extractcode's scoring: the same problem at two levels of sophistication.

Worth noting for coverage: **`x_zoo`, `x_cpio` and `x_lrzip`** are formats ziptastic does not reach.
`cpio` in particular is in every RPM and initramfs.

## 4. uniextract2 — GPL-2.0, reference only

AutoIt, 9,397 lines across four scripts, and it does not parse formats itself: it shells out. What is
worth reading:

- **The detection order** (`UniExtract.au3`): extension special-cases → PE scan for `.exe`/`.dll` →
  TrID → ExeInfo → then `CheckIso`, `CheckGame`, `CheckTotalObserver`, `CheckExt`, `check7z`. Note
  that it tries *structural* checks before falling back to the extension, in that order.
- **`def/*.ini`** — 19 plugin definitions in a tiny schema: `display`, `useCmd`, `executable`,
  `parameters`, `runInTempOutdir`, `workingdir`, `hide`, `log`, `patternSearch`, `initialShow`. That
  is almost exactly the shape heavenzip's profile files already use, which is a useful confirmation.

GPL-2.0 means: not linkable into ziptastic, and fine for heavenzip to spawn — but heavenzip would be
spawning the *tools*, not this GUI, so the practical value is the ordering and the ini schema.

## 5. UniPyX — the best data artifact here, and unusable

1,109 formats in `SUPPORTED.md`, and `lib/ddb.json` holds **777 signature rules**:

```json
{"rq": ["ARJZ", "ARJ"], "rs": "ARJZ", "s": 1}
{"rq": "MSP", "rs": "MSP", "s": 1}
{"rq": ["DLL file with 0000 Entry Point", "Resources Only", true], "rs": "Resource DLL", "s": 1}
```

`rq` required bytes/strings, `rs` resulting type, `s` start offset — with a `true` meaning "all of
these". Plus `dldb.json` (251 KB) of deeper rules. That is a ready-made content-detection table,
exactly what the fleet's "never by extension" rule needs.

**There is no licence anywhere in the tree** — no LICENSE, no COPYING, no licence field in any
packaging file, nothing in the README. Under the fleet's own rule that is a "do not use": the vault
records `parmar-main` as *"do not use — license is unverified"* for the same reason.

**So the action is not to take it; it is to ask.** A one-line licence statement from the author turns
777 rules from unusable to the most valuable artifact in this list. That is worth a message, and it
is cheaper than re-deriving the table from `file`'s magic database.

## 6. ZipXtract — GPL-3.0, but its dependency list is evidence

An Android app; 58 Kotlin files. What is worth having is `app/build.gradle`, which is a **working
answer to "which libraries cover which formats"**:

| library | covers |
|---|---|
| `org.apache.commons:commons-compress` + `org.tukaani:xz` | tar, cpio, ar, arj, zip, gzip, bzip2, xz, lzma, z, lz4, snappy |
| `net.lingala.zip4j` | zip with AES, split zips, zip64 |
| `7-Zip-JBinding` | 7z, rar, and the rest of the 7-Zip family |
| `me.zhanghai.android.libarchive` | the libarchive set |

Two useful facts fall out: libarchive alone does **not** cover 7z or RAR, which is why the app carries
three libraries; and zip4j is the one that handles **split zips**, which ziptastic has a design note
about (`SPLIT_ARCHIVES.md`).

## 7. ComfyUI-Universal-Extractor — not an archive extractor

18 MB, but 10 MB of it is `data/artists.json`. The node reads AI-model metadata files and serves
artist/tag libraries in ComfyUI; `py/nodes/extractor_node.py` resolves JSON library paths and polls
state. There is no archive parsing anywhere in it.

Rejected on the content, not the name: the word "extractor" here means "extract prompts and artist
metadata from generated images".

## 8. mixpeek-extractors — a SaaS cookbook

Twelve extractor packages (`image_extractor`, `audio_fingerprint_extractor`,
`universal_extractor`, …), each a thin wrapper that calls the Mixpeek API with Gemini embeddings.
MIT, but it is documentation for a hosted service: the "extraction" is a network call, and nothing in
it parses a container.

---

## What to do with this

| # | action | why |
|---|---|---|
| 1 | **Adopt magic-extractor's PE fallback order** in heavenzip's router | unknown `.exe` is the hardest extraction case, and this is a tested order |
| 2 | **Copy extractcode's scoring function shape**, including the `-100` for extension-only | it is our content-not-extension rule as executable arithmetic |
| 3 | **Take `extract_atomically` / staging-dir semantics** into heavenzip | a failed extraction currently leaves partial output |
| 4 | **Ask UniPyX's author for a licence** | 777 signature rules, one message away from usable |
| 5 | **Note cpio / zoo / lrzip as coverage gaps** in the recursion docs | cpio is in every RPM and initramfs, and the engine does not reach it |
| 6 | Nothing from ComfyUI-Universal-Extractor or mixpeek | neither parses a container |

Nothing here is vendored yet, and nothing should be until the vault records a pin and a licence for
it — which for magic-extractor (MIT) and extractcode (Apache-2.0) is straightforward, and for UniPyX
is not possible today.
