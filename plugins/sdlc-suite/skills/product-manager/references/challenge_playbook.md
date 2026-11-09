# Challenge Playbook

Use this bank when interrogating a feature idea in Mode A, and again as a quality gate before finalizing a PRD in Mode B. Don't ask every question mechanically — pick the ones that expose real gaps in what the user has told you. Silence on a question you didn't ask is not the same as an answer; don't fill it in yourself.

## MVP fit (check first)
- Is this feature in the Product Vision's MVP scope (§5) and Initial Feature Backlog (§7)? If not, say so plainly and ask: proceed now, defer, or update the vision first?
- Is the persona one of the vision's personas? A new persona is a vision change, not just a feature detail.
- Does it respect the vision's Product Principles (§8) and Constraints (§9)?

## Routing check (all features)
- Does this need new infrastructure, environments, secrets, jobs, third-party accounts or alerts? → platform-engineer.
- Does it need a feature flag, staged rollout, coordinated multi-surface release, forced update or store-facing changes? → release-manager.
- Does it need a technology not in the standards, or change a cross-surface contract? → tech-lead.

## Goal
- Is this a goal (an outcome) or a mechanic wearing a goal's clothes? ("Add a filter button" is not a goal. "Reduce time-to-find for repeat customers" is.)
- What does success look like if this ships and nothing else changes? What would make you consider it a failure even if it technically works?
- Is there a metric, or is this qualitative? Both are fine — but name which one.

## The Delta
- What exactly happens today, step by step, without this feature? (If the user can't say, the master doc should be checked before assuming there's a gap at all — it may already partially exist.)
- Is this net-new, or a modification of existing behavior? Modifications carry migration/compat risk that net-new doesn't.

## User Persona
- Named persona, or "users" as a catch-all? Push for specificity — a feature for "power users doing X weekly" is a different feature than one for "all users."
- Is this persona already defined in the master doc? If it conflicts with an existing persona definition, surface that.

## Core Mechanics
- Are these truly non-negotiable, or is the user bundling nice-to-haves in? Ask directly: "if you could only ship one of these, which one, and would the feature still be worth shipping?"
- Any mechanic that implies a technical approach ("use a queue", "cache this") — flag that it's drifting into implementation and belongs out of this doc.
- Do any two mechanics contradict each other, or contradict something in the master doc?

## Constraints / Out of Scope
- This section is usually the thinnest one users provide — push here specifically. Ask: "what's the thing you're worried an AI coding tool will over-build if you don't say so explicitly?"
- Check the master doc for adjacent features that might get accidentally touched — call those out as explicit exclusions.

## Cross-checking the master doc
- Does this feature already exist in some form? (Partial overlap is common — surface it rather than silently building parallel logic.)
- Does this contradict a documented constraint, decision, or pattern elsewhere in the app?
- Does this rely on an entity/module the master doc defines — and if so, is the user's mental model of it still accurate?

## Quality gate before finalizing (either doc)
- For the PRD specifically: every acceptance criterion has an ID (`AC-n`), names the FR it proves, and is testable (concrete inputs, one observable outcome, clear pass/fail). Negative paths and third-party failure behavior are covered. NFRs have numeric thresholds. No test tool is named anywhere.
- Every section filled with a real answer — no "TBD" left in unless the user explicitly agreed to defer it.
- Nothing invented that the user didn't say or confirm. In the feature doc, that means every gap was asked about, not guessed. In the PRD, that means every gap is either (a) resolved because it was foundational and got asked before drafting, or (b) was a proposable, implementation-adjacent default that went through the `**[PROPOSED]**` review pass and got explicitly confirmed or overridden.
- Constraints section is specific enough to actually stop scope creep — "keep it simple" is not a constraint.
- For the PRD specifically: every technology, library, service or pattern mentioned is allowed by `tech_standards.md`. Anything else was routed to tech-lead as an ADR, never written in.
- For the PRD specifically: non-functional requirements don't exceed what the vision's Scale & Quality section justifies.
- For the PRD specifically: no `**[PROPOSED]**` tags survive into the final saved file. They're a draft-phase-only device — by the time the file is saved, every one has either been folded into confirmed plain text or moved to Section 13 as a genuinely still-open question the user chose to defer.
