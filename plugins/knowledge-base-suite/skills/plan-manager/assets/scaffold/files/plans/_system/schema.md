# plans — field contract

Group-specific rules on top of the `personal-knowledge-base` standard (v2). Scaffolding (keys, ids, folder names, section headings) is English; content (titles, notes, labels) is Spanish.

| Domain | Type | Schema | Storage |
| --- | --- | --- | --- |
| ideas | tracked | 1 | `ideas/items/<id>.md` + `ideas/index.json` |
| trips | state | 1 | `trips/trips.yaml` |
| sources | catalog | 1 | `sources/items.yaml` |

Shared vocabularies in `_system/`: `types.yaml`, `categories.yaml`, `audiences.yaml`, `tags.yaml`, `cities.yaml`, `statuses.yaml`.

## Who writes what

- The group skill (or a scheduled search) creates items, maintains vocabularies, `sources` and `index.json`.
- The user (app, Claude or Telegram) changes `status`, `priority`, `scheduled`, `history`, `audience`, `tickets.state` and notes, and edits `trips`.
- Every writer follows the optimistic write rule and sets `updated`.

## ideas (schema 1)

One file per possible plan, whether it has a date or not. Required: `id`, `domain`, `created`, `updated`, `report_status`, `title`, `category`, `timing`, `city`, `status`. Everything else is filled when known.

### timing — the key distinction

- `dated`: has a date and expires (concert, movie in cinemas, play, fair). Uses `sessions` and/or `available_from` / `available_until`. One-off: once done it's finished.
- `timeless`: no date, never expires, repeatable (bowling, paintball, climbing gym, minigolf, a restaurant). No date fields. Each time it's done, a line is added to `history`.

### status (depends on timing)

Labels live in `_system/statuses.yaml`; apps, Telegram and chat show the label, files store the id.

| Status | Label | dated | timeless | Meaning |
| --- | --- | --- | --- | --- |
| proposed | Por revisar | ✓ | ✓ | Found by the weekly search, pending the user's review |
| wishlist | Siguiendo | ✓ | ✓ | The user is interested and wants to keep it in view; no commitment |
| scheduled | Confirmado | ✓ | ✓ | The user is going. `scheduled.start` holds the date; `null` = confirmed, date still to decide |
| done | Hecho | ✓ | — | Done; finished |
| repertoire | Para repetir | — | ✓ | Done at least once and worth repeating |
| discarded | Descartado | ✓ | ✓ | Not interested; `discard_reason` explains why (optional) |

### The user's three actions

The user controls their plans with three actions. **None deletes anything**: files are never removed, and every action can be undone by applying another one.

| Action | Sets status | Effects |
| --- | --- | --- |
| **Descartar** | `discarded` | `discard_reason` if the user gives one; `report_status: archived`. The weekly search never proposes it again (nor other editions of its `series` if the user says so) |
| **Seguir** | `wishlist` | `report_status: notified`; reminders apply (tickets on sale, last chance). Also used to bring back a discarded plan ("recupera X") |
| **Confirmar** | `scheduled` | `scheduled.start`: dated with a single session → that session; otherwise the date the user gives, or `null` if there is none yet (the digest will ask). `report_status: notified` |

- Allowed from any status (also `proposed`, `done`, `repertoire`). Un-confirming without discarding = **Seguir**.
- Bringing back a discarded plan clears `discard_reason` and sets `report_status: notified`.
- timeless: `scheduled` → after the date passes and the user confirms they went → `repertoire` + new `history` entry. Confirming it again sets `scheduled` again.
- dated: "expired" is never stored; it's computed (all sessions / `available_until` in the past and status not `done`). The skill then sets `report_status: archived`.
- Never computed and stored: last time done, times done (derive from `history`).

### report_status

- `pending`: created by the search and not yet in a weekly digest.
- `notified`: shown to the user in a digest, or added by the user.
- `archived`: discarded, expired, or done (dated). Files are never deleted.

### Fields

