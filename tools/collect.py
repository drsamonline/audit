#!/usr/bin/env python3
"""Collect the state of every drsamonline repository into state/.

Writes four JSON snapshots:

    state/repos.json      one record per repo: description, topics, homepage,
                          licence, Pages, root files, workflow files, releases
    state/schedules.json  every cron entry found in every workflow
    state/readmes.json    README.md text per repo
    state/licences.json   LICENSE text per repo

Everything is read-only against GitHub. Nothing is written outside state/.

Usage:
    GH_TOKEN=... python3 tools/collect.py
    python3 tools/collect.py --only today-card,seance     # a subset
"""
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys

OWNER = "drsamonline"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state")
LICENCE_NAMES = ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"]


def gh(path):
    """Call the GitHub API through the authenticated gh CLI."""
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def raw(repo, branch, path):
    url = "https://raw.githubusercontent.com/%s/%s/%s/%s" % (OWNER, repo, branch, path)
    r = subprocess.run(["curl", "-sS", "--max-time", "20", url],
                       capture_output=True, text=True)
    body = r.stdout
    if not body or body.strip().startswith("404:"):
        return ""
    return body


def fetch_repo(name):
    meta = gh("repos/%s/%s" % (OWNER, name)) or {}
    branch = meta.get("default_branch", "main")
    root = gh("repos/%s/%s/contents/" % (OWNER, name)) or []
    root = [f["name"] for f in root] if isinstance(root, list) else []
    wf = gh("repos/%s/%s/contents/.github/workflows" % (OWNER, name)) or []
    wf = [f["name"] for f in wf] if isinstance(wf, list) else []
    releases = gh("repos/%s/%s/releases?per_page=5" % (OWNER, name)) or []
    if not isinstance(releases, list):
        releases = []

    workflows = {}
    for f in wf:
        if f.endswith((".yml", ".yaml")):
            workflows[f] = raw(name, branch, ".github/workflows/" + f)

    readme = ""
    for cand in ("README.md", "readme.md", "README.MD", "README"):
        readme = raw(name, branch, cand)
        if readme:
            break

    licence_file, licence_text = "", ""
    for cand in LICENCE_NAMES:
        licence_text = raw(name, branch, cand)
        if licence_text:
            licence_file = cand
            break

    landing = raw(name, branch, "docs/index.html")

    return name, {
        "description": meta.get("description") or "",
        "homepage": meta.get("homepage") or "",
        "topics": meta.get("topics") or [],
        "licence_spdx": (meta.get("license") or {}).get("spdx_id"),
        "has_pages": meta.get("has_pages"),
        "default_branch": branch,
        "pushed_at": meta.get("pushed_at"),
        "root_files": root,
        "workflow_files": wf,
        "workflows": workflows,
        "releases": [{"tag": r.get("tag_name"),
                      "assets": [a["name"] for a in r.get("assets", [])]}
                     for r in releases],
        "readme": readme,
        "licence_file": licence_file,
        "licence_text": licence_text,
        "landing_html": landing,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma-separated repo names")
    args = ap.parse_args()

    repos = gh("users/%s/repos?per_page=100" % OWNER) or []
    names = [r["name"] for r in repos]
    if args.only:
        wanted = {x.strip() for x in args.only.split(",") if x.strip()}
        names = [n for n in names if n in wanted]

    if not names:
        sys.exit("no repositories found - is gh authenticated?")

    os.makedirs(STATE, exist_ok=True)
    records = {}
    with concurrent.futures.ThreadPoolExecutor(16) as ex:
        for name, rec in ex.map(fetch_repo, names):
            records[name] = rec
            print("  %-46s %s" % (name, "ok" if rec["readme"] else "NO README"), flush=True)

    schedules = {}
    for name, rec in records.items():
        for fname, text in rec["workflows"].items():
            for line in text.splitlines():
                s = line.strip()
                if s.startswith("- cron:") or s.startswith("cron:"):
                    schedules["%s/%s" % (name, fname)] = s.split(":", 1)[1].strip().strip("'\"")

    payload = {
        "repos": {n: {k: v for k, v in r.items() if k not in ("readme", "licence_text", "landing_html", "workflows")}
                  for n, r in records.items()},
        "count": len(records),
    }
    with open(os.path.join(STATE, "repos.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    with open(os.path.join(STATE, "schedules.json"), "w", encoding="utf-8") as fh:
        json.dump(schedules, fh, indent=1, sort_keys=True)
    with open(os.path.join(STATE, "readmes.json"), "w", encoding="utf-8") as fh:
        json.dump({n: r["readme"] for n, r in records.items()}, fh, indent=1, sort_keys=True)
    with open(os.path.join(STATE, "licences.json"), "w", encoding="utf-8") as fh:
        json.dump({n: {"file": r["licence_file"], "text": r["licence_text"]}
                   for n, r in records.items()}, fh, indent=1, sort_keys=True)

    print("\n%d repos -> state/repos.json, schedules.json, readmes.json, licences.json" % len(records))
    print("%d cron entries" % len(schedules))


if __name__ == "__main__":
    main()
