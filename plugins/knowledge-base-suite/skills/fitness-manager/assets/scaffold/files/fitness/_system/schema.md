# fitness — field contract

Group-specific rules on top of the `personal-knowledge-base` standard (v2). Scaffolding (keys, ids, folder names, section headings) is English; content (titles, notes, labels) is Spanish.

| Domain | Type | Schema | Storage |
| --- | --- | --- | --- |
| exercises | collection | 1 | `exercises/items/NN-<region>/<id>.md` |
| routines | collection | 3 | `routines/items/NN-<category>/<id>.md` |
| program | state, per user | 1 | `program/<user>.yaml` |
| sessions | state, per user | 2 | `sessions/<user>.yaml` |

Shared vocabularies in `_system/`: `regions`, `zones`, `muscles`, `goals`, `patterns`, `positions`, `equipment`, `resistances`, `stresses`, `levels`.

## The model in one paragraph

`exercises` is the library: what each exercise is, what it works and what it loads. `routines` are the user's sessions: which exercises, in what order and with **their** dose (sets, reps, seconds, variant, band). `program` says which routine goes on which weekday, the current phase, the constraints (what to avoid) and the journal of their physical evolution. `sessions` is the log of what they actually did each day and how they felt. The library never holds personal dose; the routine never holds execution history.

## Classification

Every exercise is classified on independent axes, so any focused plan is a filter:

| Axis | Field | Vocabulary | Example question |
| --- | --- | --- | --- |
| Body region (folder) | `region` | `regions.yaml` | "plan de tren inferior" |
| Zone | `zones` | `zones.yaml` (each zone → region) | "algo de glúteo", "brazo" |
| Muscles | `muscles.primary` / `secondary` | `muscles.yaml` (each muscle → zone) | "¿qué trabaja el oblicuo?" |
| Training type | `goals` | `goals.yaml` | "plan de fuerza", "cardio" |
| Movement pattern | `pattern` | `patterns.yaml` | balance push/pull in a plan |
| Position | `position` | `positions.yaml` | "todo tumbado" |
| Equipment | `equipment` | `equipment.yaml` | "sin banda hoy" |
| Loads to watch | `stresses` | `stresses.yaml` | filter against `program.constraints` |
| Difficulty | `level` | `levels.yaml` | progressions |

`zones` must include the zone of every primary muscle; region is the main one (an exercise working several regions picks where the main effort is; cardio, swimming, warm-ups and recovery are `full-body`).

## Who writes what

- The `fitness-manager` skill writes exercises, routines, vocabularies and the program; it adapts routines when the user reports their evolution and records why in the routine's `## History` and in `program.journal`.
- The user (through an app, Claude or Telegram) writes sessions and can change doses in routines.
- Every writer follows the optimistic write rule and sets `updated`.

## exercises (schema 1)

Required: `id`, `domain`, `created`, `updated`, `title`, `region`, `goals`, `measure`.

| Field | Rule |
| --- | --- |
| id | Slug of the Spanish name, generic (variants live in `variants`, not in new ids) |
| title / aliases | Spanish display name; other names (English, the name an app or fisio uses) |
| region | One id from `regions.yaml`; drives the folder |
| zones | List of `zones.yaml` ids |
| muscles | `{ primary: [], secondary: [] }`, ids from `muscles.yaml` |
| goals | List of `goals.yaml` ids |
| pattern / position / level | One id each from their vocabulary |
| equipment | List of `equipment.yaml` ids needed by the base form |
| laterality | `bilateral`; `each-side`: one set covers both sides back to back (right, then left) and counts as one set — reps or seconds are per side; `alternating`: sides alternate rep by rep within the set (target = reps × 2). Either way it is **one exercise**, never one entry per side |
| measure | `reps`, `time` (isometric seconds per set) or `duration` (continuous minutes: cardio, warm-up, sauna) |
| stresses | `stresses.yaml` ids the exercise puts load on; empty = none of concern |
| default_dose | Generic recommendation: `{ sets, reps, time, hold, duration_min }` (only the relevant keys) |
| range | Recommended range for progression, `{ <key>: [min, max] }` |
| variants | Map `<slug>: { label, level, equipment }` — easier/harder forms (pared → rodillas → completas) |
| figure | Optional stick-figure drawing `{ start, end }`, each `{ head: [x, y], base: [polyline], move: [], band: [] }` in a 170×90 viewBox: base gray, move orange, band dashed green |
| source | `{ type, url, author, original }`; type in `own`, `physio`, `app`, `web`, `youtube`, `instagram`, `book` |
| missing / doubts | As in food: what's unknown (`steps`, `muscles`, `figure`…) and uncertain interpretations |

