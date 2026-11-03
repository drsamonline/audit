#!/usr/bin/env python3
"""Audit a directory of repos against the repo-presentation skill, and say what each one needs.

    python3 tools/presentation_audit.py ~/code
    python3 tools/presentation_audit.py ~/code --json state/presentation-audit.json
    python3 tools/presentation_audit.py ~/code --design      # the design clusters only
    python3 tools/presentation_audit.py ~/code --strict      # accepted classes back on the list

Two questions, and the second is the one that matters.

`verify.py` (the skill's gate, copied verbatim next to this file) answers *what is missing* — but
only against a single checklist, applied to everything. A kit is not a product: it has no UI to
screenshot and no demo to embed, and asking it for both buries the real gap in noise. So this adds
**tier** — app, app-no-demo, kit, data, infra — and the tier decides which surfaces are required.

The third thing it measures is design: the CSS class tokens, declared colours, font stacks and
heading sequences of every landing page, clustered by similarity. Six pages in this fleet are two
designs repeated three times, which a structural checklist cannot see.
"""
import argparse
import fnmatch
import itertools
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    from verify import inspect, surface_rows
except ImportError:  # pragma: no cover
    sys.exit("verify.py must sit next to presentation_audit.py — copy both into tools/")

SURFACES = ["landing", "app", "badges", "shots", "readme", "support", "portrait", "theme",
            "offline", "platforms"]

# The tier decides what is required. `app` and `app-no-demo` are products; a kit is code other
# projects consume, so it is asked for a landing page and never for a screenshot of an interface
# it does not have.
REQUIRED = {
    "app":         ["landing", "app", "badges", "shots", "readme", "support", "portrait",
                    "offline", "platforms"],
    "app-no-demo": ["landing", "badges", "shots", "readme", "support", "portrait",
                    "offline", "platforms"],
    "kit":         ["landing", "badges", "readme", "support", "portrait", "offline", "platforms"],
    "data":        ["landing", "badges", "readme", "support", "portrait", "offline", "platforms"],
    "infra":       ["landing", "readme", "support", "offline", "platforms"],
}

CODE = {"landing": "LANDING", "app": "SPLIT", "badges": "BADGES", "shots": "SHOTS",
        "readme": "README", "support": "SUPPORT", "portrait": "PORTRAIT",
        "offline": "NETWORK-BADGE", "platforms": "APPLE"}

# THEME (the block inherits the host palette) can only be checked once the block exists, so it is
# not separate work: pasting the block is what makes it pass.
IMPLIED = {"THEME"}

# Classes the owner has looked at and accepted. They stay measured — the surface column keeps
# saying what is true — but they are not work, and a re-run should not put them back on the list.
ACCEPTED = {
    "NETWORK-BADGE": "shields.io badges are deliberate: a committed SVG goes stale, a live badge "
                     "does not. Accepted 2026-11-03.",
    "APPLE": "bills nothing while every repo is public. Accepted 2026-11-03; reverses if a repo "
             "goes private.",
}

# Hand-decided, because no file listing tells you whether a repo is a product or a library.
TIER_OVERRIDE = {
    "art-kit": "kit", "astro-kit": "kit", "audio-kit": "kit", "book-kit": "kit",
    "case-kit": "kit", "compress-kit": "kit", "crypto-kit": "kit", "export-kit": "kit",
    "frame-kit": "kit", "game-kit": "kit", "lan-kit": "kit", "ml-kit": "kit",
    "optical-kit": "kit", "repertory-kit": "kit", "search-kit": "kit", "srs-kit": "kit",
    "ui-kit": "kit", "web-kit": "kit", "weft8-kit": "kit", "profile-kit": "kit",
    "app-companion-forge": "kit", "neon-engine": "kit", "saga-vn-engine": "kit",
    "aethelgard-rpg-engine": "kit", "weft8-compare": "kit", "weft8-classroom": "kit",
    "weft8-hardware": "kit", "app-builder": "kit",
    "app-organon-reader": "app", "control-panel": "app", "neon-games": "app",
    "seance": "app", "today-card": "app", "MATERIA-MEDICA-BUILDER": "app",
    "All4ONE": "app-no-demo", "CLDR": "app-no-demo", "HMS": "app-no-demo",
    "NEO": "app-no-demo", "SmartNotes": "app-no-demo", "TTB": "app-no-demo",
    "The_Browser": "app-no-demo", "ULTIMATE-WINDOWS-OPTIMIZER": "app-no-demo",
    "ai-bridge": "app-no-demo", "lexora": "app-no-demo", "neon-velocity": "app-no-demo",
    "ziptastic": "app-no-demo",
    "homoeopathic-materia-medica-repertory-json": "data", "skills": "data",
    "audit": "data", "drsamonline": "data", "drsamonline.github.io": "data", "Matneo": "data",
    "backup": "infra", "compfactory": "infra", "heavenzip": "infra", "HCS": "infra",
}

