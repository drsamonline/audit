# Per-repo build list

One block per repository. Each says what the repo already has, what it is missing, and the
smallest set of changes that closes the gap. Nothing here is a rebuild: a surface marked
*already right* is left exactly as it is.

**Verdict.** `apply` — the skill applies in full, including the docs/play/ split. `apply-lite` —
landing page, README and support block apply, but there is no web app to embed as a demo.
`decide` — infrastructure or a report; whether it wants a public face is the owner's call.
`skip` — already right, leave it alone.

## aethelgard-games

*apply · split-done · web-app · effort M · 16 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## aethelgard-rpg-engine

*apply · split-needed · web-app · effort L · 18 checks failing*

**Already right:** landing, platforms.

**To build:**

1. The app entry is index.html — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
17. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
18. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
19. Failing check — the meta description fits a search result: trim it to under ~160 characters
20. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
21. Failing check — all six support handles are present: re-paste the block; never retype a handle
22. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
23. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
24. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## ai-bridge

*apply-lite · landing-only · web-app-single-file · effort M · 18 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
17. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## All4ONE

*apply-lite · landing-only · web-app-single-file · effort M · 18 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
17. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
18. Failing check — the meta description fits a search result: trim it to under ~160 characters
19. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
20. Failing check — all six support handles are present: re-paste the block; never retype a handle
21. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
22. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
23. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## ambient-sound-studio

*apply · split-done · web-app · effort M · 15 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-builder

*apply-lite · landing-only · web-app-single-file · effort M · 18 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
17. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
18. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
19. Failing check — the meta description fits a search result: trim it to under ~160 characters
20. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
21. Failing check — all six support handles are present: re-paste the block; never retype a handle
22. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
23. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
24. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-clip-loom

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
19. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-companion-forge

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
19. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
20. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-encrypted-case-log

*apply · split-done · web-app · effort S · 9 checks failing*

**Already right:** landing, app, shots, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
4. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
7. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
8. Failing check — all six support handles are present: re-paste the block; never retype a handle
9. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
10. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
11. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-image-toolkit

*apply · split-done · web-app · effort S · 8 checks failing*

**Already right:** landing, app, badges, shots, offline, platforms.

**To build:**

1. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
3. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
6. Failing check — all six support handles are present: re-paste the block; never retype a handle
7. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
8. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
9. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
10. Failing check — the app registers its service worker: call navigator.serviceWorker.register('sw.js') on load

## app-jacquard

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
18. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-lantern

*apply · split-needed · web-app-single-file · effort M · 18 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. The app entry is docs/demo/index.html — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-organon-reader

*apply · app-at-docs · web-app-single-file · effort M · 17 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. docs/index.html is the app itself — move it to docs/play/index.html, then build a landing page at docs/index.html in a different palette and type.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-panchang

*apply · split-done · web-app · effort S · 8 checks failing*

**Already right:** landing, app, badges, shots, offline, platforms.

**To build:**

1. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
3. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
6. Failing check — the meta description fits a search result: trim it to under ~160 characters
7. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
8. Failing check — all six support handles are present: re-paste the block; never retype a handle
9. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
10. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
11. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## app-poets-studio

*apply · split-done · web-app · effort S · 9 checks failing*

**Already right:** landing, app, shots, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
4. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
7. Failing check — all six support handles are present: re-paste the block; never retype a handle
8. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
9. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
10. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
11. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-thermals

*apply · split-done · web-app · effort S · 8 checks failing*

**Already right:** landing, app, badges, shots, offline, platforms.

**To build:**

1. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
3. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
6. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
7. Failing check — all six support handles are present: re-paste the block; never retype a handle
8. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
9. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
10. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
11. Failing check — the manifest is installable: add the missing fields — name, 192 and 512 icons, display: standalone
12. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## app-weft-puzzles

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
18. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## art-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## astro-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## audio-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## audit

*decide · report-page · web-app · effort M · 17 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. docs/index.html is a generated report, not an app — there is no demo to embed. The delta is the support block, the badges and the README.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## backup

*decide · no-web-surface · library-or-data · effort L · 20 checks failing*

**Already right:** offline, platforms.

**To build:**

