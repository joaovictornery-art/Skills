# Critical Financial Profile

Make every amount reproducible from versioned inputs.

- Use explicit units, currency, rounding rule, effective date, and price
  version.
- Persist the rate snapshot used for historical calculations.
- Use integer minor or micro units for storage and aggregation.
- Treat missing rates, unknown SKUs, unsupported traffic types, and absent
  usage metadata as unpriced, never free.
- Separate estimated usage cost from invoiced cost, credits, taxes, discounts,
  and exchange-rate effects.
- Probe retries, duplicate events, refunds, reversals, partial processing,
  currency conversion, boundary rounding, and aggregation drift.
- For payment, accounting, balance, credit, and settlement flows, keep an
  immutable ledger as the source of truth; materialized summaries must be
  rebuildable.
- For estimators, pricing interfaces, and quota checks, require a versioned,
  deterministic calculation and reproducible inputs; do not require a ledger
  unless the result creates or changes a financial obligation.
- Reconcile aggregates against the provider billing export before calling the
  value actual cost.
