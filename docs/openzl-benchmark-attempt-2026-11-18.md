# OpenZL benchmark — attempt and status, 2026-11-18

Plan item 1. **Not completed**, and the reason is build cost in this sandbox, not anything about
OpenZL. This file exists so the next session does not repeat the attempt blindly.

## What worked

| step | result |
|---|---|
| PyPI package | `openzl 0.3.0` installs cleanly — a manylinux abi3 wheel, imports, exposes a low-level API |
| API surface | `Compressor`, `CCtx`, `DCtx`, `Input`, `FunctionGraph`, `GraphID`, `NodeID` |
| clone + configure | `git clone -b release` (82 MB), `cmake -G Ninja` configures in 72 s with zig cc |
| build | progresses; reached **34/114** of the `zli` target across several 280-second calls |

## What blocked it

1. **There is no Linux binary.** The only release asset is `openzl-cli-windows-x64.exe`, so the CLI
   must be built.
2. **`make` is absent** in this pod; the CMake route works, but the SDDL and SDDL2 compiler
   subdirectories (`tools/CMakeLists.txt:59-60`) are unconditional — no `option()` gates them — and
   they are the expensive part: roughly one object per 280-second call near the end.
3. **The Python package cannot substitute.** It ships no prebuilt graph: `Compressor.get_node()` has
   no registry without the CLI, so the node names (`zl.Zstd`, `Zstd`, …) cannot be discovered from
   Python alone. The wheel is for people who already have a serialised graph.

## What would finish it

- a machine with `make` and gcc, where the whole CLI builds in a few minutes; or
- `zli`'s `list-profiles` output, which would name the profiles and let the Python API build an
  equivalent graph; or
- a prebuilt Linux `zli` from upstream, which does not exist today.

## Why it still matters

The benchmark is the only item on the plan that can *invalidate* a claim rather than add one: OpenZL
is BSD, format-aware, in production at Meta, and has no canonicaliser, so it is the first external
yardstick Layer 0 has faced. Being blocked on a compiler is a scheduling problem; the comparison
itself is still the highest-value thing on the list.

**Next session, first move:** install `make` or use a machine that has it, then
`cmake --build build --target zli -j$(nproc)` and `./build/cli/zli list-profiles`.
