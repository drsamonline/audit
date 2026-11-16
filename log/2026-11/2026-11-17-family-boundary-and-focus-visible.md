# The family boundary, and `:focus-visible` from upstream

Date: 2026-11-17 · Repos `drsamonline/{The_Browser,sorex,nodus,volumen}`
Commits: `8ce8a14e`, `2f63893`, `e50073e`, `60fc49f` (boundary), `4388fef3` (focus-visible)

Two things: the owner's correction that this repository is not a browser, and the next port from
`LibWeb`.

## What I looked at

Topics of all five repositories via the API, and `LibWeb`'s `Element::should_indicate_focus()`.

## 1. `audit` is not in the browser family

The owner's correction. Checked, and it was already true — `audit` carries
`changelog, devops, github-actions, tooling` and no `aetheris-family`; the four browsers each carry
`aetheris-family`.

What was missing was the rule being written down, so it cannot drift:

| Repo | FAMILY.md now states |
| --- | --- |
| The_Browser, sorex, nodus, volumen | "`drsamonline/audit` is **not** a member. It is the fleet changelog... A record that is also a participant stops being a record." |

The family is four browsers and a contract; anything else that wants in has to justify itself against
that sentence.

## 2. `:focus-visible`, ported

`should_indicate_focus()` returns true for text-entry controls, and otherwise follows whether the last
focus came from a **key** or a **pointer**. That is now the implementation:

- `VisualInteractionState` carries `FocusTrigger` (upstream's `HTML::FocusTrigger`), pointer by default.
- `:focus-visible` matches on `focused && (trigger == Key || node is input/textarea/select)`.
- `--focus-key <x> <y>` focuses with a keyboard trigger, so the rule is testable before Tab order
  exists; real keyboard focus will set the same field.

## Evidence

    fixture: #d:focus{green} #d:focus-visible{magenta}

    --click 200 80       -> div = (0, 170, 0)      :focus yes, :focus-visible no
    --focus-key 200 80   -> div = (255, 0, 255)    :focus-visible yes

    full suite: 100% tests passed out of 59
    commit: 4388fef3

**One branch is compiled but unproven**: the text-entry rule (`input`/`textarea`/`select`) could not be
checked by pixel, because this engine does not render form controls — an `<input>` paints as blank
white. That is recorded in the commit message rather than glossed as tested.

## What I deliberately did not do

- **Did not add `audit` to any family topic** or change its description. The correction was to state
  the boundary, not to move anything.
- **Did not implement Tab order.** It is what will set `FocusTrigger::Key` in real use, and it needs a
  definition of "focusable" that upstream spells out in sequential focus navigation.
- **Did not fake the text-entry branch** with a fixture that passes. A test that cannot distinguish
  the branch would be worse than the honest note.
- **Did not touch the other three browsers' code.** Documentation only there.

## Next

1. Tab order and `keyup` — the last two pieces of the focus model that upstream has.
2. Scoped style invalidation from `invalidate_style_after_pseudo_class_state_change`, replacing both
   the full rebuild on state change and the DOM fingerprint.
3. Form controls, so `:focus-visible`'s text-entry branch can be proven.
4. Family P0 builds still need a machine with dev packages.
