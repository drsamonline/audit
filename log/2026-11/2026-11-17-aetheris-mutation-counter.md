# Aetheris — a mutation counter replaces the DOM fingerprint

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `125c6aef`

The item I deferred twice because an under-counting counter recreates the stale-frame bug. Done with a
test that fails if it under-counts.

## What upstream does

`Node::invalidate_style()` marks the mutated node and its ancestors style-dirty, so the document knows
what to re-resolve without inspecting the tree. Per-node granularity is what makes upstream's scoped
invalidation possible.

## What shipped — the coarse version

| Piece | Detail |
| --- | --- |
| `rendering/dom_mutation.{hpp,cpp}` | `note_dom_mutation()` / `dom_mutation_serial()`, a plain counter (not atomic — a relaxed increment would hide a real threading bug) |
| Bumped at | `set_node_text` (textContent), `js_set_attribute`, `DomHost::{register_subtree,purge_subtree,adopt}` |
| Window | compares two integers instead of hashing the document |
| `document_fingerprint` | deleted, so nothing drifts back to it |

## Evidence

    textContent timer, 20 frames:   relayouts=6
    setAttribute timer, 20 frames:  relayouts=6
    idle timer, 20 frames:          relayouts=0

    full suite: 100% tests passed out of 59

The suite already asserted the textContent case, which is what made this safe to attempt: an
under-counting counter would have failed that test immediately. An attribute-write case is added
because a counter that only sees text is exactly the kind of half-fix that looks green.

## The limit, stated in the handover

Anything that mutates a `DomNode` without passing through those five points is invisible to the counter
and would produce a stale frame. The handover says so, with the instruction to grep for direct
`node.data =` or `attributes[...]` writes before adding a sixth mutation path.

## What I deliberately did not do

- **Did not make the counter per-node.** That is upstream's design and it is the prerequisite for
  scoped invalidation, but it needs a dirty flag on `DomNode` plus an ancestor walk — a different
  change, and the coarse counter already removes the O(n)-per-frame cost that motivated this one.
- **Did not use an atomic.** Every mutation in this engine happens on the thread that owns the document;
  an atomic would paper over a threading bug rather than surface it.
- **Did not audit every mutation path exhaustively.** Five entry points cover what the JS layer and the
  host expose today; the limit is written down rather than assumed away.
- **Did not touch the other three browser repositories.**

## Next

1. Per-node dirty flags, which is what scoped invalidation needs.
2. Symmetric-difference invalidation, once subtree relayout exists.
3. Family P0 builds still need a machine with dev packages.
4. `:focus-visible` text-entry test, once form controls render.
