# Standard Profile

Apply this profile to every gate.

## Scope and intent

- Account for every changed file and behavior, including generated artifacts.
- Trace each behavior to the spec or mark the spec gap.
- Detect partial implementation, stale UI states, dead controls, and contract
  drift between callers and callees.

## Correctness boundaries

For each changed contract, select the closest meaningful boundary or failure
path: empty/one/maximum input, duplicate submission, retry, timeout,
cancellation, partial failure, concurrent caller, stale state, or interrupted
recovery. Expand to sibling cases when the first probe produces a signal, the
change is cross-cutting, or another loaded profile requires it.

Check error translation at trust boundaries. Internal diagnostics may be
specific; user-visible errors must be stable and safe.

## Ownership and contracts

- Keep authorization at the authoritative server boundary.
- Keep idempotency and transactional invariants at the owning backend boundary.
- Preserve published or immutable state while replacements are prepared.
- Verify callers, payloads, persistence, indexes, and access rules describe the
  same contract.

## Verification

- Prefer regression tests at the real call-site seam.
- Match test breadth to blast radius.
- Treat skipped tests as explicit evidence, not a pass.
- Check observability for failures operators must distinguish.
- Check that production artifacts exclude demo data, test fixtures,
  credentials, and debug instrumentation.
