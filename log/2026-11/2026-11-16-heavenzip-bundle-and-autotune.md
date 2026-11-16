# heavenzip — the release bundle carries every tool, and autotune finds the combinations

Date: 2026-11-16 · Repos `drsamonline/heavenzip`, `drsamonline/HCS`, `drsamonline/ziptastic`
PRs merged: heavenzip #29–#39, HCS #13, ziptastic #19

## What I looked at

`heavenzip`: `AGENT_PROMPT.md`, `CMakeLists.txt`, `src/main.cpp`, `src/orchestrator/dispatcher.cpp`,
`src/orchestrator/pipeline.cpp`, `config/profiles/*.ini`, `.github/workflows/{ci,build-tools}.yml`,
`NOTICE`, `docs/PACKAGING.md`. `HCS`: `old/srep-main`, `old/paq8px`, `old/preflate-master`,
`LICENSES/INDEX.json`. `ziptastic`: `docs/FINDINGS.md` (§5, measured-and-rejected), the v1.4.2 release
assets. This repo: `README.md`, `log/2026-11/2026-11-10-ziptastic-claims-match-findings.md`.

## What was wrong

Six things, in the order they bit.

1. **The release shipped nothing runnable.** `v1.0.0` had **0 assets**. A user downloading a release
   got no engine, so every profile refused at pre-flight. `kosh` v1.1.0 was the same, and `lexora`
   v0.1.0a2 carried **0.1.0a1** wheels under an a2 tag.
2. **Every shipped profile passed options the engine does not have.** `-c lzma -9`,
   `-c brotli -q 11` — ziptastic has no `-c` and no `-q`; its options are `-9`, `--max-ratio`,
   `--no-cm-stream`, `--no-precomp`, `--no-numeric`. No test ran the *shipped* profiles against the
   *shipped* engine, so nothing noticed.
3. **Decompressing any pipeline longer than one step failed.** `run_reverse` did not clear its
   target and ziptastic refuses to overwrite, so the first reverse step died on
   `exists (use -f)` while the bytes were perfectly recoverable.
4. **`compress` trusted exit codes.** `paq8px -8` on a 1.3 MB file runs out of memory, prints
   `Out of memory.`, writes a **14-byte stub** and returns **0**. That archive would have been
   handed over as a success.
5. **srep could not run on an ordinary machine.** `-m5f` with no dictionary cap aborts with
   `Can't allocate memory: 1729 mb`.
6. **srep has no licence and nothing said so.** No file, no statement, anywhere in
   `old/srep-main` — Bulat Ziganshin's code, an unofficial repackage. The fleet's own rule said
   "srep never ships"; that rule was a note in a document, not a fact anywhere in a release.

## What I changed

**heavenzip**

- `compress` verifies by default: it reverses what it wrote and compares the bytes
  (`--no-verify` to skip). A corrupt archive is refused with a sentence, not handed over.
- `run_reverse` clears the file it is about to produce; two-step round trips now restore.
- srep and paq8px set `reverse_args = -d`; they have no `d` verb.
- `plain.ini` (engine only) is the default; `text`/`media` pass real options.
- `integration.shipped-profiles` — runs each profile's own `args` against the real engine.
- `autotune <file>`: tries the combinations the tools allow, ranks by measured size, verifies each
  by reversing it, and reports three winners — `smallest`, `fastest`, `balanced`. `--goal` picks
  which `--write` saves; `--templates <dir>` writes all three side by side.
- Steps accept `{in}`/`{out}` placeholders, so a tool whose CLI is `-o OUT IN` (brotli) is a profile
  rather than a wrapper script; the manifest records `reverse_out_index` because the restore target
  is not always the last argument.
- `build-tools.yml` builds paq8px (g++) and srep (zig) and assembles the whole bundle, which now
  carries the engine, paq8px, srep, `sources/paq8px-source.tar.gz` (GPL-2 §3),
  `sources/srep-source.tar.gz`, `SHA256SUMS` and a NOTICE that states srep's position plainly.
- `docs/TRAPS.md` — ten traps this repo has already sprung, linked from `AGENT_PROMPT.md` §11.

**HCS** — the last six `verify` rows read from their own texts. One was a surprise: **`rhefo` is
SSPL-1.0**, not open source, and `NOTICE` now says so. Coverage corrected from "53 of 53" to
**52 of 52** (the old denominator counted the unvendored `csc` queue row).

**ziptastic** — vendored copy current (`SOURCES matches HCS main (232 lines)`, 132/132 digests).

## Evidence

    ./heavenzip autotune 60 KB file
      zmax        0.2046  1.48s  verified
      srep-zmax   0.2060  1.57s  verified
      z9          0.2119  0.22s  balanced verified
      paq8        0.1915  15.8s smallest verified
      smallest paq8 0.1915 · fastest z9 0.2119 · balanced z9 0.2119

    compress with paq8px -8 on 1.3 MB
      heavenzip: the archive does not restore the input (bytes differ)   exit 1

    release v1.0.0, downloaded and run on a different machine from the builder
      sha256sum -c                     heavenzip-linux-x86_64.tar.gz: OK
      ./heavenzip validate             valid: 5 profile(s) … exit 0
      ./bin/srep    round trip        ROUND-TRIPS
      ./bin/paq8px  round trip        ROUND-TRIPS
      ./bin/ziptastic version         1.4.2 (CHCE format v8)

    heavenzip: 9/9 ctest suites; main green; 0 open PRs
    HCS: build-licences 52/52 · check-licences 0 failures · check-sources OK

## What I deliberately did not do

- **preflate is not bundled.** Apache-2.0, but `support/filestream.cpp` calls `_ftelli64` and
  `_fseeki64` unconditionally — MSVC-only, no `#ifdef`. It does not compile on Linux, so there is no
  binary to ship. The licence text travels anyway.
- **srep's licence is unresolved, not solved.** There is nothing to grant, so `NOTICE` states that
  no licence has been granted and that redistributing the binary is the publisher's decision. I did
  not invent a permission from a README line.
- **brotli, xz and zpaq are not bundled.** brotli's CMake build will not configure under the zig
  toolchain here and brotli already lives inside the engine; xz and zpaq need argument shapes a
  profile still cannot express (`xz` a redirect, `zpaq a ARCHIVE FILE`). The placeholder work makes
  the first of those expressible; the others need wrappers.
- **No number in ziptastic or lexora was touched.** ziptastic's §5 "measured and rejected" table was
  read and respected — nothing there was rebuilt. lexora's 0.3352-vs-0.3367 benchmark conflict stays
  open, because resolving it needs the run artefacts, not a better argument.
- **kosh's Pages source is still `/`.** The API refuses the change (403, needs repository admin); a
  root redirect makes the designed page reachable in the meantime.

## Next

1. The three remaining vault compressors, as wrappers or as a second placeholder form.
2. lexora's two fleet gates (badge truth, licence record) and its benchmark conflict.
3. heavenzip's `verify` on by default doubles the cost of a large compress; a `--verify=hash` mode
   would make it cheap enough to be unquestioned.
