# legal — field contract

Group-specific rules on top of the `personal-knowledge-base` standard (v2). Scaffolding (keys, ids, folder names, frontmatter) is English; content is Spanish.

| Domain | Type | Schema | Storage |
| --- | --- | --- | --- |
| legal-profile | collection | 1 | `profile/items/<user>.md` + `profile/_attachments/` |
| legal-cases | collection | 1 | `cases/items/<YYYY-MM-DD>-<slug>.md` + `cases/_attachments/` |

## Who writes what

- The `legal-advisor-es-co` skill owns the group. Other skills only read it: `finance-advisor` reads tax residence and formal obligations from the legal profile.
- Every writer follows the optimistic write rule and sets `updated`.
- Privacy: never store document numbers, NIE/NIF/NIT, IBAN, passwords, Cl@ve keys or digital certificates — only document types, validity dates and statuses. Never send this group's content through notifications.

## legal-profile (schema 1)

One item per user: the advisor's memory (situation, objectives, conclusions, verified law, deadlines calendar, open cases).

```yaml
---
id: <user>
domain: legal-profile
created: <ISO timestamp>
updated: <ISO timestamp>
user: <user>
version: 1          # bumped on every substantive update
next_deadline: null # YYYY-MM-DD of the nearest item in the deadlines calendar
legacy_file: null       # original file name, if migrated from a claude.ai Project or a download
---
```

Body: the structure of the legal-advisor-es-co skill's `assets/plantilla-perfil-legal.md` (in Spanish), including its change log.

Attachments: `profile/_attachments/<user>-viajes.csv` (travel log, columns `pais,entrada,salida`, dates `YYYY-MM-DD`) and supporting documents (`<user>-<YYYY-MM-DD>-<slug>.<ext>`).

## legal-cases (schema 1)

One item per procedure that has several steps or lasts weeks (visa renewal, company formation, answering a notice).

```yaml
---
id: <YYYY-MM-DD>-<slug>   # opening date + short Spanish slug
domain: legal-cases
created: <ISO timestamp>
updated: <ISO timestamp>
user: <user>
title: <Spanish title>
status: preparing         # preparing | filed | waiting | resolved | archived
country: co               # ISO code(s), list if both: [co, es]
objective: O2             # objective id in the legal profile, if any
deadline: null            # YYYY-MM-DD legal deadline, if any
next_step: ""             # Spanish, one line
---
```

Body: the structure of the skill's `assets/plantilla-gestion.md`. Letters, notices and resolutions go to `cases/_attachments/<id>-<n>.<ext>` and are linked from the body. The case's summary and next step are also mirrored in the profile's case table.
