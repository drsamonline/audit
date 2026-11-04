#!/usr/bin/env bash
# restore-schedules.sh — undo the 2026-11-04 pause.
#
# Every scheduled workflow in the estate was disabled on the owner's instruction so
# the audit could run against a still estate. This puts them back. It reads the
# manifest beside it, so it cannot restore a list somebody remembered rather than
# the list that was actually paused.
#
#   bash tools/restore-schedules.sh                     re-enable all 32
#   bash tools/restore-schedules.sh --verify            change nothing, report state
#   bash tools/restore-schedules.sh --only forge/new-app.yml
#   bash tools/restore-schedules.sh --dry-run           print the calls, make none
#
# Needs a token that can write Actions settings: a fine-grained PAT with
# "Actions: write" on the repositories listed in the manifest. GITHUB_TOKEN inside a
# workflow will not do it — that token is scoped to its own repository.
#
# SPDX-FileCopyrightText: 2026 Dr Sohil Momin
# SPDX-License-Identifier: LicenseRef-Forge-Proprietary
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$HERE/../state/schedules-paused-2026-11-04.json"
OWNER="${OWNER:-drsamonline}"
MODE=enable
ONLY=""
DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --verify) MODE=verify ;;
    --dry-run) DRY=1 ;;
    --only) shift; ONLY="${1:-}" ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

[ -f "$MANIFEST" ] || { echo "::error::no manifest at $MANIFEST" >&2; exit 1; }
command -v jq >/dev/null || { echo "::error::jq is required" >&2; exit 1; }

# One row per workflow: repo, numeric id, file.
rows="$(jq -r '.workflows[] | [.repo, (.workflow_id|tostring), .file] | @tsv' "$MANIFEST")"
[ -n "$rows" ] || { echo "::error::the manifest lists no workflows" >&2; exit 1; }

total=0; changed=0; already=0; failed=0

while IFS=$'\t' read -r repo id file; do
  key="$repo/$file"
  if [ -n "$ONLY" ] && [ "$key" != "$ONLY" ]; then continue; fi
  total=$((total+1))

  # Read the state, and say WHY when it cannot be read. A 403 here is a credential
  # problem, not a missing workflow — the distinction the estate has confused three
  # times (a 404 on a private repo is a wrong token, never an absent repo).
  raw="$(gh api "repos/$OWNER/$repo/actions/workflows/$id" 2>&1)"
  current="$(printf '%s' "$raw" | jq -r '.state // empty' 2>/dev/null)"
  if [ -z "$current" ]; then
    case "$raw" in
      *"Resource not accessible"*|*"403"*) current="no-actions-read" ;;
      *"Not Found"*|*"404"*)               current="not-found" ;;
      *)                                   current="unreadable" ;;
    esac
  fi

  if [ "$MODE" = verify ]; then
    case "$current" in
      active) echo "  ACTIVE     $key" ;;
      disabled_manually|disabled_inactivity) echo "  PAUSED     $key  ($current)" ;;
      no-actions-read)
        echo "  CANNOT READ $key — this token has no Actions:read on it."
        echo "              A 403 is a credential, not a missing workflow."
        failed=$((failed+1)) ;;
      *) echo "  UNREADABLE $key  ($current)"; failed=$((failed+1)) ;;
    esac
    continue
  fi

  if [ "$current" = "active" ]; then
    echo "  already active  $key"; already=$((already+1)); continue
  fi

  if [ "$DRY" = 1 ]; then
    echo "  would enable    $key  (id $id, now: $current)"; continue
  fi

  if gh api -X PUT "repos/$OWNER/$repo/actions/workflows/$id/enable" >/dev/null 2>&1; then
    after="$(gh api "repos/$OWNER/$repo/actions/workflows/$id" --jq '.state' 2>/dev/null || echo unreadable)"
    # The verdict is the state read back, not the exit code of the PUT — the estate's
    # own rule, and the reason commit-and-verify.sh exists.
    if [ "$after" = "active" ]; then
      echo "  enabled         $key"; changed=$((changed+1))
    else
      echo "  ::error::$key did not come back active (found: $after)"; failed=$((failed+1))
    fi
  else
    echo "  ::error::could not enable $key (id $id) — check the token's Actions:write"; failed=$((failed+1))
  fi
done <<< "$rows"

echo
echo "total=$total enabled=$changed already=$already failed=$failed mode=$MODE dry_run=$DRY"
[ "$failed" -eq 0 ] || exit 1

# A schedule is not a schedule until it has fired once. After restoring, the next
# fire is the real test: check the Actions tab, or run
#   gh run list --repo <owner>/<repo> --workflow <file> --limit 1
# for any workflow you care about. self-diagnose.yml checks this automatically —
# a scheduled workflow older than twice its period is not scheduled, it is broken.
