Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code and release work
- `productivity/` — general workflow tools
- `misc/` — useful but not promoted
- `personal/` — tied to a personal setup
- `in-progress/` — drafts not ready to publish
- `deprecated/` — retired skills kept for history

Every promoted skill in `engineering/` or `productivity/` must appear in the
top-level `README.md` and its bucket `README.md`. It must also have a
human-facing page at `docs/<bucket>/<skill-name>.md`.

Non-promoted skills in `misc/`, `personal/`, `in-progress/`, or `deprecated/`
must not appear in the promoted catalog and do not require a docs page.

Catalogs group promoted skills into **User-invoked** and **Model-invoked**.
A user-invoked skill carries both:

- `disable-model-invocation: true` in `SKILL.md`;
- `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

A model-invoked skill omits both controls and gives its `description` concrete
trigger language.

Each skill must be self-contained. Use relative paths from the skill root,
keep references one level deep, and exclude local absolute paths, credentials,
private project names, and undeclared dependencies on other skill packages.

When adding or changing a promoted skill:

1. Update the skill and its local resources.
2. Update its human-facing docs page.
3. Update the bucket and top-level catalogs.
4. Verify every relative link resolves.
5. Confirm user/model invocation metadata remains intentional.
6. Run `python scripts/validate_repo.py`.