| Field | Rule |
| --- | --- |
| title | Spanish, with accents |
| category | One id from `_system/categories.yaml` |
| type | Never stored. Derived from `category` → `type` in `_system/categories.yaml` (ids and labels in `_system/types.yaml`) |
| timing | `dated` or `timeless` |
| audience | List of ids from `_system/audiences.yaml` (`solo`, `couple`, `friends`, `family`); several allowed. Who the plan suits, not who goes |
| tags | List of ids from `_system/tags.yaml` |
| status | See table; must be valid for `timing` |
| priority | `low`, `normal` (default), `high` |
| city | One id from `_system/cities.yaml` |
| place | `{ name, address, neighborhood, maps_url }` |
| sessions | dated only. List of `{ start, end, note }` ISO timestamps |
| available_from / available_until | dated only. Dates (`YYYY-MM-DD`) for windows: cartelera, exposición, temporada |
| series | dated only, optional. Slug shared by every edition of a recurring event (`feria-del-libro`); edition ids add the year (`feria-del-libro-2027`) |
| scheduled | `{ start, end }` when status is `scheduled` (dated: also kept after `done` as the record) |
| history | timeless only. List of `{ date, note }`, oldest first |
| tickets | `{ required, url, on_sale, state }`; state `none`, `to-buy`, `bought` |
| price_amount / price_currency | Price "from" (tickets, entry fee), e.g. `250000` / `COP` |
| price_level | 1–4, for restaurants and bars |
| links | List of `{ label, url }` |
| source | `{ type, url, found, original }`; type `search`, `telegram`, `chat`, `app`, `web`; original = processed inbox file |
| discard_reason | Short Spanish text when `discarded` |
| photo | `plans/ideas/_attachments/<id>.<ext>` |

Body: free Spanish notes.

### type — derived from category

Every category belongs to exactly one type (`food`, `culture`, `music`, `adventure`, `sport`, `home`, `other`; labels in `_system/types.yaml`). Apps, Telegram and chat filter and group plans by type by reading `categories.yaml`; the plan file only stores `category`.

- Never write `type` in a plan. Changing a plan's category changes its type.
- Every new category added to `categories.yaml` needs its `type`; if none fits, use `other` or add a type to `types.yaml` first.

### Example (dated)

```yaml
---
id: concierto-de-ejemplo
domain: ideas
created: 2026-11-06T19:00:00-05:00
updated: 2026-11-06T19:00:00-05:00
report_status: notified
title: Concierto de ejemplo
category: concert
timing: dated
audience: [couple, friends]
tags: [big-event, night]
status: wishlist
priority: high
city: ciudad-ejemplo
place: { name: Estadio de ejemplo, address: "", neighborhood: "", maps_url: "" }
sessions:
  - { start: 2027-02-20T20:00:00-05:00, end: null, note: "" }
tickets: { required: true, url: "https://…", on_sale: 2026-11-15T10:00:00-05:00, state: to-buy }
price_amount: 250000
price_currency: COP
source: { type: search, url: "https://…", found: 2026-11-06, original: null }
---
```

### Example (timeless)

```yaml
---
id: bolera-xyz
domain: ideas
created: 2026-09-01T10:00:00-05:00
updated: 2026-11-02T22:00:00-05:00
report_status: notified
title: Bolera XYZ
category: activity
timing: timeless
audience: [friends, family, couple]
tags: [rainy-day]
status: repertoire
city: ciudad-ejemplo
place: { name: Bolera XYZ, address: "", neighborhood: "", maps_url: "" }
history:
  - { date: 2026-09-14, note: "Promo 2x1 los martes" }
  - { date: 2026-11-02, note: "" }
---
```

### Digest map (`ideas/_digest.yaml`)

System file written by the weekly search after each Telegram digest, so the user can answer by number ("me interesa el 2, descarta el 4"):

```yaml
sent: 2026-11-12T17:45:00-05:00
message_ids: [1234]
items:
  1: concierto-de-ejemplo
  2: bolera-xyz
```

Overwritten on each digest; only the latest digest's numbers are valid.

## trips (schema 1)

`trips.yaml`: `updated` + `trips` list of `{ id, city, from, to, note }` (dates `YYYY-MM-DD`, city from `cities.yaml`). A `trip-only` city is searched only for dates inside a trip.

## sources (schema 1)

`items.yaml` keyed by id: `{ name, url, cities, categories, checked, note }`. `checked: false` = seeded but not yet verified by a search run.

## Weekly search rules

- Search windows come from each city's `scope` in `_system/cities.yaml`: `everyday` → next 3 weeks, every category, plus new openings; `big-only` → only `big-event`, up to 4 months ahead; `trip-only` → only for trip dates in `trips.yaml`, starting ~5 weeks before the trip. While the user is on a trip, `everyday` cities are searched only for dates after the return.
- Dedup against `index.json` and by `series`; never re-propose `discarded` items; read `ideas/preferences.md` and past `discard_reason` first.
- New items: `status: proposed`, `report_status: pending`; after the digest → `notified`.
