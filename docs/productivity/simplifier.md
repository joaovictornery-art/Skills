# Simplifier

## Quickstart

```bash
npx skills@latest add joaovictornery-art/Skills --skill=simplifier
```

[Source](../../skills/productivity/simplifier)

## What it does

`simplifier` turns complex technical, data, product, and process explanations
into a mental model a beginner can use without changing the underlying facts.
It separates overloaded terms, places one analogy at the hardest conceptual
jump, proves the explanation with a concrete example, and makes current,
planned, prototype, and deployed states explicit.

For dashboards, metrics, filters, aggregates, caches, and data pipelines, the
skill includes a focused reference that protects formula, scope, filter,
timezone, late-update, and non-additive-metric semantics while simplifying the
explanation.

## When it runs

The model may invoke `simplifier` when someone says they are lost or new, asks
for plain language, or needs an analogy-based walkthrough. It can also be
invoked explicitly as `$simplifier`.

Use it when reducing prerequisites would help the reader make the next decision.
Do not use it to hide uncertainty, omit a correctness constraint, or make a
proposed behavior sound as if it is already deployed.
