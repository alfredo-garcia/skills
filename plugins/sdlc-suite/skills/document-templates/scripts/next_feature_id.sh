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
# Parallel work: features live on their own branches (and worktrees) until merged, so IDs are
# counted across the working tree AND every local and remote-tracking branch of the repo (same
# folder path in each). Run `git fetch` first when there's a remote, so other machines' branches
# count too.
#
# Read-only: never creates, renames or deletes anything (git is only read).

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

# --- Cross-branch scan: "<ref> <file>" for every NNN_*.md under the features folder in every branch ---
FEAT_ABS=""
if [ -d "$FEATURES_ROOT" ]; then FEAT_ABS="$(cd "$FEATURES_ROOT" && pwd -P)"
else FEAT_ABS="$(cd "$(dirname "$FEATURES_ROOT")" 2>/dev/null && pwd -P)/$(basename "$FEATURES_ROOT")"; fi
GR="$(git -C "$FOUND" rev-parse --show-toplevel 2>/dev/null || true)"
branch_files() {
  [ -n "$GR" ] || return 0
  case "$FEAT_ABS" in "$GR"/*) ;; *) return 0 ;; esac
  local rel="${FEAT_ABS#$GR/}" ref
  git -C "$GR" for-each-ref --format='%(refname:short)' refs/heads refs/remotes 2>/dev/null | grep -v '/HEAD$' | while read -r ref; do
    git -C "$GR" ls-tree --name-only "$ref" -- "$rel/" 2>/dev/null | while read -r f; do
      b="$(basename "$f")"
      case "$b" in [0-9][0-9][0-9]_*.md) echo "$ref $b" ;; esac
    done
  done
}

# --- Lookup mode ---
if [ -n "$SLUG" ]; then
  MATCH=""
  if [ -d "$FEATURES_ROOT" ]; then
    MATCH="$(find "$FEATURES_ROOT" -maxdepth 1 -type f \( -iname "[0-9][0-9][0-9]_${SLUG}.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_prd.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_ux_flow.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_test_plan.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_impl_plan.md" -o -iname "[0-9][0-9][0-9]_${SLUG}_handoff.md" \) 2>/dev/null | sort | head -1)"
  fi
  if [ -n "$MATCH" ]; then
    B="$(basename "$MATCH")"
    echo "EXISTING_ID: ${B:0:3}"
    echo "(found in $B; reuse this ID, don't mint a new one)"
  elif BM="$(branch_files | grep -i -E " [0-9]{3}_${SLUG}(_prd|_ux_flow|_test_plan|_impl_plan|_handoff)?\.md$" | head -1)" && [ -n "$BM" ]; then
    B="${BM#* }"
    echo "EXISTING_ID: ${B:0:3}"
    echo "(found in $B on branch ${BM%% *}, not in this working tree; reuse this ID and work on that branch)"
  else
    echo "NO_EXISTING_ID_FOUND for slug '$SLUG' in $FEATURES_ROOT"
    echo "(if you expected one, check the slug/case before treating this as a new feature)"
  fi
  exit 0
fi

# --- Mint mode ---
LOCAL=""
[ -d "$FEATURES_ROOT" ] && LOCAL="$(find "$FEATURES_ROOT" -maxdepth 1 -type f -name '[0-9][0-9][0-9]_*.md' -exec basename {} \; 2>/dev/null)"
BRANCHES="$(branch_files)"
# A feature branch reserves its ID as soon as it exists, even before its first commit of a doc
PID="$(grep -E '^[[:space:]]*-[[:space:]]+project_id:' "$FOUND/SDLC.md" | head -1 | sed -E 's/^[^:]*:[[:space:]]*//; s/[[:space:]]+#.*$//')"
if [ -n "$GR" ] && [ -n "$PID" ]; then
  BRANCHES="$BRANCHES
$(git -C "$GR" for-each-ref --format='%(refname:short)' refs/heads refs/remotes 2>/dev/null \
    | grep -E "(^|/)${PID}/[0-9]{3}-" | sed -E "s#^(.*(^|/)${PID}/([0-9]{3})-.*)\$#\1 \3_branch.md#")"
fi
MAX="$( { echo "$LOCAL"; echo "$BRANCHES" | sed 's/^[^ ]* //'; } | grep -E '^[0-9]{3}_' | cut -c1-3 | sort -n | tail -1)"
if [ -z "$MAX" ]; then NEXT=1; else NEXT=$((10#$MAX + 1)); fi
printf "NEXT_ID: %03d\n" "$NEXT"
if [ -n "$MAX" ]; then
  SRC="$(echo "$BRANCHES" | grep -E " ${MAX}_" | head -1 | cut -d' ' -f1)"
  echo "(highest existing: ${MAX}${SRC:+, on branch $SRC}; counted across this working tree and all local and remote branches)"
else
  echo "(no features yet in this working tree or any branch; this will be the first feature)"
fi
if [ -z "$GR" ]; then echo "(not a git repository: only this working tree was counted)"; fi
exit 0
