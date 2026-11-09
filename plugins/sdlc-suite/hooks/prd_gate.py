#!/usr/bin/env python3
"""PreToolUse hook: no product code without an approved PRD.

Runs before Write / Edit / MultiEdit / NotebookEdit. If the target file is source
code inside an SDLC project (a folder with SDLC.md), it checks the gates that
engineering-lead and product-manager define (project_context_protocol.md §8):

  1. Phase 0: product_vision and tech_foundations approved (or waived / n/a).
  2. The current git branch names a feature id (<project_id>/<id>-<slug>).
  3. That feature's PRD (<features_root>/<id>_*_prd.md) has `> Status: Approved`.

Mode comes from `- code_gate:` in SDLC.md: enforce | warn | off.
Default: enforce when rigor is production, warn when personal.

Design rules:
  * Read-only. Never edits anything.
  * Fails OPEN: any unexpected error allows the edit (a broken hook must never
    brick the session). The error goes to stderr.
  * Outside an SDLC project, or for non-code files, it does nothing.
  * Stdlib only. Needs python3.

Known limit: it sees the file tools, not shell redirections (`echo > file.py`).
It is a guardrail against drift, not a security boundary.
"""
import json
import os
import re
import subprocess
import sys

CODE_EXT = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro",
    ".py", ".rb", ".php", ".go", ".rs", ".java", ".kt", ".kts", ".scala",
    ".swift", ".m", ".mm", ".dart", ".cs", ".c", ".cc", ".cpp", ".h", ".hpp",
    ".sql", ".sh", ".bash", ".zsh", ".lua", ".ex", ".exs", ".css", ".scss",
}
OK_STATE = re.compile(r"^(approved|waived|n/a)\b", re.I)


def out(decision, reason=None, context=None):
    spec = {"hookEventName": "PreToolUse"}
    if decision:  # None = only inject context, leave the normal permission flow alone
        spec["permissionDecision"] = decision
    if reason:
        spec["permissionDecisionReason"] = reason
    if context:
        spec["additionalContext"] = context
    print(json.dumps({"hookSpecificOutput": spec}))
    sys.exit(0)


def allow():
    sys.exit(0)


def find_project_root(start):
    d = start
    while True:
        if os.path.isfile(os.path.join(d, "SDLC.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def parse_config(path):
    cfg = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\s*-\s+([A-Za-z_][\w]*):\s*(.*)$", line)
            if not m or m.group(1) in cfg:
                continue
            val = re.split(r"\s+#", m.group(2), maxsplit=1)[0].strip()
            cfg[m.group(1)] = val
    return cfg


def current_branch(directory):
    d = directory
    while d and not os.path.isdir(d):
        d = os.path.dirname(d)
    try:
        r = subprocess.run(
            ["git", "-C", d, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=3,
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def is_code(file_path, root, cfg):
    rel = os.path.relpath(file_path, root).replace(os.sep, "/")
    if rel.startswith(".."):
        return False
    skip_roots = [cfg.get(k, "") for k in ("docs_root", "features_root", "prototypes")]
    skip_roots += [".claude", ".github", ".git"]
    for s in skip_roots:
        s = s.strip("/")
        if s and s != "none" and (rel == s or rel.startswith(s + "/")):
            return False
    return os.path.splitext(rel)[1].lower() in CODE_EXT


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        allow()

    tool_input = event.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not file_path:
        allow()
    file_path = os.path.abspath(file_path)

    root = find_project_root(os.path.dirname(file_path))
    if not root:
        allow()  # not an SDLC project

    cfg = parse_config(os.path.join(root, "SDLC.md"))
    rigor = cfg.get("rigor", "personal")
    mode = cfg.get("code_gate") or ("enforce" if rigor == "production" else "warn")
    if mode not in ("enforce", "warn"):
        allow()  # off, or unknown value
    if not is_code(file_path, root, cfg):
        allow()

    problems = []

    for key in ("product_vision", "tech_foundations"):
        if not OK_STATE.match(cfg.get(key, "pending")):
            problems.append(f"{key} is '{cfg.get(key, 'pending')}' in SDLC.md (needs approved, waived or n/a)")

    project_id = cfg.get("project_id", "")
    branch = current_branch(os.path.dirname(file_path))
    m = re.search(r"(?:^|/)(\d{3})[-_]", branch)
    feat_id = m.group(1) if m else None
    if not feat_id:
        problems.append(
            f"the current branch ('{branch or 'unknown'}') does not name a feature; "
            f"work on a branch like '{project_id}/<id>-<slug>' (id = 3 digits)"
        )
    else:
        features_root = os.path.join(root, cfg.get("features_root", "docs/features"))
        prd = None
        if os.path.isdir(features_root):
            for name in sorted(os.listdir(features_root)):
                if re.match(rf"^{feat_id}_.*_prd\.md$", name):
                    prd = os.path.join(features_root, name)
                    break
        if not prd:
            problems.append(f"feature {feat_id} has no PRD (<features_root>/{feat_id}_<slug>_prd.md)")
        else:
            with open(prd, encoding="utf-8") as f:
                head = f.read(6000)
            if not re.search(r"^>\s*Status:\s*Approved\b", head, re.I | re.M):
                problems.append(f"the PRD of feature {feat_id} ({os.path.basename(prd)}) is not 'Status: Approved'")

    if not problems:
        allow()

    listing = "; ".join(problems)
    howto = (
        "Run the owning SDLC skill to close the gap (product-manager for vision/PRD, "
        "tech-lead for tech foundations). Do not write product code around the gate. "
        "Only the user can waive it, by approving a recorded waiver in SDLC.md or "
        "setting '- code_gate: off'."
    )
    if mode == "enforce":
        out("deny", f"SDLC gate blocked this code edit in project '{project_id}': {listing}. {howto}")
    out(None, context=f"SDLC gate warning (project '{project_id}', code_gate: warn): {listing}. {howto} Tell the user before continuing.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # fail open
        print(f"prd_gate: ignored internal error: {e}", file=sys.stderr)
        sys.exit(0)
