---
name: personal-knowledge-base
description: "Storage conventions (v2) and setup of the user's personal knowledge base — a local folder (usually ~/knowledge-base) synced with Google Drive: root setup, the owner profile (_profile.yaml), group scaffolds, domain types (tracked, collection, catalog, state), folder layout, file naming, frontmatter, inboxes and routing, indexes, attachments, vocabularies, cross-domain links and date/format standards. ANY skill that persists, looks up, deduplicates, routes or tracks information across sessions (recipes, plans, training, health, movies, jobs, apartments or any new domain) MUST follow this skill before reading or writing the knowledge base. Use it when setting up a knowledge base for the first time (\"monta mi knowledge base\"), syncing it with Google Drive, creating a domain or group, adding or deduplicating an item, processing an inbox, recording preferences, or linking items across domains."
---

# Personal Knowledge Base — Storage Conventions (v2)

This skill is not a task by itself. It is the shared standard every domain skill (movie-scout, job-tracker, food-manager, inbox-router…) follows so the knowledge base stays consistent, human-browsable (Finder, Drive, Obsidian, any markdown viewer) and usable by apps.

Core principles:

- **The item file is the source of truth.** Anything derived (indexes, totals, flags computable from other fields) is either not stored or is an explicitly rebuildable cache.
- **Domains stay independent across groups.** Domains inside the same group may reference each other by id; relationships between groups live only in `_links/`.
- **Scaffolding in English, content in the user's language.** Folder names, file names of system files, frontmatter keys, enum/vocabulary ids and domain names are English. Content (titles, names, notes, recipe and ingredient names, display labels) is Spanish. Vocabulary files map English ids to Spanish labels.
- **No scripts, no database engine.** Markdown + YAML + JSON, kept consistent by following these rules.

## Root location and sync

The root is a local folder, `~/knowledge-base` by default; in Cowork it is the connected folder that contains `_domains.json` (with the device shell, usually `$HOME/mnt/knowledge-base`). Find it once per session and resolve every path against it.

It is synced with Google Drive by whatever `_profile.yaml` → `sync` says: Google Drive for desktop in mirror mode (Mac/Windows) or `rclone bisync` run by cron (Linux), in which case always run sync through `sync.command`, never `rclone bisync` directly. Local agents see real files; apps use the Drive API. Sync is not instant (seconds to ~5 minutes), which is why every writer follows the optimistic write rule. Setup and troubleshooting: `references/setup-and-sync.md`.

## Owner profile (`_profile.yaml`)

The only place where personal facts about the owner live: user id, name and how to address them, content language, timezone, home city and country, relevant countries, sync method and (optional) Telegram delivery. **Skills never hardcode any of this**; they read it from here. Template: `assets/profile-template.yaml`.

- `user` is the id for every per-user file (`<domain>/<user>.yaml`, `reviews/<user>.yaml`…). `household` lists other user ids that share per-user files in this base.
- `timezone` (IANA) gives the offset of every timestamp written (`America/Bogota` → `-05:00`; `Europe/Madrid` → `+01:00` or `+02:00` depending on the date).
- `telegram.enabled: false` (or missing) means no Telegram: notifications and confirmations stay in the session.
- Personal facts that belong to a domain (health conditions, training constraints, cities to search, preferences) live in that domain's files, never here and never in a skill.

## Root setup (first run)

When no root with `_domains.json` exists, or the user asks to set up their knowledge base:

