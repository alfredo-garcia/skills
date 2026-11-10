# skills — marketplace de plugins

Skills y plugins propios de Al, listos para instalarse desde un marketplace de Claude (Claude Code / Cowork).

## Estructura

```
.claude-plugin/marketplace.json   ← catálogo del marketplace
plugins/
  sdlc-suite/            (v3.6.0) roles del ciclo de vida: product-manager, tech-lead, qa-engineer,
                         engineering-lead, ux-designer, platform-engineer, release-manager,
                         document-manager + document-templates
  knowledge-base-suite/  personal-knowledge-base, inbox-router, personal-notifications,
                         food-manager, plan-manager, fitness-manager (dependen entre sí,
                         por eso van juntas)
  finance-advisor/       asesor de inversiones
  health-advisor/        asistente de salud personal
```

`sdlc-suite` incluye un hook (`hooks/prd_gate.py`) que bloquea escribir código sin visión/tech aprobadas, rama de feature y PRD `Approved` (`code_gate` en `SDLC.md`), y el subagente `pr-reviewer` para la revisión independiente.

Cada plugin tiene `.claude-plugin/plugin.json` y sus skills en `skills/<nombre>/SKILL.md`.

## Publicar

```bash
git init && git add . && git commit -m "Initial marketplace"
git remote add origin git@github.com:alfredo-garcia/skills.git
git push -u origin main
```

## Instalar

Claude Code:

```
/plugin marketplace add alfredo-garcia/skills
/plugin install sdlc-suite@skills
```

En Claude (web/desktop): Customize → Plugins → añadir marketplace con la URL del repo.
