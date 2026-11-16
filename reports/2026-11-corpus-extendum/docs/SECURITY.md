# Security

## What this is

A static website and a set of public git repositories. There is no server, no
database, no login, no user data and no API of its own. The attack surface is
correspondingly small, and most of it belongs to GitHub.

## Reporting

Open an issue at
https://github.com/drsamonline/corpus-extendum/issues

For anything that should not be public, use GitHub's private vulnerability
reporting on the repository (Security → Report a vulnerability).

## What is in scope

| Area | Concern |
|---|---|
| `assets/app.js` | any path where remote content reaches the DOM unsanitised |
| The reader | a book file that can execute script in the page's origin |
| `scripts/*.py` | a malicious source archive that escapes its directory, or a rights gate that can be bypassed |
| The vendored libraries | pdf.js, epub.js, JSZip — versions and provenance |

## What is not in scope

- The content of public-domain books.
- GitHub Pages, jsDelivr or `raw.githubusercontent.com` infrastructure.
- Anything requiring an account, because there are none.

## How the obvious risks are handled

**No third-party code on a reading page.** pdf.js, its worker, epub.js and JSZip
are vendored in `assets/vendor/` — nothing is fetched from a CDN at read time,
so a compromised CDN cannot inject into the reader. Google Fonts is the only
external request, and blocking it costs nothing but the typeface.

**Book files are treated as data, not code.** A PDF is rendered by pdf.js into a
canvas; an EPUB is parsed by epub.js into the DOM; text goes through `esc()`
before it reaches `innerHTML`; JSON is escaped and highlighted. Nothing is
injected raw. When an HTML viewer is added it must render in a sandboxed iframe
with scripts and forms disabled — that requirement is in
[ARCHITECTURE.md](docs/ARCHITECTURE.md) and must not be quietly dropped.

**Archives are extracted with a filter.** `ingest.py` calls
`tarfile.extractall(..., filter="data")`, which refuses absolute paths, `..`
traversal, and links that escape the destination.

**No secrets in the repo.** The only credential anywhere is `CORPUS_BOT_TOKEN`,
supplied as a repository secret for rotation, never committed. If you find a
token in the tree, treat it as compromised and rotate it.

**Supply chain.** The vendored libraries came from the owner's own `app-lantern`
repository, not from a package manager at build time. Their versions are
recorded in the filenames and licences are kept beside them
(`assets/vendor/LICENSE-jszip.md`). Updating them is a deliberate commit, not an
automatic one.

## Rights as a safety property

The rights gate is the one place where a mistake is not just a bug. A book
shelved without a valid public-domain basis is a legal problem, not a cosmetic
one. That is why the gate refuses anything it cannot compute a basis for, why
the basis is written into the record, and why translations are refused outright
until the translator can be checked. See [RIGHTS.md](docs/RIGHTS.md).

## Known limitations

- The canvas-rendered PDF is not screen-reader accessible; the native viewer
  path is, which is one reason phones get it.
- No Content-Security-Policy header is set, because GitHub Pages does not allow
  custom headers. A `<meta http-equiv>` policy would be weaker than the claim it
  implies, so none is claimed.
