# Audit GitHub Repository Safety

## Quickstart

```bash
npx skills@latest add joaovictornery-art/Skills --skill=audit-github-repo-safety
```

[Source](../../skills/engineering/audit-github-repo-safety)

## What it does

`audit-github-repo-safety` is a release gate for repositories that may become
public or be shared with recruiters. It combines a redacted deterministic scan
with a mandatory semantic review of repository history, screenshots, PDFs,
generated assets, GitHub surfaces, and public claims.

The included scanner detects secret candidates, sensitive filenames, valid
Brazilian CPF and CNPJ values, email addresses, visual files that need review,
and confidential names or aliases supplied with `--private-term`. Detected
values are never printed in the report.

## When to reach for it

Invoke `$audit-github-repo-safety` manually before making a repository public,
sharing it as portfolio evidence, or publishing a sanitized replacement.

The skill is deliberately user-invoked because visibility changes, history
rewrites, credential rotation, deletion, and publication require explicit
authorization at action time.

## Release gate

The gate scans the current tree and every reachable commit, then requires each
visual candidate and available GitHub surface to be accounted for. It also
checks that claims about privacy, production use, ownership, impact, and AI are
supported by evidence.

It returns one verdict:

- `Safe to publish`
- `Safe after listed fixes`
- `Keep private`

A clean text scan cannot produce `Safe to publish` while semantic or visual
evidence remains unreviewed.

## Safety boundary

The skill is read-only by default. It redacts findings and does not commit,
push, change visibility, rewrite history, delete data, rotate credentials, or
create a replacement repository without explicit action-time approval.

For operational or confidential history, it prefers retaining the original as
a private archive and publishing a separate sanitized repository with fresh
history.
