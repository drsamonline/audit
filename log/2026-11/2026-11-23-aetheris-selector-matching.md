# Aetheris — the style pass was re-parsing every selector for every node

**Row:** `3j` in `drsamonline/The_Browser` `docs/CHECKLIST.md`.
**Date:** 2026-11-23. **Commit:** the one that carries this entry.

## What was claimed, and what was measured

Row 3j said layout costs "~0.8 ms per element, and far worse on real markup", and told the next session to
profile before touching anything. Profiling split the three stages of building a document:

| document | parse | style | layout |
| --- | --- | --- | --- |
| 400 empty divs | 15.5 ms | **392 ms** | 34 ms |
| 800 empty divs | 19.6 ms | **514 ms** | 49 ms |
| 800 divs with text | 37.4 ms | **1089 ms** | 333 ms |

The row's premise held, but its label was wrong: this was never a layout cost. Style resolution was 10-20x
geometry at every size. A second sweep varied only the number of author rules, and style cost tracked
**rules x nodes** - 445 ms at 0 rules, 3862 ms at 800 rules, a slope of 10.6 us per (rule x node).

## The cause

`StyleResolver::matches_simple` took the selector as text and re-parsed it on every call, allocating five
containers and re-scanning the characters into them - work that depends only on the selector, redone once per
node. `matches()` additionally scanned for a combinator with a lambda that re-walked the selector from index 0
for every character: O(n^2) in selector length, per node per rule. Specificity was re-scored from the same
text on every match.

Upstream parses a selector into an object once (`LibWeb/CSS/Selector.h`) and matches that object
(`LibWeb/Rust/src/css/dom_selector_matching.rs:1262`). The fix ports that shape rather than inventing one.

## What was fixed

1. Selectors are parsed once, when the stylesheet is parsed (`src/rendering/selector.cpp`,
   `CssRule::compiled`). Matching walks the parsed compound; specificity comes with it.
2. `StyleProperties::fingerprint()` was rebuilt per node - a string per property, sorted, joined - because
   layout asks every node for its parent's digest. It is cached now, invalidated by `set()`.
3. The class test built an `istringstream` and a `vector<string>` from the `class` attribute per rule x node.
   It scans for word boundaries in place instead. `[a~=v]` likewise.

Fixes 2 and 3 were found by re-running the probe after fix 1 and noticing the per-node cost had barely moved.

## Result

| case | before | after |
| --- | --- | --- |
| 400 empty divs, style | 392 ms | **98 ms** |
| 800 empty divs, style | 514 ms | **201 ms** |
| 800 divs with text, style | 1089 ms | **446 ms** |
| 800 author rules, style | 3862 ms | **933 ms** |

0.8 ms per element became 0.24 ms. The suite's own wall clock fell from ~400 s to **141.52 s / 139.62 s**,
`WindowGeometry` from 177 s to 81 s, with 66/66 green twice.

## What is not fixed

The per-node `StyleProperties`: an `unordered_map<string, string>` filled by ~80 string insertions for every
node. It is now most of what remains of the style pass. Row 3j stays `[~]` in progress rather than `[x]`.

## The mistake

The refactor was first assembled by slicing the original file with hand-computed line ranges; two were off by
one, and regenerating from `git show HEAD:` silently reverted two earlier edits. Both were re-applied and
grepped before building. Print and read the boundary before slicing source by line number.

---

# Addendum — the second term, and a fix that measurement rejected

Row 3j stayed `[~]` after the selector work, naming the per-node `StyleProperties`. This addendum
measures that term. **No engine code changed**: the fix that looked obvious measured worse.

## What a style is

`tools/style-cost.cpp` counts what a resolved style holds and splits the resolve.

