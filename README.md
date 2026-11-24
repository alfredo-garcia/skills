# skills — marketplace de plugins

Skills y plugins de Al, listos para instalarse desde un marketplace de Claude (Claude Code / Cowork). Las skills no llevan datos personales: cada persona trabaja sobre **su propio knowledge base**.

## Estructura

```
.claude-plugin/marketplace.json   ← catálogo del marketplace
plugins/
  sdlc-suite/            (v3.6.0) roles del ciclo de vida: product-manager, tech-lead, qa-engineer,
                         engineering-lead, ux-designer, platform-engineer, release-manager,
                         document-manager + document-templates
  knowledge-base-suite/  (v2.7.0) personal-knowledge-base, inbox-router, personal-notifications,
                         food-manager, plan-manager, fitness-manager (dependen entre sí,
                         por eso van juntas)
  finance-advisor/       asesor de inversiones (grupo finance del knowledge base)
  health-advisor/        asistente de salud personal (grupo health del knowledge base)
  legal-advisor-es-co/         asesor legal España–Colombia (migración, padrón, residencia fiscal,
                         Seguridad Social, empresas); coordina con finance-advisor
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

## Usarlo con tu propio knowledge base

1. Instala el marketplace y `knowledge-base-suite` (más los advisors que quieras).
2. Crea una carpeta sincronizada con Google Drive y conéctala en Cowork. Guía completa (Mac, Windows y Linux, conflictos, Telegram opcional): [`setup-and-sync.md`](plugins/knowledge-base-suite/skills/personal-knowledge-base/references/setup-and-sync.md).
3. Di «monta mi knowledge base» (o usa cualquier skill: si no encuentra knowledge base, te pide la carpeta): se crea `_profile.yaml` (tus datos: nombre, zona horaria, ciudad, países, Telegram), `_domains.json`, `_inbox/` y `_links/`.
4. Cada skill monta su propio grupo la primera vez que la usas, con su propio `scripts/scaffold.py` y su `assets/scaffold/` (schema, vocabularios, archivos vacíos); nunca sobrescribe nada. `personal-knowledge-base` solo crea el mínimo general.

Todo lo personal vive en el knowledge base de cada uno: perfil en `_profile.yaml` y datos de dominio (restricciones de entrenamiento, ciudades, preferencias, fichas, perfil legal y de inversor) en los archivos de su grupo. Las skills no contienen datos de ninguna persona ni ejemplos de su situación, y se llaman entre sí por nombre de skill, sin depender del marketplace.
