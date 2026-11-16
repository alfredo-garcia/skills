# health — field contract

Group-specific rules on top of the `personal-knowledge-base` standard (v2). Scaffolding (keys, ids, folder names, section headings) is English; content (titles, notes, labels) is Spanish.

| Domain | Type | Schema | Storage |
| --- | --- | --- | --- |
| health-profile | state, per user | 1 | `profile/<user>.yaml` |
| conditions | collection | 1 | `conditions/items/<id>.md` |
| medications | state, per user | 1 | `medications/<user>.yaml` |
| medical-records | collection | 1 | `records/items/NN-<type>/<id>.md` + `records/_attachments/` |
| health-providers | catalog | 1 | `providers/items.yaml` |

Shared vocabularies in `_system/`: `condition-statuses`, `certainty`, `body-systems`, `record-types`, `care-routes`, `provider-types`, `medication-statuses`, `locations`.

## The model in one paragraph

`health-profile` is each user's base file: identity, coverage per country, history (personal and family), allergies, habits, vaccines, priorities and to-dos. `conditions` holds one file per ailment or risk (open case, chronic, suspected, resolved) with its clinical reasoning. `medications` is the single list of everything the user takes, took or keeps on demand, each line pointing to the condition it treats. `medical-records` holds the dated evidence: each visit, imaging study, lab panel or procedure, with the original document attached and transcribed. `health-providers` is the catalog of doctors, centers, labs, insurers and their patient portals. Conditions point to records, medications and providers by id; records point to providers and conditions. Nothing is stored twice: the condition summarizes, the record is the evidence.

## Who writes what

- The `health-advisor` skill owns the group: it creates and updates conditions, records, medications, providers and the profile.
- Other skills **read** health data; they never write it. `fitness-manager` reads `conditions` (and `_links/conditions-program.json`) to keep `program.constraints` safe; `food-manager` may read `conditions` (e.g. gota, colesterol) when planning meals; `legal-advisor` / `finance-advisor` may read `health-profile.coverage`.
- Every writer follows the optimistic write rule and sets `updated`.
- Privacy: this group contains clinical data and portal credentials. Never send its content through notifications or to external services unless the user asks for that specific piece.

## health-profile (schema 1)

`profile/<user>.yaml`: `user`, `updated`, then:

- `identity`: `{ full_name, birth_date, birthplace, sex, height_cm, weight_kg, weight_date, blood_type, blood_type_source, documents, phone }`.
- `residence`: `{ main: <location id>, since, share_pct, other: [location ids], note }`.
- `occupation`: Spanish text.
- `coverage`: list `{ id, country, route, name, active, details, todo }`; `route` from `care-routes.yaml`; `country` ISO code (`es`, `co`).
- `coverage_options`: options being studied `{ id, country, label, rating, pros_cons }`.
- `personal_history`: `{ conditions: [condition ids], surgeries: [], hospitalizations: [], injuries: [{ date, text }] }`.
- `family_history`: list `{ relative, condition, age, note }` + `family_history_notes` (Spanish list).
- `allergies`: list `{ substance, reaction, confirmed_by }` (empty list = none known).
- `habits`: `{ tobacco, alcohol, diet, exercise, sleep, stress }`, Spanish text each.
- `vaccines`: list `{ vaccine, date, status, note }`; `status`: `done`, `pending`, `unknown`.
- `planned_tests`: list `{ test, reason, status }`.
- `priorities`: ordered list `{ horizon, text }`.
- `todos`: list `{ text, done, priority }`.
- `changelog`: dated list `{ date, text }`, newest last.

## conditions (schema 1)

Required: core fields, `title`, `status`, `body_system`.

| Field | Rule |
| --- | --- |
| id | Slug of the Spanish name of the condition (`gota`, `hernia-discal-l4-l5`) |
| title / aliases | Spanish display name; other names the user or doctors use |
| status | `condition-statuses.yaml` |
| body_system | `body-systems.yaml` id |
| icd10 | List of codes when a document gives them |
| onset | `YYYY-MM-DD`, `YYYY-MM` or `YYYY` (approximate dates allowed as `~` note in `onset_note`) |
| certainty | Overall certainty of the main diagnosis, `certainty.yaml` |
| location | Where it is being followed (`locations.yaml`) |
| providers / records / medications | Lists of ids in `health-providers`, `medical-records`, `medications` |
| next_review | `YYYY-MM-DD` of the next checkpoint, if any |
| legacy_file | Name of the original file (e.g. in a claude.ai Project), if migrated |

Body sections, in this order: `## Summary`, `## Timeline`, `## Objective data`, `## Assessment` (by certainty level 🟢🟡🟠🔵⚠️), `## Treatment`, `## Roadmap`, `## Open questions`, `## Changelog`.

## medications (schema 1)

`medications/<user>.yaml`: `user`, `updated`, `items` (list). Item:

`{ id, active_ingredient, brand, form, strength, dose, schedule, status, since, until, conditions: [ids], prescriber, record, notes }`

- `id`: slug of the active ingredient (`levotiroxina`, `paracetamol-hidrocodona`); unique in the file.
- `status`: `medication-statuses.yaml` (`active`, `as-needed`, `stopped`).
- `prescriber`: `health-providers` id or empty; `record`: the `medical-records` id of the prescription.
- Never delete: a stopped medication keeps its line with `status: stopped` and `until`.

## medical-records (schema 1)

One file per encounter or result. Required: core fields, `title`, `type`, `date`.

| Field | Rule |
| --- | --- |
| id | `<YYYY-MM-DD>-<slug of the Spanish title>` (`2026-10-20-rm-columna-lumbosacra`) |
| type | `record-types.yaml`; drives the folder `items/NN-<type>/` |
| date | Date of the visit or study |
| provider / center | `health-providers` ids (professional / place) |
| route | `care-routes.yaml` |
| conditions | Condition ids it informs |
| diagnoses | List `{ icd10, label }` as written on the document |
| orders | Visits only: list `{ code, label, note, status }`; `status`: `done`, `pending`, `on-hold`, `not-done` |
| prescriptions | Visits only: medication ids from `medications` |
| values | Labs only: list `{ test, value, unit, ref_low, ref_high, flag }` |
| attachments | Paths relative to the root (`health/records/_attachments/<id>.pdf`, `<id>-2.pdf`…) |
| source | `{ type, original, external_id }`; type in `pdf`, `photo`, `portal`, `oral` |
| missing | What is not stored yet (`original-pdf`, `values`…) |

Body sections: `## Summary` (plain-language reading), `## Findings` or `## Notes`, `## Transcription` (literal text of the document, so it can be searched without the PDF).

## health-providers (schema 1)

`providers/items.yaml`, keyed by id (slug of the name). Entry:

`{ name, type, specialty, center, city, route, phone, address, registration, portal, note }`

- `type`: `provider-types.yaml`; `center`: id of another entry; `city`: `locations.yaml`.
- `portal`: `{ url, login_type, username, password, note }` for patient portals. Credentials are stored here only if the user explicitly asks for it; never copy them anywhere else.