SKIP = {"lumen"}
REFERENCE_DESIGN = {"lumen", "repertory-reader", "app-thermals", "app-image-toolkit"}
# One shared design across a product family is defensible; across a game, a dashboard and a music
# app it is not.
FAMILY = {"BLINKTRANSFER / blinkcode-ai / helioprism"}

STEP = {
    "BADGES": "Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite "
              "and LICENSE. Keep the shields.io badges that are there — the local set is the "
              "offline fallback, not a replacement.",
    "SHOTS": "Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with "
             "scripts/shot.sh on a populated route.",
    "README": "README: badges first, the one-line promise, the four links, the <!-- shot:start --> "
              "block, then a ## Support table.",
    "SUPPORT": "Paste region 1 of assets/support-block.html into the landing footer and region 2 "
               "into the app header.",
    "PORTRAIT": "Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for "
                "the UPI QR.",
    "LANDING": "Build the landing page at docs/index.html from assets/landing-skeleton.html — one "
               "idea from the subject, its own palette and display face.",
}

HEAD = {
    "app-no-demo": "A desktop or extension product with no web UI: the demo band shows the "
                   "screenshots, not an iframe.",
    "kit": "A kit has no product UI — the landing page explains the API and shows a code sample, "
           "not an app screenshot. No docs/play/, no app shot.",
    "data": "A dataset or report has no demo; the landing page is the front door to the data.",
    "infra": "Infrastructure: decide first whether it wants a public face at all.",
}

SURFACE_LABELS = {"docs/index.html exists", "docs/play/index.html exists",
                  "all six badge SVGs exist",
                  "docs/assets/app-desktop.png looks like a real screenshot",
                  "README has a Support section", "landing page carries the support block",
                  "docs/assets/support-portrait.jpg exists",
                  "the support block inherits the page palette",
                  "no page loads anything from another origin",
                  "no macOS or iOS build targets"}

CANDS = ["docs/play/index.html", "docs/demo/index.html", "docs/app.html", "index.html",
         "demo/index.html", "public/index.html", "site/index.html", "app/index.html"]

# --- design -----------------------------------------------------------------
STYLE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
CLASS = re.compile(r'class="([^"]+)"')
FONT = re.compile(r"font-family\s*:\s*([a-zA-Z0-9 '\"\-]+)")
H2 = re.compile(r"<h2[^>]*>(.*?)</h2>", re.S | re.I)


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def norm(h):
    h = h.lower()
    return "".join(c * 2 for c in h) if len(h) == 3 else h


def design_of(root):
    body = read(os.path.join(root, "docs", "index.html"))
    if not body:
        return None
    style = " ".join(STYLE.findall(body))
    colours = {norm(h) for h in HEX.findall(style)}
    classes = set()
    for c in CLASS.findall(body):
        classes.update(c.split())
    fonts = set()
    for f in FONT.findall(style):
        f = f.split(",")[0].strip().strip("'\"").lower()
        if f and not f.startswith("var("):
            fonts.add(f)
    h2 = [re.sub(r"<[^>]+>", "", x).strip() for x in H2.findall(body)]
    sections = len(re.findall(r"<section", body, re.I))
    plain = (0 if sections >= 6 else 2 if sections >= 4 else 4) + \
            (0 if len(colours) >= 8 else 2 if len(colours) >= 5 else 4) + \
            (0 if fonts else 3) + (0 if "<iframe" in body else 1)
    return {
        "bytes": len(body), "colours": colours, "classes": classes, "fonts": fonts,
        "h2": h2, "sections": sections, "plain": plain,
        "skeleton_h2": any("what it refuses to do" in h.lower() for h in h2),
    }


