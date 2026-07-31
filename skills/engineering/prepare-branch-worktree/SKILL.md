---
name: prepare-branch-worktree
description: "Git isolation for starting work or preparing a PR: inspect branches and worktrees, place changes on a task branch, and verify its base and remote-tracking branch. Use when work began on the default or wrong branch, tasks are mixed, concurrent work needs a worktree, or a PR needs branch readiness."
disable-model-invocation: true
---

# Prepare Branch and Worktree

Give one task one branch; add a worktree only for concurrent isolation.

## 1. Pin the state

Read repository instructions. Inspect the repository root; current, default, and intended base branches; HEAD; remote-tracking branch; staged/unstaged/untracked changes; local naming conventions; and `git worktree list --porcelain`, including locked or prunable entries. Detect an active merge, rebase, cherry-pick, revert, or bisect. Treat the intended base and remote-tracking branch as separate facts.

Infer the task from the conversation. Choose `start` mode for isolating active work and `pre-pr` mode for checking completed work. An active Git operation blocks branch/worktree movement; preserve its state and report it. This step is complete when every current change and relevant worktree has an owner or is marked ambiguous, and the operation state is known.

## 2. Choose the smallest safe move

- Keep a dedicated, correctly based task branch in its current worktree.
- On the default branch with task changes, create the task branch in place so the working tree stays intact.
- Prefer the current worktree. Use a separate one only for concurrent isolation; follow the repository's location convention and reuse an existing worktree for the branch.
- Follow established branch naming. Otherwise use `<type>/<short-kebab-task>` with the narrowest fitting type.
- When changes from different tasks are entangled, present the split and obtain direction before moving them.

This step is complete when one destination accounts for the entire intended task without absorbing unrelated changes.

## 3. Apply the move

Use non-destructive Git operations and preserve staged state and untracked files. Reinspect immediately after each branch or worktree operation. Obtain explicit approval before discarding changes, rewriting history, deleting a branch/worktree, or moving ambiguous changes. Treat commit, push, PR, merge, and deploy as separate requests.

This step is complete when the intended changes exist on the selected task branch and all baseline changes remain accounted for.

## 4. Close the mode

In `start` mode, confirm the task branch, intended base, worktree path, and separation from other active work.

In `pre-pr` mode, also confirm the branch is not the default branch, its diff targets the intended base, no unrelated changes are included, and its remote-tracking status is known. A missing remote-tracking branch requires a separate push action.

Return:

- `READY` when isolation and all checks for the selected mode are satisfied.
- `NEEDS ACTION` when the destination is clear but a separate or unauthorized action remains.
- `BLOCKED` when a Git operation, ambiguous ownership, or unresolved destination prevents a safe move.

Follow the verdict only with branch, base, tracking branch, worktree, dirty-state summary, and next required action. The gate is complete when the verdict is supported by a fresh Git inspection.
