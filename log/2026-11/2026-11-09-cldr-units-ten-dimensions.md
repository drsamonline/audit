# CLDR — unit conversion: ten dimensions, and a split that resolves

Date: 2026-11-09
Repo: `drsamonline/CLDR` · branch `feat/units-ten-dimensions` · PR #17 (open, not merged)
Reference links taken: `sharkdp/numbat`, `printfn/fend`

## What I looked at

`src/extras.rs` (unit conversion), `src/engine.rs` (calc parser, `/cmd` output),
`Cargo.toml`, `rust-toolchain.toml`, `docs/USER_GUIDE.md`, `docs/index.html`,
`README.md`, `changes/README.md`, `.github/workflows/build-release.yml`.

The cascade in `engine.rs::smart_route` is math → units → path → PATH binary →
web. Unit conversion sat in one function, `extras.rs::convert_units`, over three
tables: length (9 units), mass (7), temperature (3). The amount side was split
by a byte scan accepting only `[-+]?digits[.digits]`.

## What was wrong

Anything outside those three dimensions fell through the cascade and became a
web search, which is a silent wrong answer rather than a refusal. Measured by
replicating the function's logic line for line:

    '2 h in min'      -> None        '10 GB in MB'     -> None
    '90 min in h'     -> None        '5 km/h in mph'   -> None
    '3 tbsp in ml'    -> None        '1 bar in psi'    -> None
    '10 in in cm'     -> None        '1e3 m in km'     -> None
    '10 km in mi'     -> 6.213712    '100 f to c'      -> 37.777778

Two of those are parse bugs rather than missing data: `10 in in cm` fails
because "in" is both a connector and the inch, and the connector was found by
first occurrence; `1e3 m in km` fails because the literal scanner has no
exponent.

## What I changed

One commit for units, one for `/cmd` truncation, both on one branch (one
project, one branch, per the brief).

1. **Units — ten dimensions.** A single table carries dimension + factor +
   canonical code per alias. Conversion requires both units to share a
   dimension; temperature stays affine. Dimensions: length, mass, time, volume,
   area, speed, data, pressure, energy, temperature. Data is decimal (1 kB =
   1000 B) with binary forms spelled out (`kib`, `mib`, `gib`, `tib`). Factors
   follow Numbat's unit module (MIT/Apache-2.0): physical constants only, no
   code, credited in the source. **No dependency added.**
2. **Parsing by resolution.** Candidate connector splits are collected and
   tried right to left; the first split that resolves on both sides wins, so
   `10 in in cm` reads as ten inches into centimetres. A suffix is accepted as
   a unit only when a number — or an expression the calc engine already handles
   — sits in front of it, which is what makes `1e3 m in km` and `2*3 km in mi`
   work while `5min` stays minutes instead of 5 metres + "in".
3. **`/cmd` truncation.** `truncate_line` appended a bare `…`; it now appends
   `… (+N chars)`. A wrapped line and a 40 KB minified JSON line looked
   identical before.
4. Docs follow behaviour: `docs/USER_GUIDE.md` (dimension table),
   `docs/index.html` (card + cascade note), README feature row and `/cmd` note.
   Two `changes/` files carry `bump: minor` and `bump: patch`; `VERSION` is
   untouched.

## Evidence

No Rust toolchain in this sandbox and `static.rust-lang.org` is not reachable,
so verification came from the repo's own CI, which runs fmt, clippy, build,
tests and `--self-test` on any branch push, on ubuntu and windows.

    $ gh run view 42613276705
    ✓ Check (ubuntu-latest) in 26s
    ✓ Check (windows-latest) in 1m17s

    cargo build --release --locked   Finished `release` profile in 7.24s
    cargo test  --release --locked   test result: ok. 20 passed; 0 failed;
                                     0 ignored; 0 measured
    cargo run --release --locked -- --self-test
                                     self-test: OK (18/18)

New tests: `conversion_time_volume_data`,
`conversion_speed_area_pressure_energy`,
`conversion_parsing_resolves_the_split`,
`long_lines_say_how_much_was_cut`. New self-test checks: h→min, gb→mb,
inch-vs-connector, exponent literal (14 → 18).

## What I deliberately did not do

- **No dependency.** clap, fend, kalker and numbat are references, not crates;
  the binary is ~600 KB and advertises zero-bloat. clap was rejected for that
  reason alone.
- **No output-format change.** `docs/USER_GUIDE.md` shows
  `10 km in mi → 6.213712 mi` with the unit; the code has never appended it.
  Pre-existing mismatch, recorded here rather than folded into this diff.
- **No compound-unit parser.** `km/h`, `m/s`, `mph`, `ft/s` are table entries.
  `5 ft 2 in in cm` (two amount tokens) still does not parse.
- **No tree-wide `cargo fmt`.** The rustfmt step was already red on `main`
  (50 diffs across 7 files, all line width) and is `continue-on-error`. My
  additions follow the file's existing long-line style and add 9 diffs of the
  same kind. Making the tree fmt-clean is its own sweep.
- **No version bump and no merge.** PR #17 waits for a decision.
- **HMS left untouched**, per instruction.

## Next

- Decision on PR #17, then the remaining part-one projects in order (`feather`
  is next after CLDR).
- Part two (`HMS`, `ULTIMATE-WINDOWS-OPTIMIZER`, `kitbox`, `lexora`,
  `ziptastic`, `The_Browser`, `ai-bridge`) is proposal-only until named.
- A conventional-commits gate (cocogitto) was proposed for CLDR's CI and is
  **not** implemented: it would add a third-party binary to the pipeline, which
  the brief says to ask about first.
