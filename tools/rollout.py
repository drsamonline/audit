#!/usr/bin/env python3
"""Paste the support block into a repo, and the Support table into its README.

    python3 tools/rollout.py <repo> --dry-run     # say what it would do, touch nothing
    python3 tools/rollout.py <repo>               # do it
    python3 tools/rollout.py <repo> --only block  # just one piece

Every step is idempotent: a marker in the file decides whether it has already been
done, so running it twice is a no-op and running it after a partial failure
finishes the job rather than duplicating it.

The handles live in the skill's assets/support-block.html and nowhere else. This
copies them; it never retypes them.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

SKILL = "/scratch/skills/repo-presentation"
BLOCK = os.path.join(SKILL, "assets", "support-block.html")
QR = os.path.join(SKILL, "assets", "upi-qr.svg")
PORTRAIT = os.path.join(SKILL, "scripts", "support_portrait.py")
README_TABLE = os.path.join(SKILL, "assets", "readme-template.md")

HANDLES = ["drsohilboi@ybl", "ko-fi.com/matneo", "paypal.me/drsohilmomin",
           "B08ZT331LY", "drsamonline.github.io", "sohilmomin2000@gmail.com"]


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except OSError:
        return ""


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s)


def region(name):
    """One of the two paste regions, without its comment scaffolding."""
    body = read(BLOCK)
    start = body.index("<!-- support:%s:start -->" % name)
    end = body.index("<!-- support:%s:end -->" % name)
    return body[start:end + len("<!-- support:%s:end -->" % name)]


def readme_support_section():
    """The `## Support` section out of the template, verbatim."""
    body = read(README_TABLE)
    i = body.index("## Support")
    j = body.index("\n## ", i + 1)
    return body[i:j].rstrip() + "\n"


# --- the pieces --------------------------------------------------------------
def do_assets(root, log):
    assets = os.path.join(root, "docs", "assets")
    os.makedirs(assets, exist_ok=True)

    qr = os.path.join(assets, "upi-qr.svg")
    if not os.path.exists(qr):
        shutil.copyfile(QR, qr)
        log.append("docs/assets/upi-qr.svg")

    jpg = os.path.join(assets, "support-portrait.jpg")
    if not os.path.exists(jpg):
        r = subprocess.run([sys.executable, PORTRAIT, "--out", "docs/assets"],
                           cwd=root, capture_output=True, text=True)
        if os.path.exists(jpg):
            log.append("docs/assets/support-portrait.jpg")
        else:
            log.append("portrait FAILED: " + (r.stderr or r.stdout).strip()[:120])


def do_landing(root, log):
    """Region 1 into the landing page, before the closing </footer>."""
    path = os.path.join(root, "docs", "index.html")
    page = read(path)
    if not page:
        log.append("no docs/index.html — skipped")
        return
    if "support:block:start" in page:
        log.append("landing page already carries the block")
        return
    block = region("block")
    if "</footer>" in page:
        page = page.replace("</footer>", block + "\n</footer>", 1)
    else:
        page = page.replace("</body>", block + "\n</body>", 1)
    write(path, page)
    log.append("docs/index.html: region 1 into the footer")


def do_app(root, log):
    """Region 2 into the app header, with region 1 inside its dialog."""
    path = os.path.join(root, "docs", "play", "index.html")
    page = read(path)
    if not page:
        log.append("no docs/play/index.html — skipped")
        return
    if "support:app:start" in page:
        log.append("app already carries the button")
        return
    block = region("app").replace(
        "<!-- paste region 1 here, with src=\"../assets/upi-qr.svg\" -->",
        region("block").replace('src="assets/upi-qr.svg"', 'src="../assets/upi-qr.svg"')
                        .replace('src="assets/support-portrait.jpg"', 'src="../assets/support-portrait.jpg"'))
    # the button belongs beside the title, so it is found where the app is read
    anchor = re.search(r'<span class="sp"></span>', page)
    if anchor:
        page = page[:anchor.start()] + block + "\n  " + page[anchor.start():]
    else:
        page = page.replace("</header>", block + "\n</header>", 1)
    write(path, page)
    log.append("docs/play/index.html: region 2 into the header")


def do_readme(root, log):
    path = os.path.join(root, "README.md")
    body = read(path)
    if not body:
        log.append("no README.md — skipped")
        return
    if re.search(r"^##\s+Support\s*$", body, re.M):
        log.append("README already has a Support section")
        return
    section = readme_support_section()
    # before a trailing licence section if there is one, else at the end
    m = re.search(r"^##\s+(Licence|License)\s*$", body, re.M)
    if m:
        body = body[:m.start()] + section + "\n" + body[m.start():]
    else:
        body = body.rstrip() + "\n\n" + section
    write(path, body)
    log.append("README.md: ## Support table")


def do_sw(root, log):
    """A returning reader is the one who will not see the new footer without this."""
    path = os.path.join(root, "docs", "play", "sw.js")
    sw = read(path)
    if not sw:
        return
    m = re.search(r"(const\s+CACHE\s*=\s*[\"'])([^\"']+)([\"'])", sw)
    if not m:
        return
    old = m.group(2)
    new = old[:-1] + "b" if old[-1].isdigit() and old[-1] != "b" else old + "-2"
    if new == old:
        new = old + "b"
    write(path, sw[:m.start(2)] + new + sw[m.end(2):])
    log.append("sw.js: CACHE %s -> %s" % (old, new))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", choices=["assets", "block", "app", "readme", "sw"])
    args = ap.parse_args()

    root = os.path.abspath(args.repo)
    if not os.path.isdir(root):
        sys.exit("not a directory: " + root)

    log = []
    steps = {
        "assets": do_assets,
        "block": do_landing,
        "app": do_app,
        "readme": do_readme,
        "sw": do_sw,
    }
    order = [args.only] if args.only else ["assets", "block", "app", "readme", "sw"]

    if args.dry_run:
        for name in order:
            print("would run:", name)
        return 0

    for name in order:
        steps[name](root, log)

    print("ROLLOUT", os.path.basename(root))
    for line in log:
        print("  ·", line)

    missing = [h for h in HANDLES
               if h not in read(os.path.join(root, "docs", "index.html"))
               and h not in read(os.path.join(root, "docs", "play", "index.html"))]
    print("  handles:", "all six present" if not missing else "MISSING " + ", ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
