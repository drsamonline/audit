# The_Browser — five stacked breaks behind a red default branch

Date: 2026-11-10 · Repo `drsamonline/The_Browser` · PR #28 (open, not merged)
Reference links taken: `servo/html5ever` (the conformance idea, deferred)

## What I looked at
`Meta/CMake/compile_options.cmake`, `use_linker.cmake`, `src/main.cpp`,
`src/js/js.cpp`, `.github/workflows/build-aetheris.yml`, the failing run 42630632338
and every run after each fix.

## What was wrong
`main` had not built since 2026-11-09. Four causes stacked, each hidden behind the
previous one:

1. `add_cxx_compile_options` applies to C, CXX and ASM, so C++-only warning flags
   reached the C compiler for third_party/gumbo and `-Werror` made that fatal.
2. `detach_child` (main.cpp:245) and `make_event` (js/js.cpp:369) had no previous
   declaration — `-Werror=missing-declarations`.
3. `aetheris --smoke-test` creates a window; the runner has no display.
4. Windows: an empty `AETHERIS_WINDOWS_LINKER_MODE` was rejected at configure.

## What I changed
CXX-only option helper and the C++-only flags moved to it; both helpers `static`;
smoke step under `xvfb-run`; unset linker mode means AUTO.

## Evidence
    run 42685097898   Build: failure → after (2): Build success, ctest 56/56,
                      Smoke-run: "Failed to create window"
    run 42685548216   Test Aetheris standalone (Linux): success
    Windows: still red — third_party/gumbo includes <strings.h>, absent in MSVC
                      (fatal error C1083), stopped deliberately

## What I deliberately did not do
- Did not port vendored gumbo to MSVC on this branch (sixth fix, own Windows run).
- No html5lib tree-construction harness: the plan for this repo, pointless while the
  build is red. Next branch.
- No version bump, no merge.

## Next
Decide on PR #28; then the gumbo `strings.h` shim; then html5lib conformance.
