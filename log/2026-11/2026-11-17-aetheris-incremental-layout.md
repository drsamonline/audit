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

---

# Third item, same session — narrow the focus-move dirty set

Commits: `6cf3becb`, `3ba021cf`, `5fa49565`.

## What I looked at upstream

Nothing new: `CSS/Invalidation/PseudoClassInvalidator.cpp` again. Upstream does not dirty an ancestor's
subtree for `:focus-within` at all. It records a state fact per element whose state changed and lets the
style engine's selector analysis decide which *other* elements a rule can reach. The ancestor's subtree is
never walked blindly.

## What shipped

The subtree walk only matters when a selector puts `:focus-within` on a compound that is not the last one —
`.card:focus-within .title`. `CssStyleSheet::uses_pseudo_class_before_combinator()` answers that for the
sheet, and the walk is skipped when the answer is no. The ancestor *chain* is still dirtied, which is what
styles the ancestor itself (`#card:focus-within{background:...}`).

The answer is sheet-wide, not per-element: one such rule anywhere turns the coarse path back on for every
focus move. That is the honest version of upstream's question without selector analysis.

## Evidence

Same 200-row page, focus move into a card at the top, paint only:

| page | resolves | hits | layouts |
| --- | --- | --- | --- |
| `#card:focus-within` only | **5** | 401 | 1 |
| plus `#card:focus-within .title` | 408 | 0 | 1 |

Both keep `layouts: 1`. The second row is the control in the test, so the first cannot pass by ignoring the
sheet.

    ctest --test-dir build --no-tests=error -j 8  ->  100% of 59, twice in a row

## What I deliberately did not do

- **No per-element analysis.** Answering "does a rule mention `:focus-within` on *this* ancestor" needs
  matching each `:focus-within` compound against the element, which `StyleResolver` can do but does not
  expose. Sheet-wide first; the sharper question is the next item.
- **No change to the hover path.** Hover already dirties only the hovered subtree, which is the set its
  descendant selectors need; the same trick would save two resolves and cost a second code path to get
  wrong.

---

# Fourth item, same session — per-element selector analysis

Commits: `45b258b9`, `de915893`, `0d4af09e`. The third item's sheet-wide answer was a stopgap: one
`.card:focus-within .title` rule anywhere made every focus move in the document coarse.

## What I looked at upstream

`CSS/Invalidation/PseudoClassInvalidator.cpp` again, for the third time in this session, and this time for the
thing it does *not* do: it never asks the sheet a global question. It records a state fact per element and
lets selector analysis narrow it to the elements a rule can actually reach. This commit is that idea with a
blunt instrument: extract the compound that holds the pseudo-class and match it against the ancestor.

## What shipped

`StyleResolver::matches_ancestor_pseudo_class_rule(node, sheet, pseudo, state)` walks the selectors, finds
`:focus-within` occurrences that are followed by a combinator (so the pseudo-class is on an ancestor, not on
the subject), slices out that compound, and matches it against the node. The state passed is the one in which
the pseudo-class holds for that chain — the new state for the element that gained focus, the old one for the
element that lost it. Using the new state for both would fail to restyle a card that just lost focus.

`CssStyleSheet::uses_pseudo_class_before_combinator()` (from `6cf3becb`) is deleted, with a note where it
lived saying why it is not kept: reaching for it again would undo this.

## Evidence

200-row page, one focus move, paint only:

| rule | focus | resolves | hits | layouts |
| --- | --- | --- | --- | --- |
| `#card:focus-within .title` | outside the card | **4** | 405 | 1 |
| `#card:focus-within .title` | inside the card | 7 | 402 | 1 |
| `body:focus-within .title` | inside the card | 408 | 1 | 1 |

The first row is the win. The third is the control in the test: a compound that matches a wide ancestor still
re-resolves the page, so the first two are not passing because the sheet is ignored.

    ctest --test-dir build --no-tests=error -j 8  ->  100% of 59, twice in a row

