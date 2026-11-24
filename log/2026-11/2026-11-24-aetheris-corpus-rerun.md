
---

# Row 0.5 — the engine was downloading the page's link graph

`tools/dep-cost.cpp` prints every discovered dependency with its resolved URL and where it came from.

| before | |
| --- | --- |
| discovered | **1,324** |
| distinct | 927 |
| duplicates | 397 over 140 URLs |
| most repeated | `Google_Chrome` 47x, `Firefox_version_history` 21x, `Pale_Moon` 19x |

Those are article hyperlinks. `discover_dependencies` took every `href`/`src` in the text with one
regex, so `<a href>` was a dependency.

## Fix one: walk tags

Skip `href` on `<a>`/`<area>`; keep `src` anywhere and `href` on `<link>`. **1,324 -> 102**.

## Fix two: what that exposed

With hyperlinks gone, the render loaded **0** resources - every URL was
`load.php?...&amp;...`. Attribute values were never HTML-decoded, so the page's own stylesheets had
never loaded; the old 188 "successes" were the hyperlinks. Decoding the five URL-relevant entities
took it from 0 to **41 real subresources**.

The page still looks unstyled - 41 stylesheets load, but this engine cannot reproduce Vector 2022.
The win is correct fetches, not fidelity.

## Row 0.6

Rendering `file://<path>` resolves every relative URL against `file://`, so the corpus harness has
never fetched a page's subresources. Every corpus measurement before today exercised markup, CSS and
layout with none of the page's own stylesheets, images or scripts.

## The stale pod

Mid-session the checkout was at `fed64d9c` while `origin/main` was `26a4ee55` - four commits behind.
Work saved as a patch, tree reset to `origin/main`, patch re-applied and rebuilt; the suite run
against the stale tree was discarded. Suite 67/67 twice on the correct base, 125.53 s and 125.82 s.
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

---

# Row 0.4 — concurrent subresources, and a premise wrong twice

`src/main.cpp` now fetches a page's subresources from a bounded pool (one worker per 16 dependencies,
capped at 8). Each worker builds its **own** `SecureFetcher` — a fetch writes into the cache, the
backend list and the policy, so sharing one would be a data race — and results are applied on one
thread in discovery order. `HttpClient`'s three statics are `thread_local`.

## What it bought: ~10%, not 7.6x

| | |
| --- | --- |
| probe (loopback, no gateway) | 7.6x at 8 workers |
| the page (through this sandbox's egress proxy) | ~10% |
| the proxy at 8-way, measured with curl | 5.0 s serial vs 2.0 s parallel = **2.5x** |

The ceiling here is the gateway, not the client. On a network without it the change is worth the
probe's figure.

## The premise was wrong twice

The row was written from "188 linked resources". Tracing the phases:

| phase | cost |
| --- | --- |
| discover + fetch | **~47 s** (1,324 dependencies) |
| `create_scripted_document` | ~14.4 s |
| paint | 68 ms |

188 is how many resources **load**; the page **discovers 1,324**. The "188 x 300 ms = 57 s" arithmetic
that motivated the row was a coincidence.

## How the wrong reading survived

Removing `<link>` changed nothing; removing `<script>` changed nothing. That looked like proof the
fetches were not the cost. It was not — the dependencies come from the stylesheet's `url()` references
as much as from the markup, so the tags were irrelevant. Both runs still printed "188 linked
resources", which was the clue that was read past.

A phase timing printed by the program is evidence. A variant of the input that "should" have removed
the work is a hypothesis.

## Left open

Row **0.5**: 1,324 discovered vs 188 loadable — 1,136 requests for resources that are not there.
Suite 67/67 twice, 147.41 s and 125.84 s.

---

# Row 0.6 — the corpus rendered files, not pages

`tools/run-corpus.sh` rendered `file://<local path>`, so every relative URL resolved against
`file://` and the corpus never fetched a page's own stylesheets, images or scripts. Every measurement
in the corpus report before today tested markup, CSS and layout with none of the page's assets.

It now renders **from the URL**, with curl-and-a-local-copy kept as the fallback for a host the proxy
refuses.

| site | mode | subresources |
| --- | --- | --- |
| `example.com` | url | 0 (it has none) |
| `en.wikipedia.org/wiki/Web_browser` | url | **42** |
| `www.debian.org` | url | **26** |
| the other 17 | — | refused by the proxy |

## Two reporting faults

1. **A refused host was reported as "rendered".** The proxy's 225-byte 502 body was fetched, written
   to disk and rendered as though it were a site — 17 of 20 lines said "rendered" for hosts that
   never loaded. A non-2xx is `refused` now.
2. **The subresource count was missing**, and it is what separates a real render from a body of text.

A summary line that says "ok" is a claim. Suite 67/67 twice, 125.29 s and 129.43 s.

---

# Row 0.5's tail — unfetchable schemes and `<base href>`

Two named remainders, both small because the diagnosis was already precise.

**47 of the 102 remaining dependencies were `mw-data:TemplateStyles:r...`** — a Wikipedia-internal
pseudo-scheme that no backend can serve, one per transcluded template style. Discovery now queues only
`http`, `https`, `file` and `data`.

**`<base href>` was ignored**, so a document that rebases was resolved against the request URL. The
first `<base href>` is the resolution base now.

| | discovered |
| --- | --- |
| before row 0.5 | 1,324 |
| after skipping hyperlinks | 102 |
| after the scheme filter and `<base href>` | **44** |

The render still loads its **42** subresources — the count is unchanged, which is the check that
matters: fewer requests, same resources. Suite 67/67 twice, 131.82 s and 132.65 s.
