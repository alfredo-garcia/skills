#!/usr/bin/env bash
# next_adr_id.sh — next ADR number for a project, counted across this working tree AND every local
# and remote-tracking branch, so two features in parallel branches never mint the same ADR number.
#
#   next_adr_id.sh <adr_dir>   -> NEXT_ADR: 004
#
# <adr_dir> is <docs_root>/architecture/adr of the project (resolved by project_context.sh).
# Run `git fetch` first when there's a remote. Read-only.
set -uo pipefail
ADR_DIR="${1:?Usage: next_adr_id.sh <adr_dir>}"
probe="$ADR_DIR"
while [ ! -d "$probe" ] && [ "$probe" != "/" ] && [ "$probe" != "." ]; do probe="$(dirname "$probe")"; done
probe="$(cd "$probe" && pwd -P)"
d="$probe"; FOUND=""
while :; do [ -f "$d/SDLC.md" ] && { FOUND="$d"; break; }; [ "$d" = "/" ] && break; d="$(dirname "$d")"; done
[ -z "$FOUND" ] && { echo "ERROR: '$ADR_DIR' is not inside a project (no SDLC.md above it)."; exit 3; }
if [ -d "$ADR_DIR" ]; then ABS="$(cd "$ADR_DIR" && pwd -P)"; else ABS="$(cd "$(dirname "$ADR_DIR")" 2>/dev/null && pwd -P)/$(basename "$ADR_DIR")"; fi
NUMS=""
[ -d "$ADR_DIR" ] && NUMS="$(find "$ADR_DIR" -maxdepth 1 -type f -name '[0-9][0-9][0-9]_*.md' -exec basename {} \; 2>/dev/null | cut -c1-3)"
GR="$(git -C "$FOUND" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$GR" ]; then
  case "$ABS" in "$GR"/*)
    REL="${ABS#$GR/}"
    for ref in $(git -C "$GR" for-each-ref --format='%(refname:short)' refs/heads refs/remotes | grep -v '/HEAD$'); do
      NUMS="$NUMS
$(git -C "$GR" ls-tree --name-only "$ref" -- "$REL/" 2>/dev/null | xargs -r -n1 basename | grep -E '^[0-9]{3}_.*\.md$' | cut -c1-3)"
    done ;;
  esac
fi
MAX="$(echo "$NUMS" | grep -E '^[0-9]{3}$' | sort -n | tail -1)"
if [ -z "$MAX" ]; then N=1; else N=$((10#$MAX + 1)); fi
printf "NEXT_ADR: %03d\n" "$N"
echo "(counted across this working tree and all local and remote branches)"
exit 0
