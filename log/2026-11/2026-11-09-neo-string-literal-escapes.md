# NEO — a newline in a string literal broke all three text backends

Date: 2026-11-09
Repo: `drsamonline/NEO` · branch `fix/escape-string-literals` · PR #18 (open, not merged)
Reference links taken: none
Same session: `2026-11-09-lumen-capture-date-and-badge.md`,
`2026-11-09-app-image-toolkit-badges.md`,
`2026-11-09-offline-pdf-toolkit-cli-refusals.md`,
`2026-11-09-feather-router-signatures.md`,
`2026-11-09-cldr-conventional-commits.md`

## What I looked at

`compiler/src/lexer/mod.rs` (numeric and string lexing), the three text backends
(`backends/c`, `backends/javascript`, `backends/rust`), `backends/wasm`,
`crates/nova-common`, `Cargo.toml` and `.github/workflows/ci.yml`.

## What was wrong

The lexer unescapes a string, so NOVA's `"two\nlines"` reaches the backends as
text containing a real newline. Each backend emitted it straight between quotes,
escaping only the backslash and the double quote:

    puts("two
    lines");

That is invalid C (a literal cannot span lines), invalid JavaScript (a raw line
terminator in a string literal) and invalid Rust. Tab, carriage return and NUL
broke the output the same way. One escape table, three wrong outputs.

## What I changed

`nova_common::escape_string_literal` — in the crate all three backends already
depend on — covering backslash, double quote, newline, carriage return, tab and
NUL, and the three call sites now use it. Other control characters are left raw
on purpose: a raw one is legal in all three targets, a raw newline is not.

Tests: `escape_tests` in `nova-common` (the six escapes; ordinary text and
Devanagari untouched) and `a_string_with_a_newline_is_written_as_an_escape` in
the C backend (the literal carries `\n`, `\t`, `\"`, and the output holds no raw
newline).

## Evidence

No Rust toolchain in this environment, so CI is the compiler. Run 42636309782,
job `Build Rust workspace`: success.

    test escape_tests::the_six_that_break_a_literal ... ok
    test escape_tests::ordinary_text_is_untouched ... ok
    test a_string_with_a_newline_is_written_as_an_escape ... ok
    test result: ok. 0 failed   (every crate)

The job also runs `tools/grammar-check.py` and `tools/example-check.py`, both
unaffected.

## What I deliberately did not do

- **The C backend's `printf` format-string path (line ~193) is untouched.** It
  assembles an already-escaped format string and would be double-escaped by this
  helper; it builds format text rather than a literal, which is a separate
  question about how `println` should treat a `%` in user text.
- **The WASM backend writes `(i32.const 0)` for every string** — a placeholder,
  not a bug in this slice. Making WASM carry strings is a feature.
- **No link work.** `borgo`, `gleam`, `gluon`, `rune`, `steel`, `artichoke`,
  `erg` — other language implementations; the transferable ideas here are
  language design, not code, and NEO has a working backend set already.
- **No version bump, no merge.**

## Next

Decide on PR #18. Worth a look separately: `read_number` accepts `e` without
requiring digits after it (`1e` reports "Invalid float"), and `0b102` silently
lexes as `0b10` followed by `2`.
