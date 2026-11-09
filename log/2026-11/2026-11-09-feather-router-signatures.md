# Feather — the router stops trusting two bytes, and a cut that lands mid-character

Date: 2026-11-09
Repo: `drsamonline/feather` · branch `fix/router-signatures` · PR #1 (open, not merged)
Reference links taken: `yazi` (signature corroboration) — see "What I deliberately
did not do" for why the rest of the list was rejected.
Same session: `2026-11-09-cldr-conventional-commits.md`,
`2026-11-09-cldr-units-ten-dimensions.md`.

## What I looked at

`crates/feather-core/src/format.rs`, `natural.rs`, `crates/feather-cli/src/main.rs`,
the workspace `Cargo.toml`, `ROADMAP.md`, `.github/workflows/ci.yml`. The router
decides once, from bytes, with the extension as a tie-breaker for zip containers.

## What was wrong

Two routes that send a file to a pipeline that cannot open it.

1. **`BM` is a two-byte signature.** `BMW service history.txt` routed to the
   image pipeline and failed to open.
2. **The text sniff cut at 512 bytes and required that slice to be valid UTF-8.**
   When byte 512 landed inside a multi-byte character — routine in a document
   with any non-Latin text — valid text was judged binary. With no extension it
   fell through to `Unknown` and would not open at all.

## What I changed

`is_bmp()` corroborates the BMP signature with the rest of the header: both
reserved words zero, and a DIB header size from the set every BMP writer emits
(12, 40, 52, 56, 64, 108, 124). The 512-byte cut steps back to the last valid
character boundary before asking whether the bytes are text. Nothing else in the
classification logic moved.

Three tests: `a_text_file_beginning_with_bm_is_not_a_bitmap`,
`a_real_bmp_header_is_still_an_image`,
`a_character_split_at_the_cut_does_not_make_text_binary`. The first and third
fail on `main`; the second is the guard that real bitmaps still route correctly.

## Evidence

CI on PR #1, run 42615062269, head `cc875f5`:

    packaging                      success
    build and test (ubuntu-latest) success  5m12s
    dependency budget              success
    build and test (windows-latest) success
    build and test (macos-14)      cancelled (0s)

From the ubuntu job:

    running 54 tests
    test format::tests::a_character_split_at_the_cut_does_not_make_text_binary ... ok
    test format::tests::a_real_bmp_header_is_still_an_image ... ok
    test format::tests::a_text_file_beginning_with_bm_is_not_a_bitmap ... ok
    test result: ok. 54 passed; 0 failed; 0 ignored
    running 14 tests ... ok
    running 3 tests  ... ok

**macos-14 was cancelled, and it is not this change.** The same job was
cancelled on `main` before the branch existed — runs 42605649360, 42575911539,
42354669258; the last macOS success is 41852415922. Recorded here rather than
silently blamed on the patch, and not fixed in this PR because it is a runner
provisioning question, not a code one.

## What I deliberately did not do

- **No shaping work (v0.2) and no PDF text extraction (v0.3).** `ROADMAP.md`
  puts both behind "a compiler in the loop", and it is right to: that is
  rasterisation, font fallback and glyph caching, not a slice to write blind.
  There is no Rust toolchain in this environment and `static.rust-lang.org` is
  not reachable, so CI is the only compiler available — I will not spend its
  cycles on a half-migrated text stack.
- **Rejected links, one line each.** `clap` — `feather-cli` has two subcommands,
  hand-rolled, and this repo gates its dependency budget. `pdf.js`,
  `pdfjs-dist`, `PyMuPDF` — other languages, against `hayro` which already
  renders. `pdfcpu` — Go tool; its structural validation is a feature, not a
  slice. `sumatrapdf` — C++ Windows app; the startup-ordering idea belongs to
  the window work in v0.4. `ripgrep-all` — shells out to external binaries; a
  single-binary viewer cannot. `mcat`, `crossterm`, `ratatui` — terminal
  rendering; this window is `winit` + `softbuffer`. `yazi` — kept only for the
  one rule applied above (corroborate a signature shorter than the structure it
  introduces). `sts10/rust-command-line-utilities`, `awesome-rust-cli-tools`,
  `awesome-pdf` — reading lists.
- **No version bump, no merge.**

## Next

Decide on PR #1. The v0.2 shaping work needs a machine with a compiler; until
then the useful work here is exactly this kind — router, layout and ordering
logic with tests that CI can run.
