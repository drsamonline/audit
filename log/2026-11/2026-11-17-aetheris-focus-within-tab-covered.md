# Aetheris — `:focus-within` covered for the Tab path

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `0cbced61`

Closing a gap I had recorded against myself: `:focus-within` was verified with clicks only, and Tab
reaches the focus state through a different helper.

## Why one path passing did not imply the other

| Path | What sets the focus |
| --- | --- |
| click | `node_at` hit-test, then `set_focus` |
| Tab | `next_focusable` DOM walk, then `set_focus` |

The state is the same field, but the node comes from a different source — and this project has already
had a session where the hit-test path painted and the DOM-walk path did not.

## Evidence

Fixture: `#outer > #inner[tabindex]`, `#outer:focus-within{background:#ff0000}`, `--key tab`, 3 frames.

    frame-1: outer_below=(0, 0, 255)  inner=(0, 170, 0)      <- before Tab
    frame-2: outer_below=(255, 0, 0)  inner=(0, 170, 0)      <- :focus-within matched
    frame-3: outer_below=(255, 0, 0)  inner=(0, 170, 0)

    full suite: 100% tests passed out of 59

The child keeps its own background, which is the useful half: it shows `:focus-within` painted the
ancestor without the child's rule being overridden.

## What shipped

A pixel assertion in `AetherisWindowScripts`: the ancestor is red after Tab, the focused child keeps its
colour. Assertions on both, so a future change that paints everything red fails as loudly as one that
paints nothing.

## What I deliberately did not do

- **Did not add a `:focus-visible` text-entry case.** It still needs form controls to render; the branch
  stays compiled and unproven, as recorded.
- **Did not re-test `:hover` for the Tab path.** Hover does not involve focus; the pointer path is the
  only one.
- **Did not touch the other three browser repositories.**

## Next

1. Per-node dirty flags — the prerequisite for scoped invalidation, and groundwork with no visible win
   on its own, so it wants a session where it can be followed through to a measurement.
2. Family P0 builds still need a machine with dev packages.
3. Form controls, which unblock the `:focus-visible` text-entry test.
4. Symmetric-difference invalidation, once subtree relayout exists.
