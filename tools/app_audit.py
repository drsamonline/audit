#!/usr/bin/env python3
"""Read an app the way a browser reads it: what did it complain about?

    python3 tools/app_audit.py <repo-dir> [...]
    python3 tools/app_audit.py <repo-dir> --wait 3000

The page checks in verify.py look at the source — does the file exist, is the
markup right. This loads the app in a real engine and records what it says: a
script that threw, a promise nobody caught, a resource that 404'd, a button that
is in the DOM but wired to nothing.

It works by copying the app, injecting a probe that listens, and reading the
result out of the document title. Crude, and it needs no CDP client, no puppeteer
and no network.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PROBE = """
<script>
/* injected by tools/app_audit.py — records what the page complains about */
(function () {
  var errs = [], missing = [], unhandled = [];
  window.addEventListener('error', function (e) {
    if (e && e.target && e.target !== window && e.target.tagName) {
      var t = e.target;
      /* A module script never loads over file:// — the browser refuses it for CORS
         reasons — so its failure here says nothing about the deployed site. */
      if (t.tagName === 'SCRIPT' && t.type === 'module') return;
      var src = t.src || t.href || '';
      if (src) missing.push(t.tagName.toLowerCase() + ':' + src.split('/').slice(-1)[0]);
      return;
    }
    errs.push(String((e && e.message) || 'error'));
  }, true);
  window.addEventListener('unhandledrejection', function (e) {
    unhandled.push(String((e && e.reason && (e.reason.message || e.reason)) || 'rejection'));
  });
  var empty = [];
  function look() {
    /* a button with no handler and no form is a button that does nothing */
    var bs = document.querySelectorAll('button');
    for (var i = 0; i < bs.length; i++) {
      var b = bs[i];
      if (b.type === 'submit' || b.closest('form') || b.dataset.k || b.dataset.go) continue;
      if (!b.getAttribute('onclick') && !b.id) empty.push((b.textContent || '?').trim().slice(0, 18));
    }
    document.title = 'AUDIT|' + JSON.stringify({
      errors: errs.slice(0, 6), rejections: unhandled.slice(0, 6),
      missing: missing.slice(0, 8), unlabelledButtons: empty.slice(0, 8)
    });
  }
  window.addEventListener('load', function () { setTimeout(look, %(wait)d); });
  setTimeout(look, %(wait)d + 1200);
})();
</script>
"""


def audit(repo, wait=2000):
    play = os.path.join(repo, "docs", "play")
    if not os.path.isdir(play):
        return {"repo": os.path.basename(repo), "skipped": "no docs/play"}

    # copy the whole docs/ tree, not just play/: an app that references ../screenshots/
    # or ../landing.css resolves those paths relative to the site root, and a copy of
    # play/ alone makes them look missing when they are not.
    tmp = tempfile.mkdtemp(prefix="appaudit-")
    work = os.path.join(tmp, "play")
    shutil.copytree(os.path.dirname(play), os.path.join(tmp, "docs"))
    work = os.path.join(tmp, "docs", "play")
    index = os.path.join(work, "index.html")
    body = open(index, encoding="utf-8", errors="replace").read()
    body = body.replace("</body>", PROBE % {"wait": wait} + "</body>", 1)
    open(index, "w", encoding="utf-8").write(body)

    try:
        out = subprocess.run(
            ["chromium", "--headless=new", "--no-sandbox", "--disable-gpu",
             "--allow-file-access-from-files", "--virtual-time-budget=%d" % (wait + 2500),
             "--dump-dom", "file://" + index],
            capture_output=True, text=True, timeout=90).stdout
    except subprocess.TimeoutExpired:
        shutil.rmtree(tmp, ignore_errors=True)
        return {"repo": os.path.basename(repo), "skipped": "timed out"}

    m = re.search(r"<title>AUDIT\|(.*?)</title>", out, re.S)
    shutil.rmtree(tmp, ignore_errors=True)
    if not m:
        return {"repo": os.path.basename(repo), "skipped": "probe did not run"}
    try:
        data = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))
    except ValueError:
        return {"repo": os.path.basename(repo), "skipped": "unreadable probe"}
    data["repo"] = os.path.basename(repo)
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repos", nargs="+")
    ap.add_argument("--wait", type=int, default=2000)
    ap.add_argument("--json")
    args = ap.parse_args()

    rows = [audit(r, args.wait) for r in args.repos]
    if args.json:
        open(args.json, "w").write(json.dumps(rows, indent=2) + "\n")

    bad = 0
    for r in rows:
        if r.get("skipped"):
            print("%-26s %s" % (r["repo"], r["skipped"]))
            continue
        n = len(r["errors"]) + len(r["rejections"]) + len(r["missing"])
        bad += 1 if n else 0
        print("%-26s %s" % (r["repo"], "clean" if not n else
                            "errors=%d rejections=%d missing=%d unlabelled=%d"
                            % (len(r["errors"]), len(r["rejections"]),
                               len(r["missing"]), len(r["unlabelledButtons"]))))
        for k in ("errors", "rejections", "missing", "unlabelledButtons"):
            for item in r[k][:3]:
                print("      %-18s %s" % (k[:-1] + ":", item))
    print("\n%d of %d apps complained about something" % (bad, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
