# Prepare Branch and Worktree

## Quickstart

```bash
npx skills@latest add joaovictornery-art/Skills --skill=prepare-branch-worktree
```

[Source](../../skills/engineering/prepare-branch-worktree)

## What it does

`prepare-branch-worktree` isolates one task on the correct Git branch while
preserving staged, unstaged, and untracked work. It inspects the intended base,
remote-tracking branch, active worktrees, naming conventions, and any merge,
rebase, cherry-pick, revert, or bisect already in progress.

The skill prefers the current worktree and creates or reuses a separate one
only when concurrent work needs isolation.

## When to reach for it

Invoke `$prepare-branch-worktree` manually before starting repository work or
before opening a pull request when work may be on the default branch, the wrong
branch, or mixed with another task.

It is deliberately user-invoked because branch and worktree operations change
repository state and should begin only on explicit command.

## Modes

- `start` establishes the task branch, intended base, and worktree before
  implementation.
- `pre-pr` verifies the final diff, base, tracking status, and isolation from
  unrelated work.

## Safety and output

The skill preserves the captured worktree state and blocks movement during an
active Git operation or when change ownership is ambiguous. Commit, push, pull
request, merge, and deploy remain separate actions.

It returns `READY`, `NEEDS ACTION`, or `BLOCKED` with only the Git state and
next required action needed to support the verdict.
