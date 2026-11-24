# food — field contract

Group-specific rules on top of the `personal-knowledge-base` standard (v2). Scaffolding (keys, ids, folder names, section headings) is English; content (titles, names, notes, labels) is Spanish.

| Domain | Type | Schema | Storage |
| --- | --- | --- | --- |
| recipes | collection | 5 | `recipes/items/NN-<category>/<id>.md` |
| ingredients | catalog | 2 | `ingredients/items.yaml` |
| pantry | state | 3 | `pantry/pantry.yaml` |
| reviews | state, per user | 1 | `reviews/<user>.yaml` |
| plan | state | 1 | `plan/plan.yaml` |

Shared vocabularies: `_system/units.yaml`, `_system/stores.yaml`.

## Who writes what

- The food-manager skill writes recipes, the ingredient catalog and every vocabulary.
- The user (through the app, Claude or Telegram) writes `curated` and `status` on recipes, the pantry, the plan and their own reviews file. Opinions (stars, comments, favorites) never live in the recipe.
- Every writer follows the optimistic write rule and sets `updated`.
- The user never maintains metadata by hand: `id`, `category`, `tags`, normalized ingredients, `health`, `missing` and `doubts` belong to the skill.

## recipes (schema 5)

Only `id`, `domain`, `created`, `updated` and `title` are required. Unknown values are left empty and declared in `missing`.

| Field | Writer | Rule |
| --- | --- | --- |
| id | skill | Slug of the Spanish title, immutable, equals filename |
| domain | skill | `recipes` |
| created / updated | skill, app | ISO timestamp with the profile timezone offset |
| title | skill | Spanish, with accents |
| category | skill | One id from `recipes/_system/categories.yaml`; drives the folder. Empty → `00-unclassified` |
| tags | skill | Map family → list of ids from `recipes/_system/tags.yaml` |
| servings | skill | `{ qty, unit }`, unit in `people`, `units`, `portions`, `g`, `ml` |
| time | skill | `{ prep, cook, rest }`, integer minutes; total is computed by the app |
| difficulty | skill | `easy`, `medium`, `hard` |
| ingredients | skill | List of ingredient lines (below) |
| source | skill | `{ type, url, author, original }`; type in `instagram`, `youtube`, `web`, `book`, `google-doc`, `own`, `family` |
| photo | skill | `food/recipes/_attachments/<id>.jpg` (path from the root) |
| curated | user | Boolean: the user has checked the recipe's data; when set to true the skill clears `doubts` |
| status | skill, user | `to-try`, `tried` or `discarded` (below). Absent = `tried` |
| health | skill | Healthiness indicator `{ score, base, cooking, estimated }` (section Healthiness). `score` 1–5 is computed by `scripts/health.py`, never by hand |
| missing | skill | Recomputed on every write; empty = complete. Values: `category`, `time`, `servings`, `quantities`, `ingredients`, `steps`, `tags`, `photo` |
| doubts | skill | Free text (Spanish) about interpretations it wasn't sure of |

`missing` rules: `quantities` when any line lacks `qty` and its unit is not `to-taste`, `pinch` or `as-needed`; `ingredients` when a step uses something not listed; `steps` when there are none or they are only a summary; `tags` when `cuisine` or `protein` is empty.

### Status

Whether the household has cooked the recipe and kept it. One value for the whole household, not per user; unrelated to `curated` (data checked) and to the stars in `reviews`.

- `to-try`: a new idea, not cooked yet. The skill writes it on every recipe it creates.
- `tried`: cooked and kept. Recipes without the field are `tried`, so the existing collection needs no migration. Giving a recipe a rating sets it to `tried` (from `to-try` or `discarded`).
- `discarded`: cooked or seen and not wanted. The file is kept (the app never deletes), clients hide it by default, and "borra la receta" means this status, not deleting the file.

The skill never changes the `status` of an existing recipe when it re-processes it.

### Ingredient line

`{ ing, qty, unit, note, group, optional, recipe }` — only `ing` is required.

- `ing`: key in `ingredients/items.yaml`. A new ingredient is added to the catalog before it is used.
- `qty`: number with decimal point. Omitted with `to-taste`, `as-needed`, and optionally `pinch`.
- `unit`: id from `_system/units.yaml`. Original units are kept, never converted.
- `note`: Spanish preparation detail ("picada", "en láminas").
- `group`: Spanish slug for multi-part recipes (`masa`, `relleno`, `para-servir`). No group = main.
- `optional: true` when the dish works without it.
- `recipe: <id>` when the ingredient is another recipe of the collection.

### Body

Fixed sections, in this order: `## Steps` (required, numbered), `## Notes`, `## Variations`. Empty ones are omitted except Steps. Section content is Spanish.

### Attachments

The skill adds photos: those the user sends through Claude, the video thumbnail for YouTube, and for Instagram the screenshot the user shared or a capture from Cowork's browser. If none is available, `photo` goes into `missing`.

## ingredients (schema 2)

