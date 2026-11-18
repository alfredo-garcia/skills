#!/usr/bin/env python3
"""Validate recipe, reviews and pantry files against the food contract.

Usage: check.py <knowledge-base-root> [recipe.md ...]
With no files, checks every recipe. Exit code 1 if any error.
"""
import sys, os, re, glob
try:
    import yaml
except ImportError:
    sys.exit("PyYAML missing: pip install pyyaml")

UNMEASURED = {"to-taste", "pinch", "as-needed"}
SERVING_UNITS = {"people", "units", "portions", "g", "ml"}
DIFFICULTY = {"easy", "medium", "hard"}
SOURCE_TYPES = {"instagram", "youtube", "web", "book", "google-doc", "own", "family"}
MISSING_VALUES = {"category", "time", "servings", "quantities", "ingredients", "steps", "tags", "photo"}
JUDGMENT = {"ingredients", "steps"}
REQUIRED = ["id", "domain", "created", "updated", "title"]
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

def load(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def split(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    food = os.path.join(root, "food")
    units = load(os.path.join(food, "_system/units.yaml"))
    cats = load(os.path.join(food, "recipes/_system/categories.yaml"))
    tags = load(os.path.join(food, "recipes/_system/tags.yaml"))
    ings = load(os.path.join(food, "ingredients/items.yaml"))
    fams = load(os.path.join(food, "ingredients/_system/families.yaml"))
    items_dir = os.path.join(food, "recipes/items")
    all_files = sorted(glob.glob(os.path.join(items_dir, "**/*.md"), recursive=True))
    files = sys.argv[2:] or all_files
    errors = 0

    def err(f, msg):
        nonlocal errors
        errors += 1
        print(f"ERROR {os.path.relpath(f, root)}: {msg}")

    nonfood = {k for k, v in fams.items() if (v or {}).get("food") is False}
    for k, v in ings.items():
        if v.get("family") not in fams:
            err(os.path.join(food, "ingredients/items.yaml"), f"ingredient '{k}' has unknown family '{v.get('family')}'")
        elif v.get("family") in nonfood and v.get("staple"):
            err(os.path.join(food, "ingredients/items.yaml"), f"non-food item '{k}' can't be a staple")

    ids = {}
    for f in all_files:
        ids.setdefault(os.path.basename(f)[:-3], []).append(f)
    for i, fs in ids.items():
        if len(fs) > 1:
            err(fs[0], f"duplicate id '{i}' in {[os.path.relpath(x, root) for x in fs]}")

    for f in files:
        fm, body = split(f)
        if fm is None:
            err(f, "no YAML frontmatter"); continue
        for k in REQUIRED:
            if not fm.get(k):
                err(f, f"required field '{k}' empty")
        if fm.get("domain") != "recipes":
            err(f, "domain must be 'recipes'")
        if fm.get("id") and os.path.basename(f) != f"{fm['id']}.md":
            err(f, "filename must be <id>.md")
        for k in ("created", "updated"):
            if fm.get(k) and not TS.match(str(fm[k]).replace(" ", "T")):
                err(f, f"'{k}' must be YYYY-MM-DDTHH:MM:SS±HH:MM (offset of the profile timezone)")
        cat = fm.get("category") or "unclassified"
        if cat not in cats:
            err(f, f"unknown category '{cat}'")
        elif os.path.basename(os.path.dirname(f)) != cats[cat]["folder"]:
            err(f, f"must live in items/{cats[cat]['folder']}/")
        t = fm.get("tags") or {}
        for fam, vals in t.items():
            if fam not in tags:
                err(f, f"unknown tag family '{fam}'"); continue
            for v in vals or []:
                if v not in tags[fam]["values"]:
                    err(f, f"unknown tag '{fam}: {v}'")
        sv = fm.get("servings") or {}
        if sv.get("unit") and sv["unit"] not in SERVING_UNITS:
            err(f, f"servings.unit must be one of {sorted(SERVING_UNITS)}")
        if fm.get("difficulty") and fm["difficulty"] not in DIFFICULTY:
            err(f, "difficulty must be easy/medium/hard")
        src = fm.get("source") or {}
        if src.get("type") and src["type"] not in SOURCE_TYPES:
            err(f, f"source.type must be one of {sorted(SOURCE_TYPES)}")
        for gone in ("rating", "favorite", "reviewed"):
            if gone in fm:
                err(f, f"'{gone}' no longer belongs in recipes (opinions live in food/reviews/<user>.yaml; 'reviewed' is now 'curated')")
        if "curated" in fm and not isinstance(fm["curated"], bool):
            err(f, "curated must be true or false")
        if fm.get("photo") and not os.path.exists(os.path.join(root, fm["photo"])):
            err(f, f"photo not found: {fm['photo']}")
        lines = fm.get("ingredients") or []
        for ln in lines:
            if ln.get("ing") not in ings:
                err(f, f"ingredient '{ln.get('ing')}' not in catalog")
            elif ings[ln["ing"]].get("family") in nonfood:
                err(f, f"'{ln['ing']}' is a non-food item; it can't be a recipe ingredient")
            if ln.get("unit") and ln["unit"] not in units:
                err(f, f"unit '{ln['unit']}' not in units.yaml")
            if ln.get("recipe") and ln["recipe"] not in ids:
                err(f, f"sub-recipe '{ln['recipe']}' not found")

        # expected `missing`
        exp = set()
        if cat == "unclassified": exp.add("category")
        tm = fm.get("time") or {}
        if tm.get("prep") is None and tm.get("cook") is None: exp.add("time")
        if not sv.get("qty"): exp.add("servings")
        if any(ln.get("qty") is None and ln.get("unit") not in UNMEASURED for ln in lines): exp.add("quantities")
        if not lines: exp.add("ingredients")
        steps = re.search(r"^## Steps\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
        if not steps or not re.search(r"^\s*1\.\s+\S", steps.group(1), re.M): exp.add("steps")
        if not t.get("cuisine") or not t.get("protein"): exp.add("tags")
        if not fm.get("photo"): exp.add("photo")
        stored = set(fm.get("missing") or [])
        bad = stored - MISSING_VALUES
        if bad:
            err(f, f"invalid values in missing: {sorted(bad)}")
        if exp - stored or (stored - exp - JUDGMENT):
            err(f, f"missing should be {sorted(exp | (stored & JUDGMENT))}, found {sorted(stored)}")
        if fm.get("curated") and fm.get("doubts"):
            err(f, "curated recipes must have empty doubts")

    # reviews files (one per user)
    for rf in sorted(glob.glob(os.path.join(food, "reviews", "*.yaml"))):
        rv = load(rf)
        user = os.path.basename(rf)[:-5]
        if rv.get("user") != user:
            err(rf, f"'user' must be '{user}' (the filename)")
        for rid in rv.get("favorites") or []:
            if rid not in ids:
                err(rf, f"favorite '{rid}' is not a recipe")
        for rid, r in (rv.get("ratings") or {}).items():
            if rid not in ids:
                err(rf, f"rating for unknown recipe '{rid}'")
            st = (r or {}).get("stars")
            if not isinstance(st, int) or not 1 <= st <= 5:
                err(rf, f"'{rid}': stars must be an integer 1-5")

    # pantry (schema 3): items.<ing>: { have, to_buy, stores }
    pp = os.path.join(food, "pantry", "pantry.yaml")
    if os.path.exists(pp):
        pantry = load(pp)
        sp = os.path.join(food, "_system", "stores.yaml")
        stores = (load(sp) if os.path.exists(sp) else {}) or {}
        for sid, sv in stores.items():
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(sid)):
                err(sp, f"store id '{sid}' must be kebab-case")
            if not (sv or {}).get("label"):
                err(sp, f"store '{sid}' needs a label")
        for k in pantry:
            if k not in ("updated", "items"):
                print(f"WARN food/pantry/pantry.yaml: top-level '{k}' is not in the contract (only 'updated' and 'items')")
        items = pantry.get("items") or {}
        for ing, e in items.items():
            if ing not in ings:
                err(pp, f"'{ing}' is not in the ingredient catalog")
            elif ings[ing].get("staple"):
                err(pp, f"'{ing}' is a staple; staples are never listed")
            e = e or {}
            for b in ("have", "to_buy"):
                if not isinstance(e.get(b), bool):
                    err(pp, f"'{ing}': {b} must be true or false")
            st = e.get("stores")
            if st is None:
                continue
            if not isinstance(st, list):
                err(pp, f"'{ing}': stores must be a list of store ids"); continue
            if len(st) != len(set(st)):
                err(pp, f"'{ing}': duplicate store in {st}")
            for sid in st:
                if sid not in stores:
                    err(pp, f"'{ing}': store '{sid}' not in food/_system/stores.yaml")
        for ing, v in ings.items():
            if not v.get("staple") and ing not in items:
                print(f"WARN food/pantry/pantry.yaml: catalog ingredient '{ing}' has no pantry entry")

    print("OK" if errors == 0 else f"{errors} error(s)")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
