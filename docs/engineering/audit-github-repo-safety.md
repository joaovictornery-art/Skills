# Audit GitHub Repository Safety

## Quickstart

```bash
npx skills@latest add joaovictornery-art/Skills --skill=audit-github-repo-safety
```

[Source](../../skills/engineering/audit-github-repo-safety)

## What it does

`audit-github-repo-safety` performs a read-only review before a repository is
published or shared. It scans current files and reachable Git history, then
reviews visuals, confidential context, GitHub surfaces, and public claims that
automated patterns cannot interpret safely.

Its report explains each issue in plain language:

- what was found;
- what it can realistically cause;
- the smallest recommended change;
- why that recommendation fits the context;
- where the evidence is located.

## Read-only by design

The skill never edits files, installs dependencies, commits, pushes, creates a
pull request or repository, changes visibility or security settings, rewrites
history, rotates credentials, deletes data, or triggers a deployment.

This remains true even when a finding is critical or a prompt asks to audit and
fix at the same time. Remediation is a separate request made after the user has
reviewed the report.

## Risk calibration

The audit distinguishes current files from historical exposure and considers
repository visibility, likely audience, whether a credential is active, and
whether the repository drives a live application. It recommends the smallest
adequate correction instead of automatically escalating to migration or
history rewriting.

The response ends by confirming that no changes were made.
