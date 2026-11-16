# Operations

The runbook. Everything here is a command that has been run, not a suggestion.

## Daily life

Nothing runs daily. The page is static; a book sits on the shelf until you add
another one.

## Add a book

1. Add an entry to `BOOKS` in `scripts/ingest.py`:

```python
dict(id=1260, slug="jane-eyre", title="Jane Eyre", author="Charlotte Bronte",
     author_file="Bronte, Charlotte", year=1847, death=1855, category="Fiction",
     se="charlotte-bronte_jane-eyre",
     blurb="…", subjects=["…"]),
```

2. **Verify the slug against codeload before anything else.** Not against the
   API — `gh api … --jq .name` prints `null` on a 404 and `null` passes a shell
   truthiness test, so a broken check says the repo exists:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -L \
  "https://codeload.github.com/standardebooks/charlotte-bronte_jane-eyre/tar.gz/refs/heads/master"
```

3. Ingest, in batches of three to five so nothing runs past the 290-second
   ceiling:

```bash
python3 scripts/ingest.py --vault ../corpus-extendum-vault-01 --only 1260
```

4. Rebuild, then commit both repositories:

```bash
python3 scripts/build_catalog.py --vault ../corpus-extendum-vault-01
python3 scripts/make_shots.py --vault ../corpus-extendum-vault-01   # if the shelf changed shape
git add -A && git commit -m "shelf: add Jane Eyre" && git push
(cd ../corpus-extendum-vault-01 && git add -A && git commit -m "vault-01: add Jane Eyre" && git push)
```

The library must be rebuilt **after** the vault is pushed, or the catalogue
points at files that are not there yet. Pages redeploys on the library push.

### When a book will not fit the budget

Typesetting is the slow part. A 900-page book can exceed the 290 s a run is given
even though the download took seconds. `--no-pdf` shelves the EPUB and the text
without one, and writes the reason into the record's `notes`:

```bash
python3 scripts/ingest.py --vault ../corpus-extendum-vault-01 --only 1676 --no-pdf
```

The reader handles a book with no PDF — the format chips show only what exists,
and the book opens in whatever format it has. Two books are shelved this way:
Plato's *Dialogues* and Chekhov's collected *Short Fiction*.

## Rebuild the catalogue without adding books

```bash
python3 scripts/build_catalog.py --vault ../corpus-extendum-vault-01
```

This is also what the weekly scan runs. It rewrites `data/catalog.json`,
`categories.json`, `search-index.json`, `shards.json`, both `index.txt` files,
each vault's `manifest.json`, and `dedupe-report.txt`.

## Check a deployment

```bash
gh api repos/drsamonline/corpus-extendum/actions/runs --jq '.workflow_runs[0] | "\(.status)/\(.conclusion)/\(.head_sha[0:7])"'
gh api repos/drsamonline/corpus-extendum/deployments --jq '.[0] | "\(.sha[0:7]) \(.environment)"'
```

The deployed SHA must match `git rev-parse --short HEAD`. If it does not, the
push did not trigger or the run failed — read the run, not the page.

## Rotation

Check whether the open vault is full:

```bash
python3 scripts/rotate_vault.py --dry-run
```

Rehearse a seal without writing anything:

```bash
python3 scripts/rotate_vault.py --dry-run --force
```

Rotate for real (needs `CORPUS_BOT_TOKEN` with Administration: write and
Contents: write):

```bash
CORPUS_BOT_TOKEN=… python3 scripts/rotate_vault.py
```

If the token is missing or cannot create repositories the script exits **3**,
prints the `gh repo create` command to run by hand, and leaves `shards.json`
untouched. The weekly scan turns that exit code into an issue.

After rotating, `build_catalog.py` writes the sealed vault's final `index.txt`
with `state: sealed`.

## Verify the reader in a real browser

Chromium is available in the build environment; use it rather than reasoning
about CSS.

```bash
# does the shelf render every book?
chromium --headless=new --no-sandbox --disable-gpu --allow-file-access-from-files \
  --virtual-time-budget=9000 --dump-dom file://$PWD/index.html | grep -c 'class="card"'

# the reader at phone and tablet widths, over a real local server
CE_TEST_ROOT=/path/to/site python3 scripts/shoot_reader.py
```

Two things to know: pdf.js's worker does not progress under
`--virtual-time-budget`, so a canvas render will hang in headless even when it
works in a real browser; and the sandbox proxy blocks jsDelivr, so test the PDF
path against a local copy (`shoot_reader.py` exists for exactly this).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| The page shows fewer books than the catalogue | a cached `catalog.json` in the browser | data fetches carry `?t=<timestamp>` and `cache: 'no-store'`; if it persists, hard-reload. The footer prints `site build <version>` — if that line is missing, the HTML itself is stale |
| A card's cover is blank | `cover.jpg` missing or the vault not yet pushed | check `raw.githubusercontent.com/.../cover.jpg` |
| Reader pane is empty on desktop | pdf.js could not fetch the PDF (CORS, 404, or a stalled load) | the reader falls back to the native viewer automatically; if it did not, check the console |
| Reader pane is empty on a phone | expected if the browser blocks the PDF plugin | the note under the frame says which viewer is in use |
| `no space left on device` during ingest | `/tmp` is a 64 MB tmpfs | set `CE_WORK` to real disk |
| An illustrated book exceeds the time budget | see [PIPELINE.md §4](PIPELINE.md#4--plates) | lower `CE_MAX_PX`, or run that book alone |
| Rotation exits 3 | no token that can create repositories | set `CORPUS_BOT_TOKEN`, or run the printed `gh` command |

## Permissions, and what each thing can do

| Actor | Can | Cannot |
|---|---|---|
| `gh` CLI / git (this environment) | push to existing repos | create repos, enable Pages, set topics, dispatch workflows — all 403 |
| GitHub MCP | create repos, enable Pages, set topics | — |
| `GITHUB_TOKEN` in Actions | write the repo the workflow runs in | create repositories |
| `CORPUS_BOT_TOKEN` (PAT) | create repositories | anything you do not grant |

That asymmetry is why Pages and topics were configured through the MCP and why
rotation needs its own token.

## Budgets

| Thing | Limit | Where it bites |
|---|---|---|
| GitHub Pages site | 1 GB published | why vaults are not Pages sites |
| GitHub single file | 100 MB hard | no book file is close; the largest is 12.6 MB |
| jsDelivr file | 20 MB | the illustrated editions are the risk; Looking-Glass is 12.3 MB |
| Vault cap | 600 books / 2.5 GB | rotation |
| Ingest run | ~290 s | 3–5 books per run |
| Scheduled workflows | disabled after 60 days idle | `scan.yml` commits a heartbeat to keep it alive |
