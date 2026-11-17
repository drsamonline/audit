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

## Batch B, first half: getBoundingClientRect()

Commits `f654adbf`, `8e90f626`, `438d0cf7`. Upstream returns the layout node's border box through the viewport
mapping (`DOM/Element.cpp`, `get_bounding_client_rect` → `Painting::bounding_client_rect`). Here the layout
node's rect is the border box in document coordinates and this path has no scroll offset, so the two coincide.
All eight DOMRect members are published.

The window loop now publishes the page it is driving (`g_current_page`), the way it already publishes the DOM
host, because the call has nothing but a handle to work from.

| box | reported |
| --- | --- |
| `#a`, 200×50 at the top | x 0, y 0, width 200, height 50 |
| its far edges | right 200, bottom 50 |
| `#b`, `margin-left:30px`, below `#a` | x 30, y 50, width 100, height 20 |

Proved by the page asserting its own numbers, which is the proof style the plan asks for: geometry checked by
arithmetic the page does, not by a pixel someone eyeballed.

**One honest difference from upstream.** There is no forced layout read. A script that runs at load has no
layout to measure and gets a zeroed rect — upstream returns an empty rect there too, but only after forcing the
read and answering with real numbers. Reading inside a timer works, which is where pages use it.

That cost one measurement: the first version returned `undefined` when no page was published yet, so
`rect.x` threw and the script produced no output at all. Silence, not a wrong number.

## The scanner row closed, and one gap left

`specificity()` was the last scanner walking a selector character by character. Probed with a rule whose score
depends on whether a space inside `[data-x="a b"]` counts as an element: it does not, so brackets are consumed
in one gulp and the row closes with no code change.

A residual is recorded rather than fixed: `specificity()` takes the **first** `)` when scoring a functional
pseudo-class, so `:is(:not(.a))` mis-scores by a class. Rare, and now written down instead of waiting to be
discovered.

## Batch B, second half: focus() and blur()

Commits `c1ec9b62`, `b73427e6`, `0889956a`. A script calls these while it is running, where the window loop's
document, interpreter and interaction state are not in scope, so they record a request and the loop performs it
with `set_focus()` — the same helper a click or a Tab key uses. The ordering written there (blur before the state
change, focus after) therefore applies unchanged.

| call | result |
| --- | --- |
| `element.focus()` on the first of two controls | magenta, the second stays green |
| `focus()` then `blur()` | back to green |

## One measurement that looked like a failure and was not

The first probe ran focus → focus → blur across three timers and ended with both controls green. I read that as
"focus does nothing". It was correct: the last call was `blur()`, and nothing was focused at the end. The
sequence has to be read before its final frame is judged.

## One real gap, opened as a row rather than hidden

The state moves and `:focus` styling follows, but a listener registered with `addEventListener('focus', ...)`
never runs. `set_focus()` guards its dispatch on `dom.handle_by_node`, so either the control has no handle or
the listener is not reachable from it — not yet established which.

It is a code comment at the call site, a row in `CHECKLIST.md` (1f3), and an entry in the open-defects table.
The test asserts the state only, because a test asserting the event would be asserting something this batch
does not do.

## Next

1. Row 1f3: why the focus event does not reach a listener. Start from `dom.handle_by_node` and whether a form
   control gets a handle at all.
2. Row 1e `localStorage`.
3. `:has(+ .x)` now that sibling matching exists.
4. Tier 0 corpus, still blocked here — no open internet.
