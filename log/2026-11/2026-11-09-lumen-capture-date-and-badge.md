# Lumen — a file name cannot name a day the calendar does not have

Date: 2026-11-09
Repo: `drsamonline/lumen` · branch `fix/capture-date-calendar-check` · PR #6
(open, not merged)
Reference links taken: none — see "What I deliberately did not do"
Same session: `2026-11-09-app-image-toolkit-badges.md`,
`2026-11-09-offline-pdf-toolkit-cli-refusals.md`,
`2026-11-09-feather-router-signatures.md`,
`2026-11-09-cldr-conventional-commits.md`

## What I looked at

`lib/core/scan/capture_date.dart` and `test/capture_date_test.dart`,
`lib/core/search/fuzzy.dart`, `ROADMAP.md`, `ARCHITECTURE.md`, `tools/badges.py`,
`.github/workflows/test.yml`, and the last green run on `main`.

## What was wrong

`CaptureDate.fromFileName` validated the month and the day separately — 1..12 and
1..31 — and then handed them to `DateTime`, which **rolls an impossible date
forward instead of rejecting it**:

    IMG_20240231_120000.jpg  ->  2024-03-02
    IMG_20240431_120000.jpg  ->  2024-05-01
    IMG_20230229_120000.jpg  ->  2023-03-01   (2023 is not a leap year)

A filename artefact came back as a capture date. This is the module whose entire
purpose is that a wrong date collapses the library into the wrong month header,
so inventing one is worse than returning null.

Second, smaller: the tests badge said **98 passing** while `flutter test` printed
**159**, and the landing page's alt text repeated the 98. Running
`tools/badges.py` with no arguments does not reproduce the committed badges —
its defaults are vaguer than the claims actually made (`build: green` for
`build: 3 platforms`, `deps: 0 runtime` for `deps: 11 packages`) — so the
documented way to regenerate silently downgrades three correct badges.

## What I changed

- Seven lines in `capture_date.dart`: the parsed name has to survive the round
  trip. If `DateTime` moved the day, month or year, the name was never a date.
- Two tests in the existing "refuses what it cannot trust" group: the three
  impossible dates, and `29 February 2024` as the guard that the check did not
  over-correct.
- `tools/badges.json` holding the claims, so `--config` reproduces every badge
  byte for byte; the tests badge regenerated from the measured count, and the
  landing page's alt text with it.

## Evidence

No Dart compiler in this environment: the Flutter 3.27.4 SDK installs and runs,
but `pub get` cannot reach `pub.dev` through the sandbox proxy — Dart's
HttpClient fails the proxy's TLS handshake (`CERTIFICATE_VERIFY_FAILED`) even
with `SSL_CERT_FILE` pointed at the vault CA, while curl to the same URL returns
200. So CI is the compiler, as it was for CLDR and feather.

What was checked locally:

    $ dart format --output=none --set-exit-if-changed lib/core/scan/capture_date.dart test/capture_date_test.dart
    Formatted 2 files (0 changed) in 0.80 seconds.      # parses, and is canonical

CI, run 42631728638, head `6a328e2`, all four jobs green:

    Analyze and test: success        Build Linux desktop: success
    Build Windows desktop: success   Build Android APK: success

    main:         00:10 +159: All tests passed!
    this branch:  00:11 +161: All tests passed!
    …: refuses what it cannot trust a date the calendar does not have      (+33)
    …: refuses what it cannot trust 29 February in a leap year is a date   (+34)

The badge is set to 161 because CI printed 161, not because 159 + 2 was
calculated.

## What I deliberately did not do

- **The clock is still clamped, not rejected.** `IMG_20240115_250000.jpg` becomes
  23:00:00 rather than null: the date is real and discarding it would lose a
  capture date over a malformed time. A deliberate asymmetry with the day,
  written down rather than left to be rediscovered.
- **No `Levels` feature.** `ROADMAP.md` names input/output levels as the next
  item and it is a good one — a LUT builder beside `ToneCurve`, ~60 lines of pure
  maths — but a model with no caller is dead code, and wiring it through the edit
  recipe and the viewer is a bigger slice with a UI decision behind it. Its own
  branch.
- **No new link work.** Rejected, one line each: `flutter_rust_bridge`,
  `flutter-rust-ffi`, `flutter_rust_bridge_template` — a Rust bridge is an
  architecture change for a pure-Dart app with no native dependency. `libcaesium`,
  `oxipng`, `libjxl`, `imageflow`, `imager-io/imager` — native or server image
  engines, and this app ships no native code. `imgo`,
  `caesium-image-compressor` — desktop GUI wrappers. `coriander_player`,
  `flutter_server_box` — Flutter apps in adjacent domains, nothing to take.
  `awesome-flutter` — an index.
- **No version bump, no merge.**

## Next

Decide on PR #6. Two things now visible and unowned in this fleet: lumen and
app-image-toolkit both had a badge that drifted from the suite, and neither had a
CI step that would have caught it. app-image-toolkit's PR adds one; lumen's could
take the same shape (`python3 tools/badges.py --config tools/badges.json` then
`git diff --exit-code`).
