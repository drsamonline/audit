# Aetheris — a generic family had no face, so every page was set in the embedded DejaVu

**Row:** `0.22` closed. **Date:** 2026-11-28.

css-fonts-4 §2.1: `sans-serif` is not a font, it is a request to the platform. `font_for_family` in
`src/rendering/font_library.cpp` looked in the engine's own face registry and then at the embedded face, so a
generic name resolved to nothing and every page whose `body` said `sans-serif` — which is nearly every page — was
set in the embedded **DejaVu Sans** whatever the machine had installed.

The generics now resolve to the files fontconfig answers with on a Debian desktop, in preference order, cached under
the generic's own name, with the embedded face still the fallback:

| generic | first candidate | second candidate |
| --- | --- | --- |
| `sans-serif`, `system-ui` | `noto/NotoSans-Regular.ttf` | `liberation/LiberationSans-Regular.ttf` |
| `serif` | `noto/NotoSerif-Regular.ttf` | `liberation/LiberationSerif-Regular.ttf` |
| `monospace` | `dejavu/DejaVuSansMono.ttf` | `liberation/LiberationMono-Regular.ttf` |

## Which face each engine actually uses

Same string, `A web browser, often abbreviated as browser, is an application`, 14px, `white-space: nowrap`, both
engines at 1024x768, rightmost dark pixel on each line. The advance column is PIL's for the same string at 14px.

| family | chromium | engine, before | engine, after | PIL advance | face |
| --- | --- | --- | --- | --- | --- |
| `sans-serif` | **385** | 440 | **405** | Noto Sans **406.83** | engine: Noto Sans · chromium: Liberation Sans |
| `serif` | **349** | 440 | **416** | Noto Serif **417.95** | engine: Noto Serif · chromium: Liberation Serif |
| `monospace` | **519** | 440 | **520** | DejaVu Sans Mono **522.16** | both: DejaVu Sans Mono |
| `'Noto Sans'` | 405 | 440 | 440 | 406.83 | by-name faces do not resolve — embedded |
| `'Liberation Sans'` | 385 | 440 | 440 | 386.66 | by-name faces do not resolve — embedded |
| `'DejaVu Sans'` | 439 | 440 | 440 | 441.61 | embedded |
| `'Noto Serif'` | 416 | — | 440 | 417.95 | chromium resolves it; the engine does not |
| `'Liberation Serif'` / `'Times New Roman'` | 349 / 349 | — | 440 | 350.77 | chromium: its own default names |
| `Arial` / `Helvetica` | 385 / 385 | — | 440 | Liberation Sans 386.66 | fontconfig substitutes Arial → Liberation Sans |

## The 20px is the reference browser's stack, not a measurement error

The engine's `sans-serif` measures **405 ink against a 406.83 advance** — the last glyph ends 1.8px short of its
advance, which is what exact looks like — and chromium's own `'Noto Sans'` line also measures **405**. The loader is
not the problem and neither is the shaper: `monospace` agrees to **1px** (519 vs 520).

Chromium does not use fontconfig's generic resolution for `sans-serif` or `serif`. It reaches them through its
**default family names** — `sans-serif` through Arial, which fontconfig substitutes to Liberation Sans
(385 = its `Arial` = its `'Liberation Sans'`), and `serif` through Times New Roman, likewise Liberation Serif
(349 = its `'Times New Roman'` = its `'Liberation Serif'`) — while agreeing with fontconfig on `monospace`. That is a
private font stack.

Following fontconfig is upstream's policy, not a local preference: `SystemFontMatcher.h:44` declares
`resolve_generic_family` as "The installed family for a generic family, such as 'sans-serif'", and
`SystemFontMatcherDirectWrite.cpp:264-266` records that DirectWrite "has no families for the generic families,
unlike fontconfig" — which is why the hardcoded table lives in the Windows backend. On Linux fontconfig **is** the
mechanism. Matching 385 would mean copying chromium's stack. Recorded, not chased.

**Correction to an earlier note in this session:** the comment that went into `font_library.cpp` first said the
browser's default `sans-serif` on this machine is Noto Sans. That was an inference from `fc-match`, and measurement
says otherwise — `fc-match sans-serif` answers Noto Sans, but the reference browser does not. The comment now says
what was measured.

## What it buys on the reference page

wikipedia `Web_browser`, self-contained, 1024x768, agreement sampled every 4px. The HTML was **421,818 bytes** and
its two stylesheets **215,769 bytes** this session.

| | pixel agreement | |
| --- | --- | --- |
| `main` (1762de2b) | 41672/49152 | 84.8% |
| `wip/row-0.22-system-font` alone | 41885/49152 | **85.2%** |
| font fix + `wip/row-0.21-line` (892a9ec3) | 41924/49152 | **85.3%** |

Per 64px band, `main` / font-only / font+0.21:

| band | main | font only | font + 0.21 |
| --- | --- | --- | --- |
| y0-63 | 88.7% | 88.6% | 88.6% |
| y64-127 | 97.4% | 97.4% | 97.4% |
| y128-191 | 92.6% | 92.6% | 92.6% |
| y192-255 | 98.0% | 97.9% | 97.9% |
| y256-319 | 94.7% | 94.9% | 94.9% |
| y320-383 | 80.3% | 81.2% | 81.2% |
| y384-447 | 92.3% | 92.0% | 92.0% |
| y448-511 | 82.5% | 79.4% | 78.9% |
| y512-575 | 77.8% | 80.1% | 81.1% |
| y576-639 | 80.4% | 77.0% | 77.4% |
| y640-703 | 50.5% | 51.1% | 51.2% |
| y704-767 | 82.2% | 90.3% | 90.3% |

One band goes down (y448, 82.5 → 79.4) and it is a face choice, not a placement error: that text is now set in a
face whose line breaks differ from the reference's. The gain is small because most of the page's text is already in
faces it names — the change matters because the **default** face is now the machine's.

The combined number confirms the 85.3% measured on the previous pod; the 84.8% baseline reproduces exactly
(41672/49152).

## Two defects found in review, and fixed

1. **The candidate list was a list only for missing files.** `system_font_path` returned the first candidate that
   *existed* and `resolve` loaded only that one, so a present-but-unparseable Noto Sans dropped straight to the
   embedded DejaVu without ever trying Liberation Sans. Every candidate is now attempted until one loads.
2. **A failed load was not cached.** A ~500KB file was read and parsed again on every `font_for_family` call, i.e.
   once per text run, on any page naming a family the machine does not have. Failures are now remembered, with the
   face registry still consulted first so a later successful registration wins.

Both are behaviour-preserving on this machine, verified rather than assumed: the fixture still measures
405 / 416 / 520, the reference page still 85.2% (41885/49152), and the comma fallback still works —
`'No Such Face', sans-serif` measures 405. Suite **67/67 twice** (205.27 s, 197.90 s) after the fixes.

## Not done

System families are still not registered by their real names, so `font-family: 'Noto Sans'` on a page still lands on
the embedded face; only generic names resolve. And nothing reads the machine's font configuration — a machine with
neither Noto nor Liberation still gets DejaVu, silently.