1. Nothing web-facing exists yet. Decide first whether this repo wants a public face; if it does, the landing page comes before everything else.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — no unfilled {{placeholders}} left: replace them: a published page still promising {{one-line promise}} is a draft with a URL
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## base-bench

*apply · split-done · web-app · effort S · 8 checks failing*

**Already right:** landing, app, badges, shots, offline, platforms.

**To build:**

1. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
3. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
6. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
7. Failing check — all six support handles are present: re-paste the block; never retype a handle
8. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
9. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
10. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
11. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark

## blinkcode-ai

*apply · split-done · web-app · effort M · 18 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — the meta description fits a search result: trim it to under ~160 characters
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
22. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
23. Failing check — the app registers its service worker: call navigator.serviceWorker.register('sw.js') on load
24. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## BLINKTRANSFER

*apply · split-done · web-app · effort M · 16 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
16. Failing check — all six support handles are present: re-paste the block; never retype a handle
17. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
18. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
19. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
20. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
21. Failing check — the app registers its service worker: call navigator.serviceWorker.register('sw.js') on load
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## bmi-bmr-tdee-macros-fluid-calculator

*apply · split-done · web-app · effort S · 9 checks failing*

**Already right:** landing, app, shots, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
4. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
7. Failing check — the meta description fits a search result: trim it to under ~160 characters
8. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
9. Failing check — all six support handles are present: re-paste the block; never retype a handle
10. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
11. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
12. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## boericke-repertory

*apply · split-done · web-app · effort S · 9 checks failing*

**Already right:** landing, app, shots, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
4. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
7. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
8. Failing check — all six support handles are present: re-paste the block; never retype a handle
9. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
10. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
11. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## book-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## canteen-lan

*apply · split-done · web-app · effort S · 9 checks failing*

**Already right:** landing, app, shots, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
4. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
7. Failing check — all six support handles are present: re-paste the block; never retype a handle
8. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
9. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
10. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## case-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## chalk-lan

*apply · split-done · web-app · effort S · 8 checks failing*

**Already right:** landing, app, badges, shots, offline, platforms.

**To build:**

1. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
2. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
3. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
4. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
5. Failing check — the meta description fits a search result: trim it to under ~160 characters
6. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
7. Failing check — all six support handles are present: re-paste the block; never retype a handle
8. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
9. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
10. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## CLDR

*apply-lite · landing-only · web-app-single-file · effort L · 19 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
16. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
17. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
18. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
19. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
20. Failing check — the meta description fits a search result: trim it to under ~160 characters
21. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
22. Failing check — all six support handles are present: re-paste the block; never retype a handle
23. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
24. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
25. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
26. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## compfactory

*decide · no-web-surface · native-app · effort L · 18 checks failing*

**Already right:** offline, platforms.

**To build:**

1. Nothing web-facing exists yet. Decide first whether this repo wants a public face; if it does, the landing page comes before everything else.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## compress-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## conqueror-os

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
15. Failing check — the meta description fits a search result: trim it to under ~160 characters
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## control-panel

*apply · app-at-docs · web-app-single-file · effort M · 18 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. docs/index.html is the app itself — move it to docs/play/index.html, then build a landing page at docs/index.html in a different palette and type.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## corefit-md

*apply · split-done · web-app · effort S · 10 checks failing*

**Already right:** landing, app, shots, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
4. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
7. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
8. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
9. Failing check — all six support handles are present: re-paste the block; never retype a handle
10. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
11. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
12. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
13. Failing check — the app registers its service worker: call navigator.serviceWorker.register('sw.js') on load
14. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
15. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark

## crypto-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## dance-fight

*apply · split-done · web-app · effort L · 15 checks failing*

**Already right:** landing, app.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Delete the Apple build target — the .dmg and its Download-for-Mac button, the macos-latest runner, the App Store link. This estate ships Windows, Linux and Android.
8. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## dashboard

*apply · split-done · web-app · effort M · 17 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
16. Failing check — all six support handles are present: re-paste the block; never retype a handle
17. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
18. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
19. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
20. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
21. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
22. Failing check — the manifest is installable: add the missing fields — name, 192 and 512 icons, display: standalone
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## drsamonline

*decide · special · library-or-data · effort L · 18 checks failing*

> The GitHub profile repo. Its README is the product; a docs/ landing page is optional.

