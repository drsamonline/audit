# The design audit: 74 landing pages, how many are actually different

The owner's rule: **a landing page must be its own design, and a landing page is mandatory even where there is no live app.** This measures how far the fleet is from that.

## What I measured

For each of the 74 pages: the CSS class tokens it uses, every hex colour declared in its `<style>` block, its font stacks, and its `<h2>` sequence. Similarity is the Jaccard overlap of those token sets, weighted with the heading sequence and the page size. Two pages built from the same template score above 0.6; two pages with the same subject and different designs score around 0.25.

## The finding

**Six pages are two designs, repeated three times each.**

| cluster | score | repos |
|---|---|---|
| Scrap-and-Gun / dashboard / musicgen | 0.76–0.78 | `Scrap-and-Gun`, `dashboard`, `musicgen` |
| BLINKTRANSFER / blinkcode-ai / helioprism | 0.56–0.66 | `BLINKTRANSFER`, `blinkcode-ai`, `helioprism` |

The first three share the heading sequence *What it does / Three ways to run it / Privacy*, three sections and no declared colours at all. The second three share *Why it is different / How it works / Free for people, licensed for business*. These are not three projects that happen to look alike — they are one page, edited three times. The second group is the same product family (optical file transfer), so one shared look there is defensible; the first group is a game, a dashboard and a music app, and it is not.

**15 more pages are plain** — few sections, few colours, no display face of their own:

`Matneo`, `Scrap-and-Gun`, `app-clip-loom`, `app-organon-reader`, `app-weft-puzzles`, `audit`, `control-panel`, `dashboard`, `musicgen`, `seance`, `today-card`, `weft8-classroom`, `weft8-compare`, `weft8-hardware`, `weft8-kit`

**5 still carry the skeleton's own heading** (*What it refuses to do*), which means the section order is the template's rather than the project's:

`app-jacquard`, `canteen-lan`, `chalk-lan`, `corefit-md`, `kent-repertory-explorer`

`lumen`, `app-thermals`, `repertory-reader` and `app-image-toolkit` carry that heading too, and are the standard rather than the problem — the heading is fine, the same nine sections in the same order with the same colours is not.

## The 26 pages that do not exist yet

These have no `docs/index.html`. Every one of them is a new design, not a port of an existing one — and for the 18 kits among them, the page has to explain an API rather than sell an app.

`HCS`, `art-kit`, `astro-kit`, `audio-kit`, `backup`, `book-kit`, `case-kit`, `compfactory`, `compress-kit`, `crypto-kit`, `drsamonline`, `drsamonline.github.io`, `export-kit`, `frame-kit`, `game-kit`, `heavenzip`, `lan-kit`, `ml-kit`, `neon-velocity`, `optical-kit`, `repertory-kit`, `search-kit`, `srs-kit`, `ui-kit`, `web-kit`, `ziptastic`

## What "its own design" means here

Not a different colour on the same layout. The test, from the skill:

| | the app (`docs/play/`) | the landing page |
|---|---|---|
| canvas | warm paper | dark, or a colour the app never uses |
| type | the app's own face | a display face the app does not use |
| rhythm | one centred column | full-bleed bands, a light interlude, a closing CTA |
| the product | is the interface | is shown inside a frame, with callouts |

And one idea taken from the subject, used in the band, the hero and one accent: a thermal gradient for `app-thermals`, a punched card for `app-jacquard`, a lamp for `app-lantern`. A page that cannot name its idea is a page with a default palette.

## How to check one

```
python3 tools/presentation_audit.py <parent-dir> --design
```

It prints the two clone clusters, the plain pages and the skeleton descendants, so the answer is a measurement rather than a memory.
