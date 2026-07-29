# Critical Data Profile

Treat data changes as restartable operations with an audit trail.

- Start with a read-only or dry-run path that reports exact impact.
- Bound the first apply to one record, then progressive batches.
- Make retries and reruns idempotent.
- Preserve before/after evidence and a practical rollback path.
- Probe partial batch failure, process interruption, concurrent execution,
  stale reads, and schema versions from before and after the change.
- Validate tenant, locale, publication state, and ownership filters before
  writes.
- Keep destructive scope explicit and smaller than the selection scope.
- Verify indexes, access rules, readers, writers, exports, and historical
  records remain compatible with the new schema.