**Already right:** offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
7. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
16. Failing check — all six support handles are present: re-paste the block; never retype a handle
17. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
18. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
19. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
20. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
21. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## drsamonline.github.io

*apply-lite · special · library-or-data · effort L · 19 checks failing*

> The estate hub. Its own index.html is the front page for everything else.

**Already right:** offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
7. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## eon-commando

*apply · split-done · web-app · effort M · 18 checks failing*

**Already right:** landing, app, offline.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Delete the Apple build target — the .dmg and its Download-for-Mac button, the macos-latest runner, the App Store link. This estate ships Windows, Linux and Android.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the meta description fits a search result: trim it to under ~160 characters
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the UPI intent asks for an open amount: delete any am= parameter — no presets, no suggested tiers
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## export-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## frame-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## game-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## gentle-pediatrics-companion

*apply · split-done · web-app · effort M · 16 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
24. Failing check — the manifest is installable: add the missing fields — name, 192 and 512 icons, display: standalone
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## HCS

*decide · no-web-surface · native-app · effort L · 18 checks failing*

**Already right:** offline, platforms.

**To build:**

1. Nothing web-facing exists yet. Decide first whether this repo wants a public face; if it does, the landing page comes before everything else.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## heavenzip

*decide · no-web-surface · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. Nothing web-facing exists yet. Decide first whether this repo wants a public face; if it does, the landing page comes before everything else.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## helioprism

*apply · split-done · web-app · effort M · 16 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
16. Failing check — all six support handles are present: re-paste the block; never retype a handle
17. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
18. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
19. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
20. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
21. Failing check — the app registers its service worker: call navigator.serviceWorker.register('sw.js') on load
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## HMS

*apply-lite · landing-only · web-app-single-file · effort L · 19 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
16. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
17. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
18. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
19. Failing check — the meta description fits a search result: trim it to under ~160 characters
20. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
21. Failing check — all six support handles are present: re-paste the block; never retype a handle
22. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
23. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
24. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## homoeopathic-materia-medica-repertory-json

*apply-lite · landing-only · web-app-single-file · effort L · 19 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
16. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
17. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
18. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
19. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
20. Failing check — the meta description fits a search result: trim it to under ~160 characters
21. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
22. Failing check — all six support handles are present: re-paste the block; never retype a handle
23. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
24. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
25. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
26. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## idle-city-ages-of-growth

*apply · split-done · web-app · effort M · 15 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
15. Failing check — the meta description fits a search result: trim it to under ~160 characters
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## kent-repertory-explorer

*apply · split-done · web-app · effort S · 10 checks failing*

**Already right:** landing, app, shots, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
4. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
7. Failing check — the meta description fits a search result: trim it to under ~160 characters
8. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
9. Failing check — all six support handles are present: re-paste the block; never retype a handle
10. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
11. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
12. Failing check — the UPI intent asks for an open amount: delete any am= parameter — no presets, no suggested tiers
13. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## lan-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## lexora

*apply-lite · landing-only · web-app-single-file · effort L · 18 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
16. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
17. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
18. Failing check — the meta description fits a search result: trim it to under ~160 characters
19. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
20. Failing check — all six support handles are present: re-paste the block; never retype a handle
21. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
22. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
23. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## lockhtml

*apply · split-done · web-app · effort L · 18 checks failing*

**Already right:** landing, app.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Delete the Apple build target — the .dmg and its Download-for-Mac button, the macos-latest runner, the App Store link. This estate ships Windows, Linux and Android.
8. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
18. Failing check — the meta description fits a search result: trim it to under ~160 characters
19. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
20. Failing check — all six support handles are present: re-paste the block; never retype a handle
21. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
22. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
23. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
24. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
25. Failing check — the manifest is installable: add the missing fields — name, 192 and 512 icons, display: standalone
26. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
27. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## lumen

*skip · split-done · web-app · effort XS · 0 checks failing*

> Already the reference shape: landing + play/ + block + badges + shots. Nothing to do.

**Already right:** landing, app, badges, shots, readme, support, portrait, theme, offline, platforms.

**To build:** nothing. Leave it alone.

## MATERIA-MEDICA-BUILDER

*apply · split-done · web-app · effort M · 16 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
24. Failing check — the app registers its service worker: call navigator.serviceWorker.register('sw.js') on load

