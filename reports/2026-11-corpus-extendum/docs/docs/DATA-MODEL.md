# Data model

Six files describe the library. Two live in each vault, four in the library
repo, and the site reads only the library's four.

```
corpus-extendum/                 corpus-extendum-vault-01/
├── data/                        ├── index.txt          ← plain text, one line per book
│   ├── catalog.json             ├── manifest.json      ← the same, machine-readable
│   ├── categories.json          └── books/<slug>/
│   ├── shards.json                  ├── <slug>.pdf
│   ├── search-index.json            ├── <slug>.epub
│   └── dedupe.json                  ├── <slug>.txt
├── index.txt                        ├── cover.jpg
└── dedupe-report.txt                └── meta.json      ← the authoritative record
```

---

## `meta.json` — the authoritative record

One per book, in the vault. Everything else is derived from these.

```json
{
  "id": "2680",
  "slug": "meditations",
  "title": "Meditations",
  "author": {
    "name": "Marcus Aurelius",
    "file_as": "Marcus Aurelius, Emperor of Rome",
    "death": 180
  },
  "year": 180,
  "category": "Philosophy",
  "language": "en",
  "subjects": ["Stoics", "Ethics -- Early works to 1800"],
  "blurb": "A Roman emperor's private notes to himself…",
  "rights": {
    "basis": "author d. 180; first published 180 — public domain in India (life + 60) and the United States (pre-1930)",
    "india": true,
    "us": true,
    "verified": "2026-11-15"
  },
  "source": {
    "name": "Standard Ebooks",
    "ref": "marcus-aurelius_meditations_george-long",
    "url": "https://standardebooks.org/ebooks/marcus-aurelius/meditations_george-long",
    "licence": "CC0 1.0 (edition) · text public domain"
  },
  "formats": ["pdf", "epub", "txt"],
  "files": {
    "pdf":   "books/meditations/meditations.pdf",
    "epub":  "books/meditations/meditations.epub",
    "txt":   "books/meditations/meditations.txt",
    "cover": "books/meditations/cover.jpg"
  },
  "cover_kind": "source",
  "vault": "corpus-extendum-vault-01",
  "added": "2026-11-15",
  "file_sha8": "0c15745e",
  "text_sha256": "8a65f94554e7fc73a1ce8b66c03763b92f990614fb36a2bdb563469a51b6",
  "translator": { "name": "George Long", "death": 1879 }
}
```

| Field | Meaning |
|---|---|
| `id` | Gutenberg ebook number. Taken from the edition's own `dc:source` where present — the script logs a correction when the hand-typed value disagrees |
| `slug` | URL and folder name; stable forever, never regenerated |
| `author.death` | drives the India rights test |
| `author.file_as` | sort order, `Surname, Forename` |
| `year` | first publication |
| `rights.basis` | the human-readable claim, written at ingest |
| `rights.india` / `rights.us` | the two tests, both must be `true` |
| `rights.verified` | date the basis was last computed |
| `source.ref` | the upstream identifier, and dedupe test 1 |
| `formats` | which files exist; drives the chips on the card |
| `files.*` | paths **relative to the vault root**, so the vault can move |
| `cover_kind` | `source` (the edition's own cover) or `generated` (drawn by us) |
| `text_sha256` | the dedupe key over normalised text |
| `file_sha8` | first 8 hex of the PDF's SHA-256 |
| `translator` | present only when the edition has one |
| `quarantined` | added by `build_catalog.py` if a duplicate slipped through; the book then disappears from the site |
| `editions` | other editions of the same work, recorded here rather than shelved as separate cards |
| `rights.translation_verified` | true when the translator's death year was read from a source |
| `notes` | present only when something was left out, e.g. a book shelved without a PDF because typesetting exceeded the run budget |

---

## `data/catalog.json`

An array of every `meta.json` from every vault, minus anything quarantined,
sorted by category then year then title. This is the only file the page reads
for book data. At 66 books it is 100 KB.

## `data/shards.json` — the vault registry

```json
[
  {
    "name": "corpus-extendum-vault-01",
    "repo": "drsamonline/corpus-extendum-vault-01",
    "cdn":  "https://cdn.jsdelivr.net/gh/drsamonline/corpus-extendum-vault-01@main",
    "raw":  "https://raw.githubusercontent.com/drsamonline/corpus-extendum-vault-01/main",
    "books": 43,
    "mb": 146.8,
    "state": "open",
    "cap_books": 600,
    "cap_mb": 2500,
    "built": "2026-11-16T02:19Z"
  }
]
```

`state` is `open` or `sealed`. Exactly one vault is open; ingest writes only
there. `cdn` and `raw` are how the page turns `files.pdf` into a URL, so the
page never hardcodes a repository name.

## `data/categories.json`

`[["Fiction", 10], ["Mystery & Detective", 5], …]` — the rail, with counts,
sorted by count descending.

## `data/search-index.json`

`[{"slug": "...", "t": ["word", "word", …]}]` — lowercased tokens of 2+ chars
from title, author, category, subjects and blurb. Prefix matching happens in the
browser. At 43 books this is 11 KB; it exists so search does not have to walk
the whole catalogue on every keystroke.

## `data/translators.json` — the translator registry

Read by the rights gate before a translated work is accepted. Keys are
normalised names; each entry carries a death year, a `verified` flag and the
source the year came from. An entry with `verified: false` is refused, so the
file is a whitelist with evidence rather than a guess. See
[RIGHTS.md](RIGHTS.md#translations).

## `data/dedupe.json` — the register

```json
{
  "source_refs": ["gutenberg:1342", "gutenberg:84", …],
  "text_sha256": { "<hash>": "pride-and-prejudice", … },
  "work_keys":  { "austen|pride and prejudice|1813": "pride-and-prejudice", … }
}
```

Read before fetching (to skip known books) and at ingest (to refuse
duplicates). `work_keys` is recorded but **not yet consulted** — dedupe tests 3
and 4 are designed, not built.

## `index.txt` — the catalogue without a browser

Two of them, both pipe-delimited, both regenerated on every build.

Library (`corpus-extendum/index.txt`):

```
# corpus-extendum | 43 books | 1 vault(s) | built 2026-11-16T02:19Z
# id | slug | title | author | year | category | formats | vault
```

Vault (`corpus-extendum-vault-01/index.txt`):

```
# corpus-extendum-vault-01 | 43 books | 146.8 MB | cap 600 books / 2500 MB | state: open | built …
# id | slug | title | author | year | category | lang | pd_basis | formats | pdf_kb | epub_kb | path | file_sha8 | text_sha8
1342|pride-and-prejudice|Pride and Prejudice|Austen, Jane|1813|Fiction|en|author d.1817; pub.1813|pdf,epub,txt|1034|803|books/pride-and-prejudice|ba2d9425|78a0a582
```

If a vault's website vanished, its repository was deleted, or the catalogue were
lost, `index.txt` is the file that still says what you had.

## Report files

| File | Written by | Contains |
|---|---|---|
| `dedupe-report.txt` | `build_catalog.py` | build time, counts, and every quarantine with its duplicate-of |
| `data/scan-log.txt` | `scan.yml` | a heartbeat line per run; also keeps GitHub from disabling the schedule |
| `data/rotation-log.txt` | `rotate_vault.py` | every seal, with the book and MB count it sealed at |
| `data/review-queue.json` | `ingest.py` | titles held by dedupe test 4, with the slug each resembles and the similarity score |
