# Critical Production Profile

Prove release behavior separately from local correctness.

- Validate required environment variables are defined and non-empty in the
  actual build and deploy environment.
- Verify service-account IAM, external project access, model availability,
  indexes, secrets, and billing prerequisites.
- Give public routes explicit cache policy, bounded instances, and safe error
  responses.
- Give triggers relevant-field guards, idempotency, and cascade protection.
- Give schedulers justified frequency, bounded work, retry safety, and an
  operator-visible owner.
- Keep hot-path logging bounded and useful.
- Verify production builds reject fixtures, demo flags, test credentials, and
  localhost dependencies.
- Record rollback steps and post-deploy smoke checks by persona.
- Mark deploy readiness false until every environment-only prerequisite is
  observed in the target environment.
