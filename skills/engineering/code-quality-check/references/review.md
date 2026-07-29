# Review Reference

Review each changed behavior along two axes. Keep their evidence and findings
distinct even when one defect appears in both.

## Standards

Apply repository rules from `AGENTS.md`, `CONTRIBUTING.md`, coding standards,
ADRs, and enforced architecture. Then apply the loaded risk profiles.

Treat tool-enforced formatting as validation evidence, not a manual finding.
Treat design smells as judgment calls unless they create a concrete correctness
or maintenance risk:

- unclear domain names;
- duplicated behavior or contract definitions;
- domain concepts represented by unbounded primitives;
- repeated conditionals on the same type or role;
- one logical change scattered across unrelated modules;
- abstractions or hooks not required by the spec;
- callers navigating through another module's internals.

For each finding, cite the rule or name the heuristic and quote the changed
behavior that triggers it.

## Spec

Trace each intended behavior to a requirement or recorded decision. Report:

- missing or partial requirements;
- behavior not requested by the spec;
- implemented requirements whose behavior is incorrect;
- ambiguous semantics that require a product decision.

Quote or precisely identify the source requirement. When no authoritative spec
exists, record the gap and evaluate only observable contracts; do not invent
product intent.

## Coverage

Account for every changed file, but organize findings by behavior rather than
file count. Probe boundaries required by the loaded profiles. A clean review
means every changed behavior was checked on both axes, not that every heuristic
produced a comment.

Maintain:

```text
ID | Axis/Profile | Severity | Evidence | Repro | Correction | Validation | Status
```

- `P0`: immediate release, security, or data-loss risk.
- `P1`: high-impact correctness or production risk.
- `P2`: normal correctness issue or meaningful missing coverage.
- `P3`: non-blocking improvement.
