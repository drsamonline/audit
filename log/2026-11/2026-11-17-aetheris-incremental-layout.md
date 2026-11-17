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

## Next

1. Cache across interaction-state changes, with upstream's per-pseudo-class traversal.
2. Extend `kLayoutProperties` alongside any new property in `style.cpp`.
3. `[a=v i]` case flag, if a page needs it.
4. Family P0 builds on a machine with dev packages; record versions in each `SOURCES.md`.
