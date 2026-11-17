# Aetheris — attribute selectors, and the loop they close

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `2133e576`

## What upstream does

Attribute selectors are part of compound matching; specificity counts them as a class (one `[` = +1
class). Upstream supports operators (`~=`, `^=`, `$=`, `*=`, `|=`), a case-sensitivity flag and
namespaces.

## What shipped

`[name]` and `[name=value]`, with an optional quoted value, parsed in the same splitter that already
handled `#`, `.` and `:`. Specificity counts an attribute selector as a class.

## Why this mattered beyond styling

The previous commit gated attribute writes: an attribute no selector mentions does not relayout.
`uses_attribute` scanned selector **text**, so it could already see `[data-x]` — but nothing could match
one, so the gate's positive case had no rule to find. The two changes together are the correct pair:

| Page | Write | Relayouts |
| --- | --- | --- |
| no `[data-x]` rule | `setAttribute('data-x')` | 0 |
| `[data-x]` rule | `setAttribute('data-x')` | 6 |

Without the selector support, the gate would have been right by accident; with it, the gate is right by
construction.

## Evidence

    [data-x] on an element with data-x   -> (255,0,255) magenta
    [data-x] on an element without       -> (0,0,255)   blue
    [data-y=one] with data-y="one"       -> (0,255,0)   green
    [data-y=one] with data-y="two"       -> (0,0,255)   blue
    timer writing an observed data-x     -> relayouts 6

    ctest -j 8  ->  100% tests passed out of 59

## The one failure on the way

`attr pixel 1` failed because the new case passed a frame directory without creating it first; every
other case in the file does `rm -rf ... && mkdir -p ...` and this one did not. Fixed in the test, not
worked around.

## What I deliberately did not do

- **Did not implement the operators.** `[name]` and `[name=value]` are what pages actually use for
  styling hooks; `^=` and friends are a follow-up with no invalidation consequence.
- **Did not implement the case-insensitivity flag or namespaces.** Recorded as limits.
- **Did not touch specificity beyond counting the bracket.** A more precise model would weight
  `[name=value]` the same, which is what the spec says.

## Next

1. Per-node dirty flags **with** incremental layout — together or not at all.
2. Family P0 builds, on a machine with dev packages.
3. Attribute selector operators, if a page needs them.
