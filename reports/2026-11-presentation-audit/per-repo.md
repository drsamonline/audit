# Per-repo build list

One block per repo: its tier, what it already carries, what its tier does not require, and the smallest set of changes that closes the gap. Nothing here is a rebuild.

| tier | required |
|---|---|
| `app` | landing, live demo at `docs/play/`, screenshots, badges, support |
| `app-no-demo` | the same minus the live demo — desktop, extension, server, compiler |
| `hub` | landing, badges, a screenshot per linked app, support — no `docs/play/` of its own |
| `engine` | landing, badges, support — **no demo**: the game built on it is the demo |
| `kit` | landing, badges, support — no demo, no app shot, no release build |
| `data` | landing, badges, support |
| `tool` | Forge tooling — no public face required |
| `infra` | decide first |

## aethelgard-games

*hub · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A hub launches apps that live in their own repos: the page needs a card and a screenshot for each one, linking out. No docs/play/index.html of its own.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — all six support handles are present: re-paste the block; never retype a handle
14. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
15. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
16. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## aethelgard-rpg-engine

*engine · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. An engine gets a landing page and never a demo — the game or app built on it is the demo, and it lives in its own repo. Link to it; do not embed it.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — all six support handles are present: re-paste the block; never retype a handle
14. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
15. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
16. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## ai-bridge

*app-no-demo · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## All4ONE

*app-no-demo · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## ambient-sound-studio

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-builder

*kit · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
7. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
12. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-clip-loom

*app · apply*

**Already right:** landing, app, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** The page is plain: 3 sections, 10 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-companion-forge

*tool · apply*

**Already right:** offline, platforms.

**Not required at this tier:** landing, app, badges, shots, support, portrait, theme.

**To build:**

1. Forge tooling run by the owner: no public face required. Leave the page alone unless it is being opened anyway.
2. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
3. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
4. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
7. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
8. Failing check — all six support handles are present: re-paste the block; never retype a handle
9. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
10. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
11. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-encrypted-case-log

*app · apply*

**Already right:** landing, app, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
4. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — all six support handles are present: re-paste the block; never retype a handle
7. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
8. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
9. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-image-toolkit

*app · apply*

**Already right:** landing, app, badges, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
3. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — all six support handles are present: re-paste the block; never retype a handle
6. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
7. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
8. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-jacquard

*app · apply*

**Already right:** landing, app, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It still carries the skeleton's *What it refuses to do* heading, so the section order is the template's, not this project's. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-lantern

*app · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. The app entry is docs/demo/index.html — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-organon-reader

*app · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. The app entry is docs/index.html (the app itself) — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. **Redesign it.** The page is plain: 1 sections, 24 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
5. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
6. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
7. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-panchang

*app · apply*

**Already right:** landing, app, badges, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
3. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — all six support handles are present: re-paste the block; never retype a handle
6. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
7. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
8. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-poets-studio

*app · apply*

**Already right:** landing, app, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
4. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — all six support handles are present: re-paste the block; never retype a handle
7. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
8. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
9. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-thermals

*app · apply*

**Already right:** landing, app, badges, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
3. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — all six support handles are present: re-paste the block; never retype a handle
6. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
7. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
8. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-weft-puzzles

*app · apply*

**Already right:** landing, app, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** The page is plain: 1 sections, 8 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## art-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## astro-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## audio-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## audit

*tool · apply*

**Already right:** offline, platforms.

**Not required at this tier:** landing, app, badges, shots, support, portrait, theme.

**To build:**

1. Forge tooling run by the owner: no public face required. Leave the page alone unless it is being opened anyway.
2. **Redesign it.** The page is plain: 0 sections, 13 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
5. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
8. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
9. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## backup

*infra · decide*

**Already right:** offline, platforms.

**Not required at this tier:** app, badges, shots, portrait, theme.

**To build:**

1. Infrastructure: decide first whether it wants a public face at all.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — no unfilled {{placeholders}} left: replace them: a published page still promising {{one-line promise}} is a draft with a URL
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## base-bench

