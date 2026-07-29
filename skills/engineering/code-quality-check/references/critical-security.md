# Critical Security Profile

Map each trust boundary from identity to persistence and response.

- Derive identity and role from authoritative server-side claims.
- Apply least privilege to callables, rules, service accounts, and cross-project
  access.
- Probe unauthenticated, wrong-domain, viewer, editor, admin, stale-claim, and
  cross-tenant callers.
- Validate and bound every external input before reads, model calls, or writes.
- Return the minimum data needed for the caller's role.
- Keep secrets, PII, tokens, raw prompts, and internal stack details out of
  logs, analytics, URLs, and client responses.
- Probe replay, duplicate submission, confused-deputy access, predictable IDs,
  and direct datastore access that bypasses authoritative services.
- Verify audit records identify the actor and action without copying sensitive
  source content.
