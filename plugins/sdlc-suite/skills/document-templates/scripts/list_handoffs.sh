#!/usr/bin/env bash
# list_handoffs.sh — features whose product work is done and that wait for the technical team.
#
#   list_handoffs.sh <features_root>
#
# Looks at every local and remote-tracking branch of the project (branch_pattern
# <project_id>/<id>-<slug>) for a PRD whose header says `Handoff: ready for development (date)`.
# Prints one line per feature: STATE id branch prd date, where STATE is READY (nobody has
# picked it up) or PICKED_UP (a technical session already took it: `picked up (date)`), plus the
# worktree path if the branch is checked out somewhere. Run `git fetch` first when there's a
# remote. Read-only.
set -uo pipefail
FEATURES_ROOT="${1:?Usage: list_handoffs.sh <features_root>}"
probe="$FEATURES_ROOT"
while [ ! -d "$probe" ] && [ "$probe" != "/" ] && [ "$probe" != "." ]; do probe="$(dirname "$probe")"; done
probe="$(cd "$probe" && pwd -P)"
d="$probe"; FOUND=""
while :; do [ -f "$d/SDLC.md" ] && { FOUND="$d"; break; }; [ "$d" = "/" ] && break; d="$(dirname "$d")"; done
[ -z "$FOUND" ] && { echo "ERROR: '$FEATURES_ROOT' is not inside a project (no SDLC.md above it)."; exit 3; }
GR="$(git -C "$FOUND" rev-parse --show-toplevel 2>/dev/null || true)"
[ -z "$GR" ] && { echo "NOT_A_GIT_REPO: handoffs need branches"; exit 0; }
if [ -d "$FEATURES_ROOT" ]; then ABS="$(cd "$FEATURES_ROOT" && pwd -P)"; else ABS="$(cd "$(dirname "$FEATURES_ROOT")" && pwd -P)/$(basename "$FEATURES_ROOT")"; fi
case "$ABS" in "$GR"/*) REL="${ABS#$GR/}" ;; *) echo "ERROR: features root outside the repo"; exit 3 ;; esac
PID="$(grep -E '^[[:space:]]*-[[:space:]]+project_id:' "$FOUND/SDLC.md" | head -1 | sed -E 's/^[^:]*:[[:space:]]*//; s/[[:space:]]+#.*$//')"

# branch -> worktree path
WT="$(git -C "$GR" worktree list --porcelain 2>/dev/null | awk '/^worktree /{p=$2} /^branch /{sub("refs/heads/","",$2); print $2" "p}')"

COUNT=0; SEEN=""
for ref in $(git -C "$GR" for-each-ref --format='%(refname:short)' refs/heads refs/remotes | grep -v '/HEAD$' | grep -E "(^|/)${PID}/[0-9]{3}-"); do
  local_name="${ref#origin/}"
  case " $SEEN " in *" $local_name "*) continue ;; esac   # local and origin copy: report once (local first)
  for f in $(git -C "$GR" ls-tree --name-only "$ref" -- "$REL/" 2>/dev/null | grep -E '/[0-9]{3}_[^/]*_prd\.md$'); do
    HEAD_TXT="$(git -C "$GR" show "$ref:$f" 2>/dev/null | head -40)"
    LINE="$(echo "$HEAD_TXT" | grep -i -E '^>[[:space:]]*Handoff:' | head -1)"
    echo "$LINE" | grep -qi 'ready for development' || continue
    ID="$(basename "$f" | cut -c1-3)"
    case "$ref" in *"/$PID/$ID-"*|"$PID/$ID-"*) ;; *) continue ;; esac  # the PRD belongs to this branch's feature
    STATE=READY; echo "$LINE" | grep -qi 'picked up' && STATE=PICKED_UP
    DATE="$(echo "$LINE" | grep -o -E 'ready for development \([0-9-]+\)' | grep -o -E '[0-9]{4}-[0-9]{2}-[0-9]{2}')"
    P="$(echo "$WT" | awk -v b="$local_name" '$1==b{print $2}')"
    echo "$STATE $ID $ref $(basename "$f") ${DATE:-?}${P:+ worktree:$P}"
    COUNT=$((COUNT+1)); SEEN="$SEEN $local_name"
  done
done
[ "$COUNT" -eq 0 ] && echo "NO_HANDOFFS (no feature branch has a PRD marked 'Handoff: ready for development')"
exit 0
