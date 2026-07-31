---
name: frontend-orthography-check
description: Frontend orthography review and cleanup for changed user-visible UI text. Use when frontend changes add or modify copy, accessibility labels, messages, validation text, or locale sources that may contain misspellings, missing diacritics, punctuation slips, or broken characters.
disable-model-invocation: true
---

# Frontend Orthography Check

Polish spelling, not prose.

## 1. Bound and declare the surface

Resolve the comparison from the user, PR base, or merge-base with the default
branch. Inventory changed user-facing strings and inspect their enclosing UI
unit, not only added lines. Include messages, validation text, placeholders,
tooltips, `alt`, `title`, `aria-*`, screen-reader text, and manually maintained
locale sources.

Exclude generated translations and build output. Treat tests as downstream
expectations: update them when runtime copy changes, but do not count mirrored
test strings as separate corrections. Expand to the full frontend only when
requested.

The final report must state the comparison, inspected files or UI units, and
important exclusions on a `Scope:` line.

## 2. Run the candidate pass

From the target repository, run:

```bash
python <skill-root>/scripts/scan_ui_text.py --repo . --base <base-ref>
```

Pass explicit paths after the options when the user names a narrower surface.
The scanner reads complete changed frontend files so nearby copy is not missed.
It reports deterministic candidates for common missing diacritics, ambiguous
auxiliary forms such as `e`/`é` and `esta`/`está`, Spanish accents, and mojibake.

Treat scanner output as candidates, never automatic truth. Exit code 1 means
candidates were found; exit code 2 means the scan failed. If Python is
unavailable, reproduce the pass with repository search tools and report that
the deterministic scanner did not run.

## 3. Proofread in place

Detect each text's language and locale from application configuration and
local context. Inspect every changed string, its enclosing UI unit, and every
scanner candidate. Correct only high-confidence spelling, diacritics,
capitalization, punctuation, and character-encoding errors.

Preserve meaning, tone, terminology, language variant, interpolation, markup,
whitespace, file encoding, and line endings. Keep product names, technical
terms, identifiers, translation keys, URLs, and ambiguous wording unchanged.
Report uncertain encoding instead of rewriting it.

Count each corrected or proposed source occurrence once per orthographic span.
Repeated occurrences count separately; mirrored test expectations do not.

## 4. Apply and check

Apply safe corrections unless the user requested review-only. In review-only
mode, do not edit files. Inspect the resulting diff to confirm code structure
and runtime values are unchanged apart from copy and necessary test mirrors.

Run `git diff --check`. For edited code-bearing files, run the repository's
cheapest targeted parser, lint, or formatter. Run focused tests when exact copy
is asserted. Leave full suites to the main quality gate.

## 5. Report tightly

Always return the `Scope:` line followed by exactly one status line:

- Review-only: `ORTHOGRAPHY: REVIEW — <n> proposed, <u> uncertain`
- Applied, nothing unresolved: `ORTHOGRAPHY: PASS — <n> corrected`
- Applied with remaining issues: `ORTHOGRAPHY: CAVEAT — <n> corrected, <m> unresolved`

List at most three file-and-line examples. Add `+<r> more` when additional
occurrences remain. Counts must reconcile with all inspected source issues.
