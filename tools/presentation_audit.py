#!/usr/bin/env python3
"""Audit a directory of repos against the repo-presentation skill, and say what each one needs.

    python3 tools/presentation_audit.py ~/code
    python3 tools/presentation_audit.py ~/code --json state/presentation-audit.json
    python3 tools/presentation_audit.py ~/code --only 'app-*'

`verify.py` (the skill's gate, copied verbatim next to this file) answers *what is missing*.
This answers the question that follows: **where does the work actually go** — is the app at
docs/play/, at docs/app.html, at the repo root, or not in the repo at all — and groups the
answer into a verdict and a build list, so a repo is worked on rather than rebuilt.

A repo that passes every surface is reported as `skip` and must be left alone.
"""
import argparse
import fnmatch
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    from verify import inspect, surface_rows
except ImportError:  # pragma: no cover
    sys.exit("verify.py must sit next to presentation_audit.py — copy both into tools/")

SURFACES = ["landing", "app", "badges", "shots", "readme", "support", "portrait", "theme",
            "offline", "platforms"]

# Where a web app entry point can hide. First hit wins.
CANDS = ["docs/play/index.html", "docs/demo/index.html", "docs/app.html", "index.html",
         "demo/index.html", "dist/index.html", "public/index.html", "src/index.html",
         "site/index.html", "app/index.html", "www/index.html"]

# Repos whose docs/index.html is the app rather than a page about it. Hand-checked; the
# heuristics below cannot tell a product page from a product.
APP_AT_DOCS = {"app-organon-reader", "control-panel"}
REPORT_PAGE = {"audit"}
SPECIAL = {
    "drsamonline": "The GitHub profile repo. Its README is the product; a docs/ landing page is optional.",
    "drsamonline.github.io": "The estate hub. Its own index.html is the front page for everything else.",
    "skills": "The skills catalogue. docs/index.html is the product, self-contained.",
    "Matneo": "The shop. docs/index.html is the storefront, not an app shell.",
    "profile-kit": "docs/index.html is the rendered profile — that is the product.",
    "neon-engine": "The engine has no demo of its own; the games it runs are in neon-games/play/.",
}
# Infrastructure: whether it wants a public face is the owner's call, not a checklist's.
DECIDE = {"backup", "compfactory", "HCS", "heavenzip", "ziptastic", "drsamonline", "audit"}

HEAD = {
    "split-done": "",
    "split-needed": "The app entry is %s — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.",
    "split-partial": "docs/play/ holds %s but no index.html — add docs/play/index.html as the entry, so the demo frame has one route to open.",
    "app-at-docs": "docs/index.html is the app itself — move it to docs/play/index.html, then build a landing page at docs/index.html in a different palette and type.",
    "no-docs": "The demo page is %s at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.",
    "landing-only": "There is no web app in this repo, so the demo band shows the screenshots rather than an iframe.",
    "no-web-surface": "Nothing web-facing exists yet. Decide first whether this repo wants a public face; if it does, the landing page comes first.",
    "report-page": "docs/index.html is a generated report, not an app — there is no demo to embed.",
    "special": "",
}

# Classes the owner has looked at and accepted. They stay measured — the surface column keeps
# saying what is true — but they are not work, and a re-run should not put them back on the list.
ACCEPTED = {
    "NETWORK-BADGE": "shields.io badges are deliberate: a committed SVG goes stale, a live badge does "
                     "not. Accepted 2026-11-03; see reports/2026-11-presentation-audit/README.md.",
    "APPLE": "bills nothing while every repo is public. Accepted 2026-11-03; reverses if a repo "
             "goes private.",
}

STEP = {
    "BADGES": "Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py, from this repo's own suite and LICENSE.",
    "SHOTS": "Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh, on a populated route.",
    "README": "README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.",
    "SUPPORT": "Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.",
    "PORTRAIT": "Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.",
    "NETWORK-BADGE": "Replace every shields.io <img> with the local docs/assets/badge-*.svg — a page that needs the network to describe itself has broken its own rule.",
    "APPLE": "Delete the Apple build target: the .dmg and its Download-for-Mac button, the macos-latest runner, the App Store link.",
}

SURFACE_LABELS = {"docs/index.html exists", "docs/play/index.html exists",
                  "all six badge SVGs exist",
                  "docs/assets/app-desktop.png looks like a real screenshot",
                  "README has a Support section", "landing page carries the support block",
                  "docs/assets/support-portrait.jpg exists",
                  "the support block inherits the page palette",
                  "no page loads anything from another origin",
                  "no macOS or iOS build targets"}


def html_under(d, depth=1):
    """Any .html at most `depth` directories below d."""
    for dirpath, dirnames, filenames in os.walk(d):
        if dirpath[len(d):].count(os.sep) > depth:
            dirnames[:] = []
            continue
        if any(f.endswith(".html") for f in filenames):
            return True
    return False


