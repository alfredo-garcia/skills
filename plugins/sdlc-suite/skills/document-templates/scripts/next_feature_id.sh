#!/usr/bin/env bash
# next_feature_id.sh — the single source of truth for Feature IDs (shared by all SDLC skills).
#
# Every feature gets a permanent, sequential, 3-digit zero-padded ID (001, 002, ...) the first
# time its feature definition doc is created (product-manager Mode A). Two modes:
#
#   Mint:   next_feature_id.sh <features_root>          -> NEXT_ID: 007
#   Lookup: next_feature_id.sh <features_root> <slug>   -> EXISTING_ID: 003  (never mints)
#
# <features_root> is the FEATURES_ROOT printed by project_context.sh. The script refuses to run
# if that folder isn't inside a project (no SDLC.md above it), so it can never count IDs from
# another project's folder by mistake.
#
# Read-only: never creates, renames or deletes anything.

set -uo pipefail

FEATURES_ROOT="${1:?Usage: next_feature_id.sh <features_root> [existing_feature_slug]}"
SLUG="${2:-}"

# --- Guard: the features root must belong to a project (an SDLC.md in it or above it) ---
probe="$FEATURES_ROOT"
while [ ! -d "$probe" ] && [ "$probe" != "/" ] && [ "$probe" != "." ]; do probe="$(dirname "$probe")"; done
probe="$(cd "$probe" && pwd -P)"
d="$probe"; FOUND=""
while :; do
  [ -f "$d/SDLC.md" ] && { FOUND="$d"; break; }
  [ "$d" = "/" ] && break
  d="$(dirname "$d")"
done
if [ -z "$FOUND" ]; then
  echo "ERROR: '$FEATURES_ROOT' is not inside a project (no SDLC.md above it). Resolve the project first (project_context.sh)."
  exit 3
fi

# --- Lookup mode ---
if [ -n "$SLUG" ]; then
  MATCH=""
  if [ -d "$FEATURES_ROOT" ]; then
    MATCH="$(find "$FEATURES_ROOT" -maxdepth 1 -type f \( -iname "[0-9][0-9][0-9]_${SLUG}.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_prd.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_ux_flow.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_test_plan.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_impl_plan.md" \) 2>/dev/null | sort | head -1)"
  fi
  if [ -n "$MATCH" ]; then
    B="$(basename "$MATCH")"
    echo "EXISTING_ID: ${B:0:3}"
    echo "(found in $B; reuse this ID, don't mint a new one)"
  else
    echo "NO_EXISTING_ID_FOUND for slug '$SLUG' in $FEATURES_ROOT"
    echo "(if you expected one, check the slug/case before treating this as a new feature)"
  fi
  exit 0
fi

# --- Mint mode ---
if [ ! -d "$FEATURES_ROOT" ]; then
  echo "NEXT_ID: 001"
  echo "(features root doesn't exist yet; this will be the first feature)"
  exit 0
fi

MAX="$(find "$FEATURES_ROOT" -maxdepth 1 -type f -name '[0-9][0-9][0-9]_*.md' -exec basename {} \; 2>/dev/null \
  | cut -c1-3 | sort -n | tail -1)"
if [ -z "$MAX" ]; then NEXT=1; else NEXT=$((10#$MAX + 1)); fi
printf "NEXT_ID: %03d\n" "$NEXT"
