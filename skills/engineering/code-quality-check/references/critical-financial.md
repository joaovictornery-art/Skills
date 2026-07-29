# Critical Financial Profile

Make every amount reproducible from immutable inputs.

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
- Keep an immutable ledger as the source of truth; materialized summaries must
  be rebuildable.
- Reconcile aggregates against the provider billing export before calling the
  value actual cost.