*app · apply*

**Already right:** landing, app, badges, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
3. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — all six support handles are present: re-paste the block; never retype a handle
6. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
7. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
8. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## blinkcode-ai

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It shares one design with BLINKTRANSFER / blinkcode-ai / helioprism — the same product family, so keep one of the three as the family look and give the other two their own idea, palette and display face. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
16. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
17. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
18. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## BLINKTRANSFER

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It shares one design with BLINKTRANSFER / blinkcode-ai / helioprism — the same product family, so keep one of the three as the family look and give the other two their own idea, palette and display face. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
16. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first

## bmi-bmr-tdee-macros-fluid-calculator

*app · apply*

**Already right:** landing, app, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
4. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — all six support handles are present: re-paste the block; never retype a handle
7. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
8. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
9. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## boericke-repertory

*app · apply*

**Already right:** landing, app, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
4. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — all six support handles are present: re-paste the block; never retype a handle
7. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
8. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
9. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## book-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## canteen-lan

*app · apply*

**Already right:** landing, app, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It still carries the skeleton's *What it refuses to do* heading, so the section order is the template's, not this project's. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
7. Failing check — all six support handles are present: re-paste the block; never retype a handle
8. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
9. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
10. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## case-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## chalk-lan

*app · apply*

**Already right:** landing, app, badges, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It still carries the skeleton's *What it refuses to do* heading, so the section order is the template's, not this project's. One idea from the subject, used in the band, the hero and one accent.
2. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
4. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — all six support handles are present: re-paste the block; never retype a handle
7. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
8. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
9. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## CLDR

*app-no-demo · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## compfactory

*infra · decide*

**Already right:** offline, platforms.

**Not required at this tier:** app, badges, shots, portrait, theme.

**To build:**

1. Infrastructure: decide first whether it wants a public face at all.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## compress-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## conqueror-os

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — all six support handles are present: re-paste the block; never retype a handle
11. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
12. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
13. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## control-panel

*tool · apply*

**Already right:** offline, platforms.

**Not required at this tier:** landing, app, badges, shots, support, portrait, theme.

**To build:**

1. Forge tooling run by the owner: no public face required. Leave the page alone unless it is being opened anyway.
2. **Redesign it.** The page is plain: 0 sections, 12 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
5. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## corefit-md

*app · apply*

**Already right:** landing, app, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It still carries the skeleton's *What it refuses to do* heading, so the section order is the template's, not this project's. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
7. Failing check — all six support handles are present: re-paste the block; never retype a handle
8. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
9. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
10. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
11. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## crypto-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## dance-fight

*app · apply*

**Already right:** landing, app.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — all six support handles are present: re-paste the block; never retype a handle
11. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
12. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
13. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## dashboard

*tool · apply*

**Already right:** offline, platforms.

**Not required at this tier:** landing, app, badges, shots, support, portrait, theme.

**To build:**

1. Forge tooling run by the owner: no public face required. Leave the page alone unless it is being opened anyway.
2. **Redesign it.** It shares one design with Scrap-and-Gun / dashboard / musicgen — a game, a dashboard and a music app are not one family, so all three need their own idea, palette and display face; the page is plain: 3 sections, 0 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
5. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
6. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
7. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
8. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
9. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
10. Failing check — all six support handles are present: re-paste the block; never retype a handle
11. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
12. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
13. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
14. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
15. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first

## drsamonline

*data · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A dataset or report has no demo; the landing page is the front door to the data.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## drsamonline.github.io

*data · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A dataset or report has no demo; the landing page is the front door to the data.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## eon-commando

*app · apply*

**Already right:** landing, app, offline.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the UPI intent asks for an open amount: delete any am= parameter — no presets, no suggested tiers
16. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
17. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first

## export-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## frame-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## game-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## gentle-pediatrics-companion

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
15. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first

## HCS

*infra · decide*

**Already right:** offline, platforms.

**Not required at this tier:** app, badges, shots, portrait, theme.

**To build:**

