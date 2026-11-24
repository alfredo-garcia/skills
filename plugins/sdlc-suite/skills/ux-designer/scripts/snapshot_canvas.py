#!/usr/bin/env python3
"""Copy the pages of a Claude Design canvas into the repo, as a reviewable snapshot.

    snapshot_canvas.py <downloaded> <out> --screens  --artifact <url> [--version <v>]
    snapshot_canvas.py <downloaded> <out> --proposal <id> --artifact <url> [--version <v>]

<downloaded>  folder with the canvas files as read from the artifact: project/canvas.json and
              project/*.dc.html (the folder that contains `project/`, or `project/` itself).
<out>         destination in the repo, replaced entirely:
              --screens   -> <docs_root>/design/screens/   (every page except "Propuesta …")
              --proposal  -> <features_root>/<id>_<slug>_design/   (only "Propuesta <id> · …")

Writes <out>/canvas.json (only the selected pages, their boards and notes, plus the design
systems), one <board>.dc.html per selected board, and <out>/design.json (artifact, version,
captured, pages). Leaves out the Claude Design runtime (artifact-type/) and the design
system copies (project/ds/): their source of truth is the code.
Compare two snapshots with `diff -r -x design.json <a> <b>`.
Read-only on <downloaded>. Exit 1 (and nothing written) if no page matches or a board file
of the selected pages wasn't downloaded.
"""
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

PROPOSAL = re.compile(r"^\s*Propuesta\s+(\d{3})\b", re.I)


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    src, out = a[0], a[1]
    opts = a[2:]

    def opt(name):
        return opts[opts.index(name) + 1] if name in opts and opts.index(name) + 1 < len(opts) else None

    proj = src if os.path.exists(os.path.join(src, "canvas.json")) else os.path.join(src, "project")
    cpath = os.path.join(proj, "canvas.json")
    if not os.path.exists(cpath):
        sys.exit(f"ERROR: no canvas.json in {src} (expected project/canvas.json)")
    canvas = json.load(open(cpath, encoding="utf-8"))
    pages = canvas.get("pages") or []

    if "--screens" in opts:
        keep = [p for p in pages if not PROPOSAL.match(p.get("name", ""))]
    elif "--proposal" in opts:
        fid = opt("--proposal")
        keep = [p for p in pages if (m := PROPOSAL.match(p.get("name", ""))) and m.group(1) == fid]
    else:
        sys.exit("ERROR: pass --screens or --proposal <id>")
    if not keep:
        sys.exit("ERROR: no page matches (screens = pages not named 'Propuesta …'; proposal = 'Propuesta <id> · …')")
    ids = {p["id"] for p in keep}

    boards = {k: v for k, v in (canvas.get("boards") or {}).items() if v.get("page") in ids}
    notes = {k: v for k, v in (canvas.get("notes") or {}).items() if v.get("page") in ids}
    snap = {
        "v": canvas.get("v"),
        "title": canvas.get("title"),
        "pages": keep,
        "boards": boards,
        "order": [b for b in canvas.get("order") or [] if b in boards],
        "notes": notes,
        "designSystems": [{k: d.get(k) for k in ("title", "namespace", "artifact")}
                          for d in canvas.get("designSystems") or []],
    }

    missing = [b for b in boards if not os.path.exists(os.path.join(proj, b))]
    if missing:
        for m in missing:
            print(f"ERROR board file not downloaded: project/{m}")
        sys.exit("Nothing written: read every listed board from the artifact and run again.")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    for name in boards:
        shutil.copyfile(os.path.join(proj, name), os.path.join(out, os.path.basename(name)))
    with open(os.path.join(out, "canvas.json"), "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=1)
        f.write("\n")
    meta = {
        "artifact": opt("--artifact"),
        "version": opt("--version"),
        "captured": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "pages": [p.get("name") for p in keep],
        "boards": len(boards),
    }
    with open(os.path.join(out, "design.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"SNAPSHOT {out}: {len(keep)} page(s), {len(boards)} board(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
