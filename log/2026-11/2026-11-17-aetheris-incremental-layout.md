# Aetheris — incremental layout, first increment

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commits: `1114541e`, `1b2417d7`, `ac4f1fdf`, `833ecabd`, `dd91e36c`

Re-applied from the handoff, from scratch. The previous session had this working and green but could not
push; the sandbox died with the work uncommitted, so the design survived and the code did not. This session
rebuilt it, measured it, and committed it in four small commits plus the docs.

## What I looked at upstream

Read after the code was written, which is the wrong order and is worth recording as such: the design came
from the handoff, and the upstream reading below was done to check the claim in `1b2417d7` rather than to
make the design. It held, and it sharpened it.

- `Layout/Node.h` — `NodeFlag::NeedsLayoutUpdate`, `set_needs_layout_update(DOM::SetNeedsLayoutReason)`.
  Upstream invalidates per box, with a reason; Aetheris has no per-box flag, so the decision is taken from
the resolved style instead.
- `DOM/Node.h` — the reason lists are the interesting part: `ENUMERATE_SET_NEEDS_LAYOUT_REASONS` includes
  `StyleChange`, and `ENUMERATE_SET_NEEDS_LAYOUT_TREE_UPDATE_REASONS` holds the structural ones
  (`NodeInsertBefore`, `NodeRemove`, `CharacterDataReplaceData`, `HTMLImageElementUpdateTheImageData`).
  Upstream separates *rebuild the layout tree* from *move the boxes*, which is the same split as
  `text_or_structure` in `relayout()`: text and structure force a pass, an attribute write does not.
- `CSS/UpdateStyle.cpp` — `RequiredInvalidationAfterStyleChange`, with `needs_relayout()` and
  `needs_layout_tree_rebuild()` computed from what actually changed, plus accumulated-visual-context and
  scroll-container invalidation as separate questions. On the relayout branch it *also* calls
  `Painting::request_document_repaint(...)`, so a relayout is not a repaint and a repaint is not a relayout.

So the port is the decision, not the mechanism: upstream asks the style *diff* which invalidation it needs;
this asks the resolved *layout key* before and after, which is the coarser version of the same question and
the right one while there is no per-property diff to consult. What is not ported is the granularity: upstream
relayouts the marked subtree (`render_state_relayout_element_after_style_change`), this decides for the whole
document.

The one upstream idea this does **not** yet cover is `ancestor_traversal_for_pseudo_class`
(`CSS/Invalidation/PseudoClassInvalidator.cpp`) — reuse across interaction-state changes. That is the next
item, and it is the reason `apply_visual_state()` still rebuilds every node.

## What shipped

| Commit | What |
| --- | --- |
| `1114541e` | `note_text_mutation()`; `note_dom_mutation_at()` clears the recorded attribute name; `js_set_attribute` calls the node-scoped note **before** `note_attribute_mutation` |
| `1b2417d7` | `RenderDocument`: `layout_key()` over 40 properties, `m_layout_keys`, `m_geometry` (rect, box model, text fragments), `layout_passes()`; `relayout()` skips the engine when no key changed; summary prints `layouts:` |
| `ac4f1fdf` | `AetherisWindowScripts`: four runs, one of them a control, one reading a frame |
| `833ecabd` | the window test removes its frame dumps on the way out |
| `dd91e36c` | `HANDOVER.md` and the session handoff record the limits and the evidence |

## Evidence

Raw summary lines, 20 frames at 16 ms per frame, `--window` against a loopback fixture:

| Page | relayouts | layouts |
| --- | --- | --- |
| class toggle changing only `background` | 6 | **1** |
| `textContent` write | 6 | 7 |
| idle | 0 | 1 |
| class toggle changing `width` (control) | 6 | 3 |

The design expected the first three. The fourth is mine: the same write changing a layout property has to
run the engine, or the skip would be unconditional and the first row would pass for the wrong reason.

Pixel, not verdict — 2-frame run, class write changing only `background`:

    (200, 84)  frame-1 (0, 0, 255)   frame-2 (255, 0, 255)
    (500, 84)  frame-1 (255,255,255) frame-2 (255, 255, 255)
    summary: relayouts: 1, layouts: 1

So a skipped layout still repaints. That is the failure mode this project has shipped twice; it is not
present here. The second coordinate is a control: it is outside the 400 px box and stays white, so the first
coordinate means something.

    ctest --test-dir build --no-tests=error -j 8   ->   100% tests passed out of 59
    (run twice in a row from a clean /tmp, 27.1 s and 26.9 s)

## Two probes that were the instrument, not the engine

1. **`FAILED: the repaint pixel is readable`** on my new test's first run. The frames were zero bytes: the
   suite writes ~58 MB of 1024x768x3 frames into a 64 MB tmpfs `/tmp` and never removed them. Moved my dump
   under the build tree and made the test clear `/tmp/aetheris-*-frames` on the way out. `AetherisDomHost`
   failed "render exits 0" in the same run for the same reason, and passed on a clean `/tmp`.
2. **`error: _FORTIFY_SOURCE requires compiling with optimization (-O)`** on the first translation unit.
   `zig cc` with `-Og` does not define `__OPTIMIZE__`, so the glibc warning becomes an error under `-Werror`.
   `-DCMAKE_CXX_FLAGS="-Wno-error=#warnings"` builds; fortify is inert at `-Og` either way. Recorded in the
   handoff so the next session does not read it as a broken tree.

Neither was the layout code. Both cost one probe each.

## What I deliberately did not do

- **No dirty-set.** The skip is whole-document: one unchanged-key check per node, then all of it or none of
  it. A per-subtree dirty set is the second increment, not this one.