def shape_of(root, name):
    play_dir = os.path.join(root, "docs", "play")
    found = [c for c in CANDS if os.path.exists(os.path.join(root, c))
             and c != "docs/play/index.html"]
    if os.path.exists(os.path.join(play_dir, "index.html")):
        return "split-done", found[0] if found else ""
    if name in APP_AT_DOCS:
        return "app-at-docs", found[0] if found else ""
    if name in REPORT_PAGE:
        return "report-page", ""
    if name in SPECIAL:
        return "special", found[0] if found else ""
    if os.path.isdir(play_dir) and html_under(play_dir):
        entries = ["docs/play/%s/" % f for f in sorted(os.listdir(play_dir))
                   if os.path.isdir(os.path.join(play_dir, f))
                   and os.path.exists(os.path.join(play_dir, f, "index.html"))]
        return "split-partial", ", ".join(entries[:2])
    if os.path.exists(os.path.join(root, "docs", "index.html")):
        return ("split-needed" if found else "landing-only"), (found[0] if found else "")
    if found:
        return "no-docs", found[0]
    return "no-web-surface", ""


def classes_of(surfaces):
    pairs = (("landing", "LANDING"), ("app", "SPLIT"), ("badges", "BADGES"),
             ("shots", "SHOTS"), ("readme", "README"), ("support", "SUPPORT"),
             ("portrait", "PORTRAIT"), ("offline", "NETWORK-BADGE"),
             ("platforms", "APPLE"))
    return [code for surf, code in pairs if surfaces.get(surf) != "pass"]


def audit_one(root, name, strict=False):
    report = inspect(root)
    surfaces = dict(surface_rows(report))
    shape, entry = shape_of(root, name)
    classes = classes_of(surfaces)
    if name in SPECIAL and not classes and shape == "split-done":
        verdict = "skip"
    elif name in DECIDE or shape in ("no-web-surface", "report-page"):
        verdict = "decide"
    elif shape in ("split-done", "split-needed", "split-partial", "app-at-docs", "no-docs"):
        verdict = "apply"
    else:
        verdict = "apply-lite"

    build = []
    head = HEAD[shape]
    if head:
        build.append(head % (entry or "it") if "%s" in head else head)
    for code in classes:
        if code in ("LANDING", "SPLIT") or (code in ACCEPTED and not strict):
            continue
        build.append(STEP[code])
    for a in report["results"]:
        if a["status"] != "pass" and a["action"] and a["label"] not in SURFACE_LABELS:
            build.append("Failing check — %s: %s" % (a["label"], a["action"]))
    seen, steps = set(), []
    for s in build:
        if s not in seen:
            seen.add(s)
            steps.append(s)

    return {
        "repo": name,
        "verdict": verdict,
        "shape": shape,
        "app_entry": entry,
        "surfaces": surfaces,
        "classes": classes,
        "accepted": [c for c in classes if c in ACCEPTED],
        "fails": report["fails"],
        "warns": report["warns"],
        "build": steps,
        "note": SPECIAL.get(name, ""),
    }


def main():
    ap = argparse.ArgumentParser(description="Audit every repo in a directory against the skill.")
    ap.add_argument("parent", help="directory holding the repos")
    ap.add_argument("--only", help="shell-style pattern the repo name must match, e.g. 'app-*'")
    ap.add_argument("--json", help="write the full audit to this path")
    ap.add_argument("--strict", action="store_true",
                    help="also list the accepted classes as work (shields.io badges, Apple targets)")
    args = ap.parse_args()

    parent = os.path.abspath(args.parent)
    if not os.path.isdir(parent):
        sys.exit("not a directory: %s" % parent)

    rows = []
    for name in sorted(os.listdir(parent)):
        root = os.path.join(parent, name)
        if not os.path.isdir(root) or not os.path.isdir(os.path.join(root, ".git")):
            continue
        if args.only and not fnmatch.fnmatch(name, args.only):
            continue
        rows.append(audit_one(root, name, args.strict))

    if args.json:
        with open(args.json, "w") as fh:
            json.dump(rows, fh, indent=1)
        print("wrote %s (%d repos)" % (args.json, len(rows)))

    mark = {"pass": "ok", "warn": "wr", "fail": "XX", "missing": "-"}
    print("\n%-42s %-11s %-14s %s" % ("repo", "verdict", "shape", " ".join(s[:5] for s in SURFACES)))
    for r in rows:
        print("%-42s %-11s %-14s %s" % (
            r["repo"], r["verdict"], r["shape"],
            " ".join("%5s" % mark.get(r["surfaces"].get(s, "missing"), "?") for s in SURFACES)))

    counts = Counter(r["verdict"] for r in rows)
    print("\n%d repos · %s" % (len(rows), ", ".join("%s %d" % kv for kv in sorted(counts.items()))))
    bad = [r for r in rows if r["verdict"] != "skip"]
    print("%d need work, %d need nothing" % (len(bad), len(rows) - len(bad)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
