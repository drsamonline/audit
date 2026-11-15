#!/usr/bin/env python3
"""Keep the README's fleet count in step with the snapshot it claims to describe.

    python3 tools/sync_readme.py            # report; exit 1 when stale
    python3 tools/sync_readme.py --write    # rewrite the line

Why this exists: the README said "78 repositories, 105 workflow files, 10 scheduled
jobs" while the committed snapshot held 135, 220 and 21. Every one of those numbers
was true when it was typed and none was true when it was read. A count in prose
drifts; a count read from a file does not.

The three figures come from the snapshot and nowhere else:

    repositories      state/repos.json  -> count
    workflow files    state/repos.json  -> sum of workflow_files per repo
    scheduled jobs    state/schedules.json -> number of entries

If a figure cannot be measured, this refuses rather than guessing.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state")
README = os.path.join(ROOT, "README.md")

# The one sentence this tool owns. Anchored on the em dash and the bold run, so a
# README edit that moves the sentence breaks the match loudly instead of silently
# rewriting the wrong words.
PATTERN = re.compile(
    r"(The change log for the drsamonline fleet — )\*\*\d+ repositories, "
    r"\d+ workflow files, \d+ scheduled jobs\*\*")


def measure() -> dict[str, int]:
    repos_path = os.path.join(STATE, "repos.json")
    sched_path = os.path.join(STATE, "schedules.json")
    if not os.path.exists(repos_path):
        sys.exit("no snapshot at %s - run tools/collect.py first" % repos_path)
    snap = json.load(open(repos_path))
    repos = snap.get("repos") or {}
    count = snap.get("count") or len(repos)
    workflows = sum(len(v.get("workflow_files") or []) for v in repos.values())
    schedules = 0
    if os.path.exists(sched_path):
        schedules = len(json.load(open(sched_path)))
    if not count:
        sys.exit("the snapshot says zero repositories - that is a failed crawl, not a fleet")
    return {"repositories": count, "workflows": workflows, "schedules": schedules}


def phrase(m: dict[str, int]) -> str:
    return ("**%d repositories, %d workflow files, %d scheduled jobs**"
            % (m["repositories"], m["workflows"], m["schedules"]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="rewrite the line")
    args = ap.parse_args()

    m = measure()
    text = open(README, encoding="utf-8").read()
    hit = PATTERN.search(text)
    if not hit:
        sys.exit("the headline sentence is gone or reworded. This tool owns exactly one "
                 "sentence, and it will not edit a README it does not recognise.")
    current = text[hit.start():hit.end()]
    wanted = hit.group(1) + phrase(m)
    if current == wanted:
        print("README is current: %s" % phrase(m))
        return 0
    if not args.write:
        print("README is stale.")
        print("  says: %s" % current.split("**")[1])
        print("  file: %s" % phrase(m).strip("*"))
        print("run: python3 tools/sync_readme.py --write")
        return 1
    open(README, "w", encoding="utf-8").write(text[:hit.start()] + wanted + text[hit.end():])
    print("README updated: %s" % phrase(m))
    return 0


if __name__ == "__main__":
    sys.exit(main())