## Two fixture traps, both the instrument

1. **Specificity, not matching.** I wrote the base rule as `#card .title{background:#00ff00}` and the focus
   rule as `body:focus-within .title{background:#ff00ff}`. The base rule is 10100, the focus rule 202, so the
   focus rule never applied. The page looked exactly like a broken `:focus-within` matcher. Read the pixels,
   then read the specificity.
2. **A bare compound does not match.** `:focus-within .title` matches nothing here: `matches_simple()` needs
   a tag, class or id in the compound. That is a pre-existing parser limit, not a new one, and it is why the
   control uses `body:focus-within .title`.

Also: `--focus-key` takes a *window* y and the window subtracts the 34 px chrome. Two of my first measurements
focused nothing and reported the load-time `resolves:` as if it were the interaction's. The coordinates in the
test were calibrated against pixels before being written down.

## What I deliberately did not do

- **No general selector analysis.** This answers the `:focus-within`-on-an-ancestor question only. `:hover`
  in the same position would need the same treatment, and it has not been needed yet: the hovered element's
  subtree is dirtied anyway.
- **No compound-level cache.** Every ancestor of a focus move re-scans the sheet. On a page with hundreds of
  rules and a deep tree that is the next cost, and it is not measured yet.
- **No sibling combinators.** Unchanged from the third item.

---

# Fifth item, same session — the layout key was an allow-list, and incomplete

Commits: `89d03716`, `a00d1bf2`, `77437cd2`. Not on the plan for this session: the plan's next item was
"extend `kLayoutProperties` when a property is added to `style.cpp`", and auditing that list against what
`layout.cpp` actually reads found the bug it was warning about.

## What I looked at upstream

Nothing new. This one is internal: the property list has no upstream counterpart to copy, because upstream
does not keep one — it derives the invalidation from the style *diff* (`RequiredInvalidationAfterStyleChange`),
which cannot forget a property. That is the point of the change below: a list that must be remembered is the
defect, and the fix is to make forgetting cheap.

## What shipped

`kLayoutProperties` (40 names, allow-list) is gone. `layout_key()` is now
`StyleProperties::digest_excluding(kPaintOnlyProperties)` — the whole resolved style minus the sixteen
properties that can only repaint. `fingerprint()` is `digest_excluding({})`, so the cache key and the layout
key share one implementation and one sort.

| Missing from the old allow-list | Read by |
| --- | --- |
| `gap`, `row-gap`, `column-gap` | `layout.cpp` |
| `flex-direction`, `flex-grow`, `align-items`, `justify-content` | `layout.cpp` |
| `grid-template-columns` | `layout.cpp` |
| `aspect-ratio` | `layout.cpp` |

## Evidence

| page | before | after |
| --- | --- | --- |
| class toggle changing only `gap` | layouts 1, second box at x 50 | layouts 2, second box at x 250 |
| class toggle changing only `background` | layouts 1 | layouts 1 |
| class toggle changing only `color` | layouts 1 | layouts 1 |

Pixels read, not inferred: `(250, 84)` is blue before and green after on the gap page — the box moved only
once the engine actually ran.

    ctest --test-dir build --no-tests=error -j 8  ->  100% of 59, twice in a row

## The failure modes, stated

An allow-list fails unsafely: a property nobody classified silently stops reflowing, and the symptom is a
stale frame. A deny-list of paint-only properties fails safely: a property nobody classified costs a layout
pass that was not needed. The cost of the safe failure is measurable and the cost of the unsafe one is the bug
above, twice now in this project's history.

## What I deliberately did not do

- **No per-property diff.** Upstream compares the style diff; this still compares the whole key before and
  after, so any non-paint change anywhere reflows the whole document. Per-node granularity is the next
  structural step and is a bigger change than this session's item.
