# KILN shipped five releases, the two toolboxes became one index, and the console reads KILN's gates

Date: 2026-11-15 · Repos `drsamonline/KILN` (v1.0.14 → v1.3.1),
`drsamonline/TOOLWORKS` (created, pushed, Pages on), `drsamonline/dashboard` (one panel added)
Reference read: `drsamonline/TTB`, `drsamonline/All4ONE`, `drsamonline/audit` (this repo),
`drsamonline/dashboard/DATA_CONTRACTS.md`

## What I looked at

The fleet audit delivered on 2026-11-14 named five recommendations, in order. This session
worked through all five, then released each one. The evidence for every number below is a
command in the repository that produced it, not a figure copied between documents.

- `KILN`: `kiln/`, `templates/app/index.html`, `catalog/`, `specs/`, `kiln/guards.py`
- `TTB`: `data/tools.js` (565 entries), `data/inputs.js` (63 control schemas)
- `All4ONE`: `TOOL_CATALOG.md` (404 entries, 16 categories)
- `dashboard`: `docs/play/index.html`, `tests/structure.test.js`, `DATA_CONTRACTS.md`

## What was wrong

| Defect | Where | How it surfaced |
|---|---|---|
| `MANIFEST.json` said **0.9.0** while the code said 1.0.14 | KILN | found on the way to the first tag; the release policy told the owner to bump both and nothing checked |
| the `image` field type was spliced into the **display** chain instead of `fieldInput` | KILN template | a size-budget test reported an unexpected `function derive`; reading the chain showed `input = document.createElement` inside `render()` |
| the crypto helpers shipped in **every** app | KILN template | the same test; a plain notes app carried `deriveKey` and the unlock dialog |
| the fleet backup copied one storage key per app | KILN fleet page | the app keeps its salt at `<key>:salt`; a backup restored elsewhere had the blob and not the salt, so a locked app could not open |
| `node_modules/` was not ignored | `dashboard` | `npm install` to run its own tests put 30k files in the working tree |
| two tool catalogues had never been reconciled | `TTB`, `All4ONE` | 969 tools across two repos, 16 names in both, and no page that listed either |

## What I changed

### KILN — v1.0.14 → v1.3.1, five releases

| Version | Change |
|---|---|
| v1.0.14 | `HANDOVER.md`, and guard C26 so the manifest and the code cannot disagree again |
| v1.1.0 | **`crypto`**: PBKDF2-SHA256 + AES-GCM at rest, one capability instead of four |
| v1.2.0 | `specs/fleet/`: three fleet apps rebuilt as specs, each naming its source repo |
| v1.3.0 | `fleet/`: all 37 apps in one installable page, with one backup for all of them |
| v1.3.1 | the backup carries the salt, so a restored locked app opens |

Guard count 455 → 465; specs 33 → 37; tests 544 → 596; releases 0 → 5. The status page,
the badge and `status.json` are all generated, and CI republishes the feed on every push to
`main`.

### TOOLWORKS — created

969 tools from `TTB` (565) and `All4ONE` (404) in one searchable index. 34 source categories
collapsed to 20 groups. **Nothing was dropped as a duplicate**: the 16 names present in both
catalogues are different tools, and the index labels each with its source. Neither original
repository was modified; `git status` is clean in both.

### dashboard — one panel

A **KILN gates** panel reads `status.json` from KILN's `status` branch and falls back to the
badge file on Pages, saying which source it used. Six assertions in `structure.test.js`
(47 pass). This is the first number on the console that arrives as data rather than being
re-derived.

## What I did not do

- **No release without the owner's word.** `RELEASE.md` recorded the policy; the owner gave
  it, and each tag was cut only after CI was green on that commit.
- **No file copied out of TTB or All4ONE.** TOOLWORKS carries ids, names, categories and the
  descriptions those projects publish. Nothing else.
- **No invented descriptions.** TTB publishes none; the index shows a dash rather than a
  guess, and 464 tools show the controls their own project declares.
- **No merge of the two tool repos.** They keep their code, history, licence and users.
- **No third-party action in KILN's CI.** Publishing uses plain `git` to an orphan branch.

## Evidence

| Claim | Command |
|---|---|
| KILN 465 guards, 0 failed | `python3 -m kiln audit` |
| KILN 37 specs, 0 failing | `python3 -m kiln verify --all` |
| KILN 596 tests | `python3 -m unittest discover -s tests` |
| the feed is live | `https://raw.githubusercontent.com/drsamonline/KILN/status/status.json` |
| TOOLWORKS 969 rows | `python3 -c "import json;print(json.load(open('data/catalogue.json'))['count'])"` |
| the two originals are untouched | `git -C TTB status --porcelain` (empty), same for All4ONE |
| the dashboard panel renders | `node tests/structure.test.js` |

## The count, settled by CI rather than by me

The README headline says **78 repositories**. The committed snapshot said 134. Today's
enumeration said 135. `gh repo list` said 142 non-fork.

`tools/collect.py` was run twice from here and **was killed at this sandbox's 300-second
command cap both times** (exit 124), after the per-repo pass and before the write, so the
snapshot was unchanged and nothing was edited to a figure I could not produce.

While this entry was being written, the scheduled refresh ran in CI — where there is no such
cap — and committed `febe4f4`, "refresh the fleet snapshot [skip ci]". That snapshot is now
**135 repositories, with `TOOLWORKS` and `KILN` both present**. The entry was rebased onto it.

| Source | Repositories | Verdict |
|---|---|---|
| `README.md`, the claim | 78 | **stale prose** |
| `state/repos.json`, refreshed by CI | **135** | current, and carries `TOOLWORKS` |
| `gh repo list`, non-fork | 142 | a different question: it counts forks and archived repos differently |

The lesson is the one KILN learned twice this session: a number in prose drifts, and a number
in a generated file does not. The README should read `state/repos.json` rather than restate it.

## Next

- Make the README count come from `state/repos.json` instead of prose. The snapshot is now
  current at 135; the prose still says 78.
- Add `TOOLWORKS` to the dashboard and the profile index now that Pages is live.
- `TOOLWORKS` should be added to the dashboard and the profile index now that Pages is live.
- The fleet page's backup is proven for `localStorage` only; an app that ever moves to
  IndexedDB would need the same treatment.
