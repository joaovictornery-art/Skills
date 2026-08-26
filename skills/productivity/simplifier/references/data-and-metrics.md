# Data, metrics and aggregation

Use this reference when simplification involves dashboards, KPIs, filters, aggregates, caches, projections, materialization, or reconciliation.

## Keep the concepts separate

- **Metric:** the business question and calculation, such as “completed orders in the selected period.”
- **Dimension:** an attribute used to split data, such as date, region, product category, or sales channel.
- **Filter:** the user's selection of dimension values.
- **Aggregate:** a smaller, precomputed representation that answers the same metric without rereading every source record.
- **Projection or materialization:** persisted derived data prepared before an interactive read.
- **Cache:** a temporary copy that accelerates repeat reads; it does not define the metric or source truth.
- **Reconciliation:** recomputing or comparing derived data so late changes, gaps, or corruption are repaired explicitly.

Phrase performance work as a change in **when and where** the same calculation runs. State separately when a proposal truly changes the calculation.

## Parity checklist

Before saying an aggregate preserves a metric, account for all of these:

- formula and unit;
- eligible population and exclusions;
- timezone and period boundaries;
- filter semantics;
- null, stale, gap, and unavailable behavior;
- late updates, deletions, and deduplication;
- exact handling of non-additive measures.

Useful exact-composition examples:

- counts: sum compatible buckets;
- unique entities: union stable irreversible identifiers;
- averages: combine sums and sample sizes, then divide;
- median and percentiles: combine exact distributions or histograms;
- entities spanning days: deduplicate across the selected range;
- late mutations: recompute every affected bucket from source facts.

## Beginner walkthrough pattern

Use one small scenario:

1. Current read scans many raw records when the screen opens.
2. Background processing prepares daily buckets beforehand.
3. The screen reads a few buckets and combines them for the selected period and filters.
4. A raw-versus-derived parity gate compares both paths across representative periods and filters.
5. Any mismatch, gap, or incompatible version blocks promotion and appears as an explicit state rather than a plausible zero.

When explaining a filter such as `all`, show that it can be a read-time union of concrete groups instead of a duplicated stored total. Then explain how non-additive metrics preserve exactness during that union.
