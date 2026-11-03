# The plan: 100 repositories, seven batches, and one application

Everything measured in `README.md`, `fleet-table.md`, `per-repo.md` and `design.md`; everything
decided is at the bottom. This file is the order the work happens in.

Current position: **nothing applied to any repo yet except `app-lantern`'s install block.** The audit
is complete, the scope is frozen, and Batch 0 starts here.

---

## 1. The estate at a glance

100 repos, all public, all on `drsamonline`. Two need nothing: **`lumen`** (passes every surface it is
required to carry) and **`repertory-reader`** (passes all surfaces, fails three other checks — a
dark-only landing page, no light palette for the contrast gate, lost `shot:start` markers).

The **tier** decides what a repo is required to carry. A kit is not asked for a screenshot of an
interface it does not have.

| tier | n | required | repos |
|---|---|---|---|
| **`app`** | 46 | landing, demo at `docs/play/`, screenshots, badges, support | BLINKTRANSFER, MATERIA-MEDICA-BUILDER, Scrap-and-Gun, ambient-sound-studio, app-clip-loom, app-encrypted-case-log, app-image-toolkit, app-jacquard, app-lantern, app-organon-reader, app-panchang, app-poets-studio, app-thermals, app-weft-puzzles, base-bench, blinkcode-ai, bmi-bmr-tdee-macros-fluid-calculator, boericke-repertory, canteen-lan, chalk-lan, conqueror-os, corefit-md, dance-fight, eon-commando, gentle-pediatrics-companion, helioprism, idle-city-ages-of-growth, kent-repertory-explorer, lockhtml, lumen, mnemosyne-companion, musicgen, neon-runner, offline-pdf-toolkit, open-materia-medica, read-live-transform-app, remedy-relationship-explorer, repertory-reader, retro-strike, seance, skin-case-tracker, smartbill-app, the-symphony-companion, today-card, unstoppable-mind-companion, whispering-body-first-aid |

## 2. What is actually missing

Counts are required repos, after the tier scoping and after the two accepted classes are removed.

| class | n | what it is |
|---|---|---|
| **README** | 98 | no `## Support` table in the README |
| **SUPPORT** | 94 | no support block on the landing page, no portrait, no QR |
| **PORTRAIT** | 90 | no `docs/assets/support-portrait.jpg` |
| **BADGES** | 85 | fewer than six local badge SVGs |
| **SHOTS** | 45 | no `docs/assets/app-desktop.png`, where an app exists |
| **LANDING** | 26 | no landing page at all |
| **DESIGN** | 18 | 3 clones + 15 plain pages, of which 5 are exempt |
| **SPLIT** | 4 | an app with no `docs/play/` |
| **NETWORK-BADGE** | 36 | loads shields.io — **accepted**, deliberate |
| **APPLE** | 6 | offers a macOS build — **accepted**, bills nothing |

**The 26 with no landing page:** HCS, art-kit, astro-kit, audio-kit, backup, book-kit, case-kit,
compfactory, compress-kit, crypto-kit, drsamonline, drsamonline.github.io, export-kit, frame-kit,
game-kit, heavenzip, lan-kit, ml-kit, neon-velocity, optical-kit, repertory-kit, search-kit, srs-kit,
ui-kit, web-kit, ziptastic.

**The 4 needing a split:** `app-lantern` (becomes a real app — see §5), `app-organon-reader`,
`seance`, `today-card`.

**The 3 clones:** `BLINKTRANSFER`, `blinkcode-ai`, `helioprism` — one product family, and all three
still get their own design.

**The 15 plain pages**, of which five are exempt (`musicgen` and `Scrap-and-Gun` are finished;
`dashboard`, `control-panel` and `audit` are Forge tooling) — **10 to judge**: `app-clip-loom`,
`app-organon-reader`, `app-weft-puzzles`, `Matneo`, `seance`, `today-card`, `weft8-classroom`,
`weft8-compare`, `weft8-hardware`, `weft8-kit`. The live link for each is in `design.md`.

**Five still on the skeleton's heading:** `app-jacquard`, `canteen-lan`, `chalk-lan`, `corefit-md`,
`kent-repertory-explorer`.

---

## 3. The batches

### Batch 0 — the rules, the gate, and the install block

No repo is edited by hand until the rules exist, because the rules are what the 100 edits follow.

