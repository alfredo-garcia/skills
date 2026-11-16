#!/usr/bin/env python3
"""Install a group's scaffold into a knowledge base, without overwriting anything.

Domain-blind: every domain skill ships its own scaffold and calls this script.

    python3 install_scaffold.py <kb-root> <scaffold-dir> [--user <id>] [--dry-run]

<scaffold-dir> contains:
    registry.json   {"groups": {...}, "domains": {...}} entries for _domains.json
                    (same shape as the registry; "created" is filled in here)
    files/          tree copied into <kb-root> as is

Placeholders replaced in file paths and file contents:
    {{user}}  user id (from --user or _profile.yaml `user`)
    {{name}}  display name (_profile.yaml `name`)
    {{now}}   ISO timestamp with the profile timezone offset
    {{today}} YYYY-MM-DD in the profile timezone

Rules:
    - Needs <kb-root>/_profile.yaml (root setup of personal-knowledge-base).
    - Creates _domains.json, _inbox/processed/ and _links/ if the root is new.
    - Existing files are never overwritten; existing registry entries are kept.
    - A domain or group name that already exists with another path is a conflict:
      reported, nothing written for it.
    - Missing storage for every registered domain of the scaffold is created
      (items/, index.json, items.yaml, <domain>.yaml or <user>.yaml) plus the
      group's _inbox/processed/.
Prints a JSON report.
"""
import json
import os
import re
import sys
from datetime import datetime

try:
    import yaml  # optional
except ImportError:  # pragma: no cover
    yaml = None


def read_profile(root):
    path = os.path.join(root, "_profile.yaml")
    if not os.path.exists(path):
        sys.exit("ERROR: no _profile.yaml in the root. Run the root setup of the "
                 "personal-knowledge-base skill first.")
    text = open(path, encoding="utf-8").read()
    if yaml:
        data = yaml.safe_load(text) or {}
    else:  # top-level scalars only
        data = {}
        for line in text.splitlines():
            m = re.match(r"^([a-z_]+):\s*(.*?)\s*(#.*)?$", line)
            if m and m.group(2):
                data[m.group(1)] = m.group(2).strip("\"'")
    return data


def now_in(tz_name):
    try:
        from zoneinfo import ZoneInfo
        dt = datetime.now(ZoneInfo(tz_name))
    except Exception:
        dt = datetime.now().astimezone()
    return dt.replace(microsecond=0)


def subst(s, ctx):
    for k, v in ctx.items():
        s = s.replace("{{" + k + "}}", v)
    return s


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    user = None
    if "--user" in args:
        i = args.index("--user")
        user = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    root, scaffold = (os.path.abspath(os.path.expanduser(a)) for a in args)

    profile = read_profile(root)
    user = user or str(profile.get("user") or "").strip()
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", user or ""):
        sys.exit("ERROR: _profile.yaml needs `user` as a lowercase kebab-case id.")
    now = now_in(str(profile.get("timezone") or ""))
    ctx = {
        "user": user,
        "name": str(profile.get("name") or user),
        "now": now.isoformat(),
        "today": now.date().isoformat(),
    }
    report = {"created": [], "kept": [], "registered": [], "conflicts": []}

    def mkdir(p):
        if not os.path.isdir(p):
            report["created"].append(os.path.relpath(p, root) + "/")
            if not dry:
                os.makedirs(p, exist_ok=True)

    def write_new(p, content):
        rel = os.path.relpath(p, root)
        if os.path.exists(p):
            report["kept"].append(rel)
            return
        report["created"].append(rel)
        if not dry:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(content)

    # Root
    reg_path = os.path.join(root, "_domains.json")
    if os.path.exists(reg_path):
        registry = json.load(open(reg_path, encoding="utf-8"))
    else:
        registry = {"version": 2, "groups": {}, "domains": {}}
        report["created"].append("_domains.json")
    registry.setdefault("groups", {})
    registry.setdefault("domains", {})
    mkdir(os.path.join(root, "_inbox", "processed"))
    mkdir(os.path.join(root, "_links"))

    # Registry merge
    scaf_reg = json.load(open(os.path.join(scaffold, "registry.json"), encoding="utf-8"))
    accepted = {"groups": [], "domains": []}
    for kind in ("groups", "domains"):
        for name, entry in (scaf_reg.get(kind) or {}).items():
            entry = json.loads(subst(json.dumps(entry, ensure_ascii=False), ctx))
            other = "domains" if kind == "groups" else "groups"
            if name in registry[other]:
                report["conflicts"].append(f"{name}: already used as a {other[:-1]}")
                continue
            cur = registry[kind].get(name)
            if cur is None:
                entry.setdefault("created", ctx["now"])
                registry[kind][name] = entry
                report["registered"].append(f"{kind[:-1]} {name}")
                accepted[kind].append(name)
            elif cur.get("path") != entry.get("path"):
                report["conflicts"].append(
                    f"{name}: registered with path {cur.get('path')!r}, scaffold wants {entry.get('path')!r}")
            else:
                accepted[kind].append(name)

    # Files
    files_dir = os.path.join(scaffold, "files")
    for dirpath, _dirs, files in os.walk(files_dir):
        for fn in files:
            src = os.path.join(dirpath, fn)
            rel = subst(os.path.relpath(src, files_dir), ctx)
            top = rel.split(os.sep)[0]
            blocked = [c.split(":")[0] for c in report["conflicts"]]
            if any(registry["groups"].get(b, {}).get("path", b).split("/")[0] == top for b in blocked):
                continue
            if fn == ".keep":
                mkdir(os.path.join(root, os.path.dirname(rel)))
                continue
            with open(src, encoding="utf-8") as fh:
                content = subst(fh.read(), ctx)
            write_new(os.path.join(root, rel), content)

    # Storage for every accepted group/domain
    for g in accepted["groups"]:
        mkdir(os.path.join(root, registry["groups"][g]["path"], "_inbox", "processed"))
    for d in accepted["domains"]:
        e = registry["domains"][d]
        base = os.path.join(root, e["path"])
        t = e.get("type")
        if t in ("collection", "tracked"):
            mkdir(os.path.join(base, "items"))
        if t == "tracked":
            write_new(os.path.join(base, "index.json"), "{}\n")
        if t == "catalog":
            write_new(os.path.join(base, "items.yaml"), "{}\n")
        if t == "state":
            fname = f"{user}.yaml" if e.get("partition") == "user" else f"{os.path.basename(e['path'])}.yaml"
            head = f"user: {user}\n" if e.get("partition") == "user" else ""
            write_new(os.path.join(base, fname), f"{head}updated: {ctx['now']}\n")
        if not e.get("group"):
            mkdir(os.path.join(base, "_inbox", "processed"))

    if not dry and report["registered"]:
        with open(reg_path, "w", encoding="utf-8") as fh:
            json.dump(registry, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    if dry:
        report["dry_run"] = True
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(1 if report["conflicts"] else 0)


if __name__ == "__main__":
    main()