- **No attempt to shrink the deny-list.** `border-style` is in it, and `border-style: none` might arguably
  affect the box model here — it does not, because `resolve_edges()` reads `border-*-width` only. That was
  read, not assumed.

## One fixture trap

My first fixture used `flex-grow` to demonstrate the bug and proved nothing: both before and after looked the
same. The `gap` page is the one that discriminates. At the time I wrote that `flex-grow` had no effect in this
engine. That was wrong — see the sixth item below, which retracts it.

---

# Sixth item, same session — `flex-grow`, and a retraction

Commit: `0e0e43d4`. The fifth item left `flex-grow` on the list as "read by `layout.cpp` and appears to have
no effect". Checked properly; there is no bug, and the claim was mine, not the engine's.

## What the code does

`LayoutEngine::layout_flex_children()`:

    float grow = std::max(0.0f, parse_length(child->style.get("flex-grow"), 0, available_width));
    if (width < 0) width = total_grow > 0 ? free_space * grow / total_grow : 0;

`parse_length("1", 0, w)` returns 1.0 (no unit, so it falls through to the bare number), so `flex-grow: 1`
works. `Tests/AetherisRendering/TestFlexLayout.cpp` has asserted it since before this session — "flex-grow
expands both items".

## Why my measurement said otherwise

The fixture's children had no `height`. A block with one line of text is ~19 px tall, so every probe at
y = 84 was *below* both children and read the parent's blue background. The children were there; I was
looking past them.

Re-measured with `height: 100px` on both children, `flex-grow: 1` against `flex-grow: 2`, 400 px row:

| fixture | x=100 | x=150 | x=200 | x=300 |
| --- | --- | --- | --- | --- |
| `flex-grow: 1` / `2` | magenta | green | green | green |
| no `flex-grow` | blue | blue | blue | blue |

Magenta to x = 133 is the 1:2 split of 400. Correct.

## What this cost and what it changes

A wrong claim went into a **pushed commit message** (`89d03716`), which cannot be rewritten under this repo's
rules, and into this entry. Both are corrected where they can be — the handoff and here — and the commit
message stands as written with the correction pointing at it.

No code change. A window-level `flex-grow` test would duplicate `TestAetherisFlexLayout`, which asserts
rect widths directly; a pixel probe is the weaker instrument here, which is the lesson of the last hour.

Third instrument failure of the session, all three the same shape: a coordinate or a fixture that did not mean
what I assumed, read as if it were the engine's answer.

---

# Seventh item, same session — two features closed by evidence, one cost paid down

Commits: `9aeaf9b0`, `4c1fdffb`, `b6112a4a`.

## `[a=v i]` and sibling combinators: not built

Both were on the list as "if a page needs it". Checked whether anything does:

    grep -rn " i\]" Tests/ docs/ src/        -> only vendored LibWeb hits, which Aetheris does not render
    grep -rE "[a-z] *[+~] *\.[a-z]" Tests/AetherisRendering/ docs/  -> nothing

So: no. Recorded as closed rather than built, and the handoff says what would have to change with them. The
sibling case matters because the invalidation code leans on it: `style.cpp` splits on whitespace and `>` only,
so a `+`/`~` selector matches nothing at all — a silent no-op, not a wrong answer. `collect_state_change_dirty()`
carries a comment at the exact line that has to change if that ever becomes real.

Not building something is only a decision if the evidence is written down; that is what this section is.

## The key walk, narrowed

The documented remaining cost of the layout skip was that it digested every node's style on every relayout.
Only a node whose style was *re-resolved* can have a different key — everything else kept the exact
`StyleProperties` the last snapshot digested — so the builder now reports the re-resolved set and the
comparison walks that.

| 200-row page (406 nodes), one hover | value |
| --- | --- |
| key comparisons, before | 406 |
| key comparisons, after | **5** |
| resolves | 5 |
| layouts | 1 |

`key checks:` is in the window summary beside `layouts:` and `resolves:`. The brief says to extend the
instrument rather than open a debugger; this is that, and it turns a cost I had described in prose into a
number.

