# Aetheris — no rebuild when no rule could match

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `c50040c9`

Straight port, no investigation. The owner's instruction was to read upstream when something is not
working and to stop looping; this session applied it to a known cost rather than an open bug.

## What upstream does

`CSS::Invalidation::invalidate_style_after_pseudo_class_state_change` (LibWeb,
`CSS/Invalidation/PseudoClassInvalidator.cpp:34`) invalidates only the elements whose pseudo-class
state actually changed:

- it builds the ancestor chain of the old state and of the new state
- `:hover` **propagates** to ancestors (`pseudo_class_propagates_to_ancestors`), `:focus` and `:active`
  do not
- it invalidates the symmetric difference of the two chains

Aetheris rebuilt the entire layout on every state change. This commit takes the cheap half of
upstream's idea — the half that needs no subtree invalidation machinery.

## What shipped

- `CssStyleSheet::uses_pseudo_class(pseudo)` — scans selector strings.
- `VisualInteractionState::last_change` — which of hover/focus/active moved.
- `RenderDocument::apply_visual_state` returns whether it rebuilt, and skips when no selector in the
  sheet mentions the class that changed.
- The three helpers in `main.cpp` count a relayout only when one actually happened.

## Evidence

    page with no :hover rule, --move over it:   relayouts=0     (was 1)
    page with #a:hover, --move over it:          relayouts=1

    full suite: 100% tests passed out of 59
    commit: c50040c9

## Deliberately conservative

`":focus"` is a prefix of `":focus-visible"`, so a sheet that uses only `:focus-visible` still rebuilds
on a focus change. The gate can miss a rebuild it should have done; it cannot skip one it needed.
That direction is stated in the commit message because the opposite mistake — skipping a rebuild that
matters — produces a stale frame, which this project has already shipped twice.

## What I deliberately did not do

- **Did not port the symmetric-difference invalidation.** It needs per-node dirty tracking and a
  layout engine that can relayout a subtree; that is a real project, not an afternoon, and half of it
  would be worse than none.
- **Did not touch the DOM fingerprint** that decides timer repaints. Same idea, different mechanism,
  and it is a separate change.
- **Did not reopen the `display` question.** It is parked in `HANDOVER.md` with its two fixtures and no
  theory attached.
- **Did not touch the other three browser repositories.**

## Next

1. The symmetric-difference invalidation, when subtree relayout exists.
2. An exact dirty flag from the JS setters, replacing the DOM fingerprint.
3. The parked `display` question, with a rule-count print rather than a fixture bisect.
4. Family P0 builds still need a machine with dev packages.