| measurement | value |
| --- | --- |
| properties in a resolved style | **17** (the previous entry's "~80" was a guess) |
| resolve, full sheet | 0.114 ms per element |
| resolve, sheet with no rules at all | 0.074 ms per element — **65%** |
| so selector matching | 0.040 ms per element — 35% |

The property work is not a remainder; it is the larger half of what is left.

## The rejected fix

The map rehashes as it grows, so reserve it. Priced alone: 0.039 ms per style, 0.005 ms with
`reserve(24)` — 8x on the component that is 65% of the cost.

Built alternately, five runs each, on the targeted measure:

| build | runs | median |
| --- | --- | --- |
| with `reserve(24)` | 0.068 / 0.063 / 0.069 / 0.064 / 0.059 ms | 0.064 ms |
| without (HEAD) | 0.048 / 0.048 / 0.075 / 0.047 / 0.048 ms | **0.048 ms** |

The reserve is **33% slower**. `StyleProperties` is not one object per element: text nodes, generated
boxes, pseudo-element styles and the temporaries inside `apply_declaration` all construct one, and
most hold a property or two. Reserving 24 buckets makes every one of them pay for a table it never
fills, which costs more than the rehashes it saves on the styles that reach seventeen.

Reverted; `git status` clean before the commit.

## What is left

Structural, not tuning: a style is seventeen string-keyed inserts into a hash map. The honest fix is
a typed property set or interned property ids, touching every consumer of `StyleProperties`.

## The measurement discipline this bought

Identical suite runs: 126.97 s and 164.79 s back to back. One probe line: 0.047 to 0.075 ms across
five runs. Anything smaller than ~20% is not measurable on this box — which is why the decision came
from an alternating build rather than a single before/after pair, and why it went against the
prediction.

---

# Row 0.3 — the engine's HTTP client had no proxy support

Created by the corpus run: the sandbox reaches the internet through an HTTP proxy, `curl` worked, and
`aetheris --fetch https://example.com` said "could not connect". Closed on 2026-11-23.

## The proof is the fetch that failed

```
$ ./build/bin/aetheris --fetch https://example.com
OK https://example.com
  Bytes: 577
```

577 bytes is what `curl` returns for that page, so the body is the origin's. `http://example.com`
also works, in absolute form, and `--fetch http://127.0.0.1:9/` still says "Could not connect to
127.0.0.1", which is `no_proxy` being honoured rather than the proxy being ignored.

## Shape

Upstream read first: `LibHTTP/Proxy.h` (a proxy is type + host + port + userinfo), `Proxy.cpp:18`
(parse), `:149` (environment, libcurl precedence), `:186` (`proxy_for`), `:252` (`is_excluded`).
Ported to `include/aetheris/network/proxy.hpp`.

| request | path |
| --- | --- |
| https | TCP to proxy → `CONNECT host:443` + `Proxy-Authorization` → 2xx → TLS **inside** the tunnel, verifying the origin's certificate |
| http | TCP to proxy → absolute-form request target + `Proxy-Authorization` |

`TlsStream::connect_over(fd, host, ca)` was added for the tunnel: it handshakes over an
already-connected descriptor, on a **duplicate**, so the `Socket` and the `TlsStream` each close what
they own.

Two upstream decisions kept deliberately: `HTTP_PROXY` is not read (CGI can set it from a request
header), and `no_proxy` matches a `.domain` plus its subdomains and ignores a port in the entry.

## How it is tested

`AetherisProxy` runs a loopback fake proxy that records the bytes sent, and asserts on the wire:

- `GET http://example.test/page HTTP/1.1` with `Proxy-Authorization: Basic …` and `Host:` intact;
- `CONNECT example.test:443 HTTP/1.1` with the credentials on the tunnel, and the resulting failure
  being a TLS failure rather than "Could not connect" — the exact distinction row 0.3 was about;
- the parse (socks5 and port 0/99999 refused, not silently treated as "no proxy"), the precedence,
  and every `no_proxy` form.

Suite 67/67 twice, 126.29 s and 135.57 s.

## Still open

`https://` proxies (TLS to the proxy) parse but are not connected through; SOCKS4/5 are refused;
`Proxy-Authorization` is Basic only. Row 0.1 remains blocked, now on the allowlist alone.

---

# Row 3j closed — and the number that started it was a build type

Every measurement in the two entries above was taken in a Debug `-O0` build with UBSan. This session
built `build-rel` (`-O2`) and asked the same questions again.

| measurement | Debug `-O0` | Release `-O2` |
| --- | --- | --- |
| resolve one element | 0.114 ms | **0.008 ms** |
| style pass, 400 empty divs | 392 ms | **4.2 ms** |
| style pass, 800 divs with text | 1089 ms | **38.2 ms** |
| 800 author rules | 3862 ms | **22.9 ms** |

The row's headline, "~0.8 ms per element", is a `-O0`-with-UBSan number: at `-O2` a 400-div page is
4.2 ms style + 1.6 ms layout, i.e. **14.5 us per element**. The fixes the row paid for stand — three
terms, each measured, suite 400 s -> 140 s — but the figure that motivated them was the build.

That also settles the `StyleProperties` refactor without doing it: at `-O2` the map is 0.004 ms per
style and the property path 0.003 ms of an 0.008 ms resolve. Rewriting every consumer to buy a
fraction of that is not a trade worth making, and a measurement is what says so.

## "Far worse on real markup" was true — and it is layout

Wikipedia prefixes, `-O2`, fetched through the proxy from row 0.3:

| bytes | elements | nodes laid out | style | layout |
| --- | --- | --- | --- | --- |
| 10,000 | 22 | 461 | 0.3 ms | 1.5 ms |
| 12,000 | 72 | 401,293 | 0.9 ms | 1,920 ms |
| 14,000 | 134 | **1,157,981** | 1.6 ms | **5,717 ms** |
| 18,000 | 238 | 1,204,549 | 3.0 ms | 5,763 ms |

A 2,500x jump then a plateau at ~1.2M: the shape of a per-character or per-fragment loop hitting a
limit, not of a large document. Ordinary markup in that range. Row **3k** carries it with the bisect
range and a first hypothesis (`overflow-wrap` from row 2f).

## The probe was broken and nobody noticed

`tools/layout-cost.cpp` looped `for (int i = 1; i + 1 < argc; ++i)`, so with one file argument it
measured nothing and printed nothing. Every earlier run passed no files, so the bug was invisible
until a real page was the point. Fixed to `i < argc`. A probe that prints nothing looks like a probe
with nothing to print.

---

# Row 3k — layout was doing every node twice, 2^depth times

The bisect from the previous entry found no single bad element: nodes grew smoothly and
superlinearly (10 KB -> 461, 12 KB -> 401,293, 14 KB -> 1,157,981). Stripping classes, `<style>`,
`<svg>` and `<img>` changed nothing; stripping the container divs collapsed it to 97.

A 40-element reproducer (`<div><span>level</span>` nested d deep) showed work **doubling per level**:
depth 4 -> 86 nodes, 8 -> 1,406, 12 -> 22,526. That is 2^d.

## Cause

`LayoutEngine::layout_inline_children` laid every child out twice — once at the whole line width to
discover its natural width, once to place it — and measured **block-level children too**, which have
no natural width because they fill the line. Each nesting level doubled the other's work.

## Fix

Measure only inline-level children; skip the second layout when the measured child already fits (a
shrink-to-fit box given more room than it needs produces the same geometry); place a block child once.

| case | before | after |
| --- | --- | --- |
| 40 elements, depth 12 | 22,526 nodes | **40** |
| wikipedia 14 KB, `-O2` | 1,157,981 nodes / 5,717 ms | **139 / 0.8 ms** |
| wikipedia 416,975 bytes, `-O2` | did not finish in 280 s | **67.9 ms** layout |

The whole page renders in the Debug app in 57.8 s and the PPM was inspected: it shows the real page
structure, so this is cheaper *and* correct.

## What the test taught

`AetherisAdvancedLayout` pins the linearity. Its first version also asserted that each nested block
sits below its parent; it failed because the engine legitimately places a nested block on its parent's
line. The assertion was rewritten, not the layout. Suite 67/67 twice, 143.39 s and 127.57 s.
