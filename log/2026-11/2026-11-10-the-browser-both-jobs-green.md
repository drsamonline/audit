# The_Browser — Windows builds for the first time; both standalone jobs green

Date: 2026-11-10 · Repo `drsamonline/The_Browser` · PR #30 (open, not merged)
Links taken: none

## What I looked at
`src/network/tls.cpp`, `include/aetheris/ui/window_manager.hpp`,
`include/aetheris/network/socket_abstraction.hpp`, `src/main.cpp`, five test files,
`src/CMakeLists.txt`, `.github/workflows/build-aetheris.yml`, and each Windows run
in turn (42765075024 → 42771005290).

## What was wrong
Nine breaks between "no Windows build at all" and "both jobs green": socket closed
with POSIX `::close` (name resolving to the member), Windows macros redefined, two
C4456 shadows, three C4505 unreferenced helpers, `unsetenv`, POSIX socket headers in
a test, `m.lib` linked unconditionally, and one test that hangs only on Windows.

## What I changed
`closesocket()` on Windows; `#ifndef` around the macros; `html_element` /
`media_sheet`; `[[maybe_unused]]`; `_putenv_s`; TLS test compiles to a skip; maths
library only when NOT WIN32; `--timeout 180` on ctest in both jobs;
`-E AetherisResourceBackends` on Windows only, with the reason in the workflow.

## Evidence
    run 42771005290  conclusion success
      Linux:   success  56/56 ctest, smoke under xvfb
      Windows: success  55/55 ctest, "Aetheris smoke test passed."

Before this branch the Windows job died in the first minute of the build.

## What I deliberately did not do
- No Winsock port of the TLS test — a skip that says so beats a half-port.
- No fix for the AetherisResourceBackends hang, only a visible exclusion: it blocks
  on Windows somewhere between a file:// URL built from a Windows path and
  NavigationController, and guessing from a log is worse than the bug.
- No change to what any test asserts.
- No version bump, no merge.

## Next
Decide on #28, #29, #30 (they are stacked; #28's Linux fix is inside #29 and #30's
history). Then the hang, on a Windows machine.
