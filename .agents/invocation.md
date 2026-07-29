# Skill Invocation

Skills use one of two invocation policies.

## User-invoked

The human must name the skill explicitly. Use this for expensive gates,
consequential workflows, or choices that should remain under direct human
control.

```yaml
# SKILL.md
disable-model-invocation: true
```

```yaml
# agents/openai.yaml
policy:
  allow_implicit_invocation: false
```

## Model-invoked

The model may select the skill when its description matches the task. Omit both
manual-only controls and give the description concrete trigger language.

Catalogs must label every promoted skill consistently with its configured
policy.