## Matneo

*apply-lite · special · web-app-single-file · effort L · 19 checks failing*

> The shop. docs/index.html is the storefront, not an app shell.

**Already right:** landing, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## ml-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## mnemosyne-companion

*apply · split-done · web-app · effort M · 15 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
16. Failing check — the meta description fits a search result: trim it to under ~160 characters
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## musicgen

*apply · split-done · web-app · effort M · 15 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## NEO

*apply-lite · landing-only · web-app-single-file · effort L · 19 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
16. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
17. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
18. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
19. Failing check — the meta description fits a search result: trim it to under ~160 characters
20. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
21. Failing check — all six support handles are present: re-paste the block; never retype a handle
22. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
23. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
24. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## neon-engine

*apply-lite · landing-only · web-app · effort L · 18 checks failing*

> The engine has no demo of its own; the games it runs are in neon-games/play/.

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## neon-games

*apply · split-partial · web-app · effort L · 18 checks failing*

**Already right:** landing, platforms.

**To build:**

1. docs/play/ holds docs/play/dead-zone/ but no index.html — add docs/play/index.html as the entry (a chooser, or one game), so the demo frame has one route to open.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
17. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
18. Failing check — the meta description fits a search result: trim it to under ~160 characters
19. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
20. Failing check — all six support handles are present: re-paste the block; never retype a handle
21. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
22. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
23. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## neon-runner

*apply · split-done · web-app · effort L · 17 checks failing*

**Already right:** landing, app.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Delete the Apple build target — the .dmg and its Download-for-Mac button, the macos-latest runner, the App Store link. This estate ships Windows, Linux and Android.
8. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
18. Failing check — the meta description fits a search result: trim it to under ~160 characters
19. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
20. Failing check — all six support handles are present: re-paste the block; never retype a handle
21. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
22. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
23. Failing check — the UPI intent asks for an open amount: delete any am= parameter — no presets, no suggested tiers
24. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## neon-velocity

*apply · no-docs · native-app · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is site/index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## offline-pdf-toolkit

*apply · split-done · web-app · effort S · 9 checks failing*

**Already right:** landing, app, shots, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
3. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
4. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
5. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
6. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
7. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
8. Failing check — all six support handles are present: re-paste the block; never retype a handle
9. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
10. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
11. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## open-materia-medica

*apply · split-done · web-app · effort M · 16 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — the meta description fits a search result: trim it to under ~160 characters
14. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
19. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
20. Failing check — the app registers its service worker: call navigator.serviceWorker.register('sw.js') on load
21. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## optical-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## profile-kit

*apply-lite · special · web-app-single-file · effort M · 18 checks failing*

> docs/index.html is the rendered profile — that is the product, not a landing page for one.

**Already right:** landing, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
7. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
12. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — no unfilled {{placeholders}} left: replace them: a published page still promising {{one-line promise}} is a draft with a URL
15. Failing check — the meta description fits a search result: trim it to under ~160 characters
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## read-live-transform-app

*apply · split-done · web-app · effort M · 16 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## remedy-relationship-explorer

*apply · split-done · web-app · effort L · 19 checks failing*

**Already right:** landing, app.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Delete the Apple build target — the .dmg and its Download-for-Mac button, the macos-latest runner, the App Store link. This estate ships Windows, Linux and Android.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
23. Failing check — the manifest is installable: add the missing fields — name, 192 and 512 icons, display: standalone
24. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## repertory-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## repertory-reader

*apply · split-done · web-app · effort XS · 3 checks failing*

**Already right:** landing, app, badges, shots, readme, support, portrait, theme, offline, platforms.

**To build:**

1. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
2. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
3. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
4. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
5. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
6. Failing check — the meta description fits a search result: trim it to under ~160 characters
7. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
8. Failing check — the manifest is installable: add the missing fields — name, 192 and 512 icons, display: standalone
9. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark

## retro-strike

*apply · split-done · web-app · effort L · 17 checks failing*

**Already right:** landing, app.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Delete the Apple build target — the .dmg and its Download-for-Mac button, the macos-latest runner, the App Store link. This estate ships Windows, Linux and Android.
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — the meta description fits a search result: trim it to under ~160 characters
18. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
19. Failing check — all six support handles are present: re-paste the block; never retype a handle
20. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
21. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
22. Failing check — the UPI intent asks for an open amount: delete any am= parameter — no presets, no suggested tiers
23. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## saga-vn-engine

