#!/usr/bin/env python3
"""Compare two state/ snapshots and print only what moved.

    python3 tools/diff.py old/state new/state
    python3 tools/diff.py state state.bak        # same tree, two moments

Silence means nothing changed. That is the point: a clean run prints
"no change", so any line of output is a real difference.
"""
import json
import os
import sys


def load(d, name):
    p = os.path.join(d, name)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    old_dir, new_dir = sys.argv[1], sys.argv[2]

    old = load(old_dir, "repos.json").get("repos", {})
    new = load(new_dir, "repos.json").get("repos", {})
    old_s = load(old_dir, "schedules.json")
    new_s = load(new_dir, "schedules.json")

    changes = []

    for name in sorted(set(new) - set(old)):
        changes.append("+ repo added: %s" % name)
    for name in sorted(set(old) - set(new)):
        changes.append("- repo removed: %s" % name)

    for name in sorted(set(old) & set(new)):
        a, b = old[name], new[name]
        for field in ("description", "homepage", "licence_spdx", "has_pages"):
            if a.get(field) != b.get(field):
                changes.append("~ %-34s %-14s %r -> %r" % (name, field, a.get(field), b.get(field)))
        for field in ("topics", "root_files", "workflow_files"):
            sa, sb = set(a.get(field) or []), set(b.get(field) or [])
            if sa - sb:
                changes.append("~ %-34s %-14s -%s" % (name, field, sorted(sa - sb)))
            if sb - sa:
                changes.append("~ %-34s %-14s +%s" % (name, field, sorted(sb - sa)))
        ra = {r["tag"]: r["assets"] for r in (a.get("releases") or [])}
        rb = {r["tag"]: r["assets"] for r in (b.get("releases") or [])}
        for tag in sorted(set(rb) - set(ra)):
            changes.append("+ %-34s release %s (%d assets)" % (name, tag, len(rb[tag])))

    for key in sorted(set(new_s) - set(old_s)):
        changes.append("+ schedule added: %s (%s)" % (key, new_s[key]))
    for key in sorted(set(old_s) - set(new_s)):
        changes.append("- schedule removed: %s" % key)
    for key in sorted(set(old_s) & set(new_s)):
        if old_s[key] != new_s[key]:
            changes.append("~ schedule %s: %s -> %s" % (key, old_s[key], new_s[key]))

    if not changes:
        print("no change")
        return
    for line in changes:
        print(line)
    print("\n%d change(s)" % len(changes))


if __name__ == "__main__":
    main()
