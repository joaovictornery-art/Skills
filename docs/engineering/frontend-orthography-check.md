# Frontend Orthography Check

## Quickstart

```bash
npx skills@latest add joaovictornery-art/Skills --skill=frontend-orthography-check
```

[Source](../../skills/engineering/frontend-orthography-check)

## What it does

`frontend-orthography-check` reviews changed user-facing frontend text without
rewriting the copy. It combines a deterministic candidate scan with contextual
proofreading for spelling, diacritics, capitalization, punctuation, and broken
character encoding.

The scanner reads complete changed frontend files, rather than only added
lines, so nearby labels, tooltips, accessibility text, and validation messages
are less likely to be missed. Candidates still require contextual confirmation.

## When to reach for it

Invoke `$frontend-orthography-check` manually after changing UI text or before
a pull request that includes user-facing frontend copy. Use review-only mode
when you want proposed corrections before changing files.

It is deliberately user-invoked because normal mode applies high-confidence
text corrections directly.

## Review surface

The default comparison comes from the user, PR base, or merge-base. The skill
inspects changed strings and their enclosing UI units, including messages,
validation text, placeholders, tooltips, `alt`, `title`, `aria-*`,
screen-reader text, and manually maintained locale sources.

Generated files are excluded. Tests may be updated when they mirror corrected
runtime copy, but those mirrors do not increase the correction count.

## Deterministic candidate scan

The bundled script has no third-party dependencies:

```bash
python scripts/scan_ui_text.py --repo /path/to/project --base origin/main
python scripts/scan_ui_text.py --repo /path/to/project frontend/src/components
python scripts/scan_ui_text.py --self-test
```

It flags common Portuguese and Spanish missing diacritics, contextual
`e`/`é` and `esta`/`está` cases, and common mojibake signatures. Its output is
a candidate list, not an automatic replacement command.

Exit code 0 means no candidates (or a passing self-test), 1 means candidates
were found, and 2 means the scan could not be completed.

## Output

Every result starts with a `Scope:` line and one status:

- `ORTHOGRAPHY: REVIEW — <n> proposed, <u> uncertain`
- `ORTHOGRAPHY: PASS — <n> corrected`
- `ORTHOGRAPHY: CAVEAT — <n> corrected, <m> unresolved`

Each count represents source occurrences. Mirrored test expectations are not
counted separately. Reports show at most three examples and summarize the rest.
