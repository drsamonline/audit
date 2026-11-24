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

---

# Row 0.4 — the ceiling, measured

The row asked for a probe before any rewrite: 188 sequential fetches against 188 concurrent ones.
`tools/fetch-cost.cpp` does that against a loopback server modelling 20 ms of round trip.

| workers | time | speedup |
| --- | --- | --- |
| serial | 4,153 ms | 1.0x |
| 2 | 2,058 ms | 2.0x |
| 4 | 1,041 ms | 4.0x |
| 6 | 705 ms | 5.9x |
| 8 | 545 ms | **7.6x** |

Essentially linear, with serial on the arithmetic floor (188 x 20 = 3,760 ms). On the real page, whose
fetches cost ~300 ms each, 57.8 s becomes roughly **8 s**.

## Two probes that measured the wrong thing first

1. **The server answered one connection at a time** — accept, sleep, reply, loop — so concurrency
   bought nothing and x2 read 4,200 ms. That was a fact about the server. Replaced with a 16-thread
   pool.
2. **One thread per connection** hit this box's thread limit at 376 threads ("Resource temporarily
   unavailable" — already a known trap in this project).

Both would have produced a confident wrong number.

## Why the probe is raw sockets

The first version called `HttpClient::get()` from several threads, which races on the cookie jar,
response cache and connection pool — all function-local statics. Making them `thread_local` was
written and measured, then **reverted**: verifying it needs a full rebuild, and the pod's recycled
CMake cache put that at ~40 minutes. Unverified engine code is not committed to save a compile, so the
`thread_local` change ships with the fix instead.

## Why the fix is not a loop swap

`SecureResourceLoader::load()` writes through to the shared `ResourceCache`, so only the network part
can run concurrently; and `HttpClient`'s three statics must become per-thread first. Row 0.4 stays
open with both named.
