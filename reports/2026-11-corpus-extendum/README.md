# corpus-extendum — the public-domain library

A free library of out-of-copyright books, built and shipped in one session, with
its documentation mirrored beside this file as evidence.

- **The shelf** — https://drsamonline.github.io/corpus-extendum/
- **The library repo** — https://github.com/drsamonline/corpus-extendum
- **The vault** — https://github.com/drsamonline/corpus-extendum-vault-01

## What was built

| Piece | State |
|---|---|
| Static shelf — search, filters, sort, dark mode | working |
| Reader — PDF (pdf.js, native on phones), EPUB, plain text, JSON record | working |
| Search inside a book — over the plain text, with jump and highlight | working |
| Reading progress, restored per book, with a continue-reading rail | working |
| Rights gate — India life+60 **and** US pre-1930, both must pass | working |
| Dedupe — source reference, normalised-text hash | working |
| Translator gate — verified registry, refuses unverified translators | working |
| Dedupe — work key, trigram similarity | working |
| Ingest pipeline — fetch, verify, typeset, hash, shelve | working |
| Vault rotation with token preflight | working |
| Weekly scan, catalogue rebuild, doc-drift repair | working |

## The measurements

| | |
|---|---|
| Books shelved | **46** |
| Categories | **12** |
| Vault | `corpus-extendum-vault-01`, **152.3 MB** of a 2.5 GB cap |
| Largest single file | 12.6 MB (an illustrated edition, 57 plates) |
| Library repo | under 5 MB including four vendored renderers and two screenshots |
| Cost | ₹0 per month — GitHub Pages plus jsDelivr |
| Runtime dependencies on the page | none |

Sources: Standard Ebooks (CC0 editions, 42 books), the GITenberg mirror of
Project Gutenberg (1 book).

## Three things that were measured, not assumed

**gutenberg.org refuses datacenter IPs.** Every path returns 403 — `/ebooks/`,
`/cache/`, `/files/`, plain `.txt`. A pipeline built on it only works from a
residential connection. The ingest reads Standard Ebooks source trees and the
GITenberg mirror through `codeload.github.com`, which has no such block and no
API rate limit.

**Most Gutenberg titles have no PDF.** The format list for every book examined
offers EPUB, plain text and HTML, and no PDF. The PDFs in this library are
typeset by us with WeasyPrint, which is also why every book looks like it came
from the same library.

**jsDelivr sends `Access-Control-Allow-Origin: *` and the right content type.**
Verified with `curl -D -`: `content-type: application/pdf`,
`access-control-allow-origin: *`. That header is the entire reason pdf.js can
read a PDF hosted on a different origin than the page.

## An installed GitHub App cannot create repositories

Confirmed on this account, twice:

```
GraphQL: Resource not accessible by integration (createRepository)
POST /user/repos → 403 Resource not accessible by integration
```

The `gh` CLI token can push code but cannot administer — Pages, topics and
workflow dispatch all return 403 through it. The **GitHub MCP** can do all of
those, and was used to create both repositories, enable Pages and set topics.
Vault rotation therefore needs its own PAT (`CORPUS_BOT_TOKEN`), and
`rotate_vault.py` proves the token's ability with a create-and-delete probe
before touching anything real — the same guard `backup/backup.py` uses, for the
same reason.

## What the session got wrong, and what caught it

| Wrong | Caught by | Cost |
|---|---|---|
| The shelf showed 10 books while holding 26 | the owner looking at it | an hour; data was correct on the server, the browser was serving cached JSON |
| README claimed in-book search and MOBI/DjVu conversion | writing the docs | none — corrected before anyone relied on it |
| Plate resolution lowered to fix a timeout | measuring instead | two wasted rebuilds; the cost was parsing paths, not drawing pixels |
| Slug check via `gh api --jq .name` | a codeload fetch 404ing | three books failed; `null` prints on a 404 and passes a shell truthiness test |
| Vault size counted `.git` | the catalogue reporting 138 MB for 87 MB of books | none — the number was visibly wrong |
| "No browser here" | finding Chromium installed | two rounds of fixing the mobile reader blind |

## Skills applied

Two of the fleet's skills were run against this repository rather than guessed
at, and both found real work.

`repo-legal-docs` — its scanner reported the legal surface complete but flagged
bundled assets. Correct: pdf.js (Apache-2.0), epub.js (BSD-2-Clause) and JSZip
(MIT or GPLv3) were shipped without being named anywhere, and neither were the
two Google Fonts. Apache-2.0 expects its notice to travel. NOTICE.md now carries
a component table with versions and links to each licence text, the two missing
files are vendored, and LEGAL-INDEX.md records what is deliberately absent.

`code-review-and-release-gate` — three defects, each proved at file:line:
ingest.py assumed the library was a sibling directory and would write the dedupe
registry to a directory invented beside the vault when run in CI; a search jump
waited a fixed 350 ms for an asynchronous render and lost the race on large
books; and the EPUB path lacked the raw fallback the PDF path already had.

## Evidence in this folder

- `docs/` — the full documentation set, mirrored at commit `fc349af`
- `SYNC.json` — source commit, sync timestamp and a hash per file, so the mirror
  can be proven current rather than assumed current

The documents are the authority, not this report. Where they disagree, they win,
because they are what ships.

## What was deliberately not done

- **No translated works.** The copyright term for a translation runs on the
  translator's death, and the gate does not read translator dates. Verne, Plato,
  Voltaire and Chekhov are available, obviously public domain in origin, and
  absent. Shelving Verne because Verne died in 1905 would be the exact quiet
  error this library claims not to make.
- **No format conversion.** MOBI, DjVu, DOCX and CBR are not handled, so a book
  that exists only in those formats is invisible.
- **No in-book search.** The reader has no text layer; the plain-text file is in
  every vault, so the gap is in the viewer, not the data.
- **No scans.** archive.org's real scans live in collections the adapter does
  not reach; its `collection:gutenberg` items are metadata stubs with no text,
  which was checked rather than assumed.
