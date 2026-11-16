# Vaults

A vault is a storage repository. It holds book files and two manifests, and
nothing else — no website, no scripts, no build.

```
corpus-extendum-vault-01/
├── README.md          what this vault holds, its state, its cap
├── index.txt          the contract: one line per book, pipe-delimited
├── manifest.json      the same data, machine-readable
└── books/
    └── <slug>/
        ├── <slug>.pdf
        ├── <slug>.epub
        ├── <slug>.txt
        ├── cover.jpg
        └── meta.json      the authoritative record
```

## Why vaults are not Pages sites

GitHub Pages caps a published site at **1 GB**. A vault is built to reach
**2.5 GB**, so it could never be published as a site. Books are served through
`cdn.jsdelivr.net/gh/<owner>/<vault>@main/…`, with
`raw.githubusercontent.com` as the download fallback. See
[DECISIONS.md D1](DECISIONS.md#d1--books-live-in-separate-vault-repos-served-by-jsdelivr-not-github-pages).

## Rules

1. **One writer per file.** `ingest.py` writes `books/`. `build_catalog.py`
   writes `index.txt` and `manifest.json`. Nothing else writes anything.
2. **`books/<slug>/` is atomic.** A book is either complete — five files,
   including `meta.json` — or it is not there. The ingest script skips a folder
   that already has a `meta.json`, and `--replace` is the only way to redo one.
3. **A sealed vault is read-only.** Sealing is a commit, never a deletion: the
   vault keeps every file it has and its `index.txt` gains `state: sealed`.
4. **Nothing is deleted from a sealed vault.** If a record is wrong, correct
   `meta.json` and remove the line from `index.txt`. The catalogue stops showing
   the book; the file stays where the record says it is.
5. **Never hand-edit `index.txt`.** It is regenerated on every build, so an edit
   survives exactly until the next scan.

## The `index.txt` contract

```
# corpus-extendum-vault-01 | 43 books | 146.8 MB | cap 600 books / 2500 MB | state: open | built 2026-11-16T02:19Z
# id | slug | title | author | year | category | lang | pd_basis | formats | pdf_kb | epub_kb | path | file_sha8 | text_sha8
1342|pride-and-prejudice|Pride and Prejudice|Austen, Jane|1813|Fiction|en|author d.1817; pub.1813|pdf,epub,txt|1034|803|books/pride-and-prejudice|ba2d9425|78a0a582
```

Line one states the vault's own state, so a vault can be understood without the
library. Line two is the column legend. Everything after is data, sorted by slug.

This file exists because it is the only description of a vault that survives the
vault: if the library repo, the catalogue and the website all vanished, `index.txt`
plus `books/` is a complete, readable library. It is deliberately plain text.

## Sealing

A vault seals at **600 books or 2.5 GB**, whichever comes first.

```bash
python3 scripts/rotate_vault.py --dry-run     # what would happen
python3 scripts/rotate_vault.py               # seal, register, create the next
```

Sealing writes `state: sealed` into the vault's `index.txt`, sets `sealed` in
`data/shards.json`, opens `corpus-extendum-vault-NN`, and logs the seal with the
book and MB count to `data/rotation-log.txt`.

Creating a repository needs a token that can create repositories — the default
`GITHUB_TOKEN` cannot, and neither can a GitHub App installation token. The
script proves the token's ability with a create-and-delete probe before touching
anything real, and refuses cleanly (exit 3) with the exact `gh` command when it
cannot.

## Current state

| Vault | Books | Size | State |
|---|---|---|---|
| `corpus-extendum-vault-01` | 79 | 243.4 MB | open |

Headroom: 557 books or 2353.2 MB.

## Adding a vault by hand

If rotation is blocked and you have no PAT:

```bash
gh repo create corpus-extendum-vault-02 --public
```

Then add its entry to `data/shards.json` with `books: 0`, `mb: 0`,
`state: "open"` and the `cdn`/`raw` URLs, and run `build_catalog.py`. The next
ingest writes there. `rotate_vault.py` does all of this for you when it has a
token.
