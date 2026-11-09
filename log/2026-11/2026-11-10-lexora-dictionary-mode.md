# lexora — dictionary mode for the zstd baseline

Date: 2026-11-10 · Repo `drsamonline/lexora` · PR #39 (open, not merged)
Reference links taken: `meta/zstd` (dictionary mode as the baseline), 
`eschluntz/compress` and `headroomlabs-ai/headroom` read for the
ratio-vs-recoverability framing, no code

## What I looked at
`src/lexora/zstd_core.py`, `container.py`, `codec_registry.py`, the 35 test files,
`pyproject.toml`, CI. Baseline run: `650 passed, 30 failed, 3 skipped`.

## What was wrong (missing, not broken)
The codec compressed every input from scratch, so a few hundred bytes of text — a
note, a rubric, a single record — had no repetition for the window to find and sat
near 0.9x. No dictionary support anywhere (`grep dict zstd_core.py` → only
`verify_roundtrip`).

## What I changed
`train_dictionary(samples, size)`; optional `dict_data` on `compress`,
`decompress`, `verify_roundtrip`; `_profile_id` reports `zstd-dict-l<level>` for a
dictionary frame. Frame format and container untouched.

## Evidence
    note: patient reports itching worse at night
      no dictionary  49 B
      dictionary     19 B          (2,340 B dict trained on 64 samples)
    round-trip byte-exact; decoding without the dictionary raises CodecError
    pytest tests/test_zstd_core.py   21 passed
    previous zstd_core.py            5 failed, 16 passed (no train_dictionary)
    pytest tests                     655 passed, 30 failed, 3 skipped
CI run 42680596549: success.

The 30 failures are pre-existing and environmental: `test_gui_service.py` and
`test_level_usage.py` need `tkinter`; this sandbox has no `libtk8.6.so`. CI runs
the GUI suite and is green on main.

## What I deliberately did not do
- No container change: FORMAT_LXZ.md says do not implement decoders from it, and a
  dictionary is not a format.
- No selection policy (when to use a dictionary) — Phase 2.
- No CLI `--dict` flag until the policy exists.
- No version bump, no merge.

## Next
Decide on PR #39; the selection policy is the natural follow-on.
