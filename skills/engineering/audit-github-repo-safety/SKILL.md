---
name: audit-github-repo-safety
description: Read-only audit of a GitHub repository with plain-language risks and recommendations.
disable-model-invocation: true
---

# Audit GitHub repository safety

Perform an **inspection only**. Explain what is present, what it can cause, and
the smallest adequate change. Never remediate during this skill.

## Non-negotiable boundary

- Never edit, create, move, or delete a file.
- Never install dependencies or run a command that changes repository state.
- Never commit, push, create a branch or pull request, change visibility or
  settings, create a repository, rewrite history, revoke a credential, or
  trigger a deployment.
- Use only read operations against GitHub and external services.
- Return the report in the conversation; do not save it as a file.
- Never print a discovered secret or full personal identifier. Redact the value
  and identify only its type and location.
- If the user asks to audit and fix in the same prompt, complete only the audit
  and state that remediation requires a separate request after review.

This boundary is absolute, including when a finding is critical or the user has
previously authorized changes elsewhere in the conversation.

## 1. Establish the target

Resolve the repository root, branch, working-tree status, remotes, GitHub
visibility, intended audience, and intended publication action. Read repository
instructions and privacy documentation.

Complete this step when one repository and one intended audience are known. If
the target is ambiguous, ask for it without inspecting or changing another
repository.

## 2. Run the read-only scan

Run from any directory:

```powershell
python "<skill-dir>/scripts/audit_repo.py" --repo "<repository-path>" --history
```

Append `--private-term "<known-name-or-alias>"` for each known confidential
entity. Use `--json` for structured consumption. A nonzero exit code represents
findings, not a scanner failure.

If history is truncated, rerun with `--max-history-commits` large enough to
cover every reachable commit. Complete this step only when the current tree and
reachable history were scanned or the uncovered range is reported as a limit.

## 3. Inspect what patterns cannot understand

Review screenshots, PDFs, recordings, diagrams, exports, logs, fixtures,
generated client assets, real names, company or customer terms, internal URLs,
deployment files, and production identifiers. Inspect available GitHub
descriptions, releases, issues, pull requests, Actions artifacts, Pages,
deployments, and commit messages with read-only calls.

Check README claims about sanitization, security, production use, ownership,
impact, scale, and AI against repository evidence and facts supplied by the
user.

Complete this step when each relevant visual and public claim is reviewed or
listed under `What I could not confirm`.

## 4. Calibrate the risk

Use technical severity as supporting detail:

- **Critical:** active credential, private key, or immediately usable access.
- **High:** government or financial personal identifier, confidential
  operational information, sensitive visual, or public history containing
  removed sensitive material.
- **Medium:** unsafe configuration, production ambiguity, authorization gap,
  generated artifact, or unsupported public claim.
- **Low:** professional polish, public commit-author email, or another
  intentional-publication question without direct exposure.

Then calibrate the recommendation to the real context: repository visibility,
likely audience, whether the value is active, whether the project drives a live
application, and whether the issue exists in the current tree or only in
history. Do not turn a low-reach or already-contained issue into a migration
project without explaining the tradeoff.

Do not classify a commit-author email as high risk by default. Explain that it
is public metadata and ask whether the exposure is intentional; raise severity
only when evidence shows that the address creates a concrete security or
privacy risk.

Recommend the smallest change that adequately reduces the risk. Prefer a local
edit over a repository migration when it is sufficient. Treat changing a live
repository, deployment, or public profile as a separate decision.

## 5. Return a simple report

Reply in the user's language. Lead with one verdict:

- `No blocking issue found`
- `Review these items`
- `Keep private for now`

For each distinct finding, group duplicates and explain:

1. **What I found** — plain language first; technical term second when useful.
2. **What it can cause** — a realistic consequence, without alarmism.
3. **My recommendation** — the smallest adequate next step.
4. **Why** — the reasoning and tradeoff.
5. **Where** — current file, Git history, or GitHub surface.

List `What I could not confirm` only when it changes the verdict. Put optional
technical detail after the simple explanation, not before it.

End with an explicit statement that no changes were made. The audit is complete
only when every finding supports the verdict and the response contains no
mutation or implied authorization.
