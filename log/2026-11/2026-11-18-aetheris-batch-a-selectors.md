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

## Row 1f3 closed: it was one request slot, not the handle guard

Commits `cffba72c`, `2323679e`, `77223d5c`. The row guessed `set_focus()`'s `dom.handle_by_node` guard. That was
wrong, and the probe that showed `__handlers_focus` had length 1 on the very handle being dispatched to killed
it in one step.

What was actually happening:

    setTimeout(function () { a.focus(); }, 5);
    setTimeout(function () { a.blur(); }, 12);

`run_timers()` runs **every timer due in one frame's budget**, so both callbacks ran in the same frame. `focus()`
set the single request slot, `blur()` replaced it with nullptr, and the loop performed a blur of nothing. The
state moved for neither, and no event fired — which looked exactly like "the event does not dispatch".

It is a queue now, drained in order:

| script | events | final state |
| --- | --- | --- |
| `focus()`, `blur()` in two timers | F, B | unfocused |
| `focus()` only | F | focused |
| `focus()`, `blur()`, `focus()` in one timer | F, B, F | focused |

## How it was narrowed, since that is the reusable part

| Probe | Result | Eliminated |
| --- | --- | --- |
| `__handlers_focus.length` on the target | 1 | "the listener is not registered" |
| same page without the `:focus` rule | event fires either way | the style re-resolve |
| both listeners, one timer | fires | the blur listener |
| one timer vs two | fires vs silent | **everything except what the two share: one `run_timers()` call** |

Four probes, each killing one hypothesis, and the fourth left a single mechanism. That is the shape to keep: the
discriminating probe is the one that varies *only* the thing you suspect.

## Row 1e: localStorage

Commits `e142b937`, `5dbd9d37`, `2d40f263`. Upstream's Storage interface (`HTML/Storage.idl`) is `length`,
`key(index)`, `getItem`, `setItem`, `removeItem`, `clear`, with one Storage object per origin held by the
document (`DOM/Document.h`, `m_local_storage_holder`).

Here the store is a map on the interpreter — which lives as long as the window — and the embedder sets the origin
when a page loads. A missing key returns `null`, not `undefined`.

| call | result |
| --- | --- |
| `setItem` twice, then `length` | 2 |
| `getItem` of a stored key | the value |
| `getItem` of a missing key | `null` |
| `key(0)` / `key(9)` | a stored key / `null` |
| `removeItem`, then `length` | 1 |
| `clear`, then `length` | 0 |

### Two limits, and one thing I refused to claim

- **In memory only.** Upstream persists a storage area per profile; this ends with the process.
- **`key(i)` is sorted, not insertion order** — the store is a `std::map`. A page walking keys by index sees
  them alphabetically.
- **Cross-load persistence is not proved.** It holds by construction (the interpreter outlives the document),
  but the harness cannot navigate: there is no `location` object and a click does not follow a link. It is a row
  in `CHECKLIST.md`, not a sentence in a commit message pretending to be evidence.

That last one is where this project keeps getting caught: a mechanism that is obviously true by construction is
exactly where an unexamined assumption survives. The row exists so the next session either proves it or finds it
broken.

## Navigation: location, and a click that follows a link

Commits `0f506632`, `58eff7ed`, `78bc3dfd`. This was the blocker for proving 1e2, and a gap in its own right.

- `location.href` (get and set), `assign()`, `reload()`. The JS module owns the object and asks the embedder two
  questions through hooks, so it knows nothing about sessions, tabs or fetching.
- A click on a link navigates unless a handler called `preventDefault()`; the anchor may sit above the node that
  was hit, so the walk goes up.
- URL resolution: absolute, root-relative, or relative to the last path segment. Not RFC 3986 — no dot-segment
  removal, no query merging — and the comment says so.

| step | result |
| --- | --- |
| page A at load | `location.href` is its own URL |
| click the link | page B loads, `location.href` is `/b` |
| page B reads localStorage | the value page A wrote |

### Two ordering bugs, both from the first probe

| Symptom | Cause |
| --- | --- |
| `location.href` empty on the first page | the URL was assigned after the page was built, and scripts run inside the build |
| localStorage `null` after navigating | the storage origin was assigned after the build, for the same reason |

Both are now set before `create_scripted_document()`. The pattern is worth naming: **anything a script can read
has to be true before the script runs**, and "before" here means before the call that runs it, not before the
function that contains that call.

### And one harness mistake of my own

The first probe served the same body for every path, so the navigation looked broken when it was working. The
second mistake was the flag: clicks take `--click X,Y`, not `--click-x`/`--click-y`, so two probes silently did
nothing. Both are the same error as ever — the instrument, not the subject.

## Next

1. `:has(+ .x)` now that sibling matching exists.
2. `history`, `location.pathname`/`search`/`hash`, dot-segment resolution (row 1g3).
3. Realm isolation on navigation (row 1g2) — the interpreter surviving is what makes localStorage work, and it
   is also why the old page's globals and listeners survive.
4. Tier 0 corpus, still blocked here — no open internet.
