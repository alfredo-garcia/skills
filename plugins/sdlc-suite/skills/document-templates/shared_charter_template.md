# Template: Shared Charter

> **What this is:** the founding document of a `type: shared` project (a ui-kit, auth, logging, a platform utility) that other projects in the same repo consume as if it were an external library. It replaces the Product Vision for shared projects: no MVP or personas, but the same discipline about scope and real needs, so the shared piece doesn't grow into a framework nobody asked for.
>
> **Produced by:** `product-manager` Mode 0 when `SDLC.md` says `type: shared`. **Consumed by:** `tech-lead` (stack and architecture of the shared piece), `ux-designer` (if it provides UI), `document-manager` (the contract's overview).
>
> **Real instance path:** `<docs_root>/product/shared_charter.md`. Its Phase 0 line in `SDLC.md` is `product_vision` (same gate, different document).

---

## Structure

```markdown
# Shared Charter: [Name]

> Project: `<project_id>`
> Type: shared
> Status: Draft / Approved (YYYY-MM-DD)

## 1. Purpose
What this shared piece does, in two or three sentences, and why it exists as a shared piece
instead of living inside one app.

## 2. Consumers
Which projects use it today or are expected to (by project_id), and what each one needs from it.
Only real, named consumers. "Future apps" isn't a consumer.

## 3. Scope
- In scope: the capabilities it provides.
- Out of scope: what consumers must do themselves, and the tempting extensions it won't take on.

## 4. Contract Principles
How it treats its consumers: what counts as public (only what's in `public_docs`), how breaking
changes are handled without versions (see §6), and stability expectations per area
(stable / evolving).

## 5. Constraints
Technical or platform limits it must respect so that every consumer can use it (runtimes,
frameworks, platforms: web/mobile).

## 6. Change Policy (no versions)
Consumers use the current state of this project directly. Therefore:
- Every merged change is classified in its changelog as breaking: yes/no.
- A breaking change lists the affected consumers and what each must do.
- Prefer additive changes; deprecate before removing whenever possible.

## 7. Open Questions
```

## Quality bar before approval
- Every in-scope capability is needed by at least one named consumer (§2).
- Out of scope names the most tempting extensions.
- §6 is accepted explicitly by the user.
