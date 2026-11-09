---
name: document-templates
description: Shared library for the SDLC skill suite (product-manager, tech-lead, qa-engineer, engineering-lead, ux-designer, platform-engineer, release-manager, document-manager) — the Project Context Protocol, shared scripts, and document templates. Not a workflow; never invoke directly. The other skills read files from here as part of their own Step 0.
disable-model-invocation: true
user-invocable: false
---

# Document Templates: Shared Library

Not a workflow. This folder only exists so the shared protocol, scripts and templates install next to the eight real skills, which read them by path (`${CLAUDE_SKILL_DIR}/../document-templates/...`). If this skill is ever triggered directly, that's a bug. See `README.md` for contents and `project_context_protocol.md` for the rules every skill follows.
