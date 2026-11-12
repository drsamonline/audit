#!/usr/bin/env python3
"""Build the fleet report from state/, so the weekly run produces it and no session has to.

Every rule here was corrected at least once against real repositories, and the comment on
each one says what it got wrong before. That history is the point: a check that recognises
one convention reports every other convention as a failure, and the fleet has several.

    python3 tools/report.py            # writes docs/report.html
"""
import html
import json
import os
import re
import sys
from datetime import datetime, timezone

STATE = os.environ.get("STATE_DIR", "state")
OUT = os.environ.get("REPORT_OUT", "docs/report.html")

META_FILES = {"readme.md", "changelog.md", "license", "licence", "credits.md", "disclaimer.md",
              "release_notes.md", "enhancements.md", "attribution.md", "todo.md", "security.md",
              "privacy.md", "contributing.md", "code_of_conduct.md", "authors.md"}

# A repository's status is stated at its top, not anywhere in its text: the hub was flagged
# "work in progress" because one line of its catalogue describes a different repository.
STATUS_RE = re.compile(r"(in development|work in progress|no hosted|demo: none|"
                       r"not yet (built|implemented)|coming soon|planned for|status: (alpha|beta|wip))", re.I)

SUPPORT_MARKS = ("drsohilboi@ybl", "ko-fi.com", "paypal.me", "sponsors/drsamonline")
BADGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*(shields\.io|badge)[^)]*\)|<img[^>]+badge", re.I)


def load():
    repos = json.load(open(f"{STATE}/repos.json"))["repos"]
    try:
        readmes = json.load(open(f"{STATE}/readmes.json"))
    except Exception:
        readmes = {}
    return repos, readmes


def is_listy(name, rec, readme):
    """A curated list, a profile or a directory is not a product with a landing page.

    The first version read only the repository description, so a list that says "This is a
    list of single-file web apps" in its opening line was measured as an app missing a demo.
    """
    d = (rec.get("description") or "").lower()
    opening = (readme or "")[:600].lower()
    return (any(w in d for w in ("curated", "directory", "awesome", "a list of"))
            or any(w in opening for w in ("this is a list", "a list of", "a curated", "awesome-"))
            or name in ("drsamonline",))


def has_demo(rec, readme):
    # any index.html at any depth, an external homepage, or a binary-only repo
    files = rec.get("root_files") or []
    if any(f.endswith(".html") for f in files) or rec.get("docs_index"):
        return True
    if rec.get("has_pages") and rec.get("homepage"):
        return True
    if re.search(r"index\.html|/play/|\.exe|\.apk", readme or "", re.I):
        return True
    return False


def gaps(name, rec, readme):
    # AN ARCHIVED REPOSITORY IS FINISHED, not deficient. A kit that was merged into another
    # one is deliberately read-only with a pointer README; measuring it for a landing page,
    # a release or a screenshot asks it to keep working after it was retired.
    if rec.get("archived"):
        return []
    # A FORK IS SOMEONE ELSE'S PROJECT. Its licence, its badges, its support block and its
    # documentation are the upstream maintainer's decisions, not this fleet's: measuring them
    # here once produced a sweep that wrote this owner's UPI into four forks of other people's
    # work, and a licence the upstream had never granted. A fork is left alone.
    if rec.get("fork"):
        return []
    g = []
    r = readme or ""
    files = {f.lower() for f in (rec.get("root_files") or [])}
    product = not is_listy(name, rec, r)
    if not rec.get("homepage") and product:
        g.append("website")
    if not rec.get("topics"):
        g.append("topics")
    if not any(m in r for m in SUPPORT_MARKS):
        g.append("support")
    if not BADGE_RE.search(r):
        g.append("badges")
    if not re.search(r"!\[[^\]]*\]\([^)]*\.(png|jpe?g|gif|webp|svg)", r, re.I):
        g.append("screenshot")
    # documentation is what remains when the meta files are removed - AND a docs/ folder
    # counts, which the first version of this rule missed: it looked only at root files, so
    # 54 repositories that keep their documentation in docs/ were reported as having none
    docs = [f for f in files if f.endswith((".md", ".rst")) and f not in META_FILES
            and not f.startswith("readme") and not f.startswith("changelog")]
    if not docs and "docs" not in files and product:
        g.append("docs")
    if (not any(f.endswith(".html") for f in files) and not rec.get("docs_index")
            and product and not rec.get("has_pages")):
        g.append("landing")
    if product and not has_demo(rec, r):
        g.append("demo")
    if product and not rec.get("releases"):
        g.append("release")
    if not rec.get("licence_file"):
        g.append("licence")
    if len(r) < 1200:
        g.append("thin_readme")
    if STATUS_RE.search(r[:2000]):
        g.append("wip")
    return g


