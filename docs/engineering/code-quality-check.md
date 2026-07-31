# Code Quality Check

## Quickstart

```bash
npx skills@latest add joaovictornery-art/Skills --skill=code-quality-check
```

[Source](../../skills/engineering/code-quality-check)

## What it does

`code-quality-check` runs a risk-scaled gate over a complete solution. It
accounts for committed, staged, unstaged, and relevant untracked changes;
checks the implementation against repository standards and the originating
specification; runs focused deterministic validation; and reports separate
readiness decisions for a pull request and a deployment.

The default mode is review-only. It produces evidence-backed findings and
specific correction guidance without changing the solution.

## When to reach for it

Invoke `$code-quality-check` manually when a solution is approaching handoff,
pull request, release, or deployment and you need a decision backed by more
than code inspection alone.

It is deliberately user-invoked because the gate can run tests, builds, and
specialized risk checks. The model should not start that work implicitly.

## Validation tiers

- **Focused** is the default: changed-file lint, affected build or typecheck,
  focused tests, diff checks, and repository guards. It runs at most one
  command per applicable validation class and uses the narrowest affected
  scope.
- **Expanded** adds relevant full suites for cross-cutting or high-impact
  changes.
- **Deployment** adds target-environment prerequisites and smoke checks.

The tier escalates only when observed risk, repository policy, or the user
requires it. Results already observed in the same run are reused, and every
escalation has a recorded reason.

Validation commands are local and non-mutating by default. Deployments,
migrations, seeders, destructive or environment-connected tests, cloud CLIs,
and other commands that may write to external systems require explicit user
authorization.

## Risk profiles

The standard profile always applies. Additional profiles are loaded only when
the changed behavior involves AI, security, data operations, financial logic,
or production infrastructure.

## Output

Every finding includes severity, impact, evidence, reproduction, a recommended
correction, and a validation check. The final verdict is one of:

- `PASS`
- `PASS WITH CAVEATS`
- `BLOCKED`

Pull-request readiness and deployment readiness remain independent. The report
also includes elapsed duration, commands run, and tier escalation reasons so
quality coverage and operating cost can be calibrated over time.

## Where it fits

A code review asks whether the diff follows standards and implements the spec.
`code-quality-check` uses those axes inside a broader release decision that
also includes executable checks, specialized risks, diagnosis, residual risk,
and environment prerequisites.
