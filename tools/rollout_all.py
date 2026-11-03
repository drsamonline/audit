#!/usr/bin/env python3
"""One pass of the presentation rollout for a repo: block, badges, shots, frame, dark.

    python3 rollout_all.py <repo-dir> [...]

Idempotent in every step: a marker in the file decides whether it has been done.
The one judgement it makes is the demo — a keyboard app is linked full screen
rather than framed, because keys go to whichever document has focus.
"""
import os
import re
import shutil
import subprocess
import sys

SKILL = "/scratch/skills/repo-presentation"
GATE = "/tmp/gate/tools"

FRAME = '''
<section id="try-it" style="padding:34px 0 10px">
  <div style="max-width:1180px;margin:0 auto;padding:0 20px">
    <h2 style="font-family:inherit;font-size:clamp(20px,2.4vw,28px);margin:0 0 6px">Try it, right here</h2>
    <p style="margin:0 0 14px;opacity:.8;font-size:15px">This is the app itself in the frame, not a picture of it.</p>
    <div style="position:relative;border:1px solid rgba(0,0,0,.14);border-radius:16px;overflow:hidden;
                background:#0b0e12;aspect-ratio:16/10">
      <img src="assets/app-desktop.png" alt="The app, on its main screen"
           style="display:block;width:100%;height:100%;object-fit:cover;object-position:top center">
      <iframe src="play/" title="The app, running here" loading="lazy"
              style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>
    </div>
    <p style="margin:10px 0 0;font-size:13.5px;opacity:.75">
      <a href="play/" target="_blank" rel="noopener">Open it full screen</a>
    </p>
  </div>
</section>
'''

LINK = '''
<section id="try-it" style="padding:34px 0 10px">
  <div style="max-width:1180px;margin:0 auto;padding:0 20px">
    <h2 style="font-family:inherit;font-size:clamp(20px,2.4vw,28px);margin:0 0 6px">Play it</h2>
    <p style="margin:0 0 14px;opacity:.8;font-size:15px">A keyboard app, so it opens full screen —
      the keys only reach it once it has the window to itself.</p>
    <a href="play/" target="_blank" rel="noopener"
       style="display:block;position:relative;border:1px solid rgba(0,0,0,.14);border-radius:16px;
              overflow:hidden;text-decoration:none">
      <img src="assets/app-desktop.png" alt="The app, on its main screen" style="display:block;width:100%;height:auto">
      <span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
                   background:rgba(8,10,14,.86);color:#fff;border-radius:999px;
                   padding:14px 26px;font:600 16px/1 system-ui,sans-serif;white-space:nowrap">
        ▶ Open full screen
      </span>
    </a>
  </div>
</section>
'''


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except OSError:
        return ""


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)


def shot(repo, name, w, h, out):
    subprocess.run(["chromium", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--virtual-time-budget=3500", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + out, "file://" + os.path.abspath(os.path.join(repo, "docs/play/index.html"))],
                   capture_output=True)
    return os.path.exists(out)


def run(repo):
    log = []
    landing_p = os.path.join(repo, "docs/index.html")
    app_p = os.path.join(repo, "docs/play/index.html")
    if not os.path.exists(landing_p):
        return ["no docs/index.html"]

    # 1. the block, the portrait, the QR, the README table
    r = subprocess.run([sys.executable, os.path.join(GATE, "rollout.py"), "."],
                       cwd=repo, capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.strip().startswith("·"):
            log.append("block: " + line.strip("· "))

    # 2. badges, with claims the repo can stand behind
    pkg = read(os.path.join(repo, "package.json"))
    deps = len(re.findall(r'"[^"]+"\s*:', pkg.split('"dependencies"')[1].split("}")[0])) if '"dependencies"' in pkg else 0
    subprocess.run([sys.executable, os.path.join(SKILL, "scripts/badges.py"),
                    "--tests", "in CI", "--deps", "%d runtime" % deps,
                    "--licence", "PolyForm NC 1.0.0", "--out", "docs/assets"],
                   cwd=repo, capture_output=True)
    log.append("badges: six local SVGs")

    # 3. two real screenshots — only where there is an app to photograph
    has_app = os.path.exists(app_p)
    if has_app:
        assets = os.path.join(repo, "docs/assets")
        os.makedirs(assets, exist_ok=True)
        shot(repo, "desktop", 1280, 900, os.path.join(assets, "app-desktop.png"))
        shot(repo, "mobile", 430, 860, os.path.join(assets, "app-mobile.png"))
        log.append("shots: desktop + mobile")

    # 4. the demo: a keyboard app is linked, everything else is framed
    landing = read(landing_p)
    if has_app and 'id="try-it"' not in landing:
        keyboard = re.search(r"addEventListener\(\s*['\"]key(?:down|up)['\"]", read(app_p)) is not None
        block = LINK if keyboard else FRAME
        landing = landing.replace("<footer", block + "\n<footer", 1) if "<footer" in landing \
            else landing.replace("</body>", block + "\n</body>", 1)
        write(landing_p, landing)
        log.append("demo: " + ("linked full screen (keyboard app)" if keyboard else "framed"))

    # 5. say what the page is
    landing = read(landing_p)
    if 'name="color-scheme"' not in landing and "color-scheme" not in landing.split("</head>")[0]:
        m = re.search(r"<meta[^>]*charset[^>]*>", landing, re.I)
        tag = '\n<meta name="color-scheme" content="dark">'
        if m:
            landing = landing[:m.end()] + tag + landing[m.end():]
        else:
            landing = landing.replace("<head>", "<head>" + tag, 1)
        write(landing_p, landing)
        log.append("theme: declared color-scheme: dark")
    return log


if __name__ == "__main__":
    for repo in sys.argv[1:]:
        if not os.path.isdir(repo):
            print("%-26s missing" % repo)
            continue
        steps = run(repo)
        print("%-26s %s" % (os.path.basename(repo), " · ".join(steps) if steps else "nothing to do"))
