#!/usr/bin/env python3
"""Compute the healthiness indicator (`health`) of recipes from their ingredients.

    health.py <kb-root>                 report every recipe whose stored `health` is wrong
    health.py <kb-root> --write         recompute and write every recipe that changed
    health.py <kb-root> --write <file>  only that recipe (plus the recipes that use it)

The rules are the contract in food/_system/schema.md ("Healthiness"). In short:
- Base version only: lines with `optional: true` are left out; `## Variations` never counts.
- Each counted line weighs its estimated grams (units table below and the ingredient's
  `unit_g`); lines whose ingredient scores 1-2 weigh double, because sugar, fats and
  processed meats matter more than their mass. Ingredients with `health: { exclude: true }`
  (water, ice) don't count.
- A sub-recipe line (`recipe: <id>`) counts with that recipe's base score.
- base = weighted mean of the ingredient scores; score = round(base + cooking modifier),
  clamped to 1-5. The cooking method is set by the skill in `health.cooking`.
The script writes only the `health` block and `updated`, and never touches anything else.
Exit code 1 if a recipe can't be computed (ingredient without a health score, unknown
cooking method) or, without --write, if any stored value is out of date.
"""
import glob
import os
import re
import sys
from datetime import datetime

try:
    import yaml
except ImportError:
    sys.exit("PyYAML missing: pip install pyyaml")

# grams per unit (volume as water: 1 ml = 1 g)
UNIT_G = {"g": 1, "kg": 1000, "ml": 1, "l": 1000, "oz": 30, "cup": 240, "tbsp": 15, "tsp": 5,
          "clove": 5, "sprig": 2, "leaf": 1, "can": 400, "packet": 10, "bunch": 50}
UNMEASURED_G = {"pinch": 1, "to-taste": 2, "as-needed": 10}
PIECE_DEFAULT_G = 100   # `unit` of an ingredient without `unit_g`
NO_QTY_G = 50           # measurable line without qty (estimated)
SUBRECIPE_PORTION_G = 150
COOKING = {"raw": 0.25, "steam": 0.25, "boil": 0.25, "stew": 0, "bake": 0, "grill": 0,
           "saute": 0, "fry": -0.5, "deep-fry": -1}