*apply · split-needed · web-app · effort L · 17 checks failing*

**Already right:** landing, platforms.

**To build:**

1. The app entry is index.html — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
15. Failing check — the meta description fits a search result: trim it to under ~160 characters
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## Scrap-and-Gun

*apply · split-done · web-app · effort M · 17 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
22. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## seance

*apply · split-needed · web-app-single-file · effort M · 16 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. The app entry is docs/app.html — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
16. Failing check — all six support handles are present: re-paste the block; never retype a handle
17. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
18. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
19. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
20. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
21. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## search-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## skills

*apply-lite · special · web-app · effort M · 17 checks failing*

> The skills catalogue. docs/index.html is the product, 1.1 MB and self-contained.

**Already right:** landing, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
7. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
11. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — no unfilled {{placeholders}} left: replace them: a published page still promising {{one-line promise}} is a draft with a URL
14. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## skin-case-tracker

*apply · split-done · web-app · effort M · 17 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
16. Failing check — the meta description fits a search result: trim it to under ~160 characters
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
23. Failing check — the manifest is installable: add the missing fields — name, 192 and 512 icons, display: standalone
24. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## smartbill-app

*apply · split-done · web-app · effort M · 15 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — every <img> carries alt text: write the alt text: what the picture shows, not 'image'
15. Failing check — the meta description fits a search result: trim it to under ~160 characters
16. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
17. Failing check — all six support handles are present: re-paste the block; never retype a handle
18. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
19. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
20. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
21. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## SmartNotes

*apply-lite · landing-only · web-app-single-file · effort L · 19 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
17. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
18. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
19. Failing check — the meta description fits a search result: trim it to under ~160 characters
20. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
21. Failing check — all six support handles are present: re-paste the block; never retype a handle
22. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
23. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
24. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## srs-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## the-symphony-companion

*apply · split-done · web-app · effort M · 18 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
16. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — sw.js declares a CACHE name: name the cache and bump it on every release
23. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
24. Failing check — the manifest is installable: add the missing fields — name, 192 and 512 icons, display: standalone
25. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
26. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## The_Browser

*apply-lite · landing-only · web-app-single-file · effort L · 19 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
16. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
17. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
18. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
19. Failing check — the meta description fits a search result: trim it to under ~160 characters
20. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
21. Failing check — all six support handles are present: re-paste the block; never retype a handle
22. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
23. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
24. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
25. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## today-card

*apply · split-needed · web-app-single-file · effort M · 16 checks failing*

**Already right:** landing, offline, platforms.

**To build:**

1. The app entry is docs/app.html — move it to docs/play/index.html and point the hero CTA and the demo frame at play/.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
19. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
20. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## TTB

*apply-lite · landing-only · web-app-single-file · effort L · 19 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
16. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
17. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
18. Failing check — the meta description fits a search result: trim it to under ~160 characters
19. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
20. Failing check — all six support handles are present: re-paste the block; never retype a handle
21. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
22. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
23. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## ui-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## ULTIMATE-WINDOWS-OPTIMIZER

*apply-lite · landing-only · web-app-single-file · effort L · 19 checks failing*

**Already right:** landing, platforms.

**To build:**

1. There is no web app in this repo, so the demo band shows the screenshots rather than an iframe. Do not put a play button on a demo that cannot load.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
8. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
9. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
10. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
11. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
12. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
13. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
14. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
15. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
16. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
17. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
18. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
19. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
20. Failing check — the meta description fits a search result: trim it to under ~160 characters
21. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
22. Failing check — all six support handles are present: re-paste the block; never retype a handle
23. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
24. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
25. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
26. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## unstoppable-mind-companion

*apply · split-done · web-app · effort M · 15 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
8. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
9. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
10. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
11. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
12. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
13. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
14. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
15. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
16. Failing check — the meta description fits a search result: trim it to under ~160 characters
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## web-kit

