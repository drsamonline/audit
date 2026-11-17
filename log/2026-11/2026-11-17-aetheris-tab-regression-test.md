# Aetheris — the Tab fix gets a test that can fail

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `bcb74730`

## What I looked at

`Tests/AetherisRendering/TestAetherisWindowScripts.cpp` and its `frame_pixel` helper, and the list of
things this project has fixed twice.

## What was wrong

Tab order and `:focus-visible` were verified with throwaway scripts in a session. That is precisely why
they broke twice: nothing in the suite failed when they did, so each regression was found by hand,
weeks of work later, by accident.

## What I changed

`AetherisWindowScripts` gains a case that drives `--key tab` against a one-element fixture and asserts
the frame after it is **magenta**.

The assertion is on the paint, not on the focus state. A stale frame with correct state is the exact
bug that shipped twice — an assertion on `relayouts` or on `activeElement` would have passed both times.

## Evidence

    ctest -R AetherisWindowScripts  ->  Passed  8.71 sec
    ctest -j 8 (full)               ->  100% tests passed out of 59

## The mistake in the first draft, kept in the record

The first version of this test had three assertions of the form

    require(std::rename(...) == 0 || true, "...");

which cannot fail. They were there because the helper only reads the last frame and I wanted to compare
before-and-after. The fix was to drop the comparison and assert the state that matters — the frame after
the Tab — rather than to keep ceremony that proves nothing.

An assertion that cannot fail is worse than no assertion: it inflates the count and teaches the next
person to trust a green suite.

## What I deliberately did not do

- **Did not add a helper for "read frame N".** It would have been three lines and it was not needed once
  the comparison was dropped; a helper that exists only to support a weak assertion is debt.
- **Did not test the wrapping behaviour** (Tab past the last element). It is one assertion away and it
  belongs with the links/form-controls work, where focusable elements become more than `tabindex`.
- **Did not touch the other three browser repositories.**

## Next

1. Links and form controls as focusable, with `:focus-within` for them.
2. Scoped style invalidation from `invalidate_style_after_pseudo_class_state_change`.
3. Tests for `:focus-visible`'s text-entry branch once form controls render.
4. Family P0 builds still need a machine with dev packages.