def similarity(a, b):
    A, B = a["classes"] | a["colours"], b["classes"] | b["colours"]
    j = len(A & B) / len(A | B) if A and B else 0
    ha = {x.lower() for x in a["h2"]}
    hb = {x.lower() for x in b["h2"]}
    h = len(ha & hb) / len(ha | hb) if ha and hb else 0
    size = min(a["bytes"], b["bytes"]) / max(a["bytes"], b["bytes"])
    return 0.5 * j + 0.35 * h + 0.15 * size


def clusters(designs, threshold=0.55):
    parent = {k: k for k in designs}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    scored = []
    for a, b in itertools.combinations(sorted(designs), 2):
        s = similarity(designs[a], designs[b])
        scored.append((s, a, b))
        if s >= threshold:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra
    scored.sort(reverse=True)
    groups = defaultdict(list)
    for k in designs:
        groups[find(k)].append(k)
    return [sorted(v) for v in groups.values() if len(v) > 1], scored


# --- the audit ---------------------------------------------------------------
def tier_of(root, name):
    if name in TIER_OVERRIDE:
        return TIER_OVERRIDE[name]
    if any(os.path.exists(os.path.join(root, c)) for c in
           ("docs/play/index.html", "docs/demo/index.html", "docs/app.html")):
        return "app"
    if os.path.exists(os.path.join(root, "test-node.js")):
        return "kit"
    return "app-no-demo"


def app_entry(root, name):
    found = [c for c in CANDS if os.path.exists(os.path.join(root, c))
             and c != "docs/play/index.html"]
    if name in ("app-organon-reader", "control-panel"):
        return "docs/index.html (the app itself)"
    play = os.path.join(root, "docs", "play")
    if os.path.isdir(play) and not os.path.exists(os.path.join(play, "index.html")):
        subs = [f for f in sorted(os.listdir(play)) if os.path.isdir(os.path.join(play, f))]
        if subs:
            return "docs/play/%s/" % subs[0]
    return found[0] if found else ""


def audit_one(root, name, design=None, clone_group=""):
    report = inspect(root)
    surfaces = dict(surface_rows(report))
    tier = tier_of(root, name)
    req = REQUIRED[tier]
    na = [s for s in SURFACES if s not in req]
    classes = [CODE[s] for s in req if s in CODE and surfaces.get(s) != "pass"]
    accepted = [c for c in classes if c in ACCEPTED]
    work = [c for c in classes if c not in ACCEPTED and c not in IMPLIED]
    if name in SKIP:
        verdict = "skip"
    elif tier == "infra":
        verdict = "decide"
    else:
        verdict = "apply"

    flags = []
    if name in SKIP or name in REFERENCE_DESIGN:
        flags.append("reference")
    if clone_group:
        flags.append("clone:" + clone_group)
    if design and design["plain"] >= 8 and name not in SKIP:
        flags.append("plain")
    if design and design["skeleton_h2"] and name not in REFERENCE_DESIGN:
        flags.append("skeleton-heading")
    if not design and "LANDING" in work:
        flags.append("no-page")

    build = []
    if verdict != "skip":
        if tier == "app" and "SPLIT" in work:
            build.append("The app entry is %s — move it to docs/play/index.html and point the hero "
                         "CTA and the demo frame at play/." % (app_entry(root, name) or "the app"))
        elif tier in HEAD:
            build.append(HEAD[tier])
        if "LANDING" in work:
            build.append(STEP["LANDING"])
        reasons = []
        if clone_group:
            if clone_group in FAMILY:
                reasons.append("it shares one design with %s — the same product family, so keep one "
                               "of the three as the family look and give the other two their own "
                               "idea, palette and display face" % clone_group)
            else:
                reasons.append("it shares one design with %s — a game, a dashboard and a music app "
                               "are not one family, so all three need their own idea, palette and "
                               "display face" % clone_group)
        if design and "plain" in flags:
            reasons.append("the page is plain: %d sections, %d colours, %s"
                           % (design["sections"], len(design["colours"]),
                              "no display face of its own" if not design["fonts"] else
                              "type " + ", ".join(sorted(design["fonts"])[:2])))
        if "skeleton-heading" in flags:
            reasons.append("it still carries the skeleton's *What it refuses to do* heading, so the "
                           "section order is the template's, not this project's")
        if reasons:
            r = "; ".join(reasons)
            build.append("**Redesign it.** " + r[0].upper() + r[1:] +
                         ". One idea from the subject, used in the band, the hero and one accent.")
        for code in ("BADGES", "SHOTS", "README", "SUPPORT", "PORTRAIT"):
            if code in work:
                build.append(STEP[code])
        for x in report["results"]:
            if x["status"] == "fail" and x["action"] and x["label"] not in SURFACE_LABELS:
                build.append("Failing check — %s: %s" % (x["label"], x["action"]))

    seen, steps = set(), []
    for s in build:
        if s not in seen:
            seen.add(s)
            steps.append(s)

    return {
        "repo": name, "tier": tier, "verdict": verdict, "app_entry": app_entry(root, name),
        "surfaces": surfaces, "required": req, "na": na,
        "classes": classes, "accepted": accepted, "work": work,
        "fails": report["fails"], "warns": report["warns"],
        "design": None if not design else {
            "sections": design["sections"], "colours": len(design["colours"]),
            "fonts": sorted(design["fonts"]), "plain": design["plain"], "h2": design["h2"]},
        "design_flags": flags, "build": steps,
    }