*apply · no-docs · library-or-data · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. The demo page is index.html at the repo root, which GitHub Pages does not serve — move it to docs/play/ and build the landing page at docs/index.html.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## weft8-classroom

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
19. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## weft8-compare

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
18. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## weft8-hardware

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
12. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
13. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
14. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
15. Failing check — all six support handles are present: re-paste the block; never retype a handle
16. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
17. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
18. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
19. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## weft8-kit

*apply · split-done · web-app · effort M · 14 checks failing*

**Already right:** landing, app, offline, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
7. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
8. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
9. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
10. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
11. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
12. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
13. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
14. Failing check — all six support handles are present: re-paste the block; never retype a handle
15. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
16. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
17. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup

## whispering-body-first-aid

*apply · split-done · web-app · effort M · 16 checks failing*

**Already right:** landing, app, platforms.

**To build:**

1. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
2. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
3. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
4. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
5. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
6. Replace every shields.io <img> on the page with the local docs/assets/badge-*.svg. A page that needs the network to describe itself has broken its own rule.
7. Failing check — no iOS wording on the pages: check the wording: a device mock is fine, an iOS download is not
8. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
9. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
10. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
11. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
12. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
13. Failing check — light palette has ink and paper: define --ink and --paper so the contrast can be computed
14. Failing check — the dark palette can be read: give the page a [data-theme="dark"] block with the same variables
15. Failing check — the page title fits a search result: aim for under ~60 characters: the app name, then the promise
16. Failing check — the meta description fits a search result: trim it to under ~160 characters
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — sw.js serves HTML network-first (looks for 'navigate'): serve the HTML network-first; keep assets cache-first
23. Failing check — manifest start_url points at the app, not the landing page: set start_url to the app's new path
24. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

## ziptastic

*decide · no-web-surface · native-app · effort L · 19 checks failing*

**Already right:** offline, platforms.

**To build:**

1. Nothing web-facing exists yet. Decide first whether this repo wants a public face; if it does, the landing page comes before everything else.
2. Generate the six local badge SVGs into docs/assets/badge-*.svg with scripts/badges.py. The claims come from this repo's own suite and its LICENSE, not from an image service.
3. Shoot docs/assets/app-desktop.png (1280×1600) and app-mobile.png (430×860) with scripts/shot.sh, on a populated route. Look at both before committing.
4. README: local badges first, the one-line promise, the four links, the <!-- shot:start --> block, then a ## Support table with the six handles.
5. Paste region 1 of assets/support-block.html into the landing footer and region 2 into the app header, and add a Support CTA in the hero beside the other two.
6. Run scripts/support_portrait.py for docs/assets/support-portrait.jpg, and scripts/support_qr.py for docs/assets/upi-qr.svg.
7. Failing check — landing page points at the app at play/: point the hero CTA and the demo frame at play/
8. Failing check — landing page is not a copy of the app: the landing page is its own design; keep the app in docs/play/ untouched
9. Failing check — landing page embeds the app in a frame: step 3: <iframe src="play/"> behind a poster, revealed on load
10. Failing check — the frame has a poster behind it: keep the screenshot behind the frame so a blocked demo still shows the product
11. Failing check — landing page respects the system theme: light is the base palette; let prefers-color-scheme decide the first paint
12. Failing check — landing page remembers its theme under its own key: store under a page-scoped key so the landing page and the app do not fight
13. Failing check — landing page has a theme toggle: add the header toggle, wired to the same variables
14. Failing check — the landing page's palette can be read: name the palette variables --ink, --paper, --muted, --accent
15. Failing check — README keeps the pipeline's shot markers: step 7: restore the shot:start/shot:end block — the pipeline writes into it
16. Failing check — README images are local files, not an image service: commit the image and reference it by relative path
17. Failing check — app carries the support button: paste region 2 into the app header, region 1 inside its dialog
18. Failing check — all six support handles are present: re-paste the block; never retype a handle
19. Failing check — docs/assets/upi-qr.svg exists and is an SVG: step 4: run scripts/support_qr.py (pip install segno)
20. Failing check — the UPI intent link is on the page: the VPA needs a upi://pay link as well as the printed text
21. Failing check — the portrait is in the support block: re-paste the block's region 1 — it carries the portrait markup
22. Failing check — the landing page declares a theme-color: add <meta name="theme-color"> for light and dark
23. Failing check — footer carries a build stamp: print build date and commit in the footer so the release is answerable