1. Infrastructure: decide first whether it wants a public face at all.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## heavenzip

*infra · decide*

**Already right:** offline, platforms.

**Not required at this tier:** app, badges, shots, portrait, theme.

**To build:**

1. Infrastructure: decide first whether it wants a public face at all.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — all six support handles are present: re-paste the block; never retype a handle
14. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
15. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
16. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## helioprism

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It shares one design with BLINKTRANSFER / blinkcode-ai / helioprism — the same product family, so keep one of the three as the family look and give the other two their own idea, palette and display face. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
16. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first

## HMS

*app-no-demo · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## homoeopathic-materia-medica-repertory-json

*data · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A dataset or report has no demo; the landing page is the front door to the data.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
7. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
12. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## idle-city-ages-of-growth

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## kent-repertory-explorer

*app · apply*

**Already right:** landing, app, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It still carries the skeleton's *What it refuses to do* heading, so the section order is the template's, not this project's. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
7. Failing check — all six support handles are present: re-paste the block; never retype a handle
8. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
9. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
10. Failing check — the UPI intent asks for an open amount: delete any am= parameter — no presets, no suggested tiers
11. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## lan-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## lexora

*app-no-demo · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## lockhtml

*app · apply*

**Already right:** landing, app.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
15. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
16. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## lumen

*app · skip*

**Already right:** landing, app, badges, shots, readme, support, portrait, offline, platforms.

**Not required at this tier:** theme.

**To build:** nothing. Leave it alone — it is the reference.

## MATERIA-MEDICA-BUILDER

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
15. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first

## Matneo

*data · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A dataset or report has no demo; the landing page is the front door to the data.
2. **Redesign it.** The page is plain: 8 sections, 0 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## ml-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## mnemosyne-companion

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## musicgen

*app · apply*

**Already right:** landing, app, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It shares one design with Scrap-and-Gun / dashboard / musicgen — a game, a dashboard and a music app are not one family, so all three need their own idea, palette and display face; the page is plain: 3 sections, 0 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — all six support handles are present: re-paste the block; never retype a handle
14. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
15. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
16. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## NEO

*app-no-demo · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## neon-engine

*engine · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. An engine gets a landing page and never a demo — the game or app built on it is the demo, and it lives in its own repo. Link to it; do not embed it.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — all six support handles are present: re-paste the block; never retype a handle
14. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
15. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
16. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## neon-games

*hub · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A hub launches apps that live in their own repos: the page needs a card and a screenshot for each one, linking out. No docs/play/index.html of its own.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
12. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## neon-runner

*app · apply*

**Already right:** landing, app.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the UPI intent asks for an open amount: delete any am= parameter — no presets, no suggested tiers
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## neon-velocity

*app-no-demo · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
5. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
6. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
7. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — all six support handles are present: re-paste the block; never retype a handle
17. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
18. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
19. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## offline-pdf-toolkit

*app · apply*

**Already right:** landing, app, shots, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
4. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — all six support handles are present: re-paste the block; never retype a handle
7. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
8. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
9. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## open-materia-medica

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — all six support handles are present: re-paste the block; never retype a handle
11. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
12. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
13. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
14. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
15. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## optical-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## profile-kit

*kit · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
7. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — no unfilled {{placeholders}} left: replace them: a published page still promising {{one-line promise}} is a draft with a URL
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## read-live-transform-app

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
15. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## remedy-relationship-explorer

*app · apply*

**Already right:** landing, app.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
16. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
17. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## repertory-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## repertory-reader

*app · apply*

**Already right:** landing, app, badges, shots, readme, support, portrait, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
2. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
3. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it

## retro-strike

*app · apply*

**Already right:** landing, app.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the UPI intent asks for an open amount: delete any am= parameter — no presets, no suggested tiers
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## saga-vn-engine

*engine · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. An engine gets a landing page and never a demo — the game or app built on it is the demo, and it lives in its own repo. Link to it; do not embed it.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## Scrap-and-Gun

*app · apply*