def main():
    ap = argparse.ArgumentParser(description="Audit every repo in a directory against the skill.")
    ap.add_argument("parent", help="directory holding the repos")
    ap.add_argument("--only", help="shell-style pattern the repo name must match, e.g. 'app-*'")
    ap.add_argument("--json", help="write the full audit to this path")
    ap.add_argument("--design", action="store_true", help="print the design clusters and exit")
    ap.add_argument("--strict", action="store_true",
                    help="also list the accepted classes as work (shields.io badges, Apple targets)")
    args = ap.parse_args()

    parent = os.path.abspath(args.parent)
    if not os.path.isdir(parent):
        sys.exit("not a directory: %s" % parent)

    repos = [n for n in sorted(os.listdir(parent))
             if os.path.isdir(os.path.join(parent, n))
             and os.path.isdir(os.path.join(parent, n, ".git"))
             and (not args.only or fnmatch.fnmatch(n, args.only))]

    designs = {}
    for n in repos:
        d = design_of(os.path.join(parent, n))
        if d:
            designs[n] = d
    groups, scored = clusters(designs)
    clone_of = {}
    for g in groups:
        label = " / ".join(g)
        for n in g:
            clone_of[n] = label

    if args.design:
        print("landing pages fingerprinted: %d\n" % len(designs))
        print("=== clusters (structure + palette, similarity >= 0.55) ===")
        for g in groups:
            print("\n%d repos: %s" % (len(g), ", ".join(g)))
            print("   headings: %s" % " | ".join(designs[g[0]]["h2"][:6]))
        print("\n=== 15 most similar pairs ===")
        for s, a, b in scored[:15]:
            print("%.3f  %-30s %s" % (s, a, b))
        plain = sorted(n for n, d in designs.items() if d["plain"] >= 8 and n not in SKIP)
        skel = sorted(n for n, d in designs.items()
                      if d["skeleton_h2"] and n not in REFERENCE_DESIGN)
        print("\n=== plain (%d) ===\n%s" % (len(plain), ", ".join(plain)))
        print("\n=== still on the skeleton's heading (%d) ===\n%s" % (len(skel), ", ".join(skel)))
        return 0

    rows = [audit_one(os.path.join(parent, n), n, designs.get(n), clone_of.get(n, ""))
            for n in repos]
    if args.strict:
        for r in rows:
            r["work"] = r["classes"]
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(rows, fh, indent=1)
        print("wrote %s (%d repos)" % (args.json, len(rows)))

    mark = {"pass": "ok", "warn": "wr", "fail": "XX", "missing": "-"}
    print("\n%-40s %-11s %-9s %s" % ("repo", "tier", "verdict",
                                     " ".join(s[:5] for s in SURFACES)))
    for r in rows:
        cells = []
        for s in SURFACES:
            if s in r["na"]:
                cells.append("%5s" % "n/a")
            else:
                st = mark.get(r["surfaces"].get(s, "missing"), "?")
                if st == "XX" and CODE.get(s) in r["accepted"]:
                    st = "acc"
                cells.append("%5s" % st)
        print("%-40s %-11s %-9s %s" % (r["repo"], r["tier"], r["verdict"], " ".join(cells)))

    print("\n%d repos · tiers %s" % (
        len(rows), ", ".join("%s %d" % kv for kv in sorted(Counter(r["tier"] for r in rows).items()))))
    print("work: " + ", ".join("%s %d" % kv for kv in
                               sorted(Counter(c for r in rows for c in r["work"]).items())))
    print("nothing to do: %d" % sum(1 for r in rows if not r["work"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
