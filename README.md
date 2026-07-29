# Skills

Agent skills I use to make engineering work more predictable, reviewable, and
safe.

The repository follows the same broad organization as
[`mattpocock/skills`](https://github.com/mattpocock/skills): skills live in
purpose-based buckets, promoted skills have human-facing documentation, and
user-invoked skills are kept distinct from model-invoked skills.

## Installation

Install a skill with an Agent Skills-compatible installer:

```bash
npx skills@latest add joaovictornery-art/Skills
```

Choose the skills and agent harnesses during installation. Access to this
repository is required while it remains private.

## Reference

### Engineering

Skills for code and release work.

**User-invoked**

- **[code-quality-check](./skills/engineering/code-quality-check/SKILL.md)** —
  Run a risk-scaled, review-only quality gate and report separate PR and deploy
  readiness.

**Model-invoked**

- None yet.

### Productivity

General workflow skills.

- None yet.

## Repository layout

```text
skills/
├── engineering/   # Daily code and release work
├── productivity/  # General workflow tools
├── misc/          # Useful but not promoted
├── personal/      # Tied to a personal setup
├── in-progress/   # Drafts not ready to publish
└── deprecated/    # Retired skills kept for history

docs/               # Human-facing pages for promoted skills
```

Each skill is a self-contained directory with a required `SKILL.md` and any
optional `agents/`, `references/`, `scripts/`, or `assets/` it needs.
