# Aetheris — what the harness/CLI disagreement is not

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `eab67dc9` (documentation only; tree clean)

Follows `2026-11-17-aetheris-field-width-text-entry-proven.md`, where a test that passes from the CLI
failed inside `AetherisWindowScripts`. Two probes, three suspects eliminated, cause still unknown. Stopped
there rather than opening a third.

## Eliminated

| Suspect | How | Result |
| --- | --- | --- |
| Page delivery (string vs served URL) | read `run_window` | it opens a loopback listener and serves the page — identical to the CLI |
| Argument splitting | read `run_window` | it builds a shell command string and runs it with `popen`, so `--click 600 300` arrives as three arguments |
| Attribute quoting (test used `id='i'`) | measured both | `(60,42)=(255,255,255)` and `(60,8)=(53,54,58)` for single and double quotes alike |

Also confirmed while measuring: window `y` below 34 is chrome, so the harness's `34 + 8` sampling
coordinate is correct — that was a plausible off-by-chrome bug and it is not the one.

## What remains

The failing assertions, verbatim:

    --click 60 42    -> field magenta   (expected: magenta, text-entry clause)
    --click 600 300  -> field magenta   (expected: white)

From the CLI, `--click 600 300` leaves the field white. Same binary, same page bytes, same arguments
according to the helper's own code. So either the helper's command differs in a way reading did not
reveal, or `frame_pixel` is reading a frame that does not belong to that run — it searches
`frame-8.ppm` down to `frame-1.ppm` and takes the first it finds, which is fine for a fresh directory
and is worth checking for a reused one.

That last sentence is the next probe, and it is a single `ls` of the directory at failure time.

## Why I stopped

The two-probe rule. This question has now had two probes; the remaining candidates are cheap but the
session's value is better spent elsewhere, and the previous four investigations today all taught the
same lesson: the fifth probe is where the guessing starts.

## What I deliberately did not do

- **Did not add a debug print to the harness.** It is the obvious next step and it belongs at the start
  of a session, not the end of one.
- **Did not ship the failing test with the negative case commented out.** Half a test is a false
  signal.
- **Did not touch the other three browser repositories.**

## Next

1. `ls` the frame directory at failure time — `frame_pixel` takes the highest-numbered frame it finds.
2. If the directory is clean, print the exact command string `run_window` builds.
3. Then re-add the text-entry test.
4. Per-node dirty flags, then scoped invalidation; family P0 builds still need dev packages.