- **No reuse across interaction-state changes.** `apply_visual_state()` still rebuilds every node and still
  counts as a layout pass. Upstream's `ancestor_traversal_for_pseudo_class` is the way in; it needs a
  per-pseudo-class invalidation set that does not exist here.
- **No change to `attribute_is_rendering_relevant`.** The attribute gate and the layout skip are separate
  gates and stay separate: one decides whether to rebuild, the other whether to reflow.
- **No cleanup of the other frame dumps** in the suite, beyond clearing them at the end of the test that
  creates them. Rewriting eight test blocks to clean up after themselves is a diff that hides this one.
- **No fix to the `position: sticky`, shaping or form-interactivity items** in `HANDOVER.md`. Untouched.

## Limits, stated in the code

- `kLayoutProperties` is hand-written. A layout-affecting property missing from it is a silent
  stale-geometry bug, not a slow path. Extend the list when `style.cpp` gains a property.
- Images cannot affect layout in this engine (`resolve_images` runs after `LayoutEngine::layout`), which is
  why an image swap needs no pass. If that order ever changes, this skip becomes wrong for `src`.
- Geometry is only reused at the width that produced it (`m_layout_width`), and only when a text or
  structural mutation did not precede it.

---

# Second item, same session — cache across interaction-state changes

Commits: `b2cc8a2f`, `88e01bbd`, `460b6595`, `cab7e8e8`. The item the handoff listed as needing upstream's
`ancestor_traversal_for_pseudo_class`.

## What I looked at upstream

Read **before** writing this one, unlike the first item.

- `CSS/Invalidation/PseudoClassInvalidator.cpp` — `ancestor_traversal_for_pseudo_class()` returns
  `AncestorTraversal::FlatTree` for `:focus-within` and `ShadowIncluding` for everything else, i.e. exactly
  one pseudo-class reaches ancestors. `pseudo_class_propagates_to_ancestors()` says the same thing in one
  line.
- The same file's `invalidate_style_after_pseudo_class_state_change()` builds the chain for the old state and
  the chain for the new one, then walks each and invalidates only the elements **not** in the other chain —
  so the dirty set is the elements whose state actually moved, and the walk stops at the first element that
  is in both chains because everything above it is too.
- `:focus-visible` publishes `element.should_indicate_focus()` rather than the focus move, which is why a
  pointer focus does not light up every script-focused element. Aetheris already had that rule in
  `style.cpp`; nothing to port.

What I checked in this tree before trusting the port: `style.cpp`'s `matches_simple()` tests `:hover`,
`:focus`, `:focus-visible` and `:active` against `interaction_state-><slot> != &node` — the element itself —
and walks the ancestor chain only for `:focus-within`. The upstream split holds exactly.

## What shipped

`apply_visual_state()` keeps the style cache and the geometry snapshot instead of clearing both. It dirties

- the subtrees of the element that lost the state and the one that gained it (`.card:hover .title` matches
  descendants),
- their ancestor chains (the element that lost the state may be an ancestor of the one that gained it),
- and, for a **focus** move only, the ancestor's whole subtree — because `.card:focus-within .title` matches
  a *sibling* of the focused input, which is neither on the chain nor in the focused subtree. That was the
  one case where the obvious dirty set is silently wrong, and it is the reason the test asserts that pixel.

The first pass now fills the cache as well, so the first interaction reuses instead of resolving the page
once for free.

## Evidence

One interaction per run, 3 frames, `--window` against a loopback fixture:

| page | before (relayouts/layouts) | after |
| --- | --- | --- |
| hover, background only | 1 / 2 | 1 / **1**, 5 resolves |
| hover, `width` (control) | 1 / 2 | 1 / 2 |
| hover, one row of a 200-row page | 1 / 2 | 1 / **1**, 5 resolves, 401 hits |
| hover, `#card:hover .title` | 1 / 2 | 1 / **1** |
| `:focus-within`, background | 1 / 2 | 1 / **1** |
| `:focus-within`, `width` (control) | 1 / 2 | 1 / 2 |
| `:focus-within`, descendant | 1 / 2 | 1 / **1** |
| `:active`, background only | 1 / 2 | 1 / **1**, 5 resolves |
| `:active`, `width` | 1 / 2 | 1 / 2 |

Pixels, read from the last frame rather than inferred: hovered element magenta and the element below it
white; `.title` magenta while `#card` stays blue; `:focus-within` ancestor yellow and `.title` magenta.

    ctest --test-dir build --no-tests=error -j 8  ->  100% of 59, twice in a row

A measurement trap worth recording: the **before** column reports `resolves: 0` on every row, and that is
not because nothing was resolved. The old state path passed no `StyleCacheStats` to the tree builder, so the
instrument had no reading for it at all. A `resolves:` number from a run before this commit means nothing.

The baseline was taken by stashing the change and rebuilding HEAD, not by reasoning about the old code.

## What I deliberately did not do

- **No selector analysis.** Upstream narrows the focus case by asking which rules mention `:focus-within`
  on this ancestor. Without that, a focus move dirties the ancestor's whole subtree — correct, and coarse.
  Hover and `:active` get the full win; focus gets only the layout skip.
- **No sibling invalidation.** `style.cpp` splits selectors on descendant and child combinators only, so
  `+` and `~` cannot reach a sibling and none is dirtied. Adding sibling combinators means adding that here.
- **No per-node dirty flag.** Still one dirty set per rebuild, not upstream's per-box flag with a reason.
- **No change to `relayout()`.** Its dirty set still comes from `collect_dirty()` with ancestors, unchanged.

## Next

1. Narrow the focus-move dirty set with selector analysis (does any rule mention `:focus-within` here).
2. Extend `kLayoutProperties` alongside any new property in `style.cpp`.
3. `[a=v i]` case flag, if a page needs it.
4. Family P0 builds on a machine with dev packages; record versions in each `SOURCES.md`.
