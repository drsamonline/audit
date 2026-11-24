# Aetheris — the black boxes were two colour bugs

**Row:** `0.8`. **Date:** 2026-11-24.

The row asked for three fixtures over a red parent: no background, `transparent`, and
`rgba(0,0,0,0)`. The first two showed the parent's red; the third painted **black**.

## Bug one: no rgb()/rgba()

`Color::parse` handled named colours, `#rgb`, `#rrggbb`, `#rrggbbaa` and `transparent` — and nothing
else. Every `rgba()` background on a real page failed to parse, and a real page uses them for most of
its backgrounds. Both functions now parse: integer or percentage channels, alpha as a 0–1 number or a
percentage, and a `/` separator.

## Bug two: unparseable meant opaque black

`PaintExecutor::command_color` was `value_or(Color{0,0,0,255})`, so anything the parser did not
understand became a black box over the page. CSS drops an invalid declaration instead, so fills now
fall back to **fully transparent** and text keeps black.

| fixture | before | after |
| --- | --- | --- |
| no background | parent red | parent red |
| `transparent` | parent red | parent red |
| `rgba(0,0,0,0)` | **black** | parent red |
| `rgba(0,0,255,0.5)` over red | — | **(127,0,128)** |
| `rgba(0,0,255,50%)` over red | — | **(127,0,128)** |

The real page's black boxes are gone: the contents sidebar renders white with a rule under its heading.

## The flake

`WindowCore` and `WindowGeometry` failed once in a full run — "the frame after Tab is readable" — and
passed on re-run and on the next full run. They drive the browser binary and read a frame, so they
flake on a busy pod. Three suite runs were done to get two clean passes (133.63 s, 181.29 s) rather
than one green run and a claim.
