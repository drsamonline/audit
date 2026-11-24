# Aetheris — the corpus re-run: the page that did not finish now does, and the time is I/O

**Row:** `0.1` re-run in `drsamonline/The_Browser`; produced row `0.4`.
**Date:** 2026-11-24.

## What the re-run found

The sandbox's egress allowlist admits **three** of the twenty corpus sites now — `example.com`,
`en.wikipedia.org`, and `www.debian.org`, which was 502 on 2026-11-23. Seventeen still return 502 or
403 from the proxy, so row 0.1 stays blocked on the network.

The result that mattered changed. The first run recorded wikipedia's 416,975-byte page as *did not
finish in 280 s*; it now renders in **57.8 s**. That is row 3k's layout fix — the page was never slow
to parse or to style, it was laying out 2^depth nodes.

## The 57.8 s is not rendering

Two probes at `-O2` on the same page:

| stage | cost |
| --- | --- |
| parse | 43.7 ms |
| CSS parse (UA + the page's 12,331 bytes of `<style>`) | 1.6 ms |
| style, 7,581 elements against 137 rules | 905.5 ms |
| layout | 67.9 ms |

About **one second of compute**. The rest is **188 linked resources fetched one at a time**: 57.8 s
with the proxy set (fetches succeed) and 60.0 s with it unset (fetches fail) — the same wall clock
either way, at roughly 300 ms per resource. Waiting, not working.

## New tooling

`tools/css-cost.cpp` extracts a page's `<style>` blocks and prices them. `tools/layout-cost.cpp`
passes no author CSS, so the two measure different work and the earlier profile was missing the
page's own stylesheet.

## Row 0.4

A page's linked resources are fetched serially — now the largest term in loading a real page, and not
a rendering problem. Upstream fetches subresources concurrently through its event loop and a per-host
pool; this engine has neither. The row names a probe as the next step: 188 sequential fetches of one
local resource against 188 concurrent ones.

## Build state

No engine source changed: docs plus one probe. The pod was recycled between sessions, which dropped
the pip toolchain and invalidated the CMake cache, so `tools/check-build.py` reports the full rebuild
as pending. The commit is byte-identical to `fed64d9c` outside `docs/` and `tools/`, where the suite
last stood at 67/67 twice.
