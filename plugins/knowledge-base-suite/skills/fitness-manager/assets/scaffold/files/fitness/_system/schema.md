# fitness — field contract

Group-specific rules on top of the `personal-knowledge-base` standard (v2). Scaffolding (keys, ids, folder names, section headings) is English; content (titles, notes, labels) is Spanish.

| Domain | Type | Schema | Storage |
| --- | --- | --- | --- |
| exercises | collection | 1 | `exercises/items/NN-<region>/<id>.md` |
| subroutines | collection | 1 | `subroutines/items/NN-<category>/<id>.md` |
| routines | collection | 4 | `routines/items/NN-<category>/<id>.md` |
| program | state, per user | 1 | `program/<user>.yaml` |
| sessions | state, per user | 3 | `sessions/<user>.yaml` |

Shared vocabularies in `_system/`: `regions`, `zones`, `muscles`, `goals`, `patterns`, `positions`, `equipment`, `resistances`, `stresses`, `levels`.

## The model in one paragraph

`exercises` is the library: what each exercise is, what it works and what it loads. `subroutines` are groups of exercises with one purpose (estabilidad, fuerza de empuje y pierna, cardio por intervalos…): which exercises, in what order and with **their** dose (sets, reps, seconds, variant, band). `routines` are the user's sessions: which sub-routines, in what order, on which weekdays. `program` holds the current phase, the constraints (what to avoid), the weekly targets and the journal of their physical evolution; the weekly plan is the `days` of the active routines. `sessions` is the log of what they actually did each day and how they felt. The library never holds personal dose; the dose lives only in the sub-routine (a different dose is a different sub-routine); no one holds execution history but `sessions`.

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

- The `fitness-manager` skill writes exercises, sub-routines, routines, vocabularies and the program; it adapts doses in sub-routines when the user reports their evolution and records why in the sub-routine's `## History` and in `program.journal`.
- The user (through an app, Claude or Telegram) writes sessions and can change doses in sub-routines.
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

## subroutines (schema 1)

A sub-routine is a group of exercises with one purpose, with the user's dose. It can be done on its own (a free session) or as part of a routine. Required: core fields, `title`, `category`, `user`, `status`, `blocks`.

| Field | Rule |
| --- | --- |
| aliases | Other names the user uses for it |
| category | One id from `subroutines/_system/categories.yaml` (e.g. `stability`, `strength`, `cardio`, `mobility`, `recovery`, `express`); drives the folder |
| user | Owner (user id) |
| status | `active`, `draft`, `archived` (never delete: archive) |
| goals / regions | Focus (ids), for "dame algo de fuerza" |
| duration_min | Approximate length |
| rest | Default seconds between sets |
| blocks | Ordered list `{ id, label, note, duration_min, range, items }`; `id` is a kebab-case English slug (`warm-up`, `main`, `strength`, `cardio`, `recovery`) |

Block item (the personal dose): `{ ex, sets, reps, time, hold, duration_min, rest, variant, resistance, range, note }` — only `ex` is required; `ex` exists in `exercises`; `variant` is a key of that exercise's `variants`; `resistance` from `resistances.yaml`; `rest` overrides the sub-routine's; `range` is the ceiling before changing variant or band. Items of a block with its own `duration_min` share that time.

Body: `## Guidelines`, `## Progression`, `## History` (dated lines: every change of dose, variant or exercise, and why).

A new sub-routine (e.g. "fuerza de pierna", "cardio suave") is built by filtering exercises by region/zone/goal and **excluding any exercise whose `stresses` intersect `program.constraints.avoid_stresses`**.

## routines (schema 4)

A routine is one session template made of sub-routines. Required: core fields, `title`, `category`, `user`, `status`, `parts`.

| Field | Rule |
| --- | --- |
| aliases | Other names the user uses for it |
| category | One id from `routines/_system/categories.yaml` (e.g. `strength`, `cardio`, `mobility`, `mixed`, `express`); drives the folder |
| days | Weekdays the routine is for: list of `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`. Empty = no fixed day. The source of truth for the weekly plan |
| user | Owner (user id) |
| status | `active`, `paused`, `draft`, `archived` (never delete: archive) |
| goals / regions | Focus of the routine (ids) |
| duration_min | Approximate length (about the sum of its parts) |
| time_of_day | Free Spanish note |
| parts | Ordered list `{ sub, note }`: `sub` is an id of `subroutines` (active); `note` is optional, only for this routine ("antes de las 10; la fuerza va después"). The same sub-routine can be in several routines |

A routine has no doses: they live in its sub-routines, so changing a sub-routine changes every routine that uses it. Archived routines from schema 3 may keep `blocks` instead of `parts` as history; readers ignore archived routines.

Body: `## Guidelines` (for the day as a whole), `## History` (dated lines: parts added, removed or reordered, days changed, and why).

## program (schema 2)

`program/<user>.yaml`, only that user's file.

- `phase`: `{ label, since, goal }` — current training phase.
- `constraints`: `avoid_stresses` (ids), `avoid_text` (Spanish list), `rules` (Spanish list: progression and safety rules), `pain_watch` (list `{ id, label }`: body areas whose pain is scored in every session, e.g. `leg`, `back`), `red_flags` (`{ urgent, soon }`, Spanish lists: symptoms that stop training — `urgent` = seek care today, `soon` = see a professional soon). Constraints come from the user, their physio or doctor, or the `health` group; only the user lifts one.
- `schedule`: `sessions_per_week` (`[min, max]`), `note`. There is no weekly calendar here: which routine goes on which weekday is only the `days` of the active routines. Schema 1 kept a copy in `schedule.week`; schema 2 drops it (delete it when migrating).
- `journal`: dated list `{ date, type, text, routine, metrics }`. `type`: `checkin` (how they feel, pain, energy), `adjustment` (routine changed), `milestone` (achievement), `measurement` (`metrics` map, e.g. `{ weight_kg: 80 }`), `setback` (worse, back to a previous level). Newest last.

## sessions (schema 3)

`sessions/<user>.yaml`: `user`, `updated`, `sessions` (list, date order).

Session: `{ date, start, routine, subroutine, status, duration_min, exercises, feel, next_day, note }`. For an `each-side` exercise, each value in `reps`/`time` is one set and applies to both sides.

- `routine`: id of the routine done. `subroutine`: id of the sub-routine when it was done on its own, without a routine (then `routine` is empty). Both empty = a free session. `status`: `completed`, `partial`, `skipped`.
- `exercises`: what was actually done. When the user just says "hice la rutina", the writer expands the current doses of the routine's sub-routines (or of the sub-routine) into this list, so history stays true when the routine changes. Entry: `{ ex, variant, resistance, sets, reps: [per set], time: [per set], hold, duration_min, skipped, note }`.
- `feel`: `{ effort, pain }`: `effort` integer 0–10 (RPE); `pain` map `<pain_watch id>` → integer 0–10 (`{ leg: 2, back: 1 }`). Optional.
- `next_day`: `better`, `same` or `worse` — the 24-hour check that decides whether to progress. Filled the day after.
- Archive: at the start of a year, sessions of the previous year move to `sessions/_archive/<user>-<YYYY>.yaml` with the same shape.
