#!/usr/bin/env bash
# project_context.sh — shared by every SDLC skill (Step 0 of project_context_protocol.md).
#
# Resolves the project root (the folder containing SDLC.md) by walking UP from the
# start directory, parses SDLC.md, validates its paths, and prints an inventory of
# the project's documents, its Phase 0 status, and isolation warnings.
#
# Read-only: never creates, modifies or deletes anything.
# Never searches outside the start directory's ancestors (upward) or its own
# subtree (downward, depth <= 3). It never scans $HOME or / broadly.
#
# Usage:  bash project_context.sh [start_dir]
# Exit:   0 = project resolved; 2 = no SDLC.md upward (candidates below are listed); 3 = invalid config

set -uo pipefail

START="${1:-$PWD}"
if ! START="$(cd "$START" 2>/dev/null && pwd -P)"; then
  echo "ERROR: start directory '${1:-$PWD}' does not exist"; exit 3
fi

# ---------- 1. Walk upward for SDLC.md ----------
ROOT=""
DIR="$START"
while :; do
  if [ -f "$DIR/SDLC.md" ]; then ROOT="$DIR"; break; fi
  [ "$DIR" = "/" ] && break
  DIR="$(dirname "$DIR")"
done

if [ -z "$ROOT" ]; then
  echo "NO_SDLC_FOUND upward from: $START"
  echo "Candidates below the start directory (depth <= 3), excluding node_modules/.git:"
  CANDS="$(find "$START" -maxdepth 3 \( -name node_modules -o -name .git \) -prune -o -type f -name SDLC.md -print 2>/dev/null | sort)"
  if [ -n "$CANDS" ]; then
    echo "$CANDS" | sed 's/^/  CANDIDATE: /'
    echo "-> Confirm with the user which project to use (never guess), then re-run with that folder."
  else
    echo "  (none)"
    echo "-> No project here. Offer Project Init (project_context_protocol.md §7)."
  fi
  exit 2
fi

CFG="$ROOT/SDLC.md"

