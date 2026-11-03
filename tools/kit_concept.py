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

# The second half of the estate: the remaining ten kits, the three engines, the
# Forge tools and ziptastic. Kept in one table so a regeneration never has to guess.
EXTRA = {
    "frame-kit": ('<rect x="76" y="44" width="168" height="92" rx="4" stroke="%s"/>'
        '<rect x="88" y="56" width="144" height="68" rx="2" stroke="%s" opacity=".55"/>'
        '<path d="M96 118 l30-32 22 24 18-16 26 24" stroke="%s"/>'
        '<circle cx="196" cy="72" r="7" stroke="%s" opacity=".7"/>' % (INK, INK, INK, INK)),
    "game-kit": ('<rect x="78" y="66" width="164" height="60" rx="26" stroke="%s"/>'
        '<path d="M108 96 h20 m-10-10 v20" stroke="%s"/>'
        '<circle cx="176" cy="88" r="5" fill="%s" stroke="none"/>'
        '<circle cx="196" cy="104" r="5" fill="%s" stroke="none"/>' % (INK, INK, ACC, ACC)),
    "lan-kit": ('<rect x="62" y="66" width="60" height="44" rx="6" stroke="%s"/>'
        '<rect x="198" y="66" width="60" height="44" rx="6" stroke="%s"/>'
        '<path d="M122 88 h76" stroke="%s" stroke-dasharray="6 6"/>'
        '<circle cx="160" cy="88" r="6" fill="%s" stroke="none"/>' % (INK, INK, ACC, ACC)),
    "ml-kit": ('<circle cx="78" cy="70" r="9" stroke="%s"/><circle cx="78" cy="112" r="9" stroke="%s"/>'
        '<circle cx="160" cy="56" r="9" stroke="%s"/><circle cx="160" cy="92" r="9" stroke="%s"/>'
        '<circle cx="160" cy="128" r="9" stroke="%s"/><circle cx="240" cy="90" r="11" stroke="%s"/>'
        '<path d="M87 70 l64-12 M87 112 l64-20 M87 112 l64 16 M169 56 l62 32 M169 92 h60 M169 128 l62-36" stroke="%s" opacity=".45"/>'
        % (INK, INK, INK, INK, INK, ACC, INK)),
    "optical-kit": ('<rect x="84" y="48" width="72" height="72" rx="4" stroke="%s"/>'
        '<path d="M96 60h12v12H96z M120 60h12v12h-12z M96 84h12v12H96z M132 84h12v12h-12z" fill="%s" stroke="none"/>'
        '<path d="M168 84 h44" stroke="%s"/><path d="M212 84 l-10-8 m10 8 l-10 8" stroke="%s"/>'
        '<circle cx="240" cy="84" r="18" stroke="%s" opacity=".6"/>' % (INK, INK, ACC, ACC, INK)),
    "repertory-kit": ('<rect x="72" y="44" width="72" height="18" rx="4" stroke="%s"/>'
        '<rect x="72" y="82" width="72" height="18" rx="4" stroke="%s" opacity=".7"/>'
        '<rect x="72" y="120" width="72" height="18" rx="4" stroke="%s" opacity=".45"/>'
        '<path d="M144 53 h28 v38 h-28 M144 91 h28 v38 h-28 M172 91 h36" stroke="%s" opacity=".6"/>'
        '<circle cx="222" cy="91" r="10" stroke="%s"/>' % (INK, INK, INK, INK, ACC)),
    "search-kit": ('<rect x="62" y="52" width="128" height="76" rx="6" stroke="%s" opacity=".5"/>'
        '<path d="M76 70h100 M76 86h100 M76 102h64" stroke="%s" opacity=".45"/>'
        '<circle cx="212" cy="86" r="26" stroke="%s"/><path d="M231 105 l22 22" stroke="%s"/>'
        % (INK, INK, ACC, ACC)),
    "srs-kit": ('<rect x="70" y="62" width="56" height="72" rx="6" stroke="%s"/>'
        '<rect x="136" y="52" width="56" height="72" rx="6" stroke="%s" opacity=".7"/>'
        '<rect x="202" y="42" width="56" height="72" rx="6" stroke="%s" opacity=".45"/>'
        '<path d="M126 98 h14 m-8-6 8 6-8 6 M192 88 h14 m-8-6 8 6-8 6" stroke="%s"/>'
        % (INK, INK, INK, ACC)),
    "ui-kit": ('<rect x="66" y="46" width="188" height="96" rx="8" stroke="%s"/>'
        '<path d="M66 72 h188 M126 72 v70" stroke="%s" opacity=".5"/>'
        '<rect x="140" y="84" width="98" height="44" rx="5" stroke="%s" opacity=".6"/>'
        % (INK, INK, INK)),
    "web-kit": ('<rect x="76" y="44" width="168" height="98" rx="8" stroke="%s"/>'
        '<path d="M76 64 h168" stroke="%s" opacity=".5"/>'
        '<circle cx="90" cy="54" r="3" fill="%s" stroke="none"/>'
        '<rect x="90" y="76" width="70" height="8" rx="3" stroke="%s" opacity=".6"/>'
        '<rect x="90" y="92" width="140" height="6" rx="3" stroke="%s" opacity=".45"/>'
        '<rect x="90" y="120" width="48" height="12" rx="4" stroke="%s" opacity=".7"/>'
        % (INK, INK, INK, INK, INK, ACC)),
    "neon-engine": ('<rect x="86" y="46" width="148" height="88" rx="6" stroke="%s"/>'
        '<path d="M86 76h148 M86 106h148" stroke="%s" opacity=".35"/>'
        '<path d="M112 60h14v14h-14z M140 60h14v14h-14z M112 90h14v14h-14z" fill="%s" stroke="none"/>'
        '<path d="M140 90h14v14h-14z M168 90h14v14h-14z" fill="%s" stroke="none" opacity=".6"/>'
        % (INK, INK, ACC, ACC)),
    "saga-vn-engine": ('<circle cx="76" cy="90" r="10" stroke="%s"/>'
        '<path d="M86 90 h34 m0 0 v-30 h24 M120 90 v30 h24" stroke="%s"/>'
        '<rect x="144" y="46" width="46" height="26" rx="5" stroke="%s"/>'
        '<rect x="144" y="106" width="46" height="26" rx="5" stroke="%s"/>'
        '<circle cx="238" cy="59" r="8" stroke="%s" opacity=".7"/>'
        '<circle cx="238" cy="119" r="8" stroke="%s" opacity=".7"/>'
        % (INK, INK, INK, INK, ACC, ACC)),
    "aethelgard-rpg-engine": ('<path d="M84 128 V64 l76-18 76 18 v64" stroke="%s"/>'
        '<path d="M84 128 h152" stroke="%s"/>'
        '<path d="M122 128 V92 h30 v36 M186 128 V80 h30 v48" stroke="%s" opacity=".55"/>'
        '<circle cx="160" cy="36" r="7" stroke="%s"/>' % (INK, INK, INK, ACC)),
    "app-companion-forge": ('<path d="M96 120 h128 l-14-24 H110 Z" stroke="%s"/>'
        '<path d="M112 96 V72 h96 v24" stroke="%s" opacity=".6"/>'
        '<path d="M160 44 v22" stroke="%s"/><path d="M132 40 l28 14 28-14" stroke="%s"/>'
        % (INK, INK, INK, ACC)),
    "profile-kit": ('<rect x="96" y="40" width="128" height="104" rx="10" stroke="%s"/>'
        '<circle cx="160" cy="74" r="18" stroke="%s"/>'
        '<path d="M132 116 a28 20 0 0 1 56 0" stroke="%s" opacity=".7"/>' % (INK, INK, INK)),
    "app-builder": ('<rect x="70" y="86" width="52" height="52" rx="5" stroke="%s"/>'
        '<rect x="70" y="46" width="52" height="26" rx="5" stroke="%s" opacity=".5"/>'
        '<path d="M134 92 h32 m-10-8 10 8-10 8" stroke="%s"/>'
        '<rect x="180" y="60" width="72" height="78" rx="8" stroke="%s"/>' % (INK, INK, ACC, INK)),
    "ziptastic": ('<rect x="66" y="72" width="60" height="40" rx="6" stroke="%s"/>'
        '<path d="M126 92 h30" stroke="%s"/>'
        '<rect x="156" y="64" width="44" height="56" rx="6" stroke="%s" opacity=".7"/>'
        '<path d="M200 92 h26" stroke="%s"/>'
        '<rect x="226" y="76" width="34" height="32" rx="5" stroke="%s"/>'
        '<path d="M78 84h36 M78 92h28 M78 100h20" stroke="%s" opacity=".4"/>'
        % (INK, ACC, INK, ACC, ACC, INK)),
}
MOTIFS.update(EXTRA)

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