Two properties of the change that had to hold:

- `restyled` empty means no style moved, so no key can have moved: one comparison instead of a walk.
- A structural mutation clears the style cache, so every node re-resolves and the set is everything. The case
  that must not skip is still the case that does not skip.
- The node-count belt stays, but counts pointers instead of digesting styles, which is why it can be paid on
  every skip.

## What I deliberately did not do

- **No per-node layout.** The skip is still all-or-nothing for the document: one changed box reflows
  everything. That is the next structural step and it is bigger than this session's remaining budget.
- **No timing measurement.** `key checks` counts the comparisons, which is the cost that changed. Wall-clock
  in a sandbox with a shared CPU would be the weaker instrument.

---

# Eighth item, same session — per-node layout

Commits: `f0ce1b21`, `5606dc69`, `30f0b793`. The second increment of incremental layout: the pass stops
entering subtrees that cannot have changed.

## What I looked at upstream

Nothing new this time, and that is worth admitting: upstream has had this since forever (`Layout/Node.h`'s
`NeedsLayoutUpdate` flag, laid out over the marked set). The port here is deliberately *not* that mechanism —
there is still no per-node invalidation flag — but a condition on the origin, which is cheaper to get right
with the data this engine keeps.

## What shipped

`LayoutReuse` carries the previous pass's geometry, the set of nodes a restyle reached (plus their ancestors),
and a counter. `LayoutEngine::reuse_subtree()` fires when the node is outside that set, has a recorded entry,
and is being laid out at the same `(x, y, available_width)`. Then the whole subtree's geometry is copied and
the pass does not enter it. `LayoutEngine`'s private walkers stopped being `static` so they can read the
context; `CachedGeometry` moved to `layout.hpp` and carries the origin.

## The invariant

A node's subtree geometry is a function of (resolved style, x, y, available_width, its DOM subtree).

| Part of the tuple | Why it is safe |
| --- | --- |
| style | a clean node's style did not change; a structural change clears the style cache, so every node restyles |
| x, y, available_width | the parent decides them, and they are in the key, so a node that moves or is given a new width is laid out again |
| DOM subtree | unchanged, or the style cache was cleared |

What would break it: anything making geometry depend on state outside that tuple. `float` is not implemented
and flex items take their width from the parent, so nothing in the engine does today. That is the sentence to
re-read before adding `float`.

## Evidence

405-node page, one edit, 2 frames:

| case | layout nodes |
| --- | --- |
| text edit in row 100 of 200 | **4** |
| first row grows 3 px → 60 px | 204 |

The second is the control and it is the one that matters: every row below the grown one moved, so none can be
reused where it used to be. Pixels: content y 1 blue (inside the grown row), content y 70 green (first row
after it). Read off the frame, not inferred.

    ctest --test-dir build --no-tests=error --junit  ->  100% of 59, twice in a row

## One fixture error, caught before it became a claim

The first version of the text-edit page had `#mid` in its stylesheet and no element with that id, so
`getElementById('mid')` found nothing, no mutation happened, and the run reported `relayouts: 0` with the
load-time counters — which reads exactly like "the reuse path did not fire". Adding the id made it 4. This is
the fourth time this session that a fixture, not the engine, was the thing to fix, and the tell was the same
each time: a number that did not match what the code plainly does.

## What I deliberately did not do

- **No per-node invalidation flag.** Upstream marks boxes; this conditions on the origin. The flag would be
  cheaper per node and is the honest long-term shape, but it is a larger change than the measurement
  justified here.
- **No timing.** `layout nodes` counts the work that changed. Wall-clock on a shared CPU is the weaker
  instrument.
- **No partial reuse inside inline flow.** `layout_inline_children()` computes text children directly rather
  than through `layout_node`, so a dirty inline container re-lays out all of its text. That is unchanged from
  before this commit and is the next place the same idea would go.

