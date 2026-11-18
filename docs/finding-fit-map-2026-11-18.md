# Which finding fits which repo

2026-11-18. Two link sets were triaged — 32 compression references and 20 PDF/EPUB extraction
references — across 152 repositories on this account. This maps each finding to the repos it
actually fits, **CHCE first**, and says plainly where it does not fit at all.

How this was checked: all 152 repo descriptions were read; the repos whose descriptions suggested
they touch the same file types were opened (`corpus-extendum`, `All4ONE`, `app-image-toolkit`,
plus the six already in hand). Where a fit is inferred from a description rather than from reading
the code, it says so.

---

# Part 1 — CHCE, in priority order

## ziptastic — the engine

| finding | what it changes | effort |
|---|---|---|
| **OpenZL** (BSD, format-aware, no canonicaliser) | the first *external* yardstick Layer 0 has ever faced. Same thesis — parse, split, transform, store a recipe, one universal decoder — arrived at independently at Meta, in production | benchmark: small |
| **OpenZL's SDL** | every new format here costs hand-written C++. Theirs costs a *description*. Study whether a declarative split covers what `png_wrap` and `sqlite_wrap` do by hand | medium |
| **ClickHouse column encodings** | the SQLite transform groups pages by B-tree kind and stops. Delta / RLE / frame-of-reference under the block loop is a named, unexplored transform with an external taxonomy | medium |
| **AIT challenge methodology** | report the **Pareto frontier**, not one number; and a **hidden test set**, because every single-fixture mistake this week (64 KiB sample, formula PNG, gzip XML, synthetic LZ4) was measuring on files I chose | small |
| **lzbench tiers** | 0.3–0.6 MB/s sits *below* brotli's slow-tier floor of 10 MB/s. The README should say so rather than let a reader find it | trivial |

## heavenzip — the orchestrator

| finding | what it changes | effort |
|---|---|---|
| ~~magic-extractor's PE fallback order~~ | **withdrawn 2026-11-18.** heavenzip does not extract third-party archives: its commands are `validate`, `detect`, `compress`, `decompress`, `bench`. A self-extracting installer is not something it opens. The list belongs where unknown files are inspected — see kosh below |
| ~~extractcode's handler scoring~~ | **withdrawn 2026-11-18.** heavenzip has no multi-detector evidence to score: `matches()` is one boolean class gate and the profile is named by the user or the default. Porting the formula would invent inputs it does not have |
| ~~`extract_atomically`~~ | **already largely present**: intermediates are written as `<output>.<step>.tmp` and a failed run keeps its logs and manifest |
| **Carpentieri, "Data Compression with a Time Limit"** | the one that does fit: choosing a profile *under a budget* is the scheduling layer above the per-file pick. A design item, not a port | medium |

## HCS — the vault

| finding | what it changes |
|---|---|
| **OpenZL** (BSD) | a legitimate vault source: a format-aware compression framework with a universal decoder. Pin + licence + integration `external-process` or `reference` |
| **docling** (MIT) | a vault source for document extraction; MIT, so also linkable |
| ~~MinerU~~ | **rejected 2026-11-18.** Its licence is Apache-2.0 *plus* terms: a separate commercial licence is required above 100M MAU or USD 20M monthly revenue, online services must attribute, and **failing the attribution terminates the licence automatically**. No fee applies at this owner's scale — but a licence with thresholds and a termination clause is legal surface the vault cannot even record, and docling (plain MIT) covers the same formats |

## kosh — the workbench

| finding | what it changes |
|---|---|
| **uniextract2's detection order**, **magic-extractor's PE fallback list**, **UniPyX's 777 signature rules** | `sniff()` in `core/optimize.py` recognises **four** signatures — png, gzip, zip, jpeg — and returns `"unknown"` for everything else. That is the whole gap: 777 rules exist, four are used, and an unknown binary is where the PE fallback order starts |
| **docling / MinerU** | `kosh` already has a document-facing surface; a `convert`-style verb over docling is the smallest useful addition |
| **ziptastic's PNG findings** | kosh drives the engine; the unfilter decision (screenshots −26.3%, photographs **+49.7%**) is the kind of thing its `optimize` verb must not get wrong |

## compfactory

The PE fallback order and the extraction-tool survey belong in the workspace notes; no code.

---

# Part 2 — the book and text pipelines

## corpus-extendum — the strongest single match in this whole survey

Its pipeline is `fetch → rights gate → typeset PDF → build EPUB → extract text → hash → dedupe →
shelve`, and today the text step extracts **from the EPUB spine**, with scans requiring `_djvu.txt`
because the OCR text is what is trusted.

