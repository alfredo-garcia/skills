# Document Templates: Shared Library

This folder isn't a workflow. It carries an inert `SKILL.md` (`disable-model-invocation: true`, `user-invocable: false`) only so it installs next to the real skills: `product-manager`, `tech-lead`, `qa-engineer`, `engineering-lead`, `ux-designer`, `platform-engineer`, `release-manager` and `document-manager`. It holds everything those skills share, defined once:

1. **The Project Context Protocol** (`project_context_protocol.md`): how every skill finds the current project, what it must read and respect, how projects stay isolated from each other, the Phase 0 order, and the gates. **Every skill runs this as its Step 0.**
2. **Shared scripts** (`scripts/`): `project_context.sh` resolves the project and inventories it; `next_feature_id.sh` mints or looks up Feature IDs and `next_adr_id.sh` numbers ADRs, both counting every branch; `list_handoffs.sh` lists the features ready for development across branches (all read-only); `gh_labels.sh` prints, or with `--apply` creates, the SDLC's GitHub labels (only after the user approves).
3. **Document templates**: the structure of every document type the suite produces.

## The one rule

**Skills are generic; projects hold everything.** No file in any skill folder contains project data, and no skill ever writes into a skill folder. Each project is a folder (usually a git repo) with `SDLC.md` at its root. That file identifies the project (`project_id`), sets its few paths, and tracks Phase 0. Everything else follows by convention (`project_context_protocol.md` §3).

## Monorepos and shared pieces

A repo may contain several projects, each with its own `SDLC.md` (`type: app` or `type: shared`). Apps keep all their own docs and never read each other. A shared piece (ui-kit, auth, logs…) is consumed like an external library: apps declare it in `shared_deps` and may read only the files it lists in `public_docs`. There are no versions: shared changes are classified as breaking or not in their changelog, and the script warns each consumer about breaking changes since its last contract review. Feature IDs are qualified as `<project_id>/<id>` in git and conversation. Full rules: `project_context_protocol.md` §10.

## Locating this library from a skill

Each skill refers to this folder as `${CLAUDE_SKILL_DIR}/../document-templates`. It's a sibling of the skill's own folder, so this works wherever the suite is installed (a Claude Code plugin, `~/.claude/skills/`, claude.ai, Cowork) as long as all the skills are installed together. If `${CLAUDE_SKILL_DIR}` isn't expanded, the skill uses the folder containing its own `SKILL.md`. Never hardcode absolute paths.

## What's here

| File | Defines | Real instance path in a project |
|---|---|---|
| `project_context_protocol.md` | Rules every skill follows (not a document type) | n/a |
| `sdlc_config_template.md` | Project config + `CLAUDE.md` snippet | `SDLC.md`, `CLAUDE.md` |
| `product_vision_template.md` | Product Vision (Phase 0.1, apps) | `<docs_root>/product/product_vision.md` |
| `shared_charter_template.md` | Shared Charter (Phase 0.1, shared projects) | `<docs_root>/product/shared_charter.md` |
| `contract_template.md` | Public contract of a shared project | `<docs_root>/contract.md` |
| `tech_standards_template.md` | Tech Standards, core (Phase 0.2) | `<docs_root>/context/tech_standards.md` |
| `tech_standards_surface_template.md` | Tech Standards per surface (Phase 0.2) | `<docs_root>/context/tech_standards/<surface>.md` |
| `test_strategy_template.md` | Test Strategy (Phase 0.2b) | `<docs_root>/quality/test_strategy.md` |
| `test_plan_template.md` | Feature test plan + traceability matrix | `<features_root>/<id>_<slug>_test_plan.md` |
| `work_tracking_guide.md` | How work is tracked in GitHub Issues (hierarchy, labels, bodies, checkpoints) | GitHub Issues of the project's repo |
| `impl_plan_template.md` | Implementation plan + review record | `<features_root>/<id>_<slug>_impl_plan.md` |
| `platform_foundations_template.md` | Platform Foundations + runbook/postmortem (Phase 0.4) | `<docs_root>/platform/…` |
| `release_process_template.md` | Release Process (Phase 0.5) | `<docs_root>/release/release_process.md` |
| `release_record_template.md` | One release | `<docs_root>/release/releases/<release-id>.md` |
| `subagent_template.md` | Claude Code subagent (only when needed) | `.claude/agents/<name>.md` |
| `hl_architecture_template.md` | High-Level Architecture (Phase 0.2) | `<docs_root>/architecture/hl_architecture.md` |
| `adr_template.md` | Architecture Decision Record | `<docs_root>/architecture/adr/<NNN>_<slug>.md` |
| `ui_standards_template.md` | UI Standards (Phase 0.3) | `<docs_root>/context/ui_standards.md` |
| `ui_kit_registry_template.md` | UI Kit Registry (Phase 0.3) | `<docs_root>/context/ui_kit_registry.md` |
| `feature_name_template.md` | Feature definition (production; folded into the PRD lite when personal) | `<features_root>/<id>_<slug>.md` |
| `feature_name_prd_template.md` | PRD (full, or Lite variant when personal) | `<features_root>/<id>_<slug>_prd.md` |
| `ux_flow_template.md` | UX Flow (component orchestration) | `<features_root>/<id>_<slug>_ux_flow.md` |
| `master_functional_spec_template.md` | Master Functional Documentation | `<docs_root>/functional-spec.md` (+ `functional/`) |

The changelog template stays inside `document-manager/assets/`, since only that skill uses it.

Every template filename ends in `_template` on purpose, so a structure definition is never mistaken for a real project document.

## Who owns what

The full role map and routing triggers are in `project_context_protocol.md` §11; depth per project rigor is in §12.

| Skill | Writes | Phase 0 step |
|---|---|---|
| `product-manager` | Vision / Shared Charter, feature docs, PRDs | 0.1 |
| `tech-lead` | hl_architecture, tech_standards (core + per surface, incl. §17 Enforcement Map), ADRs, PRD technical reviews, project subagents | 0.2, 0.2c |
| `engineering-lead` | implementation plans, small PRs, independent review records | — (per feature) |
| `qa-engineer` | test_strategy, feature test plans (traceability), acceptance tests, verification verdicts, regression tests | 0.2b (required for production) |
| `ux-designer` | ui_standards, ui_kit_registry, prototypes, UX Flow docs | 0.3 (UI surfaces) |
| `platform-engineer` | platform_foundations, runbooks, postmortems, release readiness results | 0.4 (required for production) |
| `release-manager` | release_process, release records, release notes | 0.5 (required for production) |
| `document-manager` | master functional doc / contract, changelogs (only after merge) | after each merge |

Each skill updates only its own Phase 0 line in `SDLC.md`, and only after the user approves the document.

## Feature ID convention

Every feature gets a permanent, sequential, 3-digit ID (`001`, `002`, …), minted once by `product-manager` Mode A through `scripts/next_feature_id.sh` and reused unchanged in its PRD, UX Flow and changelog filenames. Nobody else mints IDs. ADRs use their own separate sequence.

## Maintaining this library

- If you change a template's structure, check every skill's `SKILL.md` for prose that names its sections.
- Keep templates self-contained, so each one can be read on its own.
- Keep workflow logic (who asks what, approval gates) in the skills and the protocol, not in templates.
- Worked examples in templates are fictional (Acme, etc.) and must never leak into real documents.
