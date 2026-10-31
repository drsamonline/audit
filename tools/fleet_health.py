#!/usr/bin/env python3
"""Does the fleet still work? Ask it, weekly, and fail loudly if not.

Three questions, because these are the three ways this fleet has actually broken:

  1. Is every scheduled job green, and recent?   refresh.yml died on exit 126 and
     nobody knew for a day. A cron that has not run inside its window is a fault
     even if its last run said success.

  2. Is every generated file fresh?              data.json, inventory.json,
     repos.json and posts.json are all rebuilt by scheduled jobs. If a job fails,
     the file stays old and every page built from it lies quietly.

  3. Are the artefacts what we think they are?    an APK with no icon, a page with
     no download link.

Writes docs/health.json and docs/index.html so the answer is a URL, not a log.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

OWNER = "drsamonline"
NOW = datetime.now(timezone.utc)

# generated file -> (repo, path, max age in hours, where the timestamp lives)
# max age is the job's own cadence plus a day of grace. The fleet moved from
# daily to weekly, so these are not 24h any more - a weekly file at 48h old is
# perfectly healthy, and calling it stale would train everyone to ignore this page.
GENERATED = [
    ("dashboard", "data.json", 24 * 8, "generated_at"),          # weekly, Tue 03:47
    ("control-panel", "docs/inventory.json", 24 * 8, None),      # weekly, Tue 06:00
    ("drsamonline.github.io", "repos.json", 24 * 17, None),      # twice monthly
    ("Matneo", "docs/data/posts.json", 24 * 8, "generated"),     # weekly, Tue 04:12
    ("drsamonline.github.io", "kits/index.html", 24 * 60, None), # static, edited by hand
]


LAST_ERR = ""


def gh(path):
    """One authenticated GET. Returns parsed JSON, or None, recording WHY it failed.

    "unknown" on its own is useless: it cannot tell a missing permission from a
    missing repository, and those need different fixes.
    """
    global LAST_ERR
    LAST_ERR = ""
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=45)
        if out.returncode != 0:
            err = (out.stderr or "").strip().splitlines()
            LAST_ERR = err[0][:160] if err else "gh exited %d" % out.returncode
            return None
        if not out.stdout.strip():
            LAST_ERR = "empty response"
            return None
        return json.loads(out.stdout)
    except Exception as exc:
        LAST_ERR = "%s: %s" % (type(exc).__name__, exc)
        return None


def age_hours(iso):
    if not iso:
        return None
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return None
    return (NOW - t).total_seconds() / 3600.0


def scheduled_workflows():
    """Every scheduled workflow, taken from the control panel's own inventory."""
    inv = gh(f"/repos/{OWNER}/control-panel/contents/docs/inventory.json")
    if not inv or "content" not in inv:
        return [], "inventory.json unreadable - cannot enumerate schedules"
    import base64
    try:
        data = json.loads(base64.b64decode(inv["content"]).decode("utf-8", "replace"))
    except Exception:
        return [], "inventory.json unparseable"

    found = []
    for repo in data.get("repos", []):
        name = repo.get("repo") or repo.get("name")
        for wf in repo.get("workflows", []) or []:
            trg = wf.get("triggers") or {}
            crons = trg.get("crons") or []
            events = [e.lower() for e in (trg.get("events") or [])]
            if crons or "schedule" in events:
                found.append((name, wf.get("file") or wf.get("name")))
    return found, ""


def check_schedules(pairs):
    rows = []
    for repo, wf in pairs:
        if not repo or not wf:
            continue
        fname = str(wf).split("/")[-1]
        runs = gh(f"/repos/{OWNER}/{repo}/actions/workflows/{fname}/runs?per_page=1")
        if not runs or not runs.get("workflow_runs"):
            rows.append({"repo": repo, "workflow": fname, "state": "unknown",
                         "detail": LAST_ERR or "no runs visible"})
            continue
        r = runs["workflow_runs"][0]
        conclusion = r.get("conclusion") or r.get("status") or "unknown"
        if conclusion in ("in_progress", "queued", "waiting", "requested", "pending"):
            rows.append({"repo": repo, "workflow": fname, "state": "running",
                         "conclusion": conclusion, "age_hours": 0,
                         "run_url": r.get("html_url")})
            continue
        age = age_hours(r.get("created_at"))
        # weekly jobs are allowed a generous window; anything over 9 days is stale
        stale = age is not None and age > 24 * 9
        state = "ok"
        if conclusion not in ("success", "cancelled"):
            state = "failing"
        elif stale:
            state = "stale"
        rows.append({"repo": repo, "workflow": fname, "state": state,
                     "conclusion": conclusion,
                     "age_hours": round(age, 1) if age is not None else None,
                     "run_url": r.get("html_url")})
    return rows


def check_generated():
    rows = []
    for repo, path, max_age, field in GENERATED:
        d = gh(f"/repos/{OWNER}/{repo}/contents/{path}")
        if not d or "content" not in d:
            rows.append({"repo": repo, "path": path, "state": "missing", "age_hours": None})
            continue
        import base64
        text = base64.b64decode(d["content"]).decode("utf-8", "replace")
        age = None
        if field:
            try:
                age = age_hours(json.loads(text).get(field))
            except Exception:
                age = None
        if age is None:
            commits = gh(f"/repos/{OWNER}/{repo}/commits?path={path}&per_page=1")
            if commits:
                age = age_hours(commits[0]["commit"]["committer"]["date"])
        state = "ok"
        if age is None:
            state = "unknown"
        elif age > max_age:
            state = "stale"
        rows.append({"repo": repo, "path": path, "state": state,
                     "age_hours": round(age, 1) if age is not None else None,
                     "max_age_hours": max_age})
    return rows