- **The demo rule.** Embed the real app in a frame wherever it can run in one. Where it cannot — a
  Node server, a desktop binary, an engine — the demo band shows screenshots and says so, and never
  offers a play button.
- **The gate.** Two new `verify.py` checks: a `shot.png` that is a picture of a 404 fails, and two
  repos sharing a byte-identical `shot.png` fails. That is the exact bug that shipped twice
  (`seance` and `today-card` both carried a screenshot of a GitHub 404 page).
- **The shot pipeline.** `shot.sh` + headless Chromium in each repo's `tools/`, so every later batch
  shoots the same way.
- **The install block** — written, `install-block.md`. Four questions answered, not one: where do I
  get it, how do I add my own content, how do I configure it, what if it goes wrong. Plus the rule
  that makes it honest: **if the copy says "double-click", the repo ships the double-clickable file.**
  Worked on `app-lantern` — `start-lantern.bat` and `start-lantern.sh` now exist, and its release has
  a bundle behind the download button.

**Done when:** the gate catches both 404 shots and passes `lumen`, and the block is on `app-lantern`.

### Batch 1 — the estate-wide paste

The mechanical half, one class at a time across the fleet. One commit per repo, text first, PNGs one
at a time.

1. **README (98)** — badges first, one-line promise, the four links, `<!-- shot:start -->`, then a
   `## Support` table with the six handles.
2. **SUPPORT (94)** — copy the four scripts into `tools/`, `verify.py . --fix` for the QR and the
   portrait, paste region 1 into the landing footer and region 2 into the app header, add a Support
   CTA in the hero, bump the service worker `CACHE`, refresh the build stamp.
3. **PORTRAIT (90)** — `support_portrait.py`, part of the same paste.
4. **BADGES (85)** — `scripts/badges.py` with the repo's real claims. These sit *beside* the
   shields.io badges, as the offline fallback; they do not replace them.
5. **SHOTS (45)** — `shot.sh` on a populated route, then look at both images before committing.

**Done when:** the `SUPPORT` column reads 96 of 96 required, and no page shows a 404 as its product.

### Batch 2 — the two that are nearly there

`repertory-reader` (dark-only page, no light palette, lost shot markers) and the rest of the `S`
effort set. Cheap, and they prove the workflow before the big design work starts.

### Batch 3 — the redesigns

Three clones, then the plain pages the owner picks from `design.md`. Not a batch that runs in
parallel: each page needs one idea from its subject — a thermal gradient, a punched card, a lamp —
used in the band, the hero and one accent.

### Batch 4 — the 26 landings

Nineteen of them are kits and engines, so the page explains an API rather than selling an app. The
rest: `neon-velocity` (Godot), `drsamonline` (profile), `drsamonline.github.io` (the hub), and the
four `infra` repos the owner has not ruled on yet.

### Batch 5 — the four splits

`app-organon-reader` (needs a landing page: large serif type, Hahnemann's portrait, committed
locally), `seance` (the feature does not work — see §4), `today-card` (buttons and design), and
`app-lantern`, which is no longer a split but an application (§5).

### Batch 6 — Seance and Today Card, properly

**Seance.** `CryptoKit` is never defined — `app.html` calls `CryptoKit.sealString` and
`CryptoKit.openString`, and the only script it loads is `web-kit.js`, which has no `CryptoKit`. Seal
and Open throw. So: bundle crypto-kit, then build the send-and-open path in four ways — copy the
sealed text, download a `.seance` file, a share link with the payload in the URL fragment, a QR — and
make "opens once" honest (today it is a `localStorage` flag on the opening device). Then redesign
both surfaces and re-shoot.

**Today Card.** The four buttons have handlers and `web-kit.js` exposes the APIs they call, so the
failure is at runtime: headless-click each one, record what fails, fix it. Then one matching design
for app and page, and re-shoot.

### Batch 7 — the last two, by instruction

`musicgen` and `Scrap-and-Gun` go **last**. Both are finished pages, so what is left is the block, the
badges, and two two-word fixes they share: the "In the browser" card links to a doubled `play/play/`
path that has nothing behind it, and both declare a favicon at `play/icon.svg` that does not exist.

---

## 4. What is decided, and what is accepted