Body sections, in this order: `## Execution` (required), `## Common mistakes`, `## Progression`, `## Notes`.

## routines (schema 3)

A routine is one session template. Required: core fields, `title`, `category`, `user`, `status`, `blocks`.

| Field | Rule |
| --- | --- |
| aliases | Other names the user uses for it |
| category | One id from `routines/_system/categories.yaml` (e.g. `strength`, `cardio`, `mobility`, `mixed`, `express`); drives the folder |
| days | Weekdays the routine is for: list of `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`. Empty = no fixed day (express, archived). The source of truth for the weekly plan |
| user | Owner (user id) |
| status | `active`, `paused`, `draft`, `archived` (never delete: archive) |
| goals / regions | Focus of the routine (ids), for "dame mi rutina de fuerza" |
| duration_min | Approximate length |
| time_of_day | Free Spanish note |
| rest | Default seconds between sets |
| blocks | Ordered list `{ id, label, note, duration_min, range, items }`; `id` is a kebab-case English slug (`warm-up`, `main`, `strength`, `cardio`, `recovery`) |

Block item (the personal dose): `{ ex, sets, reps, time, hold, duration_min, rest, variant, resistance, range, note }` — only `ex` is required; `ex` exists in `exercises`; `variant` is a key of that exercise's `variants`; `resistance` from `resistances.yaml`; `rest` overrides the routine's; `range` is the ceiling before changing variant or band. Items of a block with its own `duration_min` share that time.

Body: `## Guidelines`, `## Progression`, `## History` (dated lines: every change of dose, variant or exercise, and why).

A new routine (e.g. "fuerza de pierna", "cardio suave") is built by filtering exercises by region/zone/goal and **excluding any exercise whose `stresses` intersect `program.constraints.avoid_stresses`**.

## program (schema 1)

`program/<user>.yaml`, only that user's file.

- `phase`: `{ label, since, goal }` — current training phase.
- `constraints`: `avoid_stresses` (ids), `avoid_text` (Spanish list), `rules` (Spanish list: progression and safety rules), `pain_watch` (list `{ id, label }`: body areas whose pain is scored in every session, e.g. `leg`, `back`), `red_flags` (`{ urgent, soon }`, Spanish lists: symptoms that stop training — `urgent` = seek care today, `soon` = see a professional soon). Constraints come from the user, their physio or doctor, or the `health` group; only the user lifts one.
- `schedule`: `sessions_per_week` (`[min, max]`), `week` (`mon`…`sun` → list of routine ids; a day can be empty `[]`), `note`. `week` is a cache rebuilt from the `days` of active routines: whoever changes a routine's `days` updates `week` in the same step; if they disagree, the routines win.
- `journal`: dated list `{ date, type, text, routine, metrics }`. `type`: `checkin` (how they feel, pain, energy), `adjustment` (routine changed), `milestone` (achievement), `measurement` (`metrics` map, e.g. `{ weight_kg: 80 }`), `setback` (worse, back to a previous level). Newest last.

## sessions (schema 2)

`sessions/<user>.yaml`: `user`, `updated`, `sessions` (list, date order).

Session: `{ date, start, routine, status, duration_min, exercises, feel, next_day, note }`. For an `each-side` exercise, each value in `reps`/`time` is one set and applies to both sides.

- `routine`: id, or empty for a free session. `status`: `completed`, `partial`, `skipped`.
- `exercises`: what was actually done. When the user just says "hice la rutina", the writer expands the routine's current doses into this list, so history stays true when the routine changes. Entry: `{ ex, variant, resistance, sets, reps: [per set], time: [per set], hold, duration_min, skipped, note }`.
- `feel`: `{ effort, pain }`: `effort` integer 0–10 (RPE); `pain` map `<pain_watch id>` → integer 0–10 (`{ leg: 2, back: 1 }`). Optional.
- `next_day`: `better`, `same` or `worse` — the 24-hour check that decides whether to progress. Filled the day after.
- Archive: at the start of a year, sessions of the previous year move to `sessions/_archive/<user>-<YYYY>.yaml` with the same shape.
