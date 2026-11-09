# app-encrypted-case-log — crypto-kit threw instead of rejecting, and guessed randomness

Date: 2026-11-09 · Repo `drsamonline/app-encrypted-case-log` · PR #4 (open, not merged)
Links taken: none

## What I looked at
`crypto-kit.js` (133 lines, read whole), `case-kit.js`, `tests/self-tests.js`,
`.github/workflows/test.yml`.

## What was wrong
1. `CK.open` threw synchronously on a malformed envelope while every other
   function returns a promise — the `.catch(showWrongPassphrase)` an app writes
   never ran, and its error path became an uncaught exception.
2. `CK.randomBytes` fell back to `Math.random()` with no CSPRNG. A salt or IV
   from `Math.random()` is a guess, not a secret.

## What I changed
`CK.open` returns a rejected promise, with the version and a new length check
inside the chain; `CK.randomBytes` throws instead of guessing.
`tests/crypto-kit.test.js` asserts both plus the round-trip and wrong-passphrase
path; `test.yml` runs it beside the app suite.

## Evidence
    node tests/crypto-kit.test.js      7 PASS, "crypto-kit: OK", exit 0
    pre-fix crypto-kit.js              FAIL "returns a promise", FAIL "rejects
                                       rather than throwing", exit 1 at .catch()
    node tests/self-tests.js           21/21 passed (unchanged)
CI run on the branch: success.

First cut of the test passed against the old code — awaiting inside try/catch
catches a synchronous throw just as happily. It now asserts the call returns a
Promise before awaiting; that version fails on the old code.

## What I deliberately did not do
- No algorithm or envelope-format change: AES-256-GCM, PBKDF2-SHA256 at 250k,
  12-byte IVs, `ver|iter|salt|iv|ct` all untouched, so existing vaults open.
- No link work: openmed/medplum/fasten/openmrs/OCD-style server suites against a
  local encrypted single-file vault.
- No version bump, no merge.

## Next
Decide on PR #4.
