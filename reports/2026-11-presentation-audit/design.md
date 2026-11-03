# The design audit: 74 landing pages, and how many are actually different

The rule from the owner: **a landing page is mandatory for every repo, and each one must be its own design.** Two pages built from the same template are not two designs.

## What I measured

For each of the 74 pages: the CSS class tokens it uses, every hex colour declared in its `<style>` block, its font stacks, and its `<h2>` sequence. Similarity is the Jaccard overlap of those token sets, weighted with the heading sequence and the page size. Pages built from one template score above 0.55; two pages with the same subject and different designs sit around 0.25.

## Decided: three pages get their own design

`BLINKTRANSFER`, `blinkcode-ai` and `helioprism` measure as one design (0.56–0.66, the same heading sequence). They are the same product family, and the owner's ruling is that all three still get their own:

| page | similarity |
|---|---|
| `blinkcode-ai` / `helioprism` | 0.658 |
| `BLINKTRANSFER` / `blinkcode-ai` | 0.586 |
| `BLINKTRANSFER` / `helioprism` | 0.555 |

Two more sets measured as clones and are **not** work:

- `Scrap-and-Gun` / `dashboard` / `musicgen` (0.76–0.78) — `musicgen` and `Scrap-and-Gun` are finished pages, and `dashboard` is Forge tooling that needs no public face at all.

## The plain pages

15 pages measure as plain — few sections, few colours, no display face of their own. Five of them are exempt for the same reasons (`musicgen`, `Scrap-and-Gun` are finished; `dashboard`, `control-panel` and `audit` are Forge tooling). That leaves **10 to judge**:

| page | sections | colours | type of its own |
|---|---|---|---|
| [app-clip-loom](https://drsamonline.github.io/app-clip-loom/) | 3 | 10 | **no** |
| [app-organon-reader](https://drsamonline.github.io/app-organon-reader/) | 1 | 24 | **no** |
| [app-weft-puzzles](https://drsamonline.github.io/app-weft-puzzles/) | 1 | 8 | **no** |
| [Matneo](https://drsamonline.github.io/Matneo/) | 8 | 0 | **no** |
| [seance](https://drsamonline.github.io/seance/) | 0 | 16 | **no** |
| [today-card](https://drsamonline.github.io/today-card/) | 0 | 15 | **no** |
| [weft8-classroom](https://drsamonline.github.io/weft8-classroom/) | 3 | 7 | **no** |
| [weft8-compare](https://drsamonline.github.io/weft8-compare/) | 3 | 11 | **no** |
| [weft8-hardware](https://drsamonline.github.io/weft8-hardware/) | 3 | 10 | **no** |
| [weft8-kit](https://drsamonline.github.io/weft8-kit/) | 3 | 11 | **no** |

## Still carrying the skeleton's own heading

These five kept the template's section order — *What it refuses to do* is the skeleton's heading, not theirs:

| page |
|---|
| [app-jacquard](https://drsamonline.github.io/app-jacquard/) |
| [canteen-lan](https://drsamonline.github.io/canteen-lan/) |
| [chalk-lan](https://drsamonline.github.io/chalk-lan/) |
| [corefit-md](https://drsamonline.github.io/corefit-md/) |
| [kent-repertory-explorer](https://drsamonline.github.io/kent-repertory-explorer/) |

`lumen`, `app-thermals`, `repertory-reader`, `app-image-toolkit`, `musicgen` and `Scrap-and-Gun` carry that heading too and are the standard, not the problem — the heading is fine; nine sections in the same order with the same colours is not.

## The 26 pages that do not exist yet

Every one is a new design, not a port:

`art-kit`, `astro-kit`, `audio-kit`, `backup`, `book-kit`, `case-kit`, `compfactory`, `compress-kit`, `crypto-kit`, `drsamonline`, `drsamonline.github.io`, `export-kit`, `frame-kit`, `game-kit`, `HCS`, `heavenzip`, `lan-kit`, `ml-kit`, `neon-velocity`, `optical-kit`, `repertory-kit`, `search-kit`, `srs-kit`, `ui-kit`, `web-kit`, `ziptastic`

## What "its own design" means here

| | the app (`docs/play/`) | the landing page |
|---|---|---|
| canvas | warm paper | dark, or a colour the app never uses |
| type | the app's own face | a display face the app does not use |
| rhythm | one centred column | full-bleed bands, a light interlude, a closing CTA |
| the product | is the interface | is shown inside a frame, with callouts |

And one idea taken from the subject, used in the band, the hero and one accent: a thermal gradient for `app-thermals`, a punched card for `app-jacquard`, a lamp for `app-lantern`.

## How to check one

```
python3 tools/presentation_audit.py <parent-dir> --design
```
