# Aetheris — batch A: sibling combinators, the attribute case flag, form states

Date: 2026-11-18 · Repo `drsamonline/The_Browser`
Commits: `dd310ca3`, `43b7ff4a`, `b97c843c`

First batch of the reviewed plan (`docs/PHASES.md`), taken straight off `docs/CHECKLIST.md`. Rows 1b, 1c, 1d —
one parser and resolver cycle, three features, because they touch the same two files.

## What I looked at upstream

Read before writing, for all three:

| Question | Where | What it said |
| --- | --- | --- |
| How are `+` and `~` matched? | `Rust/src/css/style/component_matching.rs:562` | `NextSibling` → `tree.previous_sibling(node)`, `SubsequentSibling` → `walk_back` over earlier siblings; matching runs right to left |
| How does `[a=v i]` work? | `Rust/src/css/style/selector.rs:442` | an `insensitive: bool` threaded into `equals(value, literal, insensitive)` for every match type |
| How do the form states work? | `CSS/SelectorMatching.cpp:165` | per-element facts: `matches_checked_pseudo_class()`, `matches_disabled_pseudo_class()`, `matches_placeholder_shown_pseudo_class()` |

## What shipped

| Feature | Detail |
| --- | --- |
| `+` `~` | previous-element-sibling walk, right to left; `>` and descendant unchanged |
| `[a=v i]` | flag parsed outside quotes; `[a=v s]` accepted as the default; comparison lowercased only when flagged |
| `:checked` `:unchecked` `:disabled` `:enabled` `:placeholder-shown` | attribute facts, no interaction state needed |

## The invalidation, which is the part that goes stale silently

| Change | Why it was necessary |
| --- | --- |
| `uses_positional_pseudo_class()` → `uses_sibling_sequence()` | a sibling combinator is the second way one child's presence restyles another. Without this, a child-list change would narrow to the parent alone and leave a `+`/`~` rule stale |
| a state change now dirties the element's siblings | `.a:hover + .b` is a real rule. Gated on `uses_sibling_sequence()` so pages without one pay nothing |

## Evidence

| Case | Result |
| --- | --- |
| `#r1 + .r` | only row 3 |
| `#r1 ~ .r` | rows 3 and 4 |
| `#box > .r` | unchanged, all four |
| `[data-mode=LIST i]` on `list` | matches |
| `[data-mode=LIST i]` on `grid` | does not match |
| `[data-mode=LIST]` (no flag) | does not match `list` |
| `:checked` | magenta on the checked control |
| `:disabled` | blue on the disabled control |
| `:placeholder-shown`, no value | cyan |
| `:placeholder-shown`, `value='f'` | not cyan |

    ctest --test-dir build --no-tests=error -j 8  ->  100% of 59, twice in a row (87 s)

## The fourth nested-syntax scanner, and it was brackets

`[data-mode=LIST i]` matched nothing. The space inside the brackets was read as a descendant combinator, so the
attribute selector was split into `div[data-mode=LIST` and `i]`.

Four scanners needed the same rule, and each was fixed in its own session:

| # | Scanner | Nested construct it ignored |
| --- | --- | --- |
| 1 | rule parser, comma split | `:is(a, b)` |
| 2 | combinator splitter, whitespace | `:is(a, b)` |
| 3 | compound scanner, marker stop | `:has(> .x)` |
| 4 | `depth_at()`, splitter, comma split, sibling scan | `[a=v i]` — **brackets**, not parentheses |

One mistake, four times: treating a nested construct as flat. `specificity()` is now the only scanner left that
walks a selector character by character without a depth notion, and it is flagged in `CHECKLIST.md`.

## Two "matcher bugs" that were the probe

`:checked` and `:placeholder-shown` each appeared to match the wrong control. Both times the fixture's inputs
carried the user-agent border, so a fixed 20 px probe step landed on the previous input — reading a neighbour's
colour and calling it a matcher fault. With `border:0` every case was right first time.

Three measurements lost to it, and the tell was there both times: the wrong colour was always *another
control's* colour. The test fixtures now set `border:0;margin:0;padding:0` and say why.

## What I deliberately did not do

- **No `:lang`, `:dir`, `:scope`.** They need document language and direction state that the engine does not
  carry; the row stays open in `CHECKLIST.md`.
- **No `:has(+ .x)`.** The sibling forms of `:has` still answer false. Now that `+`/`~` are matched, they could
  be implemented — but that is a separate item and it needs its own invalidation review.
- **No `:indeterminate`, `:required`, `:optional`, `:read-only`.** Each is one more attribute fact; none is on
  the plan.

## Next

1. Row 1e `localStorage` and 1f `focus()`/`getBoundingClientRect` — batch B, the JS bindings.
2. `specificity()` is the last scanner without a depth notion; check it before it becomes bug five.
3. `:has(+ .x)` now that sibling matching exists.
4. Tier 0 corpus, still blocked here — no open internet.