| decision | effect |
|---|---|
| **shields.io badges are deliberate** | measured, reported under `accepted`, out of the work list. `--strict` puts them back. |
| **Apple targets bill nothing** | 6 repos keep their `.dmg`; reverses if a repo goes private |
| **kits and engines** | landing + badges + support block. No demo, no release build |
| **hubs** | `neon-games`, `aethelgard-games` launch apps that live elsewhere; no `docs/play/` of their own |
| **Forge tooling** | `dashboard`, `control-panel`, `app-companion-forge`, `audit` need no public face |
| **`skills`** | stays public and keeps its page |
| **musicgen, Scrap-and-Gun** | finished; last in the queue |

---

## 5. Lantern — the application, as a batch of its own

`app-lantern` is no longer a landing-page job. It is the first app in the family to grow a **shell**:
two doors, folder sharing, discovery with a fallback, access modes, a shelf and a reader. The shell
is the reusable part — a photo gallery or a music streamer later is a new shelf and a new viewer, not
a new server.

**Surfaces.** The landing page stays at `docs/index.html`, untouched in design. The app is its own
thing at `docs/play/`, carrying the same lamp — the same `icon.svg`, at the same size, with the glow
and the flicker.

**v1 scope — frozen.** Nothing outside this list goes in.

1. one app at `docs/play/`, landing page separate, same lamp;
2. first screen: **Share my books** / **Read books**, with libraries already found shown;
3. share: folder picker, per-folder counts (readable / name-only), pause and remove;
4. discovery: mDNS by default, six-digit code and QR as the fallback;
5. shelf: derived titles, format on the spine, reading position per book per device, search;
6. reader: HTML/MD/TXT native, PDF and EPUB through **vendored** `pdf.js` and `epub.js`, images
   zoomable, one set of controls for all of them;
7. access: **Anyone on this Wi-Fi** or **Only people I let in** (code + QR + an approval list that is
   the allowlist); download: **read-only** or **allow download**, per library;
8. builds: HTML, Windows and Linux (Electron around the existing server), Android reader (TWA);
9. the format table and the honest read-only paragraph on the page.

**Build order.** Shell (app at `docs/play/`, two doors, folder picker on real folders) → server modes
(access + download, because the shelf depends on them) → shelf → reader (the vendored viewers last,
largest and most self-contained) → builds (Electron, then TWA).

**The read-only promise, stated honestly.** What it does: no download route at all, the reader
intercepts the context menu and `Ctrl/Cmd+S/P/C/A/U`, the packaged app has devtools off and no File
menu, and each session can stamp a traceable mark. What it cannot do: stop a photograph of the screen,
stop a browser's devtools reading the response, or stop `curl` from a machine that knows the address.
So read-only is **a promise to honest readers, not a lock**. The measures that genuinely raise the bar
are the approval list and an optional device allowlist.

**Platforms.** HTML, Windows, Linux, Android-reader. **No Android host** — serving needs a Node
runtime on the phone, and the point is one cheap computer serving the room. No Apple builds, per the
estate.

**Still open:** the watermark default — proposal: on in *Only people I let in*, off in *Anyone on this
Wi-Fi*.

---

## 6. Parked, deliberately

- **A tiny FTP/HTTP file server** that lists everything shared and lets people pull it down. Not a new
  app: it is Lantern's *allow download* mode with the shelf drawn as a file list. Build it there.
- **A photo gallery server, a music streamer, a video/classroom cast, a photo drop, an
  app-and-installer shelf, handout distribution with receipts.** All one server core plus a viewer
  per media type. `lan-kit` is already that core. Lantern's shell is the prerequisite; none of them
  starts before it exists.

---

## 7. The order

    Batch 0  rules, gate, install block            ← we are here
    Batch 1  the estate-wide paste   (98/94/90/85/45 repos)
    Batch 2  repertory-reader and the cheap set
    Batch 3  the redesigns           (3 clones + the pages the owner picks)
    Batch 4  the 26 landings
    Batch 5  the 4 splits
    Batch 6  Seance and Today Card, properly
    Batch 7  musicgen and Scrap-and-Gun, last
    ———      Lantern v1 runs alongside Batches 1–2, because it is an application, not a paste

Lantern is the one long-running piece, so it starts early and finishes when it finishes; the estate
batches are mechanical and can be interleaved without holding it up.
