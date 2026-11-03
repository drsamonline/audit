#!/usr/bin/env python3
"""Click every control and see whether anything happened.

    python3 tools/click_audit.py <repo-dir> [...]

The load audit reads what the browser complains about. This one asks a different
question: does the interface do what it looks like it does? It clicks each button
in turn and compares the document before and after. A control that changes
nothing is either wired to a feature that is not there, or waiting for a state the
page never reaches.

Destructive-sounding controls are listed but not clicked — a diagnostic that wipes
the page and then judges the rest of the controls is not a diagnostic.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SAFE_SKIP = ("clear", "delete", "remove", "reset", "wipe", "restore", "import",
             "logout", "sign out", "uninstall", "erase", "format")

PROBE = """
<script>
(function () {
  var results = {clicked: [], dead: [], skipped: [], errors: []};
  /* The fingerprint has to see more than markup: a drawing app changes pixels and
     not the DOM, and a tool button changes a JS variable and nothing else. So it
     covers the DOM, the class on <body>, what is in localStorage, and a sample of
     every canvas. */
  function fp() {
    var b = document.body;
    if (!b) return "0";
    var parts = [b.innerHTML.length, (b.textContent || "").length,
                 document.querySelectorAll("*").length, b.className || ""];
    try { parts.push(localStorage.length + ":" + JSON.stringify(localStorage).length); }
    catch (e) { parts.push("ls-x"); }
    var cvs = document.querySelectorAll("canvas");
    for (var i = 0; i < cvs.length && i < 3; i++) {
      try {
        var c = cvs[i], w = Math.min(48, c.width), h = Math.min(48, c.height);
        var d = c.getContext("2d").getImageData(0, 0, w, h).data, sum = 0;
        for (var j = 0; j < d.length; j += 97) sum = (sum + d[j]) %% 1000000;
        parts.push(sum);
      } catch (e) { parts.push("cv-x"); }
    }
    return parts.join("|");
  }
  function label(el) {
    var t = (el.textContent || "").trim().replace(/\\s+/g, " ").slice(0, 24);
    if (!t) t = el.getAttribute("aria-label") || el.title || el.id || el.className || "?";
    return t;
  }
  /* A diagnostic must not be stopped by a dialog: headless Chromium waits for a
     confirm() that nobody can answer, and the whole run hangs. */
  window.alert = function () {};
  window.confirm = function () { return false; };
  window.prompt = function () { return null; };
  window.onbeforeunload = null;

  window.addEventListener("load", function () {
    setTimeout(function () {
      var els = [].slice.call(document.querySelectorAll(
        "button, [role=button], a[href^='#'], input[type=button], input[type=submit]"));
      var i = 0;
      if (els.length > 24) els = els.slice(0, 24);
      function step() {
        if (i >= els.length) {
          document.title = "CLICK|" + JSON.stringify(results);
          return;
        }
        var el = els[i++];
        var name = label(el);
        /* a hidden or disabled control cannot be judged by clicking it */
        if (!el.offsetParent && getComputedStyle(el).position !== "fixed") {
          results.skipped.push(name); return setTimeout(step, 10);
        }
        if (el.disabled) { results.skipped.push(name); return setTimeout(step, 10); }
        var low = name.toLowerCase();
        for (var s = 0; s < %d; s++) {
          if (low.indexOf(%s[s]) !== -1) { results.skipped.push(name); return setTimeout(step, 10); }
        }
        var before = fp();
        try {
          /* A canvas app listens for pointerdown, not click. Dispatch the whole
             sequence so the control is exercised the way a hand would exercise it. */
          var r = el.getBoundingClientRect();
          var opts = {bubbles: true, cancelable: true, clientX: r.left + r.width / 2,
                      clientY: r.top + r.height / 2, pointerId: 1, isPrimary: true};
          ["pointerdown", "mousedown", "pointerup", "mouseup", "click"].forEach(function (t) {
            var E = t.indexOf("pointer") === 0 && window.PointerEvent
                      ? new PointerEvent(t, opts) : new MouseEvent(t, opts);
            el.dispatchEvent(E);
          });
        } catch (e) { results.errors.push(name + ": " + e.message); }
        setTimeout(function () {
          var after = fp();
          if (before === after) {
            /* already in that state, or genuinely inert? One more press decides. */
            try { el.click(); } catch (e) {}
            setTimeout(function () {
              var again = fp();
              results.clicked.push(name);
              if (after === again) results.dead.push(name);
              step();
            }, 60);
            return;
          }
          results.clicked.push(name);
          step();
        }, 60);
      }
      step();
    }, 700);
  });
})();
</script>
"""

SKIPS = json.dumps(list(SAFE_SKIP))


def audit(repo, wait=700):
    docs = os.path.join(repo, "docs")
    play = os.path.join(docs, "play")
    if not os.path.isfile(os.path.join(play, "index.html")):
        return {"repo": os.path.basename(repo.rstrip("/")), "skipped": "no app"}

    tmp = tempfile.mkdtemp(prefix="clickaudit-")
    shutil.copytree(docs, os.path.join(tmp, "docs"))
    index = os.path.join(tmp, "docs", "play", "index.html")
    body = open(index, encoding="utf-8", errors="replace").read()
    body = body.replace("</body>", (PROBE % (len(SAFE_SKIP), SKIPS)) + "</body>", 1)
    open(index, "w", encoding="utf-8").write(body)

    try:
        out = subprocess.run(
            ["chromium", "--headless=new", "--no-sandbox", "--disable-gpu",
             "--allow-file-access-from-files", "--virtual-time-budget=9000",
             "--dump-dom", "file://" + index],
            capture_output=True, text=True, timeout=60).stdout
    except subprocess.TimeoutExpired:
        shutil.rmtree(tmp, ignore_errors=True)
        return {"repo": os.path.basename(repo.rstrip("/")), "skipped": "timed out"}

    m = re.search(r"<title>CLICK\|(.*?)</title>", out, re.S)
    shutil.rmtree(tmp, ignore_errors=True)
    if not m:
        return {"repo": os.path.basename(repo.rstrip("/")), "skipped": "probe did not run"}
    try:
        data = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))
    except ValueError:
        return {"repo": os.path.basename(repo.rstrip("/")), "skipped": "unreadable probe"}
    data["repo"] = os.path.basename(repo.rstrip("/"))
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repos", nargs="+")
    ap.add_argument("--json")
    args = ap.parse_args()

    rows = [audit(r) for r in args.repos]
    if args.json:
        open(args.json, "w").write(json.dumps(rows, indent=2))

    for r in rows:
        if isinstance(r.get("skipped"), str):
            print("%-28s %s" % (r["repo"], r["skipped"]))
            continue
        print("%-28s clicked=%-3d dead=%-3d skipped=%-3d errors=%d"
              % (r["repo"], len(r["clicked"]), len(r["dead"]),
                 len(r.get("skipped") or []), len(r["errors"])))
        for d in r["dead"][:6]:
            print("      dead:    %s" % d)
        for e in r["errors"][:3]:
            print("      error:   %s" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