1. Agree on the folder (default `~/knowledge-base`; in Cowork, ask the user to create and connect it first — ideally a folder inside Google Drive for desktop, see `references/setup-and-sync.md`).
2. Ask, in one short message: name and how to address them, user id (suggest the first name in kebab-case), timezone, home city and country, other relevant countries, and whether they want Telegram now (default no).
3. Write `_profile.yaml` from the template with those answers (`{{now}}` = current timestamp).
4. Run `python3 scripts/install_scaffold.py <root> assets/root` (paths relative to this skill): it creates `_domains.json`, `_inbox/` with its README and `_links/`, never overwriting.
5. Tell the user which group skills can be installed next (each one sets up its own group the first time it's used) and point them to the sync guide.

Without a shell, do the same by hand: the script only copies files and merges registry entries.

## Group scaffolds (each skill sets up its own group)

This standard knows nothing about any domain. Each domain skill ships its own scaffold in `assets/scaffold/` — `registry.json` (its `groups`/`domains` entries) and `files/` (schema, vocabularies, empty stores, inbox README, per-user templates with `{{user}}`) — and installs it the first time it's needed:

```
python3 <personal-knowledge-base>/scripts/install_scaffold.py <root> <skill>/assets/scaffold
```

The script needs `_profile.yaml`, fills `{{user}}`, `{{name}}`, `{{now}}`, `{{today}}`, registers what is missing, creates the storage of every domain type, and never overwrites a file or an existing registry entry; a name already used with another path is reported as a conflict and nothing is written for it. After installing, the skill asks only its group-specific setup questions (e.g. cities to search, training constraints) and writes the answers into its own files.

Once installed, **the group's `_system/schema.md` in the knowledge base is the contract**: the skill follows the user's copy (which may have evolved), not the scaffold.

## Folder layout

```
~/knowledge-base/
  _domains.json              registry of groups and domains
  _inbox/                    global inbox, handled by inbox-router
    processed/
  _links/                    relationships between domains of different groups
    <domain-a>-<domain-b>.json
  <domain>/                  a top-level domain (no group)
  <group>/                   a group of related domains
    _system/                 vocabularies shared by the group's domains
    _inbox/                  group inbox, handled by the group's skill
      processed/
    <domain>/
```

Inside every domain folder, depending on its type (see below):

```
<domain>/
  _system/        domain vocabularies, templates, schema notes (optional)
  _attachments/   binary files referenced by items (optional)
  items/          collection and tracked types
  items.yaml      catalog type
  <domain>.yaml   state type
  index.json      tracked type only
  preferences.md  optional for every type
```

- Names that start with `_` are system folders/files: never items, and ignored when listing items or processing an inbox.
- Domain and group names are English, lowercase kebab-case, and unique across the whole knowledge base (`recipes` can exist only once).

## Domain types

| Type | Storage | Index | `report_status` | Use for |
| --- | --- | --- | --- | --- |
| `tracked` | `items/<id>.md`, flat | `index.json` required | required | Things the user is notified about (movies, job offers, apartments) |
| `collection` | `items/<id>.md`, max. one subfolder level | none | not used | Things the user browses and uses (recipes) |
| `catalog` | single `items.yaml` keyed by id | none | not used | Small reference records shared by other domains (ingredients) |
| `state` | single `<domain>.yaml` document, or one `<user>.yaml` per user | none | not used | A living document the user edits (pantry, each user's reviews) |

- `collection` subfolders: one level only, named `NN-<id>` from a vocabulary in the domain's `_system/` (e.g. `items/05-mains/`). The frontmatter field that drives the folder is the truth; if folder and field disagree, move the file.
- `catalog`: when entries outgrow a single file (photos, long notes), migrate the domain to `collection`.
- `state`: one writer at a time; every writer uses the optimistic write rule (see below). A state domain registered with `"partition": "user"` keeps one file per user, `<domain>/<user>.yaml` (user ids are lowercase kebab-case; the owner's id is `_profile.yaml` → `user`); each file starts with `user` and `updated`, and only that user changes it.

## Domain registry (`_domains.json`)

```json
{
  "version": 2,
  "groups": {
    "food": {
      "purpose": "Recetas, ingredientes y despensa de casa.",
      "path": "food",
      "skill": "food-manager",
      "created": "2026-10-26T15:00:00-05:00"
    }
  },
  "domains": {
    "movies": {
      "purpose": "New movies in cinemas the user might want to see.",
      "type": "tracked",
      "path": "movies",
      "schema": 1,
      "created": "2026-08-10T09:00:00-05:00"
    },
    "recipes": {
      "purpose": "Recetas normalizadas que se consultan y cocinan en casa.",
      "type": "collection",
      "group": "food",
      "path": "food/recipes",
      "schema": 2,
      "created": "2026-10-26T15:00:00-05:00"
    }
  }
}
```

- `purpose` — one plain sentence (Spanish is fine; it's content).
- `type` — one of the four types. `group` — present only for grouped domains.
- `skill` — optional, on a group or a domain: the skill that owns its inbox and items. `inbox-router` hands inputs to it; a domain without its own `skill` inherits its group's.
- `path` — relative to the root. Always read paths from here; never guess them from folder names.
- `partition` — `state` domains only, optional: `"user"` for one file per user.
- `schema` — version of the domain's own field contract. When it changes, the domain skill migrates every file and bumps the number in the same step.
- Maintained only through this standard: a domain or group never exists on disk without its entry, and vice versa. Check the registry before creating anything new, to avoid near-duplicates.

### Migrating from v1

A v1 registry is a flat object of domains. Move every entry under `"domains"`, add `"type": "tracked"` (or `"collection"` for reference domains that were parked at `n/a`), `"path": "<name>"`, `"schema": 1`, and add `"version": 2` and `"groups": {}`. For former reference domains converted to `collection`, delete `index.json` and drop `report_status` from their items.

## Creating a group or domain

Only create one when a task actually needs to store something in it.

1. Read `_domains.json`; reuse anything close enough.
2. For a group: create `<group>/`, `<group>/_inbox/processed/`, and register it under `groups` (with `skill` if a skill owns it).
3. For a domain: create the folder at its `path` and the storage for its type (`items/`, `items.yaml` with `{}`, or `<domain>.yaml`); for `tracked`, also `index.json` with `{}`.
4. Optionally create `preferences.md` with a single line `# <domain> preferences`.
5. Register it under `domains` with `purpose`, `type`, `group` (if any), `path`, `schema: 1`, `created`.

## Item files (`items/<id>.md`)

### ID and filename rules

- ID = lowercase kebab-case slug of the item's natural name, without accents (`Tortilla de patatas` → `tortilla-de-patatas`). Content-derived, so in the content language.
- Unique within its domain, including across subfolders of a `collection`.
- Collision with a genuinely different item: `tracked` appends the creation date (`dune-part-three-2027-03-01`); `collection` appends `-2`, `-3`.
- The ID never changes once created, even if the title does. Filename = `<id>.md`.

### Core frontmatter

Every item starts with these fields; domain fields follow in the same block:

```yaml
---
id: <slug>
domain: <domain-name>
created: <ISO datetime>
updated: <ISO datetime>
report_status: pending   # tracked domains only
---
```

- `updated` is set by whoever writes the file (skill or app), every time.
- `report_status` (tracked only): `pending` (not yet surfaced), `notified` (user told), `archived` (was relevant, no longer). Keep files; archive instead of deleting. Reference-like domains use the `collection` type instead of a `n/a` status.
- Domain-specific status lives in its own field, never in `report_status`.

### Body

Markdown below the frontmatter. Free-form unless the domain's `_system/` defines fixed sections; fixed section headings are scaffolding, so in English (e.g. `## Steps`).

## Catalog files (`items.yaml`)

A YAML map keyed by id. Each entry holds only reference fields defined by the domain (no core frontmatter per entry). Other domains in the same group reference entries by key. Adding an entry always comes before referencing it.

## State files (`<domain>.yaml`)

A single YAML document with `updated` at the top plus the domain's fields. References to other domains in the group use their ids.

## Vocabularies (`_system/`)

- Closed lists (categories, tags, units, families…) live in YAML in the domain's `_system/`, or the group's `_system/` when several domains share them.
- Format: `<english-id>: { label: <Spanish label>, ...extra }`. Data stores ids; apps show and search labels.
- A new value is added to the vocabulary before it is used in any item.

## Attachments (`_attachments/`)

Binary files referenced by items: `<domain>/_attachments/<id>.<ext>`, then `<id>-2.<ext>`… Items reference them by path relative to the root. Deleting an item deletes its attachments.

## Inboxes and routing

- **Global `_inbox/`**: anything whose destination is unknown. The `inbox-router` skill reads each entry, decides which group or top-level domain it belongs to, and moves it unchanged to that group's (or domain's) `_inbox/`, then runs the destination's `skill` if registered. If it can't decide with confidence, it leaves the entry where it is and asks the user. The router never creates items.
- **Group or domain `_inbox/`**: the destination is already known. The owning skill (the registered `skill`, e.g. food-manager) processes each entry into items, then moves the original to `_inbox/processed/<YYYY-MM-DD>--<id>.<ext>`, linking it from the item when the domain has a `source.original` field.
- **External inbound sources** (e.g. the user's Telegram bot, configured in `_profile.yaml`): `inbox-router` reads them, writes each input as a file in `_inbox/` (or hands requests straight to the owning skill) and keeps a cursor in `_inbox/_<source>.yaml` (e.g. `_telegram.yaml` with `last_message_id`). Cursors are system files, never routed.
- Entries whose name starts with `_` (e.g. `_README.md`, cursors) are ignored.
- An entry that yields several items is moved once, named after the first item.

## Index files (`index.json`, tracked domains only)

Keyed by id, minimal entries: `report_status`, `created`, `updated`, `title`. It's a cache: write the item file first, then the index. If they disagree, trust the item and repair the index.

## Dedup workflow (before creating any item)

1. Compute the candidate slug.
2. `tracked`: look it up in `index.json`. `collection`: list `items/**` filenames. `catalog`: look up keys **and** synonyms/labels in `items.yaml`.
3. Not found → create. Found and it's the same thing → update instead of duplicating (and don't re-notify if already `notified` or `archived`). Found but genuinely different → use the collision rule.

## References and links

- **Within a group**: reference by id in a field (`ing: patata`, `recipe: sofrito`). The referenced item must exist.
- **Across groups**: only through `_links/<domain-a>-<domain-b>.json`, domains sorted alphabetically:

```json
[
  {
    "domain_a": "cinemas", "id_a": "cine-colombia-santafe",
    "domain_b": "movies",  "id_b": "dune-part-three",
    "relation": "showing_at",
    "showtimes": ["2026-09-12T19:30:00-05:00"],
    "updated": "2026-09-10T08:00:00-05:00"
  }
]
```

Relationship-specific data lives only in the link record. Never create empty or speculative links.

## Optimistic writes

Any writer of a file that more than one actor can edit (skill, app, user via Claude) re-reads the file, applies its change, and saves only if the file hasn't changed since it read it (compare `updated` or the Drive `modifiedTime`); otherwise it re-reads and retries.

## Date and format standards

- **Date only**: `YYYY-MM-DD`.
- **Timestamp**: ISO 8601 with the offset of `_profile.yaml` → `timezone` at that moment, `YYYY-MM-DDTHH:MM:SS±HH:MM` (examples in this skill use `-05:00`).
- **Booleans**: `true` / `false`. **Lists**: YAML arrays, never comma strings.
- **Numbers**: decimal point, no fractions (`0.5`, never `1/2`).
- **Enums and vocabulary ids**: English lowercase kebab-case.
- **Money**: two fields, `price_amount: 1200000` and `price_currency: COP` (ISO 4217).
- **IDs, domain and group names, filenames**: lowercase kebab-case.

## Preferences (`preferences.md`)

Free-form notes for an agent to read before acting in that domain. Update only on explicit, attributable user feedback; keep entries short and plain.

```markdown
# recipes preferences

- No le gusta el cilantro: proponer perejil como sustituto.
```

## Reading and querying

- **What exists / where** → `_domains.json` (`path`, `type`). Never scan folders to discover domains.
- **Does it exist / status** → the dedup workflow.
- **Pending across domains** → `tracked` domains only: filter each `index.json` by `report_status: pending`.
- **Filter by a domain field** → `tracked`: narrow with the index, then open items. `collection`: read items (apps keep their own in-memory index).
- **Group references** → resolve ids against the referenced domain's storage.
- **Cross-group relations** → `_links/`.
- **User taste** → `preferences.md`, read whole.

## Workflow summary for any domain skill

1. Find the root and read `_profile.yaml` and `_domains.json`; if the group isn't registered, install the skill's scaffold (see Group scaffolds).
2. Read the domain's `_system/` and `preferences.md`.
3. Run the dedup workflow.
4. Write the item (core + domain fields), adding catalog entries or vocabulary values first if needed.
5. `tracked`: update `index.json`.
6. Write `_links/` records for cross-group relationships.
7. If the input came from an inbox, move the original to `processed/`.
8. Update `preferences.md` only on explicit user feedback.

See `references/examples.md` for worked examples (a tracked pair and the food group).