---

# Ninth item, same session — the instrument, and a reference to test the reuse against

Commits: `0e565ffa`, `1f6d575e`, `d0603705`.

## `layout nodes:` was under-reporting

A text run is laid out by `layout_inline_children()` directly, not through `layout_node`, so it was never
counted. On a text-heavy page the number was about half the truth — 204 for a pass that had laid out 405
nodes. Text runs are counted now, and the first pass is counted too, which is what makes a mutated run and a
fresh run comparable at all.

| case | before | after |
| --- | --- | --- |
| text edit in row 100 of 200 | 4 | 5 |
| first row grows 3 px → 60 px | 204 | 405 |

## A differential test for the reuse path

Every other test in this suite asserts what I expect. This one compares two runs and asks for equality: a page
mutated into a state, and the same page loaded in that state, byte-identical below the chrome.

| run | layout nodes |
| --- | --- |
| mutated at runtime | 5 |
| loaded in that state | 405 |

Same pixels, 80× less layout work. That is the strongest evidence this session has produced, because the
reference cannot inherit my assumptions: it is a fresh layout of the same document.

The chrome is excluded because it carries the URL, and the two runs are served on different ports. That is
also how the first version of the comparison failed — 212 differing pixels at y 11..21, all in the address
bar. The exclusion is in the helper's name, not in a comment, so nobody re-adds the chrome by accident.

## Fifth fixture error, and what caught it

The differential's first fixture set `class='hit'` instead of `class='r hit'`. The row lost `.r`, so it lost
`height: 3px`, grew to a text line, and pushed 200 rows down — which made the mutated page genuinely different
from the baked one, and made the test meaningless rather than failing loudly.

What caught it was the counter, not the frame comparison: `layout nodes: 203` where reuse should have made it
5. One temporary `fprintf` in `reuse_subtree` printed `cached y=3 now y=19.2`, and 16.2 px is a line height —
which pointed at the missing rule in one step.

That is the pattern for all five of this session's instrument failures: a number that did not match what the
code plainly does, chased with a print rather than a theory. The frame comparison would have hidden this one;
the count could not.

## What I deliberately did not do

- **No text-run reuse.** Every path that changes text replaces the text node with a new one, so a text run is
  never reusable; the case that would benefit is a *dirty inline container* whose other runs did not move.
  That is now the next item rather than this one.
- **No chrome in the comparison.** The URL differs by port; excluding it is honest, and the alternative
  (serving both pages on one fixed port) is racy.

---

# Tenth item, same session — a click is not a layout

Commits: `a1514a7b`, `9d5543b2`, `0e72efe2`. Not on the list: found while reading `dispatch_click_at()` for
the next item, and it was the largest single waste of the session.

## What it was

`dispatch_click_at()` ended with an unconditional `rendered.relayout()`. `relayout()` decides what kind of
mutation it is from `last_mutated_node()`, and a click that changed nothing leaves that at null — which the
function reads as a **structural** change. So it cleared the style cache and laid the page out from scratch.

Clicking a 405-node page whose handler only logged:

    407 resolves, 405 nodes laid out, 0 style hits

That is the most expensive path the window has, and it was reached by clicking anywhere.

## What shipped

The click path is gated like the timer and key paths already were:

    if (dom_mutation_serial() != before && attribute_mutation_needs_relayout(rendered))
        rendered.relayout();

| click handler | before | after |
| --- | --- | --- |
| logs only | layouts 2, 405 nodes | layouts 1 (no pass) |
| writes an unobserved attribute | layouts 2, 405 nodes | layouts 1, 0 nodes |
| changes a width (control) | layouts 2, 405 nodes | layouts 2, 5 nodes |

The handler still runs in all three (`MARK clicked` is asserted on the first), and the control still reflows.

## The instrument bug it exposed

