# The_Browser — MSVC build, five breaks in, two left

Date: 2026-11-10 · Repo `drsamonline/The_Browser` · PR #29 (open, not merged)
Links taken: none

## What I looked at
`third_party/gumbo/*.c`, `Meta/CMake/compile_options.cmake`, `src/rendering/geometry.cpp`,
`include/aetheris/ui/window_manager.hpp`, `src/network/tls.cpp`, and each Windows run
in turn (42763392495 → 42764551812).

## What was wrong
Five independent MSVC breaks, each behind the last:
1. gumbo includes <strings.h> (POSIX) — C1083.
2. C4530 inside <__msvc_ostream.hpp>: the STL uses try/catch, project builds /EHs-.
3. C4458: local `radius` shadows RoundedRect::radius.
4. C4566: sources are UTF-8, MSVC read the code page.
5. **window_manager.hpp: `m_window_placement` declared inside toggle_fullscreen()'s
   own body under a stray `private:`** — C2065 x2 and C2059. Nothing on Linux
   compiles that #if block, which is why the tree looked healthy.

## What I changed
gumbo compat/strings.h (MSVC-only include path); /wd4530 and /utf-8 for MSVC;
`rad` for the shadowed local; the member moved into the Windows member block.

## Evidence
    run 42764551812   Test Aetheris standalone (Linux): success
                      (build + 56/56 ctest + smoke under xvfb, every run)
    Windows           advances one class per run; still red

Remaining, named for the next branch:
    src/network/tls.cpp:51        ::close(m_fd) is POSIX — needs closesocket() on Windows
    window_manager.hpp:20         C2220 on C4005 (WIN32_LEAN_AND_MEAN / NOMINMAX
                                  defined by CMake and by the header)

## What I deliberately did not do
- No patch to vendored gumbo sources; the shim is beside them and MSVC-only.
- No further MSVC port on this branch: a first MSVC build of a 28k-file engine is
  its own work, and this branch already carries five fixes.
- No version bump, no merge.

## Next
Decide on #28 (Linux green) and #29 (MSVC progress); then one branch for the two
remaining classes above.
