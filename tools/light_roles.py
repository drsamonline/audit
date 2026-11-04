#!/usr/bin/env python3
"""A light theme for pages that name their colours by meaning.

    python3 tools/light_roles.py <repo-dir> [...]

Some pages have no `--bg` and no `--ink`. They have `--navy`, `--char`, `--bone`,
and in one case a `--ink` that is the *background* and a `--text` that is the ink.
No amount of name-matching gets those right, and flipping every lightness produced
dark text on a dark ground.

But every one of them says which variable is which, in the body rule:

    body { background: var(--navy); color: var(--ink) }

So read that: the background and the text are facts the page states, and everything
else is classified by name — a line is a line, a panel is a panel, whatever is left
is the accent.

WHERE THIS IS NOT ENOUGH, AND THE HONEST ANSWER

Twelve pages in this estate paint themselves with more than variables: a fixed
`.bg-grid` layer, a `.bg-glow` radial gradient at z-index -3, component gradients
built from their own colours. Overriding the variables leaves those layers dark,
and the result is dark text on a dark ground — worse than leaving the page alone.

Those pages are dark by design, not by accident. Converting them is a redesign of
each one, page by page, with a render check each. Do not run this tool on them and
call it done; it will produce a page that looks broken, which is what happened the
first two times.
"""
import os
import re
import sys

PAPER, CARD, INK, MUTED, LINE = "#f7f6f2", "#ffffff", "#14161a", "#5c6470", "#e2ddd2"
