# Aetheris — a field with a width, and the text-entry clause finally proven

Date: 2026-11-17 · Repo `drsamonline/The_Browser`
Commit: `dd9a0cc0`

## The one-declaration fix

`min-width: 8em` on an inline-block with no intrinsic width does nothing here, so a text field filled its
line. Every click anywhere hit it, which is why the previous entry's control case could not discriminate.

`width: 12em` gives it an extent.

## Evidence, and why the control now works

    click the field : (20,8)=(255,0,255)  (60,8)=(255,0,255)  (200,8)=(153,153,153)  (20,40)=(255,255,255)
    click away      : (20,8)=(255,255,255) (60,8)=(255,255,255) (200,8)=(153,153,153)  (20,40)=(255,255,255)

- `(200,8)=(153,153,153)` is the field's right border, so the field really ends before x=200.
- A click on the field sets `FocusTrigger::Pointer`, so the **only** clause that can make
  `:focus-visible` match is the text-entry one — and it does.
- A click away leaves the field white, so the match is caused by the focus and not by the rule existing.

That closes a gap open since `4388fef3`: the text-entry clause is proven from the CLI.

## What was reverted, and why

A test for exactly this pair was written, run, and **failed**:

    FAILED: a pointer focus elsewhere does not match :focus-visible

Both with `--click 600 42` and `--click 600 300`, the field stayed magenta inside `AetherisWindowScripts`,
while the same page and clicks leave it white from the CLI. The harness and the CLI disagree, I do not
know why, and an assertion I cannot explain is worse than none — so the test was reverted rather than
tuned until it passed.

Prime suspect: how `run_window` in the test feeds the page (a string the harness writes out, versus a
served URL from the CLI), or how the harness's frame directory is reused between cases. Both are one
print away, and neither is worth guessing at.

## What I deliberately did not do

- **Did not ship a green-but-unexplained test.** Tuning coordinates until the assertion passes is how a
  suite stops meaning anything.
- **Did not chase the harness difference now.** It is recorded with the failing command lines.
- **Did not implement value editing.** A field has a box and takes focus; typing into it is a project.
- **Did not touch the other three browser repositories.**

## Next

1. Explain the harness/CLI disagreement — the failing command lines are in the entry above.
2. Then re-add the text-entry test, and the earlier `:focus-within`/Tab cases, on whatever the answer is.
3. Per-node dirty flags, then scoped invalidation.
4. Family P0 builds still need a machine with dev packages.