# ---------- 2. Parse config ----------
# Reads "- key: value" lines; strips trailing " # comment" and surrounding whitespace.
get_from() {  # $1=file $2=key
  local line
  line="$(grep -m1 -E "^[[:space:]]*-[[:space:]]+$2:" "$1" 2>/dev/null)" || { echo ""; return; }
  line="${line#*:}"
  line="${line%% \#*}"
  echo "$line" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//'
}
get() { get_from "$CFG" "$1"; }
split_list() { echo "$1" | tr ',' '\n' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' | grep -v -E '^(none)?$'; }
is_safe_rel() {  # relative, no .., not absolute
  case "$1" in /*|~*) return 1 ;; esac
  case "/$1/" in */../*) return 1 ;; esac
  return 0
}

PROJECT_ID="$(get project_id)"
TYPE="$(get type)";                 TYPE="${TYPE:-app}"
NAME="$(get name)"
LANG_="$(get docs_language)"
RIGOR="$(get rigor)";               RIGOR="${RIGOR:-personal}"
FLOW="$(get flow)";                 if [ -z "$FLOW" ]; then [ "$RIGOR" = "production" ] && FLOW=step || FLOW=autopilot; fi
TECHDEC="$(get technical_decisions)"; TECHDEC="${TECHDEC:-user}"; TECHDEC_NOTE=""
if [ "$TECHDEC" = "auto" ]; then
  LAST_LOG="$(sed -n '/^## Decision mode log/,/^## /p' "$CFG" | grep -E '^[[:space:]]*-[[:space:]]+[0-9]{4}-[0-9]{2}-[0-9]{2}:' | tail -1)"
  if ! echo "$LAST_LOG" | grep -qE ':[[:space:]]*auto,[[:space:]]*requested by'; then
    TECHDEC_NOTE="  <WARNING: 'auto' without a matching last entry in '## Decision mode log'. Treat as 'user' and tell the user (protocol §14)>"
    TECHDEC="user"
  else
    TECHDEC_NOTE="  (log: ${LAST_LOG#*- })"
  fi
fi
SURFACES="$(get surfaces)"
LEGACY_PLATFORMS="$(get platforms)"
if [ -z "$SURFACES" ] && [ -n "$LEGACY_PLATFORMS" ]; then
  case "$LEGACY_PLATFORMS" in
    web) SURFACES="web" ;; mobile) SURFACES="android, ios" ;; web+mobile) SURFACES="web, android, ios" ;; none) SURFACES="none" ;; *) SURFACES="$LEGACY_PLATFORMS" ;;
  esac
  SURF_NOTE=" (derived from legacy 'platforms: $LEGACY_PLATFORMS' — suggest migrating to 'surfaces')"
fi
DOCS_REL="$(get docs_root)";        DOCS_REL="${DOCS_REL:-docs}"
FEAT_REL="$(get features_root)";    FEAT_REL="${FEAT_REL:-docs/features}"
BASE="$(get base_branch)";          BASE="${BASE:-main}"

echo "== SDLC project context =="
echo "PROJECT_ROOT: $ROOT"
echo "project_id:    ${PROJECT_ID:-<MISSING>}"
echo "type:          $TYPE"
echo "name:          ${NAME:-<MISSING>}"
echo "docs_language: ${LANG_:-<MISSING>}"
echo "rigor:         $RIGOR"
echo "flow:          $FLOW"
HANDOFF="$(get handoff)"; echo "handoff:       ${HANDOFF:-none}"
echo "technical_decisions: $TECHDEC${TECHDEC_NOTE}"
echo "surfaces:      ${SURFACES:-<MISSING>}${SURF_NOTE:-}"
echo "base_branch:   $BASE"

ERR=0
[ -z "$PROJECT_ID" ] && { echo "CONFIG_ERROR: project_id missing in SDLC.md"; ERR=1; }
case "$TYPE" in app|shared) ;; *) echo "CONFIG_ERROR: type must be 'app' or 'shared' (got '$TYPE')"; ERR=1 ;; esac
case "$RIGOR" in personal|production) ;; *) echo "CONFIG_ERROR: rigor must be 'personal' or 'production' (got '$RIGOR')"; ERR=1 ;; esac
case "$(get handoff)" in ""|none|after_design) ;; *) echo "CONFIG_ERROR: handoff must be 'none' or 'after_design' (got '$(get handoff)')"; ERR=1 ;; esac
case "$FLOW" in autopilot|step) ;; *) echo "CONFIG_ERROR: flow must be 'autopilot' or 'step' (got '$FLOW')"; ERR=1 ;; esac
case "$(get technical_decisions)" in ""|user|auto) ;; *) echo "CONFIG_ERROR: technical_decisions must be 'user' or 'auto' (got '$(get technical_decisions)')"; ERR=1 ;; esac
while IFS= read -r sf; do
  [ -z "$sf" ] && continue
  case "$sf" in backend|web|android|ios|cli|worker) ;; *) echo "CONFIG_ERROR: unknown surface '$sf' (allowed: backend, web, android, ios, cli, worker, none)"; ERR=1 ;; esac
done < <(split_list "$SURFACES")

# ---------- 3. Validate every path stays inside the project ----------
check_rel() {  # $1=key $2=value
  local v="$2"
  [ -z "$v" ] || [ "$v" = "none" ] && return 0
  case "$v" in
    /*|~*) echo "CONFIG_ERROR: $1 is absolute ('$v'); paths must be relative to the project root"; ERR=1 ;;
  esac
  case "/$v/" in
    */../*) echo "CONFIG_ERROR: $1 contains '..' ('$v'); it would escape the project root"; ERR=1 ;;
  esac
}
for k in docs_root features_root web_app web_components mobile_app mobile_components prototypes; do
  check_rel "$k" "$(get $k)"
done
while IFS= read -r p; do [ -n "$p" ] && check_rel public_docs "$p"; done < <(split_list "$(get public_docs)")
while IFS= read -r d; do [ -n "$d" ] && check_rel shared_deps "${d%@*}"; done < <(split_list "$(get shared_deps)")
[ "$ERR" -ne 0 ] && { echo "-> Fix SDLC.md (with the user's approval) before continuing."; exit 3; }

DOCS="$ROOT/$DOCS_REL"
FEAT="$ROOT/$FEAT_REL"
echo "DOCS_ROOT:     $DOCS"
echo "FEATURES_ROOT: $FEAT"
echo "TEMPLATES:     $(cd "$(dirname "$0")/.." && pwd -P)"
GIT_ROOT="$(git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null)"
[ -n "$GIT_ROOT" ] && GIT_ROOT="$(cd "$GIT_ROOT" && pwd -P)"
echo "GIT_ROOT:      ${GIT_ROOT:-<not a git repo>}"
if [ -n "$GIT_ROOT" ] && [ "$GIT_ROOT" != "$ROOT" ]; then
  echo "LAYOUT:        project inside a repo (monorepo); path in repo: ${ROOT#$GIT_ROOT/}"
  d="$(dirname "$ROOT")"
  while [ "${d#$GIT_ROOT}" != "$d" ]; do
    [ -f "$d/SDLC.md" ] && echo "CONFIG_ERROR: another SDLC.md exists above this project at ${d#$GIT_ROOT/}/ — nested projects are not supported; tell the user"
    [ "$d" = "$GIT_ROOT" ] && break
    d="$(dirname "$d")"
  done
fi
echo

# ---------- 4. Phase 0 status ----------
echo "--- Phase 0 (from SDLC.md) ---"
for k in product_vision tech_foundations test_strategy standards_enforcement ui_foundations platform_foundations release_process; do
  v="$(get $k)"
  if [ -z "$v" ]; then
    case "$k" in platform_foundations|release_process|test_strategy|standards_enforcement)
      if [ "$RIGOR" = "production" ]; then v="<MISSING — treat as pending (REQUIRED: rigor production)>"; else v="<MISSING — optional for rigor personal>"; fi ;;
    *) v="<MISSING — treat as pending>" ;; esac
  fi
  echo "$k: $v"
done
echo

# ---------- 5. Inventory of conventional documents ----------
echo "--- Foundation & product-wide documents ---"
show() { if [ -f "$2" ]; then echo "FOUND    $1: ${2#$ROOT/}"; else echo "MISSING  $1: ${2#$ROOT/}"; fi; }
if [ "$TYPE" = "shared" ]; then
  show "Shared Charter        " "$DOCS/product/shared_charter.md"
  show "Contract              " "$DOCS/contract.md"
else
  show "Product Vision        " "$DOCS/product/product_vision.md"
fi
show "Tech Standards        " "$DOCS/context/tech_standards.md"
if [ -f "$DOCS/context/tech_standards.md" ]; then
  if grep -qE '^##[[:space:]]+17\.?[[:space:]]+Enforcement Map' "$DOCS/context/tech_standards.md"; then
    rows=$(awk '/^##[[:space:]]+17\.?[[:space:]]+Enforcement Map/{f=1;next} /^##[[:space:]]/{f=0} f && /^\|/ && !/^\|[- |]+\|$/' "$DOCS/context/tech_standards.md" | tail -n +2 | wc -l | tr -d ' ')
    echo "         Enforcement Map (§17): $rows rule rows"
  else
    echo "         Enforcement Map (§17): MISSING (tech-lead Mode E)"
  fi
fi
show "HL Architecture       " "$DOCS/architecture/hl_architecture.md"
NSURF=$(split_list "$SURFACES" | grep -c . || true)
while IFS= read -r sf; do
  [ -z "$sf" ] && continue
  if [ -f "$DOCS/context/tech_standards/$sf.md" ]; then echo "FOUND    Tech Standards [$sf]: ${DOCS#$ROOT/}/context/tech_standards/$sf.md"
  elif [ "$RIGOR" = "production" ] || [ "$NSURF" -gt 1 ]; then echo "MISSING  Tech Standards [$sf]: ${DOCS#$ROOT/}/context/tech_standards/$sf.md (required)"
  fi
done < <(split_list "$SURFACES")
show "UI Standards          " "$DOCS/context/ui_standards.md"
show "UI Kit Registry       " "$DOCS/context/ui_kit_registry.md"
show "Master Functional Doc " "$DOCS/functional-spec.md"
show "Test Strategy         " "$DOCS/quality/test_strategy.md"
show "Platform Foundations  " "$DOCS/platform/platform_foundations.md"
show "Release Process       " "$DOCS/release/release_process.md"
if [ -d "$DOCS/platform/runbooks" ]; then echo "Runbooks: $(find "$DOCS/platform/runbooks" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"; fi
if [ -d "$DOCS/release/releases" ]; then
  echo "Releases:"; find "$DOCS/release/releases" -maxdepth 1 -type f -name '*.md' -exec basename {} .md \; | sort | tail -5 | sed 's/^/  /'
fi
if [ -d "$DOCS/architecture/adr" ]; then
  echo "ADRs: $(find "$DOCS/architecture/adr" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
fi
if [ -d "$DOCS/functional/domains" ]; then
  echo "Domain files:"; find "$DOCS/functional/domains" -maxdepth 1 -type f -name '*.md' -exec basename {} \; | sort | sed 's/^/  /'
fi
if [ -d "$DOCS/changelog" ]; then
  echo "Changelogs: $(find "$DOCS/changelog" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
fi
echo

echo "--- Features (by ID) ---"
if [ -d "$FEAT" ]; then
  IDS="$(find "$FEAT" -maxdepth 1 -type f -name '[0-9][0-9][0-9]_*.md' -exec basename {} \; | grep -oE '^[0-9]{3}' | sort -u)"
  if [ -z "$IDS" ]; then echo "(no features yet)"; fi
  for id in $IDS; do
    def="$(find "$FEAT" -maxdepth 1 -type f -name "${id}_*.md" ! -name '*_prd.md' ! -name '*_ux_flow.md' ! -name '*_test_plan.md' ! -name '*_impl_plan.md' -exec basename {} \; | head -1)"
    prd="-"; flow="-"; chg="-"; tp="-"; ip="-"
    ls "$FEAT"/"${id}"_*_prd.md >/dev/null 2>&1 && prd="PRD"
    ls "$FEAT"/"${id}"_*_ux_flow.md >/dev/null 2>&1 && flow="UXFLOW"
    if ls "$FEAT"/"${id}"_*_test_plan.md >/dev/null 2>&1; then
      tp="TESTPLAN"; grep -qiE '^>[[:space:]]*Status:[[:space:]]*Verified' "$FEAT"/"${id}"_*_test_plan.md 2>/dev/null && tp="VERIFIED"
    fi
    ls "$DOCS/changelog/${id}"_*_changelog.md >/dev/null 2>&1 && chg="DOCUMENTED"
    if ls "$FEAT"/"${id}"_*_impl_plan.md >/dev/null 2>&1; then
      ip="IMPL"; st="$(grep -m1 -oiE '^>[[:space:]]*Status:[[:space:]]*[A-Za-z ]+' "$FEAT"/"${id}"_*_impl_plan.md | sed -E 's/^>[[:space:]]*Status:[[:space:]]*//; s/[[:space:]]+$//')"
      [ -n "$st" ] && ip="IMPL:$st"
    fi
    echo "$id  ${def:-<no definition doc>}  [$prd] [$tp] [$flow] [$ip] [$chg]"
  done
else
  echo "(features root does not exist yet)"
fi
echo

# ---------- 5b. Shared dependencies (apps) / consumers (shared) ----------
breaking_since() {  # $1=changelog dir $2=since date (may be empty)
  [ -d "$1" ] || return 0
  for c in "$1"/*_changelog.md; do
    [ -f "$c" ] || continue
    grep -qiE '^>[[:space:]]*Breaking:[[:space:]]*yes' "$c" || continue
    dt="$(grep -m1 -oE 'Date applied:[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}' "$c" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')"
    if [ -z "$2" ] || [ -z "$dt" ] || [[ "$dt" > "$2" ]]; then
      echo "    BREAKING since review: $(basename "$c") (applied ${dt:-unknown date})"
    fi
  done
}
if [ "$TYPE" = "app" ]; then
  echo "--- Shared dependencies (read-only: public docs ONLY) ---"
  DEPS="$(split_list "$(get shared_deps)")"
  if [ -z "$DEPS" ]; then echo "(none declared)"; fi
  while IFS= read -r dep; do
    [ -z "$dep" ] && continue
    path="${dep%@*}"; since=""; [ "$path" != "$dep" ] && since="${dep##*@}"
    if [ -z "$GIT_ROOT" ]; then echo "DEP_ERROR: $path — project is not in a git repo, shared_deps can't be resolved"; continue; fi
    DD="$GIT_ROOT/$path"
    if [ ! -f "$DD/SDLC.md" ]; then echo "DEP_ERROR: $path — no SDLC.md there (not a project)"; continue; fi
    dtype="$(get_from "$DD/SDLC.md" type)"; did="$(get_from "$DD/SDLC.md" project_id)"
    [ "$dtype" != "shared" ] && { echo "DEP_ERROR: $path is type '${dtype:-app}', not 'shared' — apps never read other apps"; continue; }
    echo "DEP: $did ($path)   contract last reviewed: ${since:-never}"
    pubs="$(split_list "$(get_from "$DD/SDLC.md" public_docs)")"
    [ -z "$pubs" ] && echo "    WARN: it declares no public_docs; nothing may be read from it"
    while IFS= read -r p; do
      [ -z "$p" ] && continue
      if ! is_safe_rel "$p"; then echo "    DEP_ERROR: unsafe public_docs path '$p' — ignored"; continue; fi
      if [ -f "$DD/$p" ]; then echo "    READABLE: $DD/$p"; else echo "    MISSING:  $DD/$p"; fi
    done <<< "$pubs"
    ddocs="$(get_from "$DD/SDLC.md" docs_root)"; ddocs="${ddocs:-docs}"
    breaking_since "$DD/$ddocs/changelog" "$since"
  done <<< "$DEPS"
  echo
else
  echo "--- Consumers of this shared project ---"
  if [ -n "$GIT_ROOT" ]; then
    MYREL="${ROOT#$GIT_ROOT/}"; FOUNDC=0
    while IFS= read -r other; do
      [ "$other" = "$CFG" ] && continue
      deps="$(get_from "$other" shared_deps)"
      if split_list "$deps" | sed 's/@.*//' | grep -qx "$MYREL"; then
        echo "CONSUMER: $(get_from "$other" project_id) ($(dirname "${other#$GIT_ROOT/}"))"; FOUNDC=1
      fi
    done < <(find "$GIT_ROOT" -maxdepth 5 \( -name node_modules -o -name .git \) -prune -o -type f -name SDLC.md -print 2>/dev/null | sort)
    [ "$FOUNDC" -eq 0 ] && echo "(no project declares it in shared_deps yet)"
  else
    echo "(not in a git repo; consumers can't be resolved)"
  fi
  echo "Public docs:"
  pubs="$(split_list "$(get public_docs)")"
  [ -z "$pubs" ] && echo "  WARN: no public_docs declared; consumers can read nothing"
  while IFS= read -r p; do [ -n "$p" ] && { [ -f "$ROOT/$p" ] && echo "  FOUND    $p" || echo "  MISSING  $p"; }; done <<< "$pubs"
  echo
fi

# ---------- 6. Isolation check: project stamps ----------
echo "--- Isolation check (Project: stamps) ---"
MISMATCH=0
if [ -n "$PROJECT_ID" ]; then
  while IFS= read -r f; do
    stamp="$(grep -m1 -oE 'Project:[[:space:]]*`?[A-Za-z0-9._-]+' "$f" 2>/dev/null | sed -E 's/Project:[[:space:]]*`?//')"
    if [ -z "$stamp" ]; then
      echo "UNSTAMPED: ${f#$ROOT/}"
    elif [ "$stamp" != "$PROJECT_ID" ]; then
      echo "MISMATCH:  ${f#$ROOT/} says '$stamp', SDLC.md says '$PROJECT_ID' -> STOP and tell the user"
      MISMATCH=1
    fi
  done < <(
    { [ -d "$DOCS" ] && find "$DOCS" \( -name node_modules -o -name .git \) -prune -o -type f -name '*.md' -print
      [ -d "$FEAT" ] && find "$FEAT" -maxdepth 1 -type f -name '*.md' -print; } 2>/dev/null | sort -u
  )
fi
[ "$MISMATCH" -eq 0 ] && echo "No project_id mismatches."
echo

# ---------- 6a. Design tool ----------
echo "--- Design tool ---"
CD="$(get claude_design)"; CDS="$(get claude_design_system)"; CDSS="$(get claude_design_shared_system)"; CDSC="$(get claude_design_screens)"
echo "claude_design:        ${CD:-unknown (ux-designer asks once and records it)}"
echo "claude_design_shared_system: ${CDSS:-none}"
echo "claude_design_system: ${CDS:-none}"
echo "claude_design_screens: ${CDSC:-none (the first feature with UI creates \"<App> · Screens\" and records it)}"
echo

# ---------- 6a2. Work tracking ----------
echo "--- Work tracking ---"
WT="$(get work_tracker)"; WT="${WT:-none}"
echo "work_tracker:   $WT"
if [ "$WT" = "github" ]; then
  echo "github_repo:    $(get github_repo | sed 's/^$/origin/')"
  echo "external_epics: $(get external_epics | sed 's/^$/none/')"
  if command -v gh >/dev/null 2>&1; then
    if gh auth status >/dev/null 2>&1; then echo "gh:             available, authenticated"
    else echo "gh:             installed, NOT authenticated (ask the user to run: gh auth login)"; fi
  else
    echo "gh:             NOT available here: queue tracker operations in ${DOCS_REL}/work/pending_tracker_ops.md"
  fi
  PEND="$DOCS/work/pending_tracker_ops.md"
  if [ -f "$PEND" ]; then
    n=$(grep -cE '^[[:space:]]*-[[:space:]]' "$PEND" || true)
    [ "${n:-0}" -gt 0 ] && echo "PENDING tracker operations: $n (apply them first, with the user's approval)"
  fi
  DL="$(get decision_label)"; DL="${DL:-needs-decision}"
  echo "decision_label: $DL"
  echo "resume:         gh issue list --state open --label in-progress ; gh issue list --state open --label $DL"
fi
echo

# ---------- 6b. Subagents ----------
echo "--- Subagents (Claude Code) ---"
DECL="$(split_list "$(get subagents)")"
if [ -d "$ROOT/.claude/agents" ]; then
  while IFS= read -r a; do
    n="$(basename "$a" .md)"
    if echo "$DECL" | grep -qx "$n"; then echo "OK         $n"; else echo "UNDECLARED $n (exists in .claude/agents but not listed in SDLC.md)"; fi
  done < <(find "$ROOT/.claude/agents" -maxdepth 1 -type f -name '*.md' | sort)
fi
while IFS= read -r n; do
  [ -z "$n" ] && continue
  [ -f "$ROOT/.claude/agents/$n.md" ] || echo "MISSING    $n (listed in SDLC.md, no .claude/agents/$n.md)"
done <<< "$DECL"
[ -z "$DECL" ] && [ ! -d "$ROOT/.claude/agents" ] && echo "(none)"
if ! echo "$DECL" | grep -q -- '-pr-reviewer$' && [ ! -f "$ROOT/.claude/agents/${PROJECT_ID}-pr-reviewer.md" ]; then
  case "$(get standards_enforcement)" in
    approved*) echo "WARN: no ${PROJECT_ID}-pr-reviewer, but standards_enforcement is approved; it's mandatory (tech-lead Mode D step 0)" ;;
    *) echo "NOTE: ${PROJECT_ID}-pr-reviewer not created yet (mandatory; tech-lead creates it in Phase 0.2c)" ;;
  esac
fi
echo

# ---------- 7. Git (for merge checks) ----------
echo "--- Git ---"
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "repo: yes   current branch: $(git -C "$ROOT" branch --show-current 2>/dev/null)"
  git -C "$ROOT" rev-parse --verify --quiet "$BASE" >/dev/null && echo "base branch '$BASE': exists" || echo "base branch '$BASE': NOT FOUND locally"
else
  echo "repo: no (merge status can't be verified automatically; ask the user)"
fi
echo "== end =="
exit 0
