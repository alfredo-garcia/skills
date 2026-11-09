# Vision Playbook (Mode 0)

The question bank for building a Product Vision. Pick the questions that expose real gaps in what the user has said; don't run it as a form. Silence on a question you didn't ask isn't an answer, so never fill it in yourself.

## Problem
- What exactly hurts today, and for whom? Describe the last time it happened.
- How do they cope now (tool, spreadsheet, nothing)? Why isn't that good enough?
- If this product never existed, what would they lose?

## Persona
- Who is the *first* user, specifically? (If the answer is "everyone", push: who'd use it first and most?)
- Are you the user yourself? Fine, but say so; it's a different validation story.
- What would make this persona switch from their current alternative?

## MVP
- What do we need to *learn or prove* with the first version? (That's the hypothesis.)
- If you could only ship three capabilities, which ones, and would it still test the hypothesis?
- What are you most tempted to include that could wait? (Name 2-3 explicitly; they go to "out of scope".)
- What observable condition means "the MVP is done"? (Not a date: a state.)
- How will you know it worked: a metric, or a qualitative signal? What's the target?

## Constraints (feed tech-lead directly)
- Who builds this? Which languages and frameworks do they already know well?
- How much time per week? Any target date?
- Monthly budget for hosting and services? Are paid tools OK?
- Any legal or regulatory angle: personal data, payments, health, minors?
- Must it integrate with or run on something specific?

## Scale & quality (the main guard against over-architecture)
- Realistically, how many users at launch? In 12 months? (Order of magnitude is enough.)
- How often will they use it? Are there peaks?
- What data is stored? Is any of it sensitive? How long must it be kept?
- If it's down for an hour, is that annoying, costly, or unacceptable?
- Do you truly need offline use, real time, or multi-device sync, or would it just be nice?

## Product principles
- When two options conflict (speed vs. completeness, simplicity vs. flexibility), which wins by default?

## Quality bar before approval
- The hypothesis is testable and the MVP done-condition is observable.
- Every "MVP: yes" backlog item maps to the MVP in-scope list, and vice versa.
- Scale & quality has real numbers, or an explicit "unknown, assume small".
- Out of scope names the most tempting deferrals.
- No technology choices anywhere (those are tech-lead's job); technology *constraints* are fine in §9.
