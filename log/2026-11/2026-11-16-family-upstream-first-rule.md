# The browser family adopts "upstream first" as a written rule

Date: 2026-11-16 (twentieth session) · Repos `drsamonline/The_Browser`, `sorex`, `nodus`, `volumen`
Commits: `9da4628` (sorex), `3535fe6` (nodus), `9afac0f` (volumen), `174db915` + `8d19e9dc` (Aetheris)

The owner's instruction, after watching a day of Aetheris work loop on problems that were already
solved upstream: apply the same rule to every browser in the family. Done — as a document with a real
file map per codebase, not a slogan.

## What I looked at

Each vendored tree, to write a map that matches the code rather than my memory of it: `sorex/lout/`,
`dw/`, `dpi/`, `dpid/`; `nodus/content/handlers/{html,css,image,javascript}/`, `desktop/layout.c`,
`frontends/`; `volumen/src/GridText.c`, `src/HTML.c`, `src/LYForms.c`,
`WWW/Library/Implementation/`. And `Libraries/LibWeb` for the shared second reference.

## What was wrong

Three of the four browsers had no instruction at all about reading their own upstream, and the fourth
(Aetheris) had only a gotcha buried at item 7 of a handover. A new session on any of them would start
by designing from scratch, which is exactly what produced today's three reverted attempts.

## What I changed

`docs/UPSTREAM-FIRST.md` in all four repositories:

- **The rule**: find it upstream before designing; read the neighbouring frontends before growing a
  core API; say so in `DESIGN.md` when upstream has no answer; fix the function that drops the state,
  not the call site that notices it.
- **A feature-to-file map per codebase**, so "read upstream" has an address. Dillo's layout is
  `lout/`, NetSurf's is `desktop/layout.c`, Lynx's is `src/GridText.c`; the network is `dpi/` +
  `dpid/`, `content/fetch.c`, `WWW/Library/Implementation/` respectively.
- **A shared second reference**: Ladybird's `Libraries/LibWeb`, with the sparse-clone command, for
  anything interaction-shaped — focus, hover, `:active`, event bubbling, style invalidation.
- **The evidence**, so the rule is not just an opinion: on the Aetheris tier, three bugs were each
  machinery that existed with nothing feeding it, and every feature ported from LibWeb after reading
  it landed first time.

`AGENTS.md` and `START_PROMPT.md` in the three family repos now list it as step 0. Aetheris has
neither file — its entry point is `docs/HANDOVER.md`, so the pointer went at the top of that.

## Evidence

    docs/UPSTREAM-FIRST.md, via the API:
      The_Browser: 3060 bytes
      sorex:       3904 bytes
      nodus:       3803 bytes
      volumen:     3606 bytes

    commits: 9da4628 (sorex), 3535fe6 (nodus), 9afac0f (volumen),
             174db915 + 8d19e9dc (Aetheris)

One mistake worth recording: the first Aetheris commit tried to patch `AGENTS.md` and
`START_PROMPT.md`, which do not exist in that repo — the family repos have them, Aetheris does not.
The doc still landed; the pointer was added to `HANDOVER.md` in a second commit.

## What I deliberately did not do

- **Did not write a map I had not checked.** Every path in the four tables was listed from the tree
  with `ls`, not recalled. A map that is wrong is worse than no map, because a session follows it.
- **Did not touch the vendored sources.** Documentation only; no file under any upstream tree was
  edited.
- **Did not re-open the family builds.** They remain blocked by missing dev headers and no `make`,
  recorded separately.
- **Did not touch any repository outside the four browsers.**

## Next

1. Each family repo's P0 (build green) still needs a machine with dev packages; the maps in
   `UPSTREAM-FIRST.md` are what a session should read the moment it can build.
2. Aetheris: `:focus-visible` from `should_indicate_focus()`, then scoped invalidation from
   `invalidate_style_after_pseudo_class_state_change`.
3. The family landing page stays deferred until all four reach v1.0.
