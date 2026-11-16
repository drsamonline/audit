# Upstream-first, part two: prior art per innovation and a gate in every roadmap

Date: 2026-11-16 (twenty-first session) · Repos `drsamonline/{The_Browser,sorex,nodus,volumen}`
Commits: `fadcfcd` (sorex), `1f14899` (nodus), `e449dc7` (volumen), `fc20a064` (Aetheris)

Yesterday's entry wrote the rule into each repo as a document. This one puts it where the work is
actually decided: the innovation backlog and the phase gates.

## What I looked at

Each repo's `INNOVATIONS.md` and `ROADMAP.md`, then the vendored trees to confirm every path cited:
`sorex/src/{cache,actions,dilloc}.c`, `sorex/{lout,dw,dpi,dpid}/`; `nodus/content/{llcache.c,fs_backing_store.c}`,
`nodus/desktop/layout.c`, `nodus/frontends/monkey/`, `nodus/content/handlers/javascript/`;
`volumen/src/{GridText.c,HTML.c,LYForms.c}`, `volumen/WWW/Library/Implementation/{HTAccess.c,HTTCP.c}`.

Also checked the whole fleet for other browser repos, so "all" really means all: the only
browser-shaped repos are these four. `neon-engine`, `saga-vn-engine`, `aetheris-rpg-engine` and the
rest are game engines that run *in* a browser, not browsers.

## What was wrong

The rule existed as a document but nothing pointed at it from the two files that drive a session:

- `INNOVATIONS.md` listed 10-12 enhancements per repo with no mention that most of them have prior
  art in the vendored tree. A session reading it would design from the item text alone.
- `ROADMAP.md`'s P0 gate said "build green" and nothing about reading upstream first.
- Aetheris's roadmap had no gate at all.

## What I changed

- **`INNOVATIONS.md` gains "Prior art in this tree"** in all three family repos: every innovation
  mapped to the upstream file or directory that already does part of it. Dillo's memory ceiling points
  at `src/cache.c`; NetSurf's ABI work points at `include/` and its nine existing frontends; Lynx's
  structured dump points at the `src/HTML.c` callbacks that already see every element.
- **`ROADMAP.md` P0 now opens by requiring that read**, and asks each item's commit message to say
  what upstream does and what the fork changes. Aetheris's roadmap gets the same gate at its top.

## Evidence

    docs/UPSTREAM-FIRST.md, via the API:
      The_Browser 3060 B | sorex 3904 B | nodus 3803 B | volumen 3606 B
    roadmap gate reference present in:
      docs/ROADMAP.md (Aetheris), ROADMAP.md (sorex, nodus, volumen)  -> 1 each

    commits: fadcfcd, 1f14899, e449dc7, fc20a064

**Two verification mistakes, both caught and corrected in-session.** The first API check looked for
`docs/ROADMAP.md` in all four, but the family repos keep `ROADMAP.md` at the root — it reported zero
references everywhere and would have looked like the work had failed. The second: Aetheris's roadmap
has no `## P0 - Scaffold` heading to anchor to (it uses `## Done` / `## Remaining`), so the first patch
silently did nothing and `git commit` reported "nothing to commit". Both were caught because the
verification ran and disagreed with the claim.

## What I deliberately did not do

- **Did not write paths from memory.** Every file and directory in the three tables was listed with
  `ls` first. A map that is wrong is worse than no map.
- **Did not apply the rule to the game-engine repos.** They are not browsers and have their own
  upstreams; the instruction was about browsers.
- **Did not touch any vendored source.** Documentation and gates only.
- **Did not reopen the family builds.** Still blocked: no `make`, no `autoconf`, no dev headers.

## Next

1. P0 in the three family repos still needs a machine with dev packages — the prior-art tables are
   what a session should read the moment it can build.
2. Aetheris: `:focus-visible` from `should_indicate_focus()`, then scoped invalidation.
3. The landing page stays deferred until all four reach v1.0.
