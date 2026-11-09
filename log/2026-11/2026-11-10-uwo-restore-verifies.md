# ULTIMATE-WINDOWS-OPTIMIZER — the undo said "restored" without checking

Date: 2026-11-10 · Repo `drsamonline/ULTIMATE-WINDOWS-OPTIMIZER` · PR #4
(open, not merged)
Reference links taken: `farag2/Sophia-Script-for-Windows` (revert discipline),
`ChrisTitusTech/winutil` (preset/undo design) — as the standard to hold, not code

## What I looked at
`scripts/UWO.psm1` (restore paths, de-duplication), `Undo-All-Changes.ps1`,
`Compare-Results.ps1`, `Common-Functions.ps1`, the four Pester files, `ci.yml`.

## What was wrong
`Restore-RegistryBackupRecord` wrote the value and logged "Restored ... to original
value" as soon as `New-ItemProperty` returned — no read-back. And its internal
`catch` swallowed failures, so `Undo-All-Changes.ps1` incremented `$restoredCount`
anyway and printed "N record(s) restored" in green. The header promises "a genuine
full rollback"; a failed restore was counted as a success.

## What I changed
Read-back and compare (`[string]` both sides) after the write; verify removal in the
`Existed = $false` branch; drop the internal catch so the caller's handler counts a
failure as failed.

## Evidence
    Pester 5.7.1, windows-latest, run 42675226508 — success
      [+] throws when the write does not land, instead of reporting success  39ms
    three existing restore tests unchanged (happy paths still assert value
    restored / value removed / created key kept)

## What I deliberately did not do
- De-duplication (`Select-BackupRecordsToRestore`) untouched — already keeps the
  oldest original and is already tested.
- Service / hibernation / power-plan restores untouched: the same read-back belongs
  there and is the obvious next branch.
- No version bump, no merge.

## Next
Decide on PR #4, then the same treatment for the service and power-plan restores.
