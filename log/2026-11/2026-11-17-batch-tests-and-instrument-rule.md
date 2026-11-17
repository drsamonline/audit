# Batch: colour helpers, the pseudo-class gate as tests, and "check the instrument" in five repos

Date: 2026-11-17 · Repos `drsamonline/{The_Browser,sorex,nodus,volumen}`
Commits: `79466784`, `b71a0f8`, `efe46a7`, `2d2ef9c`

Four items in one pass, at the owner's request to stop taking single small steps.

## 1. Colour helpers in the window test

```cpp
static bool is_magenta(int const (&rgb)[3]) { return rgb[0] > 200 && rgb[1] < 100 && rgb[2] > 200; }
static bool is_red(...); static bool is_green(...); static bool is_blue(...);
```

The three cases added today now use them instead of inline comparisons. The comment above them says why:
white is `(255,255,255)`, so `r > 200 && b > 200` matches white as well as magenta and quietly stops
asserting anything — which cost a session.

## 2. The pseudo-class gate, as two tests

| Page | `--move` over it | Asserted |
| --- | --- | --- |
| no `:hover` rule | `relayouts: 0` | no relayout |
| `#a:hover{...}` | not 0 | relayout |

Both directions, so a gate that stops rebuilding when it should rebuild fails as loudly as one that
rebuilds when it should not.

## 3. "Check the instrument before the subject" in five repos

| Repo | File | Commit |
| --- | --- | --- |
| The_Browser | `docs/HANDOVER.md` (before "Where things live") and `docs/UPSTREAM-FIRST.md` | `79466784` |
| sorex | `AGENTS.md` | `b71a0f8` |
| nodus | `AGENTS.md` | `efe46a7` |
| volumen | `AGENTS.md` | `2d2ef9c` |

The family repos keep the rule in `AGENTS.md`; `docs/UPSTREAM-FIRST.md` does not exist there, which the
first attempt discovered by failing to find it.

## 4. What the batch cost

| Step | Calls |
| --- | --- |
| state check | 1 |
| all edits | 1 |
| build (failed, two guards wrong) | 1 |
| fix + build + suite | 1 |
| family docs + commits | 1 |
| rebase + push | 1 |
| this entry | 1 |

Seven calls for four items, against roughly four calls per item before. The wasted call was a guard that
checked for the wrong string (`is_magenta` appeared inside a lambda that was later deleted) and a handover
heading that does not exist.

## Evidence

    ctest -j 8  ->  100% tests passed out of 59
    ahead/behind after push: 0 in all four repos

## What I deliberately did not do

- **Did not batch unrelated features into the same commit.** Each item is its own commit with its own
  message; batching is about round trips, not about blurring history.
- **Did not skip the audit entry.** One entry per batch, not one per commit.
- **Did not touch per-node dirty flags.** They remain the next real feature, and they want a session
  where scoped invalidation can follow in the same pass.

## Next

1. Per-node dirty flags + scoped invalidation, in one pass.
2. Family P0 builds, on a machine with dev packages.
3. `:focus-visible` for links (upstream's `is_focusable` interplay), if wanted.