def load(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def split(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, None, text
    return yaml.safe_load(m.group(1)) or {}, m.group(1), m.group(2)


def now_iso(root):
    tz = None
    pp = os.path.join(root, "_profile.yaml")
    if os.path.exists(pp):
        tz = (load(pp) or {}).get("timezone")
    try:
        from zoneinfo import ZoneInfo
        dt = datetime.now(ZoneInfo(tz)) if tz else datetime.now().astimezone()
    except Exception:
        dt = datetime.now().astimezone()
    return dt.replace(microsecond=0).isoformat()


def grams(line, ing):
    """(grams, estimated?) for one ingredient line."""
    unit, qty = line.get("unit"), line.get("qty")
    if unit in UNMEASURED_G:
        return UNMEASURED_G[unit] * (qty or 1), False
    if qty is None:
        return NO_QTY_G, True
    if unit in UNIT_G:
        return qty * UNIT_G[unit], False
    # piece ("unit" or none): grams per piece of this ingredient
    ug = (ing or {}).get("unit_g")
    if ug:
        return qty * ug, False
    return qty * PIECE_DEFAULT_G, True


class NoIngredients(Exception):
    """A recipe without countable ingredients has no health score yet (it is in `missing`)."""


def round_half_up(x):
    return int(x + 0.5)


class Calc:
    def __init__(self, root):
        food = os.path.join(root, "food")
        self.ings = load(os.path.join(food, "ingredients/items.yaml"))
        self.files = {os.path.basename(f)[:-3]: f for f in
                      glob.glob(os.path.join(food, "recipes/items/**/*.md"), recursive=True)}
        self.fm = {}
        self.cache = {}

    def front(self, rid):
        if rid not in self.fm:
            self.fm[rid] = split(self.files[rid])[0] or {}
        return self.fm[rid]

    def compute(self, rid, stack=()):
        """dict(score, base, cooking, estimated) or raises ValueError."""
        if rid in self.cache:
            return self.cache[rid]
        if rid in stack:
            raise ValueError(f"sub-recipe loop: {' -> '.join(stack + (rid,))}")
        fm = self.front(rid)
        cooking = ((fm.get("health") or {}).get("cooking"))
        if cooking is not None and cooking not in COOKING:
            raise ValueError(f"unknown health.cooking '{cooking}' (allowed: {', '.join(COOKING)})")
        tot_w = tot = 0.0
        estimated = []
        for ln in fm.get("ingredients") or []:
            if ln.get("optional"):
                continue
            if ln.get("recipe"):
                if ln["recipe"] not in self.files:
                    raise ValueError(f"sub-recipe '{ln['recipe']}' not found")
                sub = self.compute(ln["recipe"], stack + (rid,))
                score = sub["base"]
                if ln.get("qty") is not None and ln.get("unit") in UNIT_G:
                    g, est = ln["qty"] * UNIT_G[ln["unit"]], False
                else:
                    g, est = (ln.get("qty") or 1) * SUBRECIPE_PORTION_G, True
                name = ln["recipe"]
            else:
                ing = self.ings.get(ln.get("ing"))
                if ing is None:
                    raise ValueError(f"ingredient '{ln.get('ing')}' not in catalog")
                h = ing.get("health") or {}
                if h.get("exclude"):
                    continue
                if not isinstance(h.get("score"), int) or not 1 <= h["score"] <= 5:
                    raise ValueError(f"ingredient '{ln['ing']}' has no health score (1-5) in the catalog")
                score = h["score"]
                g, est = grams(ln, ing)
                name = ln["ing"]
            w = g * (2 if score <= 2 else 1)
            tot_w += w
            tot += w * score
            if est and name not in estimated:
                estimated.append(name)
        if tot_w == 0:
            raise NoIngredients()
        base = tot / tot_w
        score = min(5, max(1, round_half_up(base + COOKING.get(cooking, 0))))
        res = {"score": score, "base": round(base, 1), "cooking": cooking, "estimated": estimated}
        self.cache[rid] = res
        return res

    def users_of(self, rid):
        """Recipes that use rid as a sub-recipe, transitively."""
        out, todo = set(), [rid]
        while todo:
            cur = todo.pop()
            for other in self.files:
                if other in out:
                    continue
                if any(ln.get("recipe") == cur for ln in self.front(other).get("ingredients") or []):
                    out.add(other)
                    todo.append(other)
        return out


def block(res):
    lines = ["health:", f"  score: {res['score']}", f"  base: {res['base']}"]
    lines.append(f"  cooking: {res['cooking']}" if res["cooking"] else "  cooking:")
    if res["estimated"]:
        lines.append(f"  estimated: [{', '.join(res['estimated'])}]")
    return "\n".join(lines)


def same(stored, res):
    stored = stored or {}
    return (stored.get("score") == res["score"] and stored.get("base") == res["base"]
            and (stored.get("cooking") or None) == res["cooking"]
            and list(stored.get("estimated") or []) == res["estimated"])


def write(path, res, now):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    fm, rest = m.group(1), text[m.end():]
    new_block = block(res)
    hb = re.search(r"^health:.*?(?=^\S|\Z)", fm + "\n", re.S | re.M)
    if hb:
        fm = (fm + "\n")[:hb.start()] + new_block + "\n" + (fm + "\n")[hb.end():]
        fm = fm.rstrip("\n")
    elif re.search(r"^missing:", fm, re.M):
        fm = re.sub(r"^missing:", new_block + "\nmissing:", fm, count=1, flags=re.M)
    else:
        fm = fm + "\n" + new_block
    fm = re.sub(r"^updated:.*$", f"updated: {now}", fm, count=1, flags=re.M)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"---\n{fm}\n---\n{rest}")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    root = args[0]
    do_write = "--write" in args
    targets = [a for a in args[1:] if a != "--write"]
    calc = Calc(root)
    if targets:
        ids = set()
        for t in targets:
            rid = os.path.basename(t)[:-3]
            ids |= {rid} | calc.users_of(rid)
    else:
        ids = set(calc.files)
    now = now_iso(root)
    errors = stale = changed = 0
    for rid in sorted(ids):
        rel = os.path.relpath(calc.files[rid], root)
        try:
            res = calc.compute(rid)
        except NoIngredients:
            print(f"WARN {rel}: no countable ingredients yet; no health score")
            continue
        except ValueError as e:
            errors += 1
            print(f"ERROR {rel}: {e}")
            continue
        if res["cooking"] is None:
            print(f"WARN {rel}: health.cooking not set (no cooking modifier applied)")
        if same(calc.front(rid).get("health"), res):
            continue
        if do_write:
            write(calc.files[rid], res, now)
            changed += 1
            print(f"UPDATED {rel}: score {res['score']} (base {res['base']}, cooking {res['cooking']})")
        else:
            stale += 1
            print(f"STALE {rel}: health should be score {res['score']}, base {res['base']}")
    print(f"{len(ids)} recipe(s): {changed} updated, {stale} out of date, {errors} error(s)")
    sys.exit(1 if errors or stale else 0)


if __name__ == "__main__":
    main()
