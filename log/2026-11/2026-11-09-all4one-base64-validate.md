# All4ONE — base64 decode discarded every character it did not recognise

Date: 2026-11-09 · Repo `drsamonline/All4ONE` · PR #25 (open, not merged)
Links taken: none

## What I looked at
`tools/encoding.py`, `scripts/audit.py`, `tests/sweep.py`, `tests/windows_stub.py`,
`.github/workflows/ci.yml`. Local gates before any change: audit 46 checks,
sweep 313/313 tools, Windows stub 23 tools 0 problems.

## What was wrong
`base64.b64decode(raw, validate=False)` silently drops characters outside the
alphabet: `"!!!!"` decoded to `b""` and was reported as a successful empty file,
`"not base64!!"` decoded to noise, and the `except binascii.Error` →
"Not valid Base64" could never fire for the input it exists for. The URL-safe
alphabet was mangled by the same leniency instead of decoded.

## What I changed
URL-safe (`-`, `_`) mapped to standard first, then `validate=True`.
`tests/test_encoding.py` added and wired into the CI focused-tests step.

## Evidence
    python tests/test_encoding.py     8 passed
    before                            5 passed, 3 failed (URL-safe refused;
                                      "!!!!" and "====" returned results)
    python scripts/audit.py           46 checks passed
    python tests/sweep.py             313 / 313
CI: success.

## What I deliberately did not do
- Other codecs (base32, ascii85, hex) and `base64-file` untouched.
- No new dependency.
- No link work: CyberChef and it-tools are browser toolboxes this repo is the
  offline-desktop equivalent of; py7zr is an archive library; the rest are indexes.
- No version bump, no merge.

## Next
Decide on PR #25.