Both skip paths left `layout nodes:` reporting the **previous** pass. So `click_attr` printed 405 after a
relayout that had laid out nothing — the number looked like evidence and was a leftover. Both paths reset it
to zero now. A stale counter is worse than no counter.

This is the sixth time this session that a number, not the engine, needed fixing first. It is also the second
time the fix was to the instrument rather than the subject (`key checks` and now this) — which is what the
project's own "check the instrument before the subject" rule is for, and I still needed six reminders.

## What I deliberately did not do

- **No per-click repaint decision.** `dispatch_click_at()` still returns true, so the caller repaints. A
  click may change something the engine does not track (a canvas, a timer scheduled by the handler), and a
  repaint is cheap next to being wrong about it.
- **No equivalent audit of the key path's `relayout()` call.** It already has the serial gate.

---

# Eleventh item, same session — upstream first

Commits: `06dd8bf4`, `d1180e76`, `da6f4ebf`. Read upstream *before* writing this one; that ordering is the
whole point of the entry.

## The inline item, closed without code

`DOM/CharacterData.cpp` on a text data change: `marks.text_data_changed = true; mark_box(marks)` — the text
node's own box is marked, and the layout engine re-runs the formatting context. `set_needs_layout_tree_update`
is called only for whitespace-only changes and emptiness, where a box may appear or disappear. Style
invalidation for a text change is `invalidate_style_after_text_change_under()`, which exists for `:dir` and
language and returns immediately on a document with no auto-directionality.

So there is no per-run text reuse at this layer to port. The formatting context is the unit, which is what this
engine already does. Implementing per-run reuse would have been an invention resting on this engine's per-run
wrapping — a real line breaker's run depends on its neighbours — and inventing an optimisation that upstream
deliberately does not make is not "porting the shape".

That is a decision, not a task skipped. It is written down because the item had been carried for three turns.

## The structural item, from the same reading

Any structural mutation cleared the whole style cache. Upstream records a tree delta for the sequence a node
left or joined — `record_subtree_disconnecting()` with `PreviousSiblings::Arrived/Departed`, per element — and
the style engine recomputes the affected nodes.

Ported as: the DOM says **which parent's child list changed** (`note_child_list_mutation_at`), and `relayout()`
invalidates that parent's subtree plus the chain above it. Several child-list changes in one frame accumulate,
so `appendChild` twice invalidates both parents; a note of any other kind clears the list.

Narrowed once more, and this is the part worth stating: a positional selector is the only way one child's
presence can restyle another, and the user-agent sheet has none (checked). When the page's sheet has none
either, only the parent can change (`:empty`) — the new children resolve themselves because they have no cache
entry — so the parent and its ancestors are dirtied and not the subtree.

## Evidence

| 200-row page, one mutation, 2 frames | before | after |
| --- | --- | --- |
| append a span inside row 150 | 407 resolves, 405 nodes | **6**, 7 |
| innerHTML replace inside row 150 | 407 resolves, 405 nodes | **6**, 6 |
| append a div to body, no positional selector | 406 resolves, 405 nodes | **5**, 5 |
| append a div to body, `:first-child` in the sheet | 406 resolves, 405 nodes | 406 (on purpose) |

The fourth row is the control. The `:empty` case is asserted by pixel: appending a child into an empty box
restyles the box, so the parent's own state is re-evaluated even when no sibling can see the change.

    ctest --test-dir build --no-tests=error -j 8  ->  100% of 59, twice in a row

## The sharp edge this introduced

`register_subtree()` and `purge_subtree()` no longer note a mutation — they walk the tree to hand out and free
JS handles, and their callers now note which child list changed. A new caller that forgets to will leave the
page stale. That is written in the handoff's next list rather than buried in the code, because it is the kind
of omission that produces a silent stale frame.

## What I deliberately did not do

- **No per-run text reuse.** See above: upstream does not do it at this layer.
- **No per-selector analysis of positional selectors.** The question is asked of the sheet, not of the
  specific siblings whose index moved. Upstream has the finer version; this is the honest coarse one.
