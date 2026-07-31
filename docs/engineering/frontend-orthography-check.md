# Frontend Orthography Check

## Quickstart

```bash
npx skills@latest add joaovictornery-art/Skills --skill=frontend-orthography-check
```

[Source](../../skills/engineering/frontend-orthography-check)

## What it does

`frontend-orthography-check` corrects high-confidence spelling, diacritics,
capitalization, punctuation, and character-encoding problems in changed
user-facing frontend text without rewriting the copy.

It works in the language and locale already present, preserves product and
technical terminology, and leaves generated translations untouched.

## When to reach for it

Invoke `$frontend-orthography-check` manually after changing UI text or before
a pull request that includes user-facing frontend copy.

It is deliberately user-invoked because it applies text corrections directly
and should not expand a frontend task implicitly.

## Review surface

The default surface is each changed string and its enclosing UI unit. It
includes messages, validation text, placeholders, tooltips, `alt`, `title`,
`aria-*`, and screen-reader text. A whole file is read only when local context
is insufficient; a full frontend audit requires an explicit request.

## Safety and output

The skill preserves meaning, language variant, interpolation, markup,
whitespace, encoding, and line endings. It runs diff integrity and the
cheapest targeted syntax check available for edited code-bearing files.

It returns `ORTHOGRAPHY: PASS` with the correction count or
`ORTHOGRAPHY: CAVEAT` with total unresolved items and up to three examples.
