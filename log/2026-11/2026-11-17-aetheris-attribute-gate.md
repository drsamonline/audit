# Aetheris — attribute writes gated like pseudo-classes

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `48089be1`

Second half of the "invalidate only what a rule can observe" idea, in one pass with its tests.

## What upstream does

`Node::invalidate_style()` marks the mutated node and its ancestors; the document then re-resolves only
what a rule can see. A `data-` attribute that no selector mentions is not observable, so upstream does not
relayout for it.

## What shipped

| Piece | Detail |
| --- | --- |
| `note_attribute_mutation(name)` | records the name and bumps the serial |
| `CssStyleSheet::uses_attribute` | asks whether a selector mentions `[name]` (attribute selectors are not parsed yet, so false today — the right question for later) |
| `attribute_is_rendering_relevant` | the names the engine reads outside the cascade: `class`, `id`, `style`, `src`, `href`, `width`, `height`, `type`, `value`, `checked`, `disabled`, `hidden`, `colspan`, `rowspan`, `alt` |
| window | both the timer path and the key/click paths ask before rebuilding |

## Evidence

    20 frames each:

    setAttribute('data-n')  -> 0 relayouts   (was 6)
    setAttribute('class')   -> 6 relayouts
    textContent             -> 6 relayouts
    idle                    -> 0 relayouts

    ctest -j 8              -> 100% tests passed out of 59

Both directions are asserted. The first attempt missed the timer path — the gate was wired into two call
sites and the timer relayout is a third — which the measurement caught immediately: `data-n` still showed 6.

## The one test that had to change

`"an attribute write triggers a layout"` wrote `data-n` and asserted a relayout. The behaviour it asserted
is the behaviour this commit deliberately changes, so it now writes `class` and asserts the same thing about
an attribute the engine actually reads. Changing a test because the behaviour changed on purpose is not the
same as changing a test until it passes, and the commit message says which one this is.

## The risk, written down

`attribute_is_rendering_relevant` is a list, and a list can go stale. A new code path that reads an
attribute — say a renderer that starts honouring `loading` — must add it, or pages will silently stop
updating. `HANDOVER.md` carries that instruction next to the limitation.

## What I deliberately did not do

- **Did not gate text writes.** A `textContent` write can always change layout; there is nothing to observe
  cheaply that would prove otherwise.
- **Did not implement attribute selectors** to make `uses_attribute` meaningful. That is a CSS feature, not
  an invalidation change.
- **Did not gate per subtree.** This is still document-wide: one observable mutation rebuilds everything.
  Per-node dirty flags are the next step and they are only worth doing with incremental layout to spend them
  on.

## Next

1. Per-node dirty flags + incremental layout, together or not at all.
2. Family P0 builds, on a machine with dev packages.
3. Attribute selectors, which would make `uses_attribute` load-bearing.
