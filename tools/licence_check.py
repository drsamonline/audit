#!/usr/bin/env python3
"""Check the licence badge in every README against the LICENSE file it links to.

Four faults are detected, in the order they matter:

  1. CONTRADICTION  the badge names a licence the LICENSE file does not grant.
                    This is the one that matters - it is a legal statement.
  2. BROKEN URL     the badge URL contains a raw space (or an unescaped dash),
                    so GitHub truncates it and the badge renders short.
  3. NOASSERTION    a dynamic github/license badge on a repo GitHub cannot
                    classify, which renders the word "NOASSERTION".
  4. NO BADGE       a LICENSE file with no licence badge in the README.

Also checks the badge's alt text, because several READMEs carry
`![License: MIT]` in front of a PolyForm badge - the alt text is what a
screen reader and a failed image load both show.

Reads state/readmes.json, state/licences.json and state/repos.json.
The four faults above FAIL the check. Two further readings are reported and do
not: NO LICENCE (no LICENSE file, so a badge would claim something the repo does
not grant) and SUMMARY (a free-text claim no program can verify). Add --strict to
gate on those too.

    python3 tools/licence_check.py            # summary + every problem
    python3 tools/licence_check.py --quiet    # counts only
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state")

COLOURS = {
    "brightgreen", "green", "yellowgreen", "yellow", "orange", "red", "blue",
    "lightgrey", "lightgray", "grey", "gray", "blueviolet", "success",
    "important", "critical", "informational", "inactive", "purple", "pink",
    "black", "white", "teal", "cyan", "navy", "maroon", "olive", "lime",
    "aqua", "fuchsia", "silver",
}


def load(name, key=None):
    p = os.path.join(STATE, name)
    if not os.path.exists(p):
        sys.exit("missing %s - run tools/collect.py first" % p)
    with open(p, encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get(key, {}) if key else data


WINDOW = 600

# Order matters, and the window matters more. Reading the whole file picks up
# third-party credits ("built on the Android SDK (Apache License 2.0)") and
# withdrawal notices ("the MIT License previously applied is withdrawn"), both of
# which describe someone else's licence, not this repository's.
STANDARD = [
    ("polyform noncommercial", "PolyForm Noncommercial 1.0.0"),
    ("polyform small business", "PolyForm Small Business 1.0.0"),
    ("attribution-noncommercial-sharealike", "CC BY-NC-SA 4.0"),
    ("apache license", "Apache-2.0"),
    ("gnu general public", "GPL-3.0"),
    ("mit license", "MIT"),
    ("permission is hereby granted, free of charge", "MIT"),
    ("creative commons zero", "CC0 1.0"),
]

CUSTOM = ("proprietary", "all rights reserved", "free-to-use", "free to use",
          "not an open-source", "source-available", "eula", "permission from the author")


def actual_licence(text):
    """Name the licence the LICENSE file actually grants, from its opening."""
    head = text[:WINDOW].lower()
    full = text.lower()
    if "two different licences" in full or ("cc0 1.0" in full and "gnu general public" in full):
        return "Split licence (CC0 data + GPL-3.0 code)"
    for needle, name in STANDARD:
        if needle in head:
            return name
    if any(w in head for w in CUSTOM):
        return "All rights reserved"
    return "Unknown"


def badge_urls(text):
    """Every shields.io image URL in the README, .svg suffix stripped."""
    urls = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", text)
    urls += re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", text)
    # a URL with a raw space is truncated by the regex above, so catch those too
    urls += re.findall(r"(https?://img\.shields\.io/[^\n\"'<>]*?)\s*[\"')]", text)
    out = []
    for u in urls:
        if "shields.io" not in u:
            continue
        out.append(re.sub(r"\.svg(\?.*)?$", "", u))
    return out


def alt_texts(text):
    return re.findall(r"!\[([^\]]*)\]\(https?://img\.shields\.io/[^)]*licen[cs]e[^)]*\)", text, re.I)


def is_colour(c):
    c = c.lower()
    return c in COLOURS or bool(re.fullmatch(r"[0-9a-f]{3}|[0-9a-f]{4}|[0-9a-f]{6}|[0-9a-f]{8}", c))


FAMILIES = [
    ("mit", ("mit",)),
    ("polyform", ("polyform",)),
    ("apache", ("apache",)),
    ("cc", ("cc by", "cc-by", "creative commons")),
    ("gpl", ("gpl", "gnu general public")),
    ("proprietary", ("all rights reserved", "proprietary")),
    ("cc0", ("cc0", "public domain")),
]


def family(text):
    """The licence family a claim names, or None if it is a free-text summary."""
    t = (text or "").lower()
    for fam, needles in FAMILIES:
        if any(n in t for n in needles):
            return fam
    return None


def check(name, readme, licence_text, spdx):
    actual = actual_licence(licence_text)
    act_fam = family(actual)

    urls = [u for u in badge_urls(readme)
            if "licen" in u.lower() and ("/badge/" in u or "/github/license" in u)]
    if not urls:
        if not (licence_text or "").strip():
            # No LICENSE file at all. A badge here would claim a licence the
            # repository does not grant, which is worse than no badge - so this
            # is reported, not failed.
            return actual, "NO LICENCE", "", [
                "no LICENSE file - a badge here would claim a licence the repository "
                "does not grant; add the licence first, or leave it unbadged"]
        return actual, "NO BADGE", "", []

    problems, verdicts = [], []

    for u in urls:
        if "/github/license" in u:
            if spdx in (None, "NOASSERTION", "Other"):
                problems.append("dynamic github/license badge renders NOASSERTION for %s" % actual)
                verdicts.append("NOASSERTION")
            else:
                verdicts.append("ok")
            continue

        body = u.split("/badge/", 1)[1].split("?")[0]
        structural = []
        if " " in body:
            structural.append("raw space in URL - GitHub truncates the badge")
        decoded = body.replace("%20", " ").replace("_", " ")
        parts = decoded.split("-")
        if len(parts) < 3:
            structural.append("fewer than 3 segments, so there is no colour")
        else:
            if not is_colour(parts[-1]):
                structural.append('colour "%s" is not a valid shields colour' % parts[-1])
            if len(parts) > 3 and "--" not in body:
                structural.append('unescaped "-" splits the badge fields')
        claimed = "-".join(parts[1:-1]) if len(parts) > 2 else (parts[-1] if parts else "")
        claim_fam = family(claimed)

        if claim_fam and act_fam and claim_fam != act_fam:
            problems.append('badge says "%s" but LICENSE says "%s"' % (claimed, actual))
            verdicts.append("CONTRADICTION")
        if structural:
            problems.extend(structural)
            verdicts.append("BROKEN URL")
        if not claim_fam and not structural:
            problems.append('free-text claim "%s" - not a licence name, check it is still true'
                            % claimed)
            verdicts.append("SUMMARY")
        if claim_fam == act_fam and not structural:
            verdicts.append("ok")

    for alt in alt_texts(readme):
        alt_fam = family(alt)
        if alt_fam and act_fam and alt_fam != act_fam:
            problems.append('alt text says "%s" but LICENSE says "%s"' % (alt, actual))
            verdicts.append("CONTRADICTION")

    claimed = ""
    for u in urls:
        if "/badge/" in u:
            b = u.split("/badge/", 1)[1].split("?")[0].replace("%20", " ").replace("_", " ")
            p = b.split("-")
            claimed = "-".join(p[1:-1]) if len(p) > 2 else (p[-1] if p else "")
            break

    for v in ("CONTRADICTION", "BROKEN URL", "NOASSERTION", "SUMMARY", "ok"):
        if v in verdicts:
            return actual, v, claimed, sorted(set(problems))
    return actual, "ok", claimed, []


def main():
    quiet = "--quiet" in sys.argv
    readmes = load("readmes.json")
    licences = load("licences.json")
    repos = load("repos.json", "repos")

    rows = []
    for name in sorted(readmes):
        text = (licences.get(name) or {}).get("text", "")
        spdx = (repos.get(name) or {}).get("licence_spdx")
        actual, verdict, claimed, problems = check(name, readmes[name], text, spdx)
        rows.append(dict(repo=name, actual=actual, verdict=verdict,
                         claimed=claimed, problems=problems))

    order = ["CONTRADICTION", "BROKEN URL", "NOASSERTION", "NO BADGE",
             "NO LICENCE", "SUMMARY", "ok"]
    # What actually fails the run. The four faults are checkable against the
    # LICENSE file. NO LICENCE and SUMMARY are for a human to read: one says the
    # repository grants nothing, the other quotes a free-text claim ("free to
    # use") that no program can verify. Gating on those made this check red for
    # weeks over wording nobody had ruled wrong - a check that cries wolf gets
    # switched off. --strict puts them back in the gate.
    GATING = ("CONTRADICTION", "BROKEN URL", "NOASSERTION", "NO BADGE")
    counts = {k: sum(1 for r in rows if r["verdict"] == k) for k in order}

    print("licence badge check - %d repos\n" % len(rows))
    for k in order:
        print("  %-14s %d" % (k, counts[k]))
    strict = "--strict" in sys.argv
    bad = [r for r in rows
           if r["verdict"] in GATING or (strict and r["verdict"] != "ok")]
    advisory = [r for r in rows if r["verdict"] not in GATING and r["verdict"] != "ok"]
    print("\n  %d of %d repos fail the gate%s"
          % (len(bad), len(rows), "" if not advisory else
             " (%d more are advisory only - read them, they do not fail)"
             % len(advisory)))

    if not quiet:
        for k in order[:-1]:
            group = [r for r in rows if r["verdict"] == k]
            if not group:
                continue
            print("\n=== %s (%d) ===" % (k, len(group)))
            for r in group:
                print("  %-40s claims=%-32s actual=%s" % (r["repo"], r["claimed"] or "-", r["actual"]))
                for p in r["problems"]:
                    print("      - %s" % p)

    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
