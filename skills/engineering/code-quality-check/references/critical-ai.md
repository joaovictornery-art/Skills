# Critical AI Profile

Select controls by model behavior; model use alone does not make every control
applicable.

## Grounded claims

Apply this section when output makes factual, procedural, navigational, policy,
approval, or product claims, or when RAG is intended to ground the response.

- Trace each consequential claim to approved evidence.
- Probe a supported clause followed by an invented clause in the same output.
- Probe claims in headings, lists, tables, code blocks, summaries, and content
  near configured limits.
- Treat style examples as style-only unless approved as evidence.
- Fail closed when required evidence is absent, truncated, stale, or from the
  wrong tenant, language, portal, group, or target.
- Verify generated URLs, IDs, menu paths, rules, and approval claims cannot be
  invented.

For classification, extraction, transformation, creative output, or code
generation, require source grounding only when the product contract requires
it. Otherwise validate the relevant schema, constraints, deterministic
postconditions, and fallback behavior.

## Prompt and data safety

- Probe prompt injection in user-controlled and retrieved fields that can alter
  instructions, evidence selection, or tool behavior.
- Remove PII before prompting, logging, persistence, and error reporting when
  the product contract does not require it.
- Keep prompts, response bodies, secrets, session IDs, and direct identifiers
  out of logs and user-visible diagnostics.

## Execution semantics

- Probe retries, timeouts, duplicate requests, partial batches, validation
  rejection after a billable response, and interrupted-run recovery where
  those paths exist.
- Verify idempotency across consequential model calls and persistence.
- Record the model/config version, prompt version, attempts, token classes,
  latency, outcome, and stable error code when operational traceability
  requires them.
- Treat missing usage metadata and unknown pricing as `unknown`, never zero.

## Human control and production

- Preserve required human approval before publication or consequential action.
- Bound tool calls and external mutations to the approved product behavior.
- Keep fixtures and demo-generated content unreachable in production.
- Record model/config drift and external IAM as deployment prerequisites.