**Already right:** landing, app, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. **Redesign it.** It shares one design with Scrap-and-Gun / dashboard / musicgen — a game, a dashboard and a music app are not one family, so all three need their own idea, palette and display face; the page is plain: 3 sections, 0 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — all six support handles are present: re-paste the block; never retype a handle
14. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
15. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
16. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
17. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
18. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first

## seance

*app · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. The app entry is docs/app.html — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. **Redesign it.** The page is plain: 0 sections, 16 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
5. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
6. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
7. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## search-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## skills

*data · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A dataset or report has no demo; the landing page is the front door to the data.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — no unfilled {{placeholders}} left: replace them: a published page still promising {{one-line promise}} is a draft with a URL
13. Failing check — all six support handles are present: re-paste the block; never retype a handle
14. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
15. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
16. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## skin-case-tracker

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
15. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
16. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## smartbill-app

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
7. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
8. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
9. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
10. Failing check — every <img> carries alt text: write the alt text: what the picture shows, not 'image'
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## SmartNotes

*app-no-demo · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## srs-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## the-symphony-companion

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
15. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
16. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
17. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## The_Browser

*app-no-demo · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## today-card

*app · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** theme.

**To build:**

1. The app entry is docs/app.html — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. **Redesign it.** The page is plain: 0 sections, 15 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
5. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
6. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
7. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## TTB

*app-no-demo · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## ui-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## ULTIMATE-WINDOWS-OPTIMIZER

*app-no-demo · apply*

**Already right:** landing, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
3. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## unstoppable-mind-companion

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
11. Failing check — all six support handles are present: re-paste the block; never retype a handle
12. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
13. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
14. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## web-kit

*kit · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## weft8-classroom

*kit · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. **Redesign it.** The page is plain: 3 sections, 7 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## weft8-compare

*kit · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. **Redesign it.** The page is plain: 3 sections, 11 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## weft8-hardware

*kit · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. A kit has no product UI — the landing page explains the API and shows a code sample, not an app screenshot. No docs/play/, no app shot.
2. **Redesign it.** The page is plain: 3 sections, 10 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## weft8-kit

*engine · apply*

**Already right:** landing, offline, platforms.

**Not required at this tier:** app, shots, theme.

**To build:**

1. An engine gets a landing page and never a demo — the game or app built on it is the demo, and it lives in its own repo. Link to it; do not embed it.
2. **Redesign it.** The page is plain: 3 sections, 11 colours, no display face of its own. One idea from the subject, used in the band, the hero and one accent.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
6. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
11. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
12. Failing check — all six support handles are present: re-paste the block; never retype a handle
13. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
14. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
15. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## whispering-body-first-aid

*app · apply*

**Already right:** landing, app, platforms.

**Not required at this tier:** theme.

**To build:**

1. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
2. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
3. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
5. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
8. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
9. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
10. Failing check — all six support handles are present: re-paste the block; never retype a handle
11. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
12. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
13. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
14. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
15. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path

## ziptastic

*app-no-demo · apply*

**Already right:** offline, platforms.

**Not required at this tier:** app, theme.

**To build:**

1. A desktop or extension product with no web UI: the demo band shows the screenshots, not an iframe.
2. Build the landing page at docs/index.html from assets/landing-skeleton.html — one idea from the subject, its own palette and display face.
3. Six local badge SVGs into docs/assets/badge-*.svg, claims from this repo's own suite and LICENSE. Keep the shields.io badges that are there — the local set is the offline fallback, not a replacement.
4. Shoot docs/assets/app-desktop.png (1280x1600) and app-mobile.png (430x860) with scripts/shot.sh on a populated route.
5. README: badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table.
6. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header.
7. Run scripts/support_portrait.py for the portrait and scripts/support_qr.py for the UPI QR.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — docs/assets/app-mobile.png looks like a real screenshot: step 5: scripts/shot.sh <repo> app app "#/<populated route>"
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — all six support handles are present: re-paste the block; never retype a handle
17. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
18. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
19. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

