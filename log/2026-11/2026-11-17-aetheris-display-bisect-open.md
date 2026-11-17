# Aetheris — `display:block` on an anchor applies or not, depending on the fixture

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
No commit. Tree clean at `8ee71471`.

Follows `2026-11-17-aetheris-links-focusable.md`, which recorded that `a{display:block}` was honoured by
`--render` and ignored by `--window`. That framing was wrong: the difference is not the mode, it is the
fixture.

## What I measured

| Fixture | Mode | Layout |
| --- | --- | --- |
| `a{display:block;width:400px;height:100px;background:#00f}` | `--render` | stacked |
| same | `--window`, no key | **stacked** |
| same | `--window`, `--key tab` | **stacked** |
| `a{display:block;width:400px;height:100px;background:#00f;color:#fff}` + `a:focus-visible{background:#f0f}` | `--render` | stacked |
| same | `--window`, `--key tab` | **side by side** |

And the CSS handed to the page builder is byte-identical on both paths:

    [probe] render css=77
    [probe] window css=77

So: not the mode, not the CSS string, not the cascade as a whole. Two extra declarations change the
outcome — `color:#fff` and the `a:focus-visible` rule — and I did not get to which one.

## What this rules out

- **The window path is not at fault**, which is what the previous entry claimed. The same window run
  stacks the same links when those two declarations are absent.
- **`collect_page_style` is not mangling the CSS.** Both paths hand over 77 bytes; the probe printed the
  same length for each.
- **The user-agent stylesheet is present.** Settled two entries ago by the same probe.

## What is left, and the next probe

One of these two, and it is one bisect away:

1. `color:#fff` — a three-digit hex inside the same rule as `display:block`. If the declaration parser
   stops at an unsupported value, it would drop the *rest of the rule*; `display` is first, so this only
   explains the result if the whole rule is discarded and the visible boxes come from somewhere else.
2. `a:focus-visible` — the rule added this week. If its selector parse fails, it could disturb the
   preceding rule.

Next: run the four fixtures — with `color` only, with `:focus-visible` only, with neither, with both —
and print the parsed rule count from `create_from_document`. That is two builds and one probe, and it
answers it.

## What I deliberately did not do

- **Did not guess which declaration.** The last three sessions are a list of guesses that cost more than
  the bisect would have.
- **Did not leave the probe in.** `src/main.cpp` restored; `git status --porcelain` is empty.
- **Did not retract the previous entry's evidence, only its conclusion.** The measurements there were
  real; the attribution to "the window path" was not.
- **Did not touch the other three browser repositories.**

## Next

1. The four-fixture bisect above, with the parsed rule count printed.
2. Then the `display` fix, if there is one, in its own commit.
3. Scoped style invalidation from `invalidate_style_after_pseudo_class_state_change`.
4. Family P0 builds still need a machine with dev packages.
