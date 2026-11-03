#!/usr/bin/env python3
"""Read an app over the DevTools protocol: what did it complain about, and did it paint?

    python3 tools/cdp_audit.py <repo-dir> [...]

Two questions, one browser each:

  1. did anything throw, and did any request fail?
  2. did the app actually render — how many elements, how much text?

The second matters as much as the first. An app can throw nothing and still show
an empty shell: one bad string in a single inline script kills the whole script
and leaves the rest of the document alive and silent. That is what had happened to
conqueror-os for its whole life.

This reader works where the injected-probe audits cannot: a page with a
Content-Security-Policy that refuses inline script, or one that overwrites the
document title a probe would write into.
"""
import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

import websocket

# The sandbox routes HTTP through a proxy; 127.0.0.1 must not go through it, or the
# devtools endpoint is unreachable and the reader looks broken.
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class Chrome:
    def __init__(self):
        self.port = free_port()
        self.last_err = None
        self.proc = subprocess.Popen(
            ["chromium", "--headless=new", "--no-sandbox", "--disable-gpu",
             "--allow-file-access-from-files", "--disable-dev-shm-usage",
             "--remote-debugging-port=%d" % self.port,
             "--remote-allow-origins=*", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.ws = None
        for _ in range(60):
            try:
                with OPENER.open("http://127.0.0.1:%d/json/version" % self.port, timeout=1) as r:
                    info = json.load(r)
                self.ws = websocket.create_connection(
                    info["webSocketDebuggerUrl"], timeout=20,
                    http_proxy_host=None, http_no_proxy=["127.0.0.1", "localhost"])
                break
            except Exception as e:
                self.last_err = "%s: %s" % (type(e).__name__, e)
                time.sleep(0.25)
        if not self.ws:
            raise RuntimeError("devtools did not come up: %s" % (self.last_err,))
        self.n = 0

    def send(self, method, params=None):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                return msg.get("result", {})

    def open_page(self, url, wait=3.0, collect=None):
        """Navigate a fresh tab and (optionally) collect events for `wait` seconds."""
        target = self.send("Target.createTarget", {"url": "about:blank"})["targetId"]
        sid = self.send("Target.attachToTarget", {"targetId": target, "flatten": True})["sessionId"]

        def cmd(method, params=None):
            self.n += 1
            self.ws.send(json.dumps({"id": self.n, "method": method, "sessionId": sid,
                                     "params": params or {}}))
            while True:
                m = json.loads(self.ws.recv())
                if m.get("id") == self.n:
                    return m.get("result", {})

        for m in ("Runtime.enable", "Log.enable", "Network.enable", "Page.enable"):
            cmd(m)
        cmd("Page.navigate", {"url": url})

        if collect is None:
            for _ in range(40):
                r = cmd("Runtime.evaluate", {"expression": "document.readyState",
                                             "returnByValue": True})
                if r.get("result", {}).get("value") == "complete":
                    break
                time.sleep(0.25)
            time.sleep(1.2)
        else:
            self.ws.settimeout(0.5)
            deadline = time.time() + wait
            while time.time() < deadline:
                try:
                    msg = json.loads(self.ws.recv())
                except Exception:
                    continue
                collect(msg)

        return cmd

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except Exception:
            self.proc.kill()


def audit(repo, wait=3.0):
    play = os.path.join(repo, "docs", "play")
    name = os.path.basename(repo.rstrip("/"))
    if not os.path.isfile(os.path.join(play, "index.html")):
        return {"repo": name, "skipped": "no app"}

    tmp = tempfile.mkdtemp(prefix="cdpaudit-")
    shutil.copytree(os.path.dirname(play), os.path.join(tmp, "docs"))
    index = os.path.join(tmp, "docs", "play", "index.html")
    url = "file://" + index

    errors, failed, painted = [], [], {}
    ch = None
    try:
        # 1. what did the page complain about
        ch = Chrome()

        def collect(msg):
            meth, p = msg.get("method"), msg.get("params", {})
            if meth == "Runtime.exceptionThrown":
                d = p.get("exceptionDetails", {})
                desc = ((d.get("exception", {}) or {}).get("description")
                        or d.get("text") or "exception")
                where = " @ %s:%s" % (d["url"].split("/")[-1], d.get("lineNumber", 0) + 1) \
                        if d.get("url") else ""
                errors.append(desc.splitlines()[0][:110] + where)
            elif meth == "Runtime.consoleAPICalled" and p.get("type") == "error":
                args = " ".join(str(a.get("value", a.get("description", "")))
                                for a in p.get("args", []))
                errors.append("console: " + args[:110])
            elif meth == "Log.entryAdded":
                e = p.get("entry", {})
                if e.get("level") == "error":
                    txt = e.get("text", "")[:100]
                    (failed if e.get("source") == "network" else errors).append(txt)
            elif meth == "Network.loadingFailed":
                failed.append(p.get("errorText", "failed"))
        ch.open_page(url, wait=wait, collect=collect)
        ch.close()
        ch = None

        # 2. did it paint
        ch = Chrome()
        cmd = ch.open_page(url, wait=wait)
        r = cmd("Runtime.evaluate", {
            "expression": "JSON.stringify({nodes: document.querySelectorAll('*').length,"
                          " text: (document.body ? document.body.innerText : '').trim().length,"
                          " title: document.title})",
            "returnByValue": True})
        painted = json.loads(r["result"]["value"])
    except Exception as e:
        painted = {"error": str(e)[:70]}
    finally:
        if ch:
            ch.close()
        shutil.rmtree(tmp, ignore_errors=True)

    return {"repo": name, "errors": errors[:8], "rejections": [], "missing": failed[:8],
            "painted": painted}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repos", nargs="+")
    ap.add_argument("--json")
    args = ap.parse_args()

    rows = []
    for r in args.repos:
        try:
            rows.append(audit(r))
        except Exception as e:
            rows.append({"repo": os.path.basename(r.rstrip("/")), "skipped": str(e)[:60]})
    if args.json:
        open(args.json, "w").write(json.dumps(rows, indent=2))

    blanks = 0
    for r in rows:
        if r.get("skipped"):
            print("%-26s %s" % (r["repo"], r["skipped"]))
            continue
        n = len(r["errors"]) + len(r["missing"])
        pt = r.get("painted") or {}
        blank = pt.get("nodes", 99) < 12 or pt.get("text", 99) < 40
        blanks += 1 if blank else 0
        state = "clean" if not n else "errors=%d failed=%d" % (len(r["errors"]), len(r["missing"]))
        if blank:
            state += "   ** EMPTY SHELL (%s nodes, %s chars)" % (pt.get("nodes"), pt.get("text"))
        print("%-26s %s" % (r["repo"], state))
        for e in r["errors"][:3]:
            print("      error:   %s" % e)
        for f in r["missing"][:3]:
            print("      failed:  %s" % f)
    print("\n%d of %d painted nothing" % (blanks, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
