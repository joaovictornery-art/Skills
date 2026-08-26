---
name: simplifier
description: Explain complex technical, data, product, or process topics to beginners when they say they are lost or new, ask for plain language, or need a faithful analogy-based walkthrough.
---

# Simplifier

Translate without flattening. Build a mental model accurate enough for the user to understand the work and make the next decision. Reduce prerequisites while preserving meaning.

## Translation loop

1. **Orient.** Lead with the user's real goal and the invariant behind the discussion. Name the specific point that became confusing. Complete when the reader knows why the topic matters and what must remain unchanged.
2. **Disambiguate.** Separate overloaded names and layers before explaining mechanics. Define only the terms needed now. When version labels appear, distinguish the product or screen from an internal contract, prototype, rollout, or deployed system. Complete when each label refers to exactly one thing.
3. **Bridge.** Put one analogy at the hardest conceptual jump. Map each important part of the analogy back to the real system and state its boundary when extending it would mislead. Complete when the analogy explains a relationship, not merely decorates the prose.
4. **Prove.** Walk through a small concrete scenario, preferably with numbers, a before/after flow, or one representative example. When the topic concerns dashboards, metrics, filters, aggregation, or data pipelines, read [references/data-and-metrics.md](references/data-and-metrics.md). Complete when the user can predict the example's result.
5. **Contrast.** Separate `current`, `prototype`, `planned`, and `deployed`, then show what changes and what remains the same. Use a compact table when those mappings repeat. Complete when plans cannot be mistaken for delivered behavior.
6. **Protect.** Explain the validation or guardrail that preserves correctness. Distinguish facts found in the system from recommendations awaiting a decision. Complete when the user knows how a silent change or regression would be detected.
7. **Hand back.** Restate the open decision in everyday language and give a recommended answer with its reason. If no decision remains, end with a compact recap of goal, current state, proposed change, and next step.

Collapse the loop into a few paragraphs for a narrow question. Use the full walkthrough when the confusion spans goals, terminology, implementation state, and trade-offs.

## Accuracy locks

- Preserve the original goal, formula, scope, and authorization boundary.
- Introduce the plain-language explanation first, then attach the exact domain term so the user learns reusable vocabulary.
- Label facts, inferences, recommendations, and decisions distinctly.
- Surface any nuance whose removal would change the answer or the user's decision.
- For a proposed technical change, explicitly state its effect on visible behavior, business rules, data, and operations.

## Analogy discipline

An analogy is a bridge. Use it where the reader lacks a prerequisite, map it back immediately, and keep the real terms beside it. Prefer familiar systems with matching structure—restaurant prep for precomputation, envelopes for partitions, or a ledger for reconciliation—over vivid but structurally weak comparisons.

## Completion criterion

The explanation is complete when a beginner can distinguish the goal, current behavior, proposed behavior, unchanged invariants, delivery status, correctness guardrail, and next decision without relying on unexplained jargon.