- **No change to the `:empty` handling.** The parent is dirtied; whether the *parent's* parent could match
  something is not a question this engine's selector set can ask.

---

# Twelfth item, same session — reftests in upstream's shape, and a SIGSEGV they found

Commits: `1e7fb156`, `253ab301`, `87f9f7d3`. Upstream checked first: Ladybird verifies rendering with
`Tests/LibWeb/Ref`, where an input declares `<link rel="match" href="...-ref.html">` and the two must render
identically. The item was to generalise the single differential into that shape.

## What shipped

Five shapes, each a page mutated at runtime compared byte for byte below the chrome against the same state
loaded fresh, over a 200-row page so reuse is doing real work:

| shape | mutation |
| --- | --- |
| a text write | `textContent`, same length |
| a width change by class | class `r hit`, 400 → 200 px |
| a paint-only class change | class `r hot`, background only |
| an appended child | `appendChild` a styled span |
| an innerHTML replace | `innerHTML` = one styled span |

## What it found

The innerHTML case **crashed the browser**:

    thread 29145 panic: member access within misaligned address 0x92234d379374c60c for type
    'const aetheris::rendering::DomNode', which requires 8 byte alignment
    /scratch/work/The_Browser/src/rendering/render_document.cpp:254 in relayout
        for (auto const* current = node; current; current = current->parent)

`js_inner_html_set()` inserted the parsed children with `push_back()`, so they kept the parent pointer they
were given while parsing — to the fragment root, which dies at the end of the block. Nothing walked `parent`
after an `innerHTML` set, so the dangling pointer never showed, until the layout dirty-set walk (added two
items ago) walked it. `append_child()` sets the link and every other insertion path already used it.

This is the strongest argument the session has for reference-based testing: five cases agreed with what I
expected, and the sixth was a use-after-free in the DOM layer. Asserting expectations would never have found
it — I did not know it was there.

## Two fixture errors on the way

- `className` is not implemented here (only `classList`), so the appended span had no class and the case
  failed for the wrong reason. `setAttribute` fixed it. Recorded as the next item, because a page setting
  `className` silently gets nothing.
- The failure message said "a reftest input run exits cleanly" for all five cases. Naming the case is what
  made the crash reachable in one step; `require` now gets a built string.

## Cost

The window test went from ~50 s to ~95 s: ten extra browser runs over 200-row pages. The suite is ~65–70 s
wall clock at `-j 8`. That is worth it for the only test that does not encode my assumptions, and it is
written down so nobody removes it for being slow.

---

# Thirteenth item, same session — classList was writing to the DOM and telling nobody

Commits: `0d52e64e`, `3fcdc1c1`, `4ed2c48c`. Upstream first: `DOM/Element.idl` has
`[CEReactions, Reflect=class] attribute DOMString className` — a reflected attribute, the `class` content
attribute read and written, nothing more.

## What the reading turned up

Looking for where to add `className` found the bigger problem. `write_classes()` — the single place
`classList` writes — set `node->attributes["class"]` directly and noted **no mutation at all**.

| page | before | after |
| --- | --- | --- |
| `classList.add('on')` | relayouts 0, pixel blue | relayouts 1, layouts 1, pixel magenta |
| `className = 'on'` | relayouts 0, pixel blue | relayouts 1, layouts 1, pixel magenta |

A page that toggles a class with `classList` — which is how most pages toggle a class — wrote the attribute,
invalidated nothing, and left the frame blue. No error, no warning, nothing to notice unless you look at the
pixel.

Both now go through `set_class_attribute()`, which writes the attribute and notes it in the order
`js_set_attribute` uses: the node-scoped note first, because it clears the recorded attribute name. `className`
is a reflected accessor, absent reading as `""`.

Both are in the reftest matrix now, mutated against baked. That is the second bug in two items that the
reference comparison caught and an expectation would not have — I had no reason to suspect either, and no test
asserted either.

