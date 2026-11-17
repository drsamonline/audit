# Aetheris — per-node invalidation with a style cache

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `408c4c1a`

The item deferred as "a session of its own". Done in one, with a measurement that shows the win in the
window's own summary.

## What upstream does

`Node::invalidate_style()` marks the mutated node and its ancestors; the document re-resolves what a rule
can see and keeps the rest. Layout in Aetheris is still a full rebuild, so the cache applies to the part
that can be incremental today: selector matching, one resolve per node per rebuild.

## Design

| Piece | Detail |
| --- | --- |
| Dirty set | the mutated node, its **ancestors** (inheritance) and its **descendants** (descendant selectors) |
| Cache key | `StyleProperties::fingerprint()` of the parent — a changed parent forces a re-resolve, the only way a clean node's style can change |
| Cleared by | structural mutations (structure drives `:first-child`, `:last-child`, sibling selectors) and any interaction-state change (pseudo-classes) |
| Visibility | the summary prints `resolves:` and `style hits:` beside `relayouts:` |

## Evidence

    200-node page, one textContent write per frame, 20 frames:

    before: 410 resolves per relayout
    after : 5 resolves, 405 style hits

    ctest -j 8  ->  100% tests passed out of 59

## The two tests, and why both

1. **The resolve count stays small** (`0 < resolves < 40`) *and* the relayout still happens — the cache
   cannot pass by dropping the work.
2. **A class write that changes a background still repaints** (pixel asserted magenta) — the failure mode
   of this feature is a stale frame, which this project has shipped twice. A cache that is fast and wrong
   is worse than no cache.

## The correctness argument

A node's style depends on its own attributes and position, the interaction state, and its parent's style.
The dirty set covers the first and third for the mutated branch; interaction state clears the whole cache;
structural mutations clear it too. What would break it is a selector depending on a **sibling** beyond the
structural pseudo-classes already handled — none exists here, and the handover says so in those words.

## What I deliberately did not do

- **Did not make layout incremental.** Following siblings' heights and positions depend on the changed
  subtree; that is the next project, and the cache is worth having on its own.
- **Did not cache across interaction-state changes.** That needs "which nodes can `:hover` affect", which
  is upstream's `ancestor_traversal_for_pseudo_class` — real work, not a shortcut.
- **Did not add a fifth mutation path.** `note_dom_mutation_at` is called by `set_node_text` and
  `js_set_attribute`; structural paths call the plain version, which clears the cache.

## Note on this entry

Three attempts to write it hit a sandbox infrastructure error; a fourth succeeded. Nothing was lost: the
code commit was already pushed before any of them.

## Next

1. Incremental layout, where the remaining time goes.
2. Family P0 builds, on a machine with dev packages.
3. Cache across interaction-state changes, via upstream's per-pseudo-class traversal.
