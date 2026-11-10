# The_Browser — the Windows "hang" was a failed assert in an abort dialog

Date: 2026-11-10 · Repo `drsamonline/The_Browser` · PR #31 (merged)
Links taken: none

## What I looked at
`Tests/AetherisRendering/TestResourceBackends.cpp`, `src/rendering/file_resource_backend.cpp`,
`resource_loader.cpp`, `resource.cpp`, `content_type.cpp`, `url.cpp`, and two
instrumented Windows runs (42776432872, then 42777132506).

## What was wrong
`AetherisResourceBackends` timed out at 180 s on Windows and only on Windows. It was
not a hang. `Url::path()` for `file:///C:/dir/file` returns `/C:/dir/file`, and
`std::filesystem::path` reads a leading separator as the root of the current drive,
so the path became `\C:\dir\file` and every `file://` load failed. The test then hit
`assert(document.succeeded())`, and a Debug build on Windows sits in the CRT abort
dialog rather than dying — nobody on a runner can dismiss it, so the process never
exited and ctest reported Timeout.

## What I changed
- `[step]` markers before each stage, flushed (kept: they cost 0.00 s and name the
  next stop).
- `FileResourceBackend::load` drops the leading separator when a drive letter
  follows it. Product code: every Windows `file://` load went through this.
- The `-E AetherisResourceBackends` exclusion added in #30 is removed.

## Evidence
    run 42777132506  both jobs success
      28/56 Test #28: AetherisResourceBackends ..... Passed  0.00 sec
      Windows 100% of 56   (was 55 with the test excluded)
      Linux   100% of 56

Marker trail that found it:
    [step] load document
    [step]   path=/C:/Users/RUNNER~1/.../index.html
    [step] backend load
    [step]   state=2

## What I deliberately did not do
- No percent-decoding of file URLs: `file:///C:/my%20dir/x.html` still will not
  open. Separate gap, now visible.
- No change to how an assert looks on Windows. A Debug run that asserts will hang
  the same way in any test; that is a harness question, not this bug.
- No version bump.

## Next
Percent-decoding in file URLs; and consider making asserts on Windows exit instead
of opening a dialog, so the next one fails in seconds.