| finding | what it changes |
|---|---|
| ~~docling~~ | **rejected 2026-11-18**: 6.4 GB install, will not start in 2 GB RAM, and the existing spine extractor already reproduces the shipped text at **100.00% similarity**. See corpus-extendum D13 |

MinerU was the other candidate for the scanned books and is **rejected on licence**: Apache-2.0 plus commercial thresholds, an attribution obligation, and automatic termination if that obligation is missed. It costs nothing at this scale, but it is a licence with a tripwire where a plain-MIT tool does the same job.

## lexora

PDF ingestion is listed as **Planned** in its roadmap. **docling** was the candidate, and the
"it does not require a lot" claim was wrong: `pip install docling` pulls **6.4 GB**, including torch
and 3.0 GB of CUDA runtime. Its declared core is light; the metapackage is not. For PDF *text* the
right tool is pypdf or pdfminer.six (MIT, pure Python, kilobytes); docling is worth its weight only
for scanned pages where layout must be inferred.

And it belongs in an **extra**, not the core, which is exactly what lexora already does for the GUI
(ADR-0008 decision 1: *"core install stays Qt-free"*). The base install is `zstandard` alone and
should stay that way; `lexora[pdf]` is the shape.

MinerU is rejected here too — same licence terms, no benefit over docling for text.

## All4ONE — 403 tools, 24 of them PDF

| finding | what it changes |
|---|---|
| **docling** | a plausible backend for its PDF tools — but it is a portable single Windows binary. docling's *core* is eight small pure-Python dependencies (no torch), so a parse-only install is feasible; the layout and OCR extras are what would not fit |
| ~~MinerU~~ | rejected on licence (see above), and it also needs model weights |

## the materia medica family — inferred from descriptions, not read

`open-materia-medica` (344 remedy portraits), `MATERIA-MEDICA-BUILDER`,
`remedy-relationship-explorer` (Boericke 1927, Clarke 1900, Hering 1879), `UniRep` (classical
repertories), `mnemosyne-companion` — all are built from **scanned, out-of-copyright materia
medica books**, which is exactly the MinerU/docling use case: layout-aware OCR of two-column
nineteenth-century typesetting.

I have not opened these repos, so this is a fit by description. It is worth confirming before
acting: if their sources are already transcribed, the extraction tools add nothing.

## skills

The two survey documents (`extraction-tools-2026-11-18.md`, `compression-links-2026-11-18.md`) are
catalogue-shaped already; `skills` is where a "choose an extraction backend" recipe belongs.

---

# Part 3 — images

`app-image-toolkit`, `lumen`, and All4ONE's image tools all compress and convert photographs.

**ziptastic's PNG measurement is the finding that matters here**, and it is a warning rather than a
tool: unfiltering a PNG before compression is **−26.3% on a flat-colour screenshot and +49.7% on a
photograph**. An image toolkit that applies one policy to both loses a third of the file on one half
of its inputs. The rule — *measure the content, never assume the class* — transfers directly.

---

# Part 4 — infrastructure

| repo | fit |
|---|---|
| `knowledge` | the two survey documents belong here as the system's reference shelf |
| `forge`, `registry`, `dashboard`, `control-panel` | weak. The AIT Pareto idea is about *compression* results; forcing it onto build-health reporting would be cargo-culting. Not recommended |
| `audit` | holds both surveys; already done |

---

# Part 5 — where nothing fits

Games and engines (`aethelgard-*`, `neon-engine`, `retro-strike`, `aethelgard-rpg-engine`),
`NEO` (a language compiler), `The_Browser`, `tessera*` (CRM/ledger), `sui` (AI gateway),
`pico` (automation), the planner/wellness/book-companion apps, `astro-kit`, `weft8-kit`.

Neither link set has anything for these, and inventing a fit would waste the owner's time. The
compression findings are about bytes and structure; the extraction findings are about documents.
A planner app is neither.

---

# The order I would work in

1. **ziptastic: benchmark against OpenZL** — the first external check on the engine's central claim, and small.
2. **corpus-extendum: docling for the text step** — the strongest single match, MIT, and it is the pipeline's weakest stage.
3. **heavenzip: the PE fallback order and the scoring function** — both small, both from tested code.
4. **ziptastic: Pareto reporting and a hidden test set** — cheap, and it would have caught this week's four single-fixture mistakes.
5. **ziptastic: column encodings under the SQLite transform** — the largest ratio opportunity on the list.
6. **HCS: record OpenZL, docling and MinerU as sources**, and fix the licence column so "Apache-2.0 + additional terms" can be said.
