# Session handoff and start prompt committed; the sandbox died mid-session

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commits: `c3695533` (handoff), `c884bf23` (start prompt)

## What happened

The session's code work was committed and pushed throughout: `408c4c1a` (style cache), `261feebe`
(attribute operators), `2133e576` (attribute selectors), `48089be1` (attribute gate), and earlier the
focus work. Then the sandbox began returning HTTP 500 for every command — including `pwd` — and stayed
that way for the rest of the session.

One change was **applied, built and green (59/59) but never committed**: incremental layout, first
increment. `/scratch/work` does not survive a recycle, so it is treated as lost. Its design is written
into the handoff so it can be re-applied in one pass.

## What was committed, and how

With the shell unavailable, both documentation files were committed through the GitHub contents API
instead — the same commits, same author, no shell needed. That is worth remembering: a dead sandbox does
not block repository writes when an API tool exists.

| File | Size | Commit |
| --- | --- | --- |
| `docs/SESSION-HANDOFF-2026-11-17.md` | 6421 B | `c3695533` |
| `docs/START-PROMPT.md` | 4639 B | `c884bf23` |

The start prompt deliberately carries **no state of its own**: it instructs the new session to clone and
read the handoff, `HANDOVER.md` and `UPSTREAM-FIRST.md` from the repository. A prompt that duplicates
state goes stale the moment the state changes; one that points at the repo cannot.

## What the handoff records

- the tree state at `408c4c1a` and the audit log at `b8b9d53`
- twelve commits with the evidence each was accepted on
- the incremental-layout design, including the call-order trap in `js_set_attribute`
  (`note_dom_mutation_at` clears the attribute name, so it must run before `note_attribute_mutation`)
- the environment recipe, including that a restored tree may be stale
- the five working rules the session earned
- four parked questions and the next four items in order

## What I deliberately did not do

- **Did not re-apply the lost change blind.** Writing a geometry-carry-over while the pod drops commands
  is how the stale-frame bug gets shipped a third time.
- **Did not put the design only in the prompt.** It is in the handoff, where the next session will look.
- **Did not claim the sandbox work was saved.** It was not; the handoff says so in the second section.

## Next

1. Re-apply incremental layout from the handoff and commit it; verify with its three-row table.
2. Cache across interaction-state changes.
3. Family P0 builds, on a machine with dev packages.
