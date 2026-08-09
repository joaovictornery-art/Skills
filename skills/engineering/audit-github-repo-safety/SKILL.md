---
name: audit-github-repo-safety
description: Manually gate a GitHub repository before public release or recruiter sharing.
disable-model-invocation: true
---

# Audit GitHub repository safety

Use this skill as a **release gate**. Apply the same evidence sequence on every run; a clean text scan alone never clears a repository for publication.

## Safety boundary

- Remain read-only by default.
- Never print a discovered secret or full personal identifier. Report its type and location with the value redacted.
- Do not commit, push, change visibility, rewrite history, delete a repository, rotate a credential, or create a replacement repository without explicit action-time approval.
- Before an external change, state the exact `owner/repository` and intended action.
- Treat user files and unrelated working-tree changes as out of scope.

## Release gate

### 1. Establish the target

Resolve the repository root, current branch, working-tree status, remotes, GitHub visibility, intended audience, and intended action. Read repository instructions such as `AGENTS.md`, `agents.md`, `CONTRIBUTING.md`, and privacy documentation.

This step is complete only when one local root and, when a remote exists, one `owner/repository` are identified. If either target or intended action is ambiguous, stop before any mutation and ask for the missing fact.

### 2. Scan the tree and every reachable commit

From any directory, run:

```powershell
python "<skill-dir>/scripts/audit_repo.py" --repo "<repository-path>" --history
```

Append one `--private-term "<known-name-or-alias>"` per known confidential entity. Use `--json` when another tool must consume the findings. A nonzero exit code means the audit found warnings or higher-severity candidates; inspect the report rather than treating it as a script failure.

The default history limit is 500 commits. If the report says the scan was truncated, count reachable commits and rerun with `--max-history-commits` high enough to cover all of them. The scanner detects candidates, not intent; verify every finding in context.

This step is complete only when the current tree and every reachable commit were scanned, or the uncovered range is explicitly reported as a release blocker.

### 3. Inspect semantic and visual evidence

Account for what patterns cannot judge:

- screenshots, recordings, PDFs, diagrams, exports, fixtures, seeds, logs, caches, and built frontend assets;
- real names, company marks, customer names, internal URLs, tenant identifiers, proprietary terminology, financial values, schedules, and operational data;
- `.env.example`, workflows, deployment files, mobile/web bundles, and generated assets that can embed client-side values;
- repository descriptions, topics, releases, issues, pull requests, Actions artifacts, Pages deployments, and commit messages when GitHub access is available.

Render PDFs page by page and open images. Review current files and historically removed visuals; an unreferenced tracked file remains downloadable. Search known private entity names together with aliases, product names, former names, and spelling variants. If no private-term list is available, record that semantic search limitation without treating the audit as clean evidence.

This step is complete only when every visual candidate is classified as reviewed, sensitive, intentionally public, or unavailable, and every available GitHub surface above is checked. Any unavailable mandatory evidence keeps the gate closed.

### 4. Reconcile public claims with evidence

Search the README and portfolio copy for claims such as:

- `sanitized`, `anonymous`, `privacy-aware`, or `secure`;
- `production`, `in daily use`, `deployed`, or `used by customers`;
- `AI agent`, `autonomous`, `evaluation`, `monitoring`, or `tested`;
- exclusive ownership, leadership, scale, savings, or performance metrics.

Verify each claim against the repository and facts supplied by the user. Downgrade or mark an unverified claim instead of strengthening it.

This step is complete only when every material security, privacy, production, ownership, impact, scale, and AI claim is supported, qualified, or removed.

### 5. Classify findings and close or block the gate

- **Critical:** active credential, private key, authentication secret, or immediately exploitable sensitive access.
- **High:** valid personal identifier, confidential company/customer data, sensitive screenshot, public history containing removed sensitive material, or false sanitization/security claim.
- **Medium:** unsafe configuration, authorization mismatch, tracked log/build artifact, missing privacy boundary, or unverified production/ownership claim.
- **Low:** professional polish or discoverability issue that does not create direct exposure.

For every finding, report severity, current-tree or history location, why it matters, safest remediation, and whether Codex can perform it with approval or an external owner must act.

Choose exactly one verdict:

- `Safe to publish`: no critical or high finding, every mandatory review completed, and no unresolved evidence gap.
- `Safe after listed fixes`: a bounded set of fixes can close every finding and evidence gap.
- `Keep private`: confidential history, active exposure, unavailable evidence, or an external decision prevents safe publication.

This step is complete only when every finding maps to the verdict and no critical exposure is buried under portfolio polish.

### 6. Remediate only when authorized

- For an exposed credential, contain public access when authorized, require revocation or rotation through its provider, remove it from the current tree, and clean history before republishing.
- For a personal identifier, making the repository private stops ordinary public access but does not undo prior exposure. Remove it from the current tree and prefer a new clean public snapshot.
- Do not claim that a force-push alone guarantees removal. Old commit URLs, forks, caches, releases, artifacts, or provider retention may preserve access.
- For confidential operational projects, keep the original repository private and publish a separate anonymized snapshot with fresh history.
- Re-scan the clean candidate before changing visibility to public.

This branch is complete only when each authorized fix is validated and the release gate is rerun from step 1. Never inherit the previous verdict after a mutation.

## Output format

Lead with the verdict, then provide:

1. prioritized findings;
2. current-tree versus Git-history exposure;
3. automated-scan limitations and manual checks completed;
4. `Codex can do now`;
5. `User or provider action required`;
6. exact validation needed before public release.
