# Output Contract

List open findings first:

```text
[CQ-001][P0 | P1 | P2 | P3] <short title>
Problem: <what is wrong>
Impact: <what can happen and who is affected>
Evidence: <file/line, command output, or external prerequisite>
Reproduction: <deterministic signal or documented blocker>
Recommended correction: <specific implementation direction>
Recommended validation: <test or check that proves the correction>
Dependencies/decision: <required decision or "none">
```

Then report:

```text
Quality Gate: PASS | PASS WITH CAVEATS | BLOCKED
Tier: focused | expanded | deployment
Profiles: standard, ...
Fixed point: <ref>
Review mode: integrated | independent
Duration: <elapsed time>
Commands run: <count>
Tier escalations: <reason or "none">

Findings: <found> found, <fixed> fixed, <open> open
Validation:
- <check>: <result>

Checks not run:
- <check and reason, or "none">

Residual risks:
- <risk or "none">

Ready for PR: yes | no
Ready for deploy: yes | no
```

State every selected check that could not run and why. In review-only mode,
report `0 fixed` unless the reviewed solution already contains a verified
correction. Keep PR and deployment readiness independent.
