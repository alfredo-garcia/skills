#!/usr/bin/env bash
# gh_labels.sh — the SDLC suite's GitHub labels (work_tracking_guide.md §3).
# Default: prints the gh commands (dry run). With --apply: creates/updates them (idempotent, --force).
# Run --apply only after the user approves. Requires gh, authenticated, inside the project's repo.
set -uo pipefail
APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1
# The decision label comes from SDLC.md (decision_label), searched upward from the current directory.
DL="needs-decision"; d="$PWD"
while :; do
  if [ -f "$d/SDLC.md" ]; then
    v="$(grep -m1 -E '^[[:space:]]*-[[:space:]]+decision_label:' "$d/SDLC.md" | sed -E 's/^[^:]*:[[:space:]]*//; s/[[:space:]]+#.*$//; s/[[:space:]]+$//')"
    [ -n "$v" ] && DL="$v"; break
  fi
  [ "$d" = "/" ] && break; d="$(dirname "$d")"
done
LABELS="feature:1D76DB story:5319E7 task:0E8A16 bug:D73A4A tech-debt:B60205 chore:C5DEF5 idea:FBCA04 phase-0:006B75
role:pm:BFD4F2 role:tech-lead:BFD4F2 role:qa:BFD4F2 role:eng:BFD4F2 role:ux:BFD4F2 role:platform:BFD4F2 role:release:BFD4F2 role:docs:BFD4F2
needs-triage:EDEDED in-progress:0052CC blocked:B60205 ${DL}:FF7619 risk:high:B60205 sdlc:5A5A5A"
for entry in $LABELS; do
  color="${entry##*:}"; name="${entry%:*}"
  cmd=(gh label create "$name" --color "$color" --force)
  if [ "$APPLY" -eq 1 ]; then "${cmd[@]}" >/dev/null && echo "ok      $name" || echo "FAILED  $name"
  else printf '%q ' "${cmd[@]}"; echo; fi
done
[ "$APPLY" -eq 0 ] && echo "# dry run; re-run with --apply after the user approves"
exit 0
