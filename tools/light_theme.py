#!/usr/bin/env python3
"""Give a landing page a light theme, in the page's own variables.

    python3 tools/light_theme.py <repo-dir> [...]

Reads the `:root` block, works out which variable means background, ink, muted,
line and card, and appends one override with light values. The accent is kept
unless it is too pale to read on paper, in which case it is darkened by the
smallest amount that makes it legible.

Nothing else is touched: no markup, no layout, no fonts.
"""
import os
import re
import sys

LIGHT = {
    "bg": "#f7f6f2", "paper": "#f7f6f2", "page": "#f7f6f2", "base": "#f7f6f2",
    "card": "#ffffff", "surface": "#ffffff", "panel": "#ffffff", "panel2": "#fbfaf7",
    "ink": "#14161a", "fg": "#14161a", "text": "#14161a", "on-board": "#14161a",
    "mut": "#5c6470", "muted": "#5c6470", "dim": "#5c6470", "fg2": "#5c6470",
    "line": "#e2ddd2", "border": "#e2ddd2", "frame": "#e2ddd2",
}
BG_NAMES = ("bg", "paper", "page", "base")
INK_NAMES = ("ink", "fg", "text")

BLOCK = """
  /* ---------- light theme ----------
     Added so the page reads on paper. It overrides the page's own variables and
     nothing else — no markup, no layout, no type. */
  :root, html {
    color-scheme: light;
%s
  }
"""


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    r, g, b = hex_rgb(h)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255


def darken(h, target=0.42):
    """Bring a colour down until it reads on a light ground."""
    if lum(h) <= target:
        return h
    r, g, b = hex_rgb(h)
    k = target / max(lum(h), 0.01)
    return "#%02x%02x%02x" % (max(0, min(255, int(r * k))),
                              max(0, min(255, int(g * k))),
                              max(0, min(255, int(b * k))))


def do(repo):
    page = os.path.join(repo, "docs", "index.html")
    if not os.path.exists(page):
        return "no docs/index.html"
    body = open(page, encoding="utf-8").read()
    if "light theme" in body and "--bg:#f7f6f2" in body.replace(" ", ""):
        return "already light"

    root = re.search(r":root\s*\{([^}]*)\}", body)
    if not root:
        return "no :root block to read"
    declared = dict(re.findall(r"--([a-z0-9-]+)\s*:\s*([^;]+)", root.group(1)))

    out = []
    for name, value in declared.items():
        value = value.strip()
        if name in LIGHT:
            out.append("    --%s: %s;" % (name, LIGHT[name]))
        elif name in ("acc", "accent") and value.startswith("#"):
            out.append("    --%s: %s;" % (name, darken(value)))
    if not any(("--" + n) in "\n".join(out) for n in BG_NAMES):
        return "could not tell which variable is the background"

    style_close = body.rfind("</style>")
    if style_close == -1:
        return "no <style> block"
    body = body[:style_close] + (BLOCK % "\n".join(out)) + body[style_close:]
    open(page, "w", encoding="utf-8").write(body)
    return "light theme added (%d variables)" % len(out)


if __name__ == "__main__":
    for repo in sys.argv[1:]:
        print("%-16s %s" % (os.path.basename(repo.rstrip("/")), do(repo)))