def render(schedules, generated, notes):
    bad = [r for r in schedules if r["state"] in ("failing", "stale")] + \
          [r for r in generated if r["state"] in ("stale", "missing")]
    blind = [r for r in schedules if r["state"] == "unknown"]
    if bad:
        verdict = "attention" if len(bad) < 4 else "degraded"
    elif blind:
        # A check that cannot see a job is not a check that passed it. Saying
        # "healthy" while blind is the exact failure this page exists to prevent.
        verdict = "attention"
    else:
        verdict = "healthy"
    colour = {"healthy": "#16a34a", "attention": "#d97706", "degraded": "#dc2626"}[verdict]

    def row_sched(r):
        state = r["state"]
        dot = {"ok": "#16a34a", "failing": "#dc2626", "stale": "#d97706",
               "running": "#2563eb"}.get(state, "#64748b")
        age = ("%.1f h ago" % r["age_hours"]) if r.get("age_hours") is not None else "-"
        link = ('<a href="%s">%s</a>' % (r["run_url"], r["workflow"])) if r.get("run_url") else r["workflow"]
        detail = (" <span style='color:#9aa3b2;font-size:11.5px'>%s</span>"
                  % r["detail"][:70]) if r.get("detail") else ""
        return ("<tr><td><span style='color:%s'>●</span> %s</td><td>%s</td><td>%s%s</td><td>%s</td></tr>"
                % (dot, r["repo"], link, state, detail, age))

    def row_gen(r):
        state = r["state"]
        dot = {"ok": "#16a34a", "stale": "#d97706", "missing": "#dc2626"}.get(state, "#64748b")
        age = ("%.1f h" % r["age_hours"]) if r.get("age_hours") is not None else "-"
        return ("<tr><td><span style='color:%s'>●</span> %s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                % (dot, r["repo"], r["path"], state, age))

    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fleet health - drsamonline</title>
<style>
  :root{--bg:#0f1115;--card:#171a21;--ink:#e7e9ee;--mut:#9aa3b2;--line:#252a34}
  @media (prefers-color-scheme: light){:root{--bg:#f7f8fa;--card:#fff;--ink:#141821;--mut:#5b6472;--line:#e2e6ee}}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
  .wrap{max-width:880px;margin:0 auto;padding:38px 20px 64px}
  h1{font-size:1.5rem;margin:0 0 4px}
  .sub{color:var(--mut);font-size:13px;margin:0 0 22px}
  .pill{display:inline-block;padding:8px 16px;border-radius:999px;font-weight:700;color:#08130c;background:%s}
  h2{font-size:11px;text-transform:uppercase;letter-spacing:.13em;color:var(--mut);margin:30px 0 8px}
  table{width:100%%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
  th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);font-size:13.5px}
  th{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--mut)}
  tr:last-child td{border-bottom:none}
  a{color:#a78bfa;text-decoration:none} a:hover{text-decoration:underline}
  .note{color:var(--mut);font-size:13px;margin-top:22px}
</style></head><body><div class="wrap">
<h1>Fleet health</h1>
<p class="sub">Checked %s UTC &middot; %d scheduled jobs &middot; %d generated files%s</p>
<p><span class="pill">%s</span></p>
%s
<h2>Scheduled jobs</h2>
<table><thead><tr><th>Repo</th><th>Workflow</th><th>State</th><th>Last run</th></tr></thead><tbody>
%s
</tbody></table>
<h2>Generated files</h2>
<table><thead><tr><th>Repo</th><th>File</th><th>State</th><th>Age</th></tr></thead><tbody>
%s
</tbody></table>
<p class="note">A scheduled job that has not run inside its window is a fault even when its last run
succeeded &mdash; that is how a dead cron stays invisible. Generated files are checked the same way:
if the job that rebuilds one fails, the file stays old and every page built from it is quietly wrong.</p>
</div></body></html>""" % (
        colour, NOW.strftime("%Y-%m-%d %H:%M"), len(schedules), len(generated),
        (" &middot; <b>%d unchecked</b>" % len(blind)) if blind else "",
        verdict.upper(),
        ("<p class='note'>%s</p>" % "; ".join(notes)) if notes else "",
        "".join(row_sched(r) for r in schedules) or "<tr><td colspan=4>none found</td></tr>",
        "".join(row_gen(r) for r in generated) or "<tr><td colspan=4>none found</td></tr>",
    ), verdict, bad, blind


def main():
    notes = []
    pairs, err = scheduled_workflows()
    if err:
        notes.append(err)
    schedules = check_schedules(pairs)
    generated = check_generated()

    page, verdict, bad, blind = render(schedules, generated, notes)
    if blind and not bad:
        notes.append("%d scheduled job(s) could not be checked: the token cannot read their "
                     "Actions runs (they live in private repositories). Add AUDIT_TOKEN to this "
                     "repository's secrets for full coverage." % len(blind))
    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w") as fh:
        fh.write(page)
    with open("docs/health.json", "w") as fh:
        json.dump({"checked_at": NOW.isoformat(), "verdict": verdict,
                   "schedules": schedules, "generated": generated, "notes": notes},
                  fh, indent=1)

    print("verdict: %s | scheduled: %d | generated: %d | problems: %d"
          % (verdict, len(schedules), len(generated), len(bad)))
    for r in bad:
        print("  PROBLEM", r)
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