LABEL = {"website": "no website link", "topics": "no topics", "support": "no support block",
         "badges": "no README badges", "screenshot": "no screenshot", "docs": "no docs past README",
         "landing": "no landing page", "demo": "nothing clickable", "release": "no release",
         "licence": "no licence", "thin_readme": "thin README", "wip": "marked work-in-progress"}
ORDER = ["licence", "support", "website", "topics", "badges", "docs", "landing", "demo",
         "release", "screenshot", "thin_readme", "wip"]


def main():
    repos, readmes = load()
    rows, counts = [], {k: 0 for k in ORDER}
    for name in sorted(repos):
        rec = repos[name]
        g = gaps(name, rec, readmes.get(name, ""))
        for k in g:
            counts[k] = counts.get(k, 0) + 1
        rows.append((name, rec, g))
    total = len(repos)
    clean = sum(1 for _, _, g in rows if not g)
    now = datetime.now(timezone.utc).strftime("%d %B %Y")

    body = []
    for name, rec, g in sorted(rows, key=lambda x: (-len(x[2]), x[0])):
        if not g:
            continue
        body.append(
            "<tr><td><a href='https://github.com/drsamonline/%s'>%s</a></td><td>%s</td>"
            "<td>%s</td></tr>" % (
                html.escape(name), html.escape(name),
                html.escape(rec.get("description") or "—")[:150],
                ", ".join(LABEL[k] for k in ORDER if k in g)))

    cards = "".join(
        "<div class='card'><div class='n'>%d</div><div class='l'>%s</div></div>" % (counts[k], LABEL[k])
        for k in ORDER if counts[k])

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fleet report — {now}</title>
<style>
 body{{margin:0;font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",sans-serif;background:#f7f6f2;color:#1a1a1a}}
 .wrap{{max-width:64rem;margin:0 auto;padding:2.5rem 1.25rem}}
 h1{{font-size:2rem;margin:0 0 .25rem}} .sub{{color:#5c6470;margin:0 0 2rem}}
 .cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(11rem,1fr));gap:.75rem;margin:0 0 2rem}}
 .card{{background:#fff;border:1px solid #e2ddd2;border-radius:.6rem;padding:.9rem 1rem}}
 .card .n{{font-size:1.7rem;font-weight:700;line-height:1.1}} .card .l{{color:#5c6470;font-size:.86rem}}
 table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e2ddd2;border-radius:.6rem;overflow:hidden}}
 th,td{{text-align:left;padding:.6rem .8rem;border-bottom:1px solid #eee;vertical-align:top;font-size:.92rem}}
 th{{background:#f1efe9;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:#5c6470}}
 a{{color:#1f5f7a}}
</style></head><body><div class="wrap">
<h1>Fleet report</h1>
<p class="sub">{total} public repositories · {clean} with nothing outstanding · measured {now}</p>
<div class="cards">{cards}</div>
<table><thead><tr><th>Repository</th><th>What it is</th><th>Outstanding</th></tr></thead>
<tbody>{''.join(body) or '<tr><td colspan=3>nothing outstanding</td></tr>'}</tbody></table>
</div></body></html>"""

    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"{total} repos, {clean} clean, {sum(counts.values())} gaps -> {OUT}")
    for k in ORDER:
        if counts[k]:
            print(f"  {LABEL[k]:28} {counts[k]}")


if __name__ == "__main__":
    main()