## A third specificity trap, on the way

My first `className` fixture used `#a{background:#0000ff}` against `.on{background:#ff00ff}` — 10000 against
100 — so the rule never applied and the working fix looked broken. Same trap as the `body:focus-within .title`
fixture two items ago. The tell is the same both times: a relayout count that is right and a pixel that is not.

## What I deliberately did not do

- **No audit of the other attribute-writing APIs.** `set_control_value()`, the `value`/`checked` setters and
  `classList`'s siblings may have the same defect. That is a sweep, not this item, and it is written down as
  the next one rather than half-done here.
- **No `classList` additions** (`.replace`, `.item`, `.length`, indexed access). Only what was there, made to
  work.

---

# Fourteenth item, same session — the audit, and one choke point instead of six

Commits: `9ab00cfc`, `a8e96ddf`, `2fe25873`. Upstream first: `Element::m_attributes` is private
(`OwnPtr<AttributeList>`, `friend class NamedNodeMap`), and every write runs `Element::set_attribute` →
`run_attribute_change_steps` → `invalidate_style_after_attribute_change`. The guarantee is in the type system: a
caller cannot write an attribute and forget to invalidate, because there is no way to write one.

Here the map is public, so the audit was a grep for `attributes[...] =`. Six runtime writers noted nothing:

| writer | what a page does with it |
| --- | --- |
| `js_style_set_property` | `el.style.setProperty(p, v)` |
| `js_style_set` | `el.style = '...'` |
| `js_dataset_set` | `el.dataset.x = v` |
| `js_checked_set` | `el.checked = true` |
| `set_control_value` | `el.value = '...'` |
| `set_class_attribute` | `classList`, `className` (previous item) |

| write | before | after |
| --- | --- | --- |
| `el.style = 'background:#ff00ff'` | relayouts 0, blue | relayouts 1, magenta |
| `el.style.setProperty('background', …)` | relayouts 0, blue | relayouts 1, magenta |
| `el.dataset.x = '1'` | relayouts 0, blue | relayouts 1, magenta |

`set_attribute()` / `remove_attribute()` in `dom_mutation.hpp` are the choke point now, and `js_set_attribute`
and `set_class_attribute` use them too — the note order (node-scoped first, because it clears the attribute
name) lives in one place instead of four.

## What this says about the last two items

`classList` was not an isolated mistake. It was the one I happened to look at. Six APIs had the same defect,
all in the same way, all silent. The pattern is that the engine's invalidation contract was a convention
("remember to note it") rather than a structure — and a convention with six call sites had five failures.

Upstream does not have the convention. That is the difference the port is meant to close.

## A fourth specificity trap

The `dataset` fixture first used `#a{background}` against `[data-x]{background}` — 10000 against 100 — and read
blue. The relayout count said the note worked; the pixel said the rule lost. That tell is now reliable enough
to name: **relayout right, pixel wrong, look at specificity.** Fourth time in this session.

## What I deliberately did not do

- **No CSSStyleDeclaration.** `el.style.background = v` still sets a property on the throwaway object
  `js_style_get()` returns. Upstream has `[PutForwards=cssText] readonly attribute CSSStyleDeclaration style`.
  That is a CSSOM feature, not an invalidation fix, and it is the next item.
- **No change to `DocumentRuntime::set_attribute()`**, which has its own `mark_dirty()` mechanism for the
  non-JS host path. It is a separate contract and would need its own audit.

## Next

1. `el.style.background = v` needs a real `CSSStyleDeclaration`; today it silently does nothing.
2. `[a=v i]` and `+`/`~` remain unbuilt by evidence; revisit only when a page needs them.
3. Family P0 builds on a machine with dev packages; record versions in each `SOURCES.md`.
4. Any new caller of `register_subtree()`/`purge_subtree()` must note the child-list change itself.
