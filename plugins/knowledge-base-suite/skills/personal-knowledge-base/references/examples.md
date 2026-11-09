# Worked examples (v2)

## 1. Top-level domains: movies (tracked) + cinemas (collection)

```
~/knowledge-base/
  _domains.json
  _inbox/
  _links/
    cinemas-movies.json
  movies/
    items/dune-part-three.md
    index.json
    preferences.md
  cinemas/
    items/cine-colombia-santafe.md
```

`movies/items/dune-part-three.md`

```markdown
---
id: dune-part-three
domain: movies
created: 2026-08-10T09:00:00-05:00
updated: 2026-08-15T18:30:00-05:00
report_status: notified
title: Dune Part Three
genre: [sci-fi, thriller]
release_date: 2026-09-12
interested: yes
---

Tercera entrega. A Al le gustó el estilo de efectos prácticos de las dos primeras.
```

`movies/index.json`

```json
{
  "dune-part-three": {
    "report_status": "notified",
    "created": "2026-08-10T09:00:00-05:00",
    "updated": "2026-08-15T18:30:00-05:00",
    "title": "Dune Part Three"
  }
}
```

`cinemas/items/cine-colombia-santafe.md` — a `collection`, so no `report_status` and no index:

```markdown
---
id: cine-colombia-santafe
domain: cinemas
created: 2026-06-01T10:00:00-05:00
updated: 2026-06-01T10:00:00-05:00
title: Cine Colombia Santafé
neighborhood: Santa Fe
---
```

`movies` and `cinemas` are top-level domains (no shared group), so their relationship lives in `_links/cinemas-movies.json` (alphabetical order), never inline.

## 2. A group: food (recipes, ingredients, pantry)

```
~/knowledge-base/
  food/
    _system/
      schema.md          field contract for the group
      units.yaml         shared by recipes (and future domains)
    _inbox/
      processed/
    recipes/             collection
      _system/categories.yaml, tags.yaml, template.md
      _attachments/tortilla-de-patatas.jpg
      items/05-mains/tortilla-de-patatas.md
      preferences.md
    ingredients/         catalog
      _system/families.yaml
      items.yaml
    pantry/              state
      pantry.yaml
    reviews/             state, partition: user
      al.yaml
```

Inside the group, references are inline by id:

- a recipe line `{ ing: patata, qty: 800, unit: g }` → key `patata` in `food/ingredients/items.yaml`;
- `pantry.yaml` → `have: [patata, huevo]`, same keys;
- `reviews/al.yaml` → `favorites: [tortilla-de-patatas]` and `ratings.tortilla-de-patatas.stars: 4`, keyed by recipe id (opinions never live inside the recipe);
- a recipe line `{ ing: sofrito, recipe: sofrito }` → `food/recipes/items/**/sofrito.md`.

Routing: a screenshot dropped in `~/knowledge-base/_inbox/` is classified by `inbox-router` as a recipe and moved unchanged to `food/_inbox/`. The food-manager skill then writes the recipe, adds any new ingredient to the catalog first, and moves the screenshot to `food/_inbox/processed/2026-10-26--tortilla-de-patatas.jpg`.
