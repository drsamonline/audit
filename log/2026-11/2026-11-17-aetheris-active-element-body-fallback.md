# Aetheris — `activeElement` falls back to `body`

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `ae20834e`

Small straight port, no investigation.

## What upstream does

`Document::active_element()` (`DOM/Document.cpp:4295`) returns `m_active_element` if set, **else
`body()`**. A page can therefore assume `document.activeElement` is always an element. Aetheris returned
null when nothing was focused.

## What shipped

The window's `active_element` hook returns the focused element's handle, else the handle for the first
`body` in the document, else undefined.

## Evidence

    nothing focused, from a timer callback:   [js] MARK after thebody
    a click on a nested div (earlier test):   [js] MARK active inner
    full suite: 100% tests passed out of 59

## The limit, stated rather than hidden

The same fixture logs `null` for a script that runs *during* load:

    [js] MARK before null
    [js] MARK after thebody

Inline scripts execute inside `create_scripted_document`, before the window has a page to ask, so the
fallback has nothing to walk. Closing that needs the document root passed into the hook during
construction — a different change, recorded in `HANDOVER.md` under known limitations.

It is worth being precise about why this is acceptable rather than merely noted: `activeElement` is read
by event handlers and timers, both of which run after load. The load-time window is real but narrow, and
a page that reads it there gets `null` — the same as before this change, so nothing regressed.

## What I deliberately did not do

- **Did not pass the document root into the hook.** It touches the builder's signature and its two
  callers for a load-time-only case.
- **Did not add a test.** The behaviour is one console line away and the window-scripts test is already
  long; the next test added there should be the fingerprint replacement, which is worth more.
- **Did not start the DOM-fingerprint replacement.** It needs a mutation counter wired into every JS
  setter, and an under-counting counter produces exactly the stale-frame bug this project has shipped
  twice. It deserves a session where it can be done properly, not the tail of this one.
- **Did not touch the other three browser repositories.**

## Next

1. The mutation counter, replacing the DOM fingerprint — carefully, with every setter wired.
2. The parked `display` question, with a rule-count print.
3. Symmetric-difference invalidation, once subtree relayout exists.
4. Family P0 builds still need a machine with dev packages.
