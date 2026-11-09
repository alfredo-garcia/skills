# Template: High-Level Architecture

> **What this is:** the shape of the system and the reasoning behind it, at the level a new developer (or an AI agent) needs to place any feature correctly. It explains *why* the system is built this way; `tech_standards.md` (core + per surface) holds the binding *rules*, and `platform_foundations.md` holds *how it runs*.
>
> **Two failure modes it guards against:** over-architecture (every element must trace to a driver in the Product Vision; §12 records what we deliberately don't build yet, with a revisit signal) and under-architecture (with `rigor: production`, the Cross-Cutting Concerns Register in §9 forces an explicit decision on *every* concern, so nothing important is simply forgotten).
>
> **Produced by:** `tech-lead` Mode A, from the approved Product Vision. Updated through `tech-lead` Mode B (ADRs).
>
> **Real instance path:** `<docs_root>/architecture/hl_architecture.md`.

---

## Structure

```markdown
# High-Level Architecture: [Product Name]

> Project: `<project_id>`
> Rigor: personal | production
> Surfaces: … (from SDLC.md)
> Status: Draft / Approved (YYYY-MM-DD)
> Derived from: `product/product_vision.md` (approved YYYY-MM-DD)

## 1. Architecture Drivers
The facts from the vision that shape the architecture, each cited (e.g. "Vision §10: ~50k MAU
in 12 months, personal + payment data → PCI scope minimization, managed identity"). 3-7 items
for personal; as many as needed for production (typically 8-15).

## 2. Quality Attribute Targets (production: mandatory)
Availability, latency, throughput, data durability (RPO/RTO), security/compliance, scalability
horizon. Each with a target and the driver it comes from. These become SLOs in
platform_foundations.md.

## 3. Architectural Style
The overall approach and why it's the simplest fit for §1-§2 (e.g. "modular monolith backend +
native mobile clients + SSR web, one Postgres, async events via managed queue for X and Y only").

## 4. System Context
Users, surfaces, external systems. Mermaid welcome:
    ```mermaid
    flowchart LR
      Android & iOS & Web --> API --> DB[(DB)]
    ```

## 5. Surfaces & Building Blocks
One subsection per surface in SDLC.md: what it is, the option chosen and the main alternative
rejected (link the ADR), its main modules, and how it talks to the others.

## 6. Core Data Model (high level)
Main entities, ownership (which service/module), relationships, data classification
(public / internal / personal / sensitive).

## 7. Key Flows
The 3-5 most important end-to-end flows across surfaces (e.g. sign-up, the core job-to-be-done,
payment), as short sequence descriptions or Mermaid sequence diagrams.

## 8. Integrations
External services, purpose, data shared, failure mode and fallback, contractual/vendor risk.

## 9. Cross-Cutting Concerns Register
One row per concern from tech-lead's cross-cutting checklist. **production: every row decided;
personal: at least the "always" rows.**
| Concern | Decision: adopt / defer / n/a | How (summary) | Driver or reason | Revisit when | Rule in |
|---|---|---|---|---|---|
| Logging | adopt | structured JSON, correlation IDs | Vision §10 availability | — | tech_standards §5 |
| … | | | | | |

## 10. Deployment Topology (summary)
Environments and where each surface runs, at summary level. Detail is owned by platform-engineer
in platform_foundations.md.

## 11. Key Decisions
Index: decision → chosen option → ADR link.

## 12. Deliberately Deferred
| Deferred | Why not now (driver) | Revisit when (concrete signal) |
|---|---|---|

## 13. Risks & Open Questions
Technical risks (likelihood/impact, mitigation) and unresolved items with a due point.
```

## Guidance

- Prefer one deployable per surface, one database and managed services unless a driver says otherwise, in both rigor levels.
- §9 and §12 are where "exhaustive but not over-built" lives: a production project can have many rows that say "defer" with a clear signal. That's a good outcome.
- For production, aim for decisions an architect reviewer could challenge line by line. For personal, keep it short.
