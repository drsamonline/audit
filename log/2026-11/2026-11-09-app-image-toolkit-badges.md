# Image Toolkit — the numbers the repository publishes about itself

Date: 2026-11-09
Repo: `drsamonline/app-image-toolkit` · branch `fix/badges-are-computed` · PR #3
(open, not merged)
Reference links taken: none — see "What I deliberately did not do"
Same session: `2026-11-09-offline-pdf-toolkit-cli-refusals.md`,
`2026-11-09-feather-router-signatures.md`,
`2026-11-09-cldr-conventional-commits.md`

## What I looked at

`scripts/badges.py`, `docs/assets/badge-*.svg`, `README.md`, `docs/index.html`,
`test-node.js` (including its offline rule), `CHANGELOG.md`, `.github/workflows/test.yml`.
The engine (`docs/play/imgtool.js`) was read for defects as well.

## What was wrong

Three numbers described one test suite and none agreed:

    docs/assets/badge-tests.svg   tests: 206 passing
    README.md                     alt="tests: 162 passing"
    docs/index.html               alt="tests: 84 passing"
    node test-node.js             207 passed, 0 failed

And the deps badge was wrong in the other direction. `runtime_deps()` counted
every `https?://` in `docs/play`, so the support block's three `<a href>`
anchors — Ko-fi, PayPal, the bookstore — counted as runtime dependencies. The
committed badge says `0 runtime`, which is the truth; the *script* would have
rewritten it to `3` the next time anyone ran it. `test-node.js` already had the
right rule, with a comment saying why ("an anchor is not a network dependency").
The two disagreed and nothing checked.

`badges.py`'s own docstring: "The number the suite actually prints — never a
number typed from memory." The alt text was typed from memory.

## What I changed

- `runtime_deps()` counts what the browser *fetches on its own*, the same rule as
  the offline test: `src`/`srcset`/`poster`, `<link href>`, CSS `url()`,
  `@import`, `importScripts`, plus `fetch(`/`XMLHttpRequest` outside `sw.js`,
  plus a `package.json` if one appears. It reads 0.
- `badges.py` writes the badge **and** the alt text in `README.md` and
  `docs/index.html` from the same run.
- A step in `test.yml` regenerates the badges and fails on any diff, the way the
  VERSION check already works.

## Evidence

Local, both directions:

    $ python3 scripts/badges.py
    wrote docs/assets/badge-tests.svg -> 207 passing
    wrote docs/assets/badge-deps.svg -> 0 runtime
    wrote README.md -> tests: 207 passing, deps: 0 runtime
    wrote docs/index.html -> tests: 207 passing, deps: 0 runtime

    $ python3 scripts/badges.py && git diff --exit-code -- docs/assets README.md docs/index.html
    STEP WOULD PASS (exit 0)            # idempotent on a clean tree

    # badge hand-edited back to 206 → the same step exits non-zero

In CI, run 42627035143, every step green:

    4 The engine — sniff, strip, resize, budget: success        207 passed, 0 failed
    5 The app ships what it says it ships: success
    6 The scripts still run, and the version is in sync: success
    7 The badges, and the alt text beside them, …: success      wrote … 207 passing / 0 runtime
    8 The app in a browser: success

**The first run of the same tree failed**, at `scripts/shot.py:143` —
`RuntimeError: Chromium did not open a debugging port` — before any page loaded.
An empty commit was pushed to get a second run of identical code; that run
passed end to end. Recorded because "it went green" and "it went green the
second time" are different claims, and the difference is a launch race in the
browser harness that will bite again. The app's own runs on `main` show the same
intermittency (42341804011 and 42353599556 failed on 2026-11-07).

## What I deliberately did not do

- **No version bump.** `VERSION` stays 1.3.2; the entry sits under `Unreleased`
  and names the assertion count, as the changelog's own rule asks.
- **One engine defect found, not fixed here.** `outName(".hidden", "webp")`
  returns `-min.webp`: `replace(/\.[^.]+$/, "")` treats a leading dot as an
  extension, so a dotfile loses its name and the output starts with a hyphen.
  Two lines plus a test, its own commit whenever it is wanted. Left out to keep
  this PR one idea.
- **No new link work.** Rejected, one line each: `libcaesium`,
  `caesium-image-compressor`, `imgo`, `imageflow`, `imager-io/imager`,
  `TinyPNG4Mac` — desktop or server compressors against an app that is one HTML
  page with zero dependencies. `oxipng`, `libjxl` — need a native binary or a
  decoder browsers do not have. `FLIF` — a dead format. `compressorjs`,
  `slimdeer` — canvas-based browser compressors doing what this app already
  does. `RgbQuant.js` — the one that genuinely fits (palette quantisation), but
  it needs a PNG *encoder*, and this app writes PNG through `canvas.toBlob`;
  that is a feature with a quality/UI decision behind it, not a slice.
  `Image-Compression-Benchmark` — a corpus and a method, no code.
  `topics/image-compression`, `awesome-wasm` — index pages.

## Next

Decide on PR #3. Two things are now visible and unowned: the `outName` dotfile
bug, and the intermittent Chromium launch in `scripts/shot.py` (which makes a red
run mean "try again" on this repo, and that is worth fixing before it hides a
real failure).