`items.yaml` is a map: `<id>: { name, synonyms, family, staple, health, unit_g }`.

- `id`: Spanish (Spain) kebab-case, singular, the most specific form that matters when shopping (`pimiento-rojo` ≠ `pimiento-verde`; `tomate` = `tomates`).
- `name`: Spanish (Spain) display name. `synonyms`: other regional or language variants (`papa`, `choclo`, `crema de leche`, `potato`).
- Fresh meat names the concrete cut and the animal: id `<corte>-de-<animal>`, name `<corte> (<animal>)` (`espaldilla-de-ternera` → "espaldilla (ternera)", `pechuga-de-pollo` → "pechuga (pollo)"). No generic meat ingredients (`ternera`, `pollo`, `carne-picada`); if the source doesn't say the cut, pick the usual one for the dish and note it in `doubts`. Cured and processed meats (beicon, jamón, chorizo, morcilla) keep their product name.
- State goes in the recipe line's `note`, not in the id (`ajo` + `note: picado`), except products bought that way (`tomate-triturado`, `caldo-de-pollo`).
- `family`: id from `ingredients/_system/families.yaml`. Families with `food: false` are non-food (below); absent = food.
- **Non-food items** (household products tracked in the pantry: paper, cleaning, personal care): same catalog, with a `family` marked `food: false` in `families.yaml`. They are never used in recipe lines, never created from a recipe, never staples, and get a pantry entry like any other item. Names follow the same rules (Spanish (Spain), singular, the user's wording as a synonym). Clients show them only in Despensa and the shopping list, never in recipe editors or ingredient pickers.
- `health` (schema 2, food items only): `{ score, nova }`. `score` 1–5 is how healthy the ingredient is in itself; `nova` 1–4 is its processing level (NOVA: 1 unprocessed or minimally processed, 2 processed culinary ingredient, 3 processed food, 4 ultra-processed). Water and ice are `{ exclude: true }` (they don't count). Rubric in section Healthiness. Non-food items have no `health`.
- `unit_g` (optional): grams of one piece (`unit`) of the ingredient, so a line like "2 huevos" has a weight (`huevo: … unit_g: 55`). Set it for every ingredient that recipes count in pieces.
- `staple: true`: assumed always available; ignored by "what am I missing". Which ingredients are staples is the user's decision (default: only water, `agua`); record it in `recipes/preferences.md`.

## Healthiness

An indicator from 1 (least healthy) to 5 (healthiest) for each recipe, built from its ingredients, their quantities and how the dish is cooked. Clients show it on recipe cards, in the recipe detail and as a filter (1–5).

**Ingredient score** (`health.score`, judgment of the skill, set when the ingredient enters the catalog):

| Score | Typical ingredients |
| --- | --- |
| 5 | Vegetables, fruit, legumes, fish, whole grains, nuts and seeds, herbs and spices |
| 4 | Eggs, plain yogurt, poultry, extra virgin olive oil, whole-grain bread and pasta, tinned fish in water or olive oil |
| 3 | Refined grains (white rice, pasta, white flour, bread), red meat, milk, cheese, other vegetable oils, broth |
| 2 | Butter, cream, cured and processed meats (beicon, chorizo, jamón), salt, sauces and condiments with added sugar or fat, honey |
| 1 | Sugar and syrups, sweets, soft drinks, pastries and other ultra-processed sweets or snacks |

Processing caps the score: `nova: 4` (ultra-processed) → 2 at most; `nova: 3` → 4 at most.

**Recipe score** (`health` in the recipe, computed by `scripts/health.py`):
- **Base version only**: lines with `optional: true` don't count, and `## Variations` never counts. An alternative written in a line's `note` ("o jamón") doesn't count either: the line's `ing` does.
- Each counted line weighs its grams: `g`, `kg`, `ml`, `l` as is (1 ml = 1 g); `cup` 240, `tbsp` 15, `tsp` 5, `oz` 30, `clove` 5, `sprig` 2, `leaf` 1, `can` 400, `packet` 10, `bunch` 50; pieces (`unit`) × the ingredient's `unit_g`; `pinch` 1, `to-taste` 2, `as-needed` 10. A line without quantity counts 50 g, a piece without `unit_g` 100 g; both are listed in `health.estimated`.
- Ingredients scoring 1 or 2 weigh **double** (sugar, fats and processed meats matter more than their mass). `exclude` ingredients (water) don't count.
- A sub-recipe line (`recipe: <id>`) counts with that recipe's `base`, weighing its quantity if it is in a mass or volume unit, otherwise 150 g per portion.
- `base` = weighted mean of the counted scores (one decimal).
- `cooking`: the main cooking method of the dish, one of `raw`, `steam`, `boil` (+0.25), `stew`, `bake`, `grill`, `saute` (0), `fry` (−0.5, shallow frying), `deep-fry` (−1). Set by the skill from the steps; the method of the main component wins.
- `score` = `base` + the cooking modifier, rounded half up and kept within 1–5.

```yaml
health: { score: 4, base: 3.8, cooking: bake, estimated: [huevo] }
```

**Recalculation.** `health` is recomputed with `scripts/health.py <root> --write` whenever anything it depends on changes: an ingredient line of the recipe (ingredient, quantity, unit, `optional`, a sub-recipe), its cooking method, or an ingredient's `health` or `unit_g` in the catalog (every recipe that uses it, and the recipes that use those as sub-recipes). A change in `health` sets the recipe's `updated`. Nothing else in the recipe changes.

## pantry (schema 3)

`pantry.yaml`: `updated` and `items`, a map with one entry per non-staple ingredient of the catalog: `<ingredient-id>: { have, to_buy, stores }`. `have: true` = at home; `to_buy: true` = on the shopping list. Anything with `have: false` is considered missing; staples are never listed and always available. No quantities.

- `stores` (optional, schema 3): list of store ids from `_system/stores.yaml` ("centros de compra") where the user buys that ingredient. An item can have several. Absent or empty = no store assigned yet. The user writes it (app, Claude or Telegram: "el arroz lo compro en D1 y en Éxito"); order is irrelevant, no duplicates. Schema 2 files (no `stores`) are valid as they are; no migration.
- The app's Despensa filters by store: choosing a centro shows the items that list it (an item with two stores appears under both); with `to_buy: true` that is the shopping list for that store. A "Sin centro" filter shows items with no store.
- Adding a store: if the user names one that isn't in `stores.yaml`, add it there first (id = Spanish kebab-case slug of the name, `label` = the name as the user writes it), then reference it. Renaming only changes `label`; the id never changes. Removing a store from the vocabulary removes its id from every pantry item.

```yaml
arroz: { have: true, to_buy: false, stores: [exito, d1] }
```

- When an ingredient is added to the catalog (non-staple), add it here too with `{ have: false, to_buy: false }`.
- "compré X" → `have: true, to_buy: false`. "se acabó X" → `have: false`. "apunta X" → `to_buy: true`.

## reviews (schema 1)

One file per user, `reviews/<user>.yaml` (user ids from `_profile.yaml`). Only that user (through the app, Claude or Telegram) changes it.

```yaml
user: <user>
updated: 2026-10-28T09:00:00-05:00
favorites: [tortilla-de-patatas]
ratings:
  tortilla-de-patatas: { stars: 4, comment: "Mejor con cebolla", date: 2026-10-28 }
```

- `favorites`: recipe ids. `ratings`: recipe id → `stars` (integer 1–5, required), `comment` (Spanish, optional), `date` (`YYYY-MM-DD`, last change).
- Every id must exist in `recipes`. If a recipe is deleted, its entries are removed from every reviews file.

## plan (schema 1)

`plan.yaml`: what the household plans to eat. `updated` and `days`, a map `YYYY-MM-DD` → list of meals. A day can have any number of meals, including several of the same slot (two lunches: one at home and a tupper). Empty plan = `days: {}`.

```yaml
updated: 2026-11-01T10:00:00-05:00
days:
  2026-11-02:
    - slot: lunch
      label: En casa
      dishes:
        - { recipe: lentejas, servings: 2 }
        - { recipe: ensalada-de-manzana-verde-y-nueces, servings: 2 }
    - slot: lunch
      label: Tupper
      dishes:
        - { recipe: arroz-con-pollo-colombiano, servings: 1 }
    - slot: dinner
      dishes:
        - { out: eat-out }
```

| Slot | Label |
| --- | --- |
| breakfast | Desayuno |
| lunch | Comida |
| snack | Merienda |
| dinner | Cena |

- Meal: `{ slot, label, note, dishes }`. `slot` is required (one id from the table). `label` is an optional Spanish name that tells meals of the same slot apart ("En casa", "Tupper", "Con amigos"). `note` is optional Spanish. `dishes` is a non-empty list.
- Dish: `{ recipe, servings, note }`, `{ text, note }` or `{ out }`. `recipe` is an id that exists in `recipes`; `servings` (number) is how many people it's cooked for, defaulting to the recipe's servings; `text` is a free Spanish description for food without a recipe ("Sobras", "Fruta"); `note` is optional Spanish.
- `out`: the meal isn't cooked at home. Values: `eat-out` (Comer fuera) or `delivery` (Pedir a domicilio). An `out` dish has no other fields, adds no ingredients and is never a shopping candidate. A meal with `eat-out` has no other dishes. A meal with `delivery` can also have `recipe` or `text` dishes (pizza delivered plus a salad cooked at home), but only one `delivery` dish.
- A day's meals are kept in slot order (breakfast, lunch, snack, dinner); meals of the same slot keep the order they were added. Days without meals are omitted; days in date order.
- No cooking history: days before today may be removed by any writer.
- Shopping from the plan: the non-optional, non-staple ingredients of the planned recipes whose pantry entry has `have: false` are the candidates for `to_buy: true`; they're set only after the user confirms.
- If a recipe is deleted, its dishes are removed from the plan, and meals left with no dishes are removed too.
