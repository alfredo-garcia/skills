# finance — field contract

Group-specific rules on top of the `personal-knowledge-base` standard (v2). Scaffolding (keys, ids, folder names, frontmatter) is English; content is Spanish.

| Domain | Type | Schema | Storage |
| --- | --- | --- | --- |
| investor-profile | collection | 1 | `profile/items/<user>.md` + `profile/_attachments/` |

## Who writes what

- The `finance-advisor` skill owns the group. `legal-advisor` may read it (assets abroad, real estate, company shares).
- Every writer follows the optimistic write rule and sets `updated`.
- Privacy: no account numbers, IBAN, passwords or login data. Never send this group's content through notifications unless the user asks for that specific piece.

## investor-profile (schema 1)

One item per user: the investor profile and its change log.

```yaml
---
id: <user>
domain: investor-profile
created: <ISO timestamp>
updated: <ISO timestamp>
user: <user>
risk_profile: ""       # conservador | moderado | equilibrado | dinamico | agresivo
last_statement: null   # YYYY-MM-DD of the latest portfolio statement analysed
legacy_file: null       # original file name, if migrated from a claude.ai Project or a download
---
```

Body: the structure of the finance-advisor skill's `references/perfil-template.md` (in Spanish), including its change log.

Attachments: portfolio statements and screenshots as `profile/_attachments/<user>-<YYYY-MM-DD>-<platform>.<ext>` (account numbers redacted when possible).
