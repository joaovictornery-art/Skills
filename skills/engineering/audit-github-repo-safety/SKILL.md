---
name: audit-github-repo-safety
description: Read-only audit of a GitHub repository with plain-language risks and recommendations.
disable-model-invocation: true
---

# Audit GitHub repository safety

Perform an **inspection only**. Explain what is present, what it can cause, and
the smallest adequate change. Confirm the repository scope before inspecting
anything, and never remediate during this skill.

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

## 1. Confirm the target and stop

Before any audit, identify only the repository candidate implied by the current
working directory. Use the folder name, repository root, and configured origin
URL when available; do not inspect repository contents, history, or GitHub
surfaces yet.

Ask one concise question in the user's language that names the candidate and
offers three scopes: this repository, another repository, or multiple
repositories. For example:

> It looks like I am in `<repository>`. Should I audit this repository, another
> one, or several? If another repository is involved, send its path or URL.

Always ask for this confirmation, even when the invocation already names a
repository. Then stop and wait for the user's reply. Do not combine the question
with scan results or begin the audit in the same turn.

Complete this gate only when the user has explicitly confirmed every target.

## 2. Establish the confirmed scope

For each confirmed repository, resolve the root, branch, working-tree status,
remotes, GitHub visibility, intended audience, and intended publication action.
Read repository instructions and privacy documentation.

Complete this step when every repository and its intended audience are known.
If the user confirmed several repositories, audit and report them separately so
evidence and recommendations do not get mixed.

## 3. Run the read-only scan

Prefer an independent cold-audit subagent when subagent tools are available
after the user confirms scope. Start it without conversation history or prior
implementation rationale, and pass only the confirmed repository path or URL,
intended audience/publication context, known private terms, and this skill's
read-only boundary. Require the subagent to return plain-language risks,
evidence locations, and uncertainty, with no remediation. Verify and calibrate
its findings before reporting them. Fall back to local inspection when
subagent tools are unavailable, the repository cannot be shared safely, or the
audit depends on credentials/session state only available locally.

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

## 4. Inspect what patterns cannot understand

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

## 5. Calibrate the risk

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

## 6. Return a simple report

Reply in the user's language. Lead with one verdict:

- `No blocking issue found`
- `Review these items`
- `Keep private for now`

For each distinct finding, group duplicates and explain:

1. **What I found** - plain language first; technical term second when useful.
2. **What it can cause** - a realistic consequence, without alarmism.
3. **My recommendation** - the smallest adequate next step.
4. **Why** - the reasoning and tradeoff.
5. **Where** - current file, Git history, or GitHub surface.

List `What I could not confirm` only when it changes the verdict. Put optional
technical detail after the simple explanation, not before it.

End with an explicit statement that no changes were made. The audit is complete
only when every finding supports the verdict and the response contains no
mutation or implied authorization.
