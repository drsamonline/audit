# Implementation plan: the four split repos, and the demo rule

Written after reading the four repos end to end. Everything below is grounded in what is in the
tree today, not in what the audit assumed.

## What the four actually are

| repo | what is there | what is broken |
|---|---|---|
| `app-lantern` | a real 482-line Node server (`server.js`), a client in `public/`, a bundled `dist/lantern.js`, and a demo in `docs/demo/` with a 2 KB `library.json` generated from `examples/starter-pack.json` | **no content ships with the app** — there is no `packs/` folder, so `npm start` opens an empty library. The demo is client-only and static: it has no server, so it cannot show the thing the product is (serving over a LAN) |
| `app-organon-reader` | the reader itself at `docs/index.html`, with `reader.js` and `organon-data.js` | **no landing page at all.** A stranger's first screen is the reader, with nothing explaining what it is |
| `seance` | seal/open UI, tabs, copy button | **`CryptoKit` is never defined.** `app.html` calls `CryptoKit.sealString` and `CryptoKit.openString`; the only script it loads is `web-kit.js`, which has no `CryptoKit`. Seal and Open throw `CryptoKit is not defined`. The headline feature does not work |
| `today-card` | four buttons, all with handlers, and `web-kit.js` does expose `Loom.csv`, `Loom.theme`, `Loom.i18n`, `Loom.storage` | the wiring looks correct on paper, so the failure is at runtime — needs a headless click test to find it. Design is the real problem |

And the screenshots: `seance/docs/shot.png` and `today-card/docs/shot.png` are **byte-identical**
(`b23fa03c…`), and the image is a **screenshot of a GitHub Pages 404 page**. Someone shot the 404
and committed it, twice.

## Batches

### Batch 0 — the rules, and the gate that keeps them
- Write the demo rule into the skill's method for this estate: a landing page embeds the real app in
  a frame wherever the app can run in one; where it cannot (a Node server, a desktop binary), the
  demo band shows screenshots and says so, and never offers a play button.
- Add a `verify.py` check: **two repos may not share a byte-identical `docs/shot.png`**, and a shot
  whose top line reads `404` is a failure. That is the class of bug that put a 404 page on two
  landing pages, and it is mechanically detectable.
- Pin the shot pipeline (`shot.sh` + headless Chromium) in each repo's `tools/`, so every later
  batch shoots the same way.
- Done when: the gate catches both existing 404 shots and passes `lumen`.

### Batch 1 — Seance: make the feature work, then make it worth looking at
- Bundle `crypto-kit` into the app (or vendor the two functions it needs) so `CryptoKit.sealString`
  and `CryptoKit.openString` exist. Nothing else in this batch matters until that is true.
- Build the send-and-open path properly. Today it is copy-paste text only. It becomes four ways:
  1. **Copy the sealed text** — what exists now;
  2. **Download a `.seance` file** — a sealed note as a file you can attach to anything;
  3. **A share link** — the sealed payload in the URL fragment (`#s=…`), so no server ever sees it,
     opened by the recipient pasting the link into the Open tab;
  4. **A QR** — the sealed payload as a scannable code, for phone to phone with no channel at all.
  The recipient side accepts all four: paste text, drop a file, open a link, scan.
- Make "opens once" honest. Today it is a `localStorage` flag on the *opening* device — clear the
  storage and it opens again. Either say that plainly on the page, or make it a real one-time
  envelope (a nonce burned on first open, plus a clear warning that a client-side "once" is a
  promise, not a guarantee).
- Redesign the landing page and the app together, on one idea: a wax seal, an envelope, a dark
  reading room. The app and the page must read as two objects, not one template twice.
- Re-shoot both screenshots after the redesign.
- Done when: seal → link/file/QR → open works in a fresh profile, in both themes, and the shots are
  of the real pages.

### Batch 2 — Today Card: design, and four buttons that do something
- Headless-test each of the four buttons and record what actually fails (Save, Theme, Language,
  Export all have handlers, so this is a runtime bug, not a missing one).
- Make each one earn its place: Save shows the saved state and the streak; Export produces a CSV of
  every day, not just today; Theme and Language give visible feedback instead of silently cycling.
- One design for the app and the page, matching: a card, a date, a streak. Large type, one accent.
- Re-shoot both screenshots.
- Done when: every button changes something a user can see, and the shots are real.

### Batch 3 — Organon Reader: a landing page worth the book
- Build `docs/index.html` as a real page: **large serif display type**, Hahnemann's portrait, what
  the Organon is, what the reader does, the six sections it covers.
- Move the reader to `docs/play/` and embed it in the page with guided buttons into real paragraphs.
- The portrait must be **committed locally**, not hotlinked — public domain, so it can be. If the
  sandbox cannot reach a source, ask the owner for the file rather than shipping a grey box.
- Badges, support block, screenshots, README.
- Done when: a stranger who has never heard of the Organon understands it in one screen, and can be
  reading a paragraph two clicks later.

### Batch 4 — Lantern: content in the box, and a demo that shows the product
- Ship a **starter pack in `packs/`**, generated from `examples/starter-pack.json` by the existing
  `tools/build.mjs`, so `npm start` serves a library on first run instead of an empty page.
- Give the **demo a server**: a small `demo-server.js` shim that answers the same `/p/<pack>` and
  search endpoints from `library.json`, so `docs/play/` behaves like the real thing without Node.
- **Enrich the demo library** — several packs, dozens of documents, so search has something to rank
  and browsing has something to browse. A 2 KB pack cannot demonstrate a library.
- Landing page: the LAN story in one line, the demo embedded, a screenshot of a real search result.
- Done when: a visitor can search the demo and open a document without installing anything, and a
  person who runs `npm start` sees content immediately.

### Batch 5 — the estate-wide paste
- The 94 support blocks, 98 README Support tables, 85 badge sets, 45 screenshot sets — one commit
  per repo, text first, PNGs one at a time.
- Done when the `SUPPORT` column reads 96 of 96 required.

### Batch 6 — the redesign queue, then the last two
- The 3 clones (`BLINKTRANSFER`, `blinkcode-ai`, `helioprism`) and the plain pages the owner picks
  from `design.md`.
- `musicgen` and `Scrap-and-Gun` **last**, by the owner's instruction: both are finished pages, so
  what is left on them is the block and the badges, plus the two-word fixes — the doubled
  `play/play/` demo link and the `play/icon.svg` favicon that does not exist.

## Two things to settle before Batch 1

1. **Seance's "once"** — is a client-side once-per-device good enough (say so on the page), or does
   it need to be a burned nonce that cannot be reopened even by clearing storage?
2. **Hahnemann's portrait** — I will look for a public-domain scan; if the sandbox cannot reach one,
   the owner sends the file and I commit it.

## What is already decided and not in this plan

- Apple targets: accepted, they bill nothing while the repos are public.
- shields.io badges: accepted, deliberate.
- Kits and engines: landing page + badges + support block; no demo, no release build.
- Forge tooling (`dashboard`, `control-panel`, `app-companion-forge`, `audit`): no public face.
