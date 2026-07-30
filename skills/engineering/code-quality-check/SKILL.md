---
name: code-quality-check
description: Review-only, risk-scaled quality gate with evidence-backed findings and separate PR/deploy readiness.
disable-model-invocation: true
---

# Code Quality Check

Run a risk-scaled quality gate over the complete solution. Default to
**review-only**: preserve repository state and return evidence, corrections,
and validation guidance. Enter fix mode only when the user explicitly asks to
apply corrections. Branch, commit, push, PR, merge, and deploy are separate
actions that each require an explicit request.

## 1. Pin the gate

1. Read applicable `AGENTS.md` files and the plan, ADR, issue, PRD, or recorded
   decisions that define the intended solution.
2. Resolve one fixed point, in order:
   - the ref supplied by the user;
   - the base of the current PR;
   - the merge-base with the repository default branch;
   - the empty tree for a repository with no usable history.
3. Ask for the fixed point only when available sources conflict.
4. Inventory committed, staged, unstaged, and relevant untracked changes.
   Record the dirty-worktree baseline and preserve unrelated changes.
5. Record the spec sources, standards sources, fixed point, diff commands, and
   validation commands used by the gate.

This step is complete when the comparison resolves, every changed file is
accounted for, and intended behavior has a source or an explicit spec gap.

## 2. Scale the gate

Always load [references/standard.md](references/standard.md). Load only the
profiles triggered by changed behavior:

- [critical-ai.md](references/critical-ai.md): model output, RAG, prompts,
  embeddings, agents, or consequential tool calls.
- [critical-security.md](references/critical-security.md): auth, IAM, secrets,
  PII, permissions, public endpoints, or trust boundaries.
- [critical-data.md](references/critical-data.md): migrations, backfills,
  schema changes, destructive scripts, or bulk writes.
- [critical-financial.md](references/critical-financial.md): prices, billing,
  payments, currencies, ledgers, quotas, or cost attribution.
- [critical-production.md](references/critical-production.md): deployment
  configuration, public routes, caches, schedulers, triggers, production
  logging, or fixtures.

Profiles are additive. Apply their invariants only to affected behavior; mark
an applicable invariant as an automated check, targeted probe, external
prerequisite, or `not applicable` with a concrete reason.

Choose one validation tier:

- **Focused** (default): run at most one command for each applicable validation
  class, always at the narrowest affected scope: changed-file lint, affected
  build/typecheck, focused tests, diff integrity, and required repository
  guards. Reuse results already observed in the current run.
- **Expanded**: focused checks plus relevant full suites. Use for cross-cutting
  changes, shared infrastructure, open `P0`/`P1`, an explicit repository rule,
  or a user request.
- **Deployment**: expanded checks plus target-environment prerequisites and
  smoke checks. Use only when deployment readiness is in scope and the target
  environment is accessible.

Do not run sibling-package or repository-wide suites when a focused equivalent
covers the changed behavior. Keep the selected tier unless observed risk
requires escalation, and record each escalation reason. Record higher-tier
checks as prerequisites rather than running them for completeness.

This step is complete when every changed behavior has a risk profile and the
validation tier has a stated reason.

## 3. Establish the baseline

Start an elapsed-time and command-count log before the first validation
command. Build one deduplicated command plan from the applicable validation
classes. A command that covers multiple classes counts once; do not run an
equivalent alternate command unless the first result is ambiguous.

Run only checks known to be local and non-mutating outside the worktree.
Deploys, migrations, seeders, destructive or environment-connected tests,
cloud CLIs, and commands that may write to a database or external service
require explicit user authorization. When command safety is unknown, do not
run it; record it as a check not run and state the missing assurance.

Run the selected deterministic checks once, cheapest and most focused first.
Classify each failure as introduced, pre-existing, or unknown; verify a
pre-existing claim against the fixed point when feasible. If a check creates
artifacts, account for them against the worktree baseline.

This step is complete when every selected check has an observed result and
every failure has a classification.

## 4. Review the solution

Load [references/review.md](references/review.md). Review the complete change
surface in one integrated pass by default, while keeping the Standards and
Spec axes distinct. Map each changed behavior to both axes and its profiles
during that pass; do not repeat file traversal separately for each axis. Use
independent parallel review only when the user asks for it.

For each plausible defect class, probe the closest boundary or failure path.
Expand to sibling inputs, roles, retries, or partial failures only when the
first probe produces a signal or the loaded profile requires it.

This step is complete when every changed behavior is covered by Standards,
Spec, and its loaded profiles, and every actionable finding has a ledger ID.

## 5. Diagnose blockers

For every `P0`, `P1`, and ambiguous `P2`, load
[references/diagnosis.md](references/diagnosis.md). In review-only mode, use
existing seams and non-mutating probes. Stop after three targeted probes per
finding when the signal remains unavailable; record the missing access or seam
instead of broadening the investigation indefinitely.

This step is complete when each investigated finding has a reproducible signal,
a confirmed or falsified root cause, or a precise blocker.

## 6. Recommend or fix

In review-only mode, give every finding its impact, evidence, reproduction
signal, concrete correction, validation check, and required decision or
external prerequisite.

In explicitly authorized fix mode:

1. Confirm the authorized ledger items when scope is ambiguous.
2. Add a regression test first when a correct seam exists.
3. Apply the smallest correction that closes the defect class.
4. Run the focused regression immediately and update the ledger.
5. Pause when the correction changes product semantics, data ownership, public
   behavior, or an architectural decision.

Preserve unrelated worktree changes. Fixing is complete when every authorized
finding is closed, accepted by the user, or blocked by a named prerequisite.

## 7. Close the gate

In review-only mode, reuse observed check results and confirm the worktree
matches its captured baseline except for user-authorized artifacts.

In fix mode, rerun each focused regression, then the checks made stale by the
fix. Run relevant full suites only when the selected tier requires them. Allow
at most two general closure rounds.

Return one verdict:

- `PASS`: no open `P0`-`P2`; all checks required by the selected tier pass.
- `PASS WITH CAVEATS`: no code blocker; only explicit pre-existing failures,
  higher-tier checks, unavailable non-code prerequisites, or deploy-only
  validation remains.
- `BLOCKED`: an open `P0`-`P2`, required failing check, unresolved product
  semantics, or missing prerequisite prevents a reliable decision.

Deployment readiness is `yes` only when deployment-tier prerequisites were
observed in the target environment or are demonstrably not applicable.

Load [references/output.md](references/output.md) and return its complete
contract. Closing is complete when the ledger, observed validations, checks not
run, residual risks, command count, elapsed duration, tier escalations, and
separate PR/deploy decisions support the verdict.
