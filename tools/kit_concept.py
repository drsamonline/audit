#!/usr/bin/env python3
"""Draw each kit's idea as a small SVG, and put it on the kit's page.

    python3 tools/kit_concept.py <repo-dir> [...]

One visual language for all of them — a 320x180 frame, thin strokes, one accent,
no gradients, no text — so the estate reads as a family. The motif is the kit's
concept, not its name in a box:

    art      three primitives overlapping
    astro    orbits around a body
    audio    a waveform in a frame
    book     stacked signatures, one open
    case     a folder with a seal
    compress nested frames, shrinking
    crypto   a key and a sealed note
    export   a tray with an arrow leaving
"""
import os
import re
import sys

W, H = 320, 180
INK, ACC, DIM = "#101728", "#a97b1e", "#c9cfdd"

def frame(inner, accent=ACC):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
        'aria-label="A diagram of what this kit does">\n'
        '  <rect width="%d" height="%d" rx="14" fill="none" stroke="%s" stroke-width="1" opacity=".45"/>\n'
        '  <g fill="none" stroke="%s" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">\n'
        '%s\n  </g>\n</svg>\n' % (W, H, W, H, DIM, accent, inner))


MOTIFS = {
    "art-kit": (
        '<circle cx="126" cy="88" r="34" stroke="%s"/>'
        '<rect x="150" y="56" width="62" height="62" rx="6" stroke="%s"/>'
        '<path d="M112 128 L140 74 L168 128 Z" stroke="%s" opacity=".75"/>' % (INK, INK, INK)),

    "astro-kit": (
        '<circle cx="160" cy="90" r="16" fill="%s" stroke="none"/>'
        '<ellipse cx="160" cy="90" rx="86" ry="34" stroke="%s"/>'
        '<ellipse cx="160" cy="90" rx="62" ry="60" stroke="%s" opacity=".6" '
        'transform="rotate(-24 160 90)"/>'
        '<circle cx="238" cy="74" r="5" fill="%s" stroke="none"/>' % (INK, INK, INK, INK)),

    "audio-kit": (
        '<path d="M60 90 h18 l10-30 14 60 12-44 10 28 12-16 h124" stroke="%s"/>'
        '<path d="M60 132 h200" stroke="%s" opacity=".4" stroke-dasharray="4 6"/>' % (INK, INK)),

    "book-kit": (
        '<path d="M84 118 V58 h58 v60" stroke="%s"/>'
        '<path d="M142 58 l34-14 v60 l-34 14" stroke="%s"/>'
        '<path d="M84 118 l34-14" stroke="%s"/>'
        '<path d="M196 60 v58 h44" stroke="%s" opacity=".55"/>' % (INK, INK, INK, INK)),

    "case-kit": (
        '<path d="M78 74 h48 l10 12 h106 v58 H78 Z" stroke="%s"/>'
        '<path d="M78 74 v-8 h34 v8" stroke="%s" opacity=".6"/>'
        '<circle cx="208" cy="118" r="16" stroke="%s"/>'
        '<path d="M208 110 v6 l6 6" stroke="%s"/>' % (INK, INK, ACC, ACC)),

    "compress-kit": (
        '<rect x="56" y="46" width="120" height="88" rx="8" stroke="%s" opacity=".45"/>'
        '<rect x="86" y="66" width="80" height="58" rx="6" stroke="%s" opacity=".7"/>'
        '<rect x="112" y="84" width="42" height="30" rx="4" stroke="%s"/>'
        '<path d="M204 90 h56 m-14-14 14 14-14 14" stroke="%s"/>' % (INK, INK, INK, ACC)),

    "crypto-kit": (
        '<circle cx="104" cy="90" r="16" stroke="%s"/>'
        '<path d="M120 90 h84 m-16 0 v16 m-18-16 v12" stroke="%s"/>'
        '<rect x="206" y="66" width="54" height="48" rx="6" stroke="%s" opacity=".7"/>'
        '<path d="M206 78 l27 18 27-18" stroke="%s" opacity=".7"/>' % (INK, INK, INK, INK)),

    "export-kit": (
        '<path d="M74 76 h96 v64 H74 Z" stroke="%s"/>'
        '<path d="M74 76 l24-18 h72 v18" stroke="%s" opacity=".7"/>'
        '<path d="M122 132 V92 m-16 16 16-16 16 16" stroke="%s"/>'
        '<path d="M196 90 h50 m-14-14 14 14-14 14" stroke="%s"/>' % (INK, INK, ACC, ACC)),
}

BLOCK = '''
<figure style="margin:26px 0 0;text-align:center">
  <img src="assets/concept.svg" alt="A diagram of what this kit does"
       style="width:100%%;max-width:320px;height:auto">
</figure>
'''


def do(repo):
    name = os.path.basename(repo.rstrip("/"))
    motif = MOTIFS.get(name)
    if not motif:
        return "no motif drawn for this kit yet"
    page = os.path.join(repo, "docs", "index.html")
    if not os.path.exists(page):
        return "no docs/index.html"
    os.makedirs(os.path.join(repo, "docs", "assets"), exist_ok=True)
    svg = frame(motif)
    open(os.path.join(repo, "docs", "assets", "concept.svg"), "w").write(svg)

    body = open(page, encoding="utf-8").read()
    if "assets/concept.svg" in body:
        return "concept already on the page"
    # after the first paragraph of the page, which is where the idea is stated
    m = re.search(r"</p>", body, re.I)
    at = m.end() if m else body.find("</h1>")
    if at == -1:
        return "could not find a place to put it"
    body = body[:at] + BLOCK % () + body[at:]
    open(page, "w", encoding="utf-8").write(body)
    return "concept drawn and placed"


if __name__ == "__main__":
    for repo in sys.argv[1:]:
        print("%-16s %s" % (os.path.basename(repo.rstrip("/")), do(repo)))
