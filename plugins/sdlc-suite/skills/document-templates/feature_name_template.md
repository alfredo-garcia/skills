# Template: Feature Definition Doc

> **What this is:** the short, challenged, agreed-upon statement of what a single feature is and
> why it's worth building — the contract a user and an agent agree to before any implementation
> detail gets written. Deliberately small: six fields, no technical detail, no exceptions.
>
> **Produced by:** the `product-manager` skill's Mode A, after an interview/challenge process
> (see that skill's `references/challenge_playbook.md`) — never drafted straight from a raw idea
> without that step.
>
> **Consumed by:** the `product-manager` skill's own Mode B (expands this into a full PRD using
> `feature_name_prd_template.md`'s structure) and cross-checked against by `document-manager` (as part of
> "Document A" content, alongside a design/flow doc, when folding a shipped feature into the Master
> Functional Documentation).
>
> **Real instance filename:** `<feature-id>_<feature-slug>.md` — `<feature-id>` is this feature's
> permanent, sequential 3-digit ID (minted once by `product-manager`, see its
> `scripts/next_feature_id.sh`), `<feature-slug>` in whatever case style the project uses
> (kebab-case by default). Saved alongside the project's other feature docs (commonly
> `docs/features/`).
>
> **Contains no technical implementation detail** — no libraries, data structures, endpoints, or
> architecture. That belongs in the PRD (`<feature-id>_<feature-slug>_prd.md`), one step
> downstream, not here.

---

## Structure

Exactly these six fields, in this order, no additional sections:

```markdown
# [Feature Name]

> Project: `<project_id>`
> MVP: yes / no (Product Vision §5/§7) — Backlog item: [# or "new, not in backlog"]
> Epic: [external key, e.g. ABC-123, or none] · Issue: [#n of the `[Feature]` issue, or n/a]

* **Feature Name:** [Short but clear name/description of the feature.]

* **Goal:** [What we aim to achieve — the success condition for this feature. Should be
  outcome-oriented, not a restatement of the mechanics.]

* **The Delta:** [What are we adding or changing relative to the current application. Be specific
  about the "before" state.]

* **User Persona:** [Who specifically benefits from this. Name the persona, not "all users"
  unless genuinely universal.]

* **Core Mechanics (High Level):**
  - [Non-negotiable behavior #1. 1-2 sentences. No technical implementation detail.]
  - [Non-negotiable behavior #2.]
  - [...]

* **Constraints / Out of Scope:**
  - [What the AI/dev should NOT invent or include. Be explicit — this is the guardrail against
    scope creep.]
  - [...]
```

## Field-by-Field Guidance

### Feature Name
A short, unambiguous label — specific enough that two different features couldn't share it. Prefer a name that describes the capability, not the implementation ("Guest Checkout," not "Anonymous Order Flag").

### Goal
An **outcome**, not a mechanic wearing a goal's costume. "Add a filter button" describes a mechanic; "reduce time-to-find for repeat customers" describes a goal. If the stated goal is really just a restatement of what the feature does, it hasn't been pushed on hard enough yet — see the challenge playbook's Goal section for the questions that surface this.

- **Good:** "Let returning customers find their most-ordered items in under 5 seconds, instead of re-browsing the full catalog every time."
- **Weak:** "Add a 'Recently Ordered' section." *(This is a mechanic, not a goal — it doesn't say why it matters or what success looks like.)*

### The Delta
The concrete, current "before" state, stated specifically enough that someone unfamiliar with the product could picture it. Vague deltas ("make ordering easier") hide the fact that the actual gap hasn't been identified yet.

- **Good:** "Today, a returning customer must re-search or re-browse the full catalog every time, even if they order the same 3 items every week."
- **Weak:** "Ordering could be faster."

### User Persona
Name a specific persona, not "users" as a catch-all — unless the feature is genuinely universal, in which case say so explicitly rather than defaulting to it out of vagueness. If the master functional spec already defines personas, use one of those rather than inventing a parallel one, and flag if this feature seems to redefine an existing persona's expectations.

- **Good:** "Repeat customers who order weekly (3+ orders in the last 60 days)."
- **Weak:** "Users."

### Core Mechanics (High Level)
The non-negotiable behaviors — what must be true for this feature to exist at all, described at the level a stakeholder would describe them, not the level an engineer would implement them. 1-2 sentences per bullet. No mention of specific libraries, data structures, caching strategy, or architecture — if a mechanic implies a technical approach ("use a queue," "cache this locally"), it's drifted into implementation territory and belongs in the PRD instead, not here.

Each mechanic should be genuinely non-negotiable — if asked "if you could only ship one of these, which one, and would the feature still be worth shipping?", every bullet here should survive that question. Nice-to-haves that don't survive it belong in the PRD's proposed defaults instead, not bundled in here as if they were load-bearing.

### Constraints / Out of Scope
The guardrail against scope creep — explicit statements of what should **not** be invented or included, even if it seems like a natural extension. This is usually the thinnest section people provide by default; it deserves real, specific content, not "keep it simple." A good constraints section names the adjacent things someone might assume are included and explicitly excludes them.

- **Good:** "Does not include bulk reordering (adding all 3 items at once) — single-item quick-add only in this version. Does not apply to guest checkout users, only logged-in accounts."
- **Weak:** "Keep it simple. Don't over-engineer."

## Worked Example

```markdown
# Quick Reorder for Repeat Customers

* **Feature Name:** Quick Reorder

* **Goal:** Reduce time-to-find for repeat customers from a full catalog browse down to under 5
  seconds for their regular items.

* **The Delta:** Today, a returning customer must re-search or re-browse the full catalog every
  time, even if they order the same items every week. There is no concept of "past orders" surfaced
  anywhere in the current shopping flow.

* **User Persona:** Repeat customers who've placed 3+ orders in the last 60 days.

* **Core Mechanics (High Level):**
  - Show a "Reorder" section on the home screen listing the customer's 5 most-frequently-ordered
    items from the last 60 days.
  - Tapping an item's quick-add button adds it to the cart at its current price and availability —
    no bulk "reorder everything" action in this version.
  - If an item is no longer available, it's excluded from the list rather than shown as
    unavailable.

* **Constraints / Out of Scope:**
  - No bulk reordering (adding all frequent items at once) — single-item quick-add only.
  - Does not apply to guest checkout users, only logged-in accounts with order history.
  - Does not include reordering a specific past order in full (e.g. "reorder my order from last
    Tuesday") — that's a separate, larger feature.
```
