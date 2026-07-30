#!/usr/bin/env python3
"""Validate repository conventions without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
PROMOTED_BUCKETS = {"engineering", "productivity"}
LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
LOCAL_PATH_PATTERNS = (
    re.compile(r"(?i)\b[a-z]:[\\/](?:users|documents|desktop)[\\/]"),
    re.compile(r"(?i)/(?:users|home)/[^/\s]+/"),
)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return {}


def markdown_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
        return None

    path_part = unquote(target.split("#", 1)[0])
    if not path_part:
        return None
    return (source.parent / path_part).resolve()


def validate_markdown_links(errors: list[str]) -> None:
    for source in ROOT.rglob("*.md"):
        text = source.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = markdown_target(source, match.group(1))
            if target is not None and not target.exists():
                errors.append(
                    f"{source.relative_to(ROOT)}: unresolved link "
                    f"{match.group(1)!r}"
                )


def validate_skill(skill_file: Path, errors: list[str]) -> None:
    skill_root = skill_file.parent.resolve()
    relative_skill = skill_file.relative_to(ROOT)
    metadata = frontmatter(skill_file)
    name = metadata.get("name")

    if not metadata:
        errors.append(f"{relative_skill}: missing or invalid frontmatter")
        return
    if name != skill_root.name:
        errors.append(
            f"{relative_skill}: name {name!r} must match directory "
            f"{skill_root.name!r}"
        )
    if not metadata.get("description"):
        errors.append(f"{relative_skill}: missing description")

    package_files = [
        path
        for path in skill_root.rglob("*")
        if path.is_file()
        and path.suffix.lower()
        in {".md", ".yaml", ".yml", ".json", ".py", ".ps1", ".sh"}
    ]
    for source in package_files:
        text = source.read_text(encoding="utf-8")
        for pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"{source.relative_to(ROOT)}: contains an absolute local path"
                )
                break
        if source.suffix.lower() != ".md":
            continue
        for match in LINK_RE.finditer(text):
            target = markdown_target(source, match.group(1))
            if target is not None and not target.is_relative_to(skill_root):
                errors.append(
                    f"{source.relative_to(ROOT)}: dependency escapes skill root "
                    f"via {match.group(1)!r}"
                )

    openai_yaml = skill_root / "agents" / "openai.yaml"
    openai_text = (
        openai_yaml.read_text(encoding="utf-8") if openai_yaml.exists() else ""
    )
    manual_skill = metadata.get("disable-model-invocation", "").lower() == "true"
    manual_policy = bool(
        re.search(r"(?m)^\s*allow_implicit_invocation:\s*false\s*$", openai_text)
    )
    if manual_skill != manual_policy:
        errors.append(
            f"{relative_skill}: manual-invocation controls are not aligned"
        )
    if openai_text and name and f"${name}" not in openai_text:
        errors.append(
            f"{openai_yaml.relative_to(ROOT)}: default prompt must mention ${name}"
        )

    bucket = skill_file.parent.parent.name
    if bucket not in PROMOTED_BUCKETS or not name:
        return

    root_catalog = (ROOT / "README.md").read_text(encoding="utf-8")
    bucket_catalog_path = ROOT / "skills" / bucket / "README.md"
    bucket_catalog = bucket_catalog_path.read_text(encoding="utf-8")
    root_link = f"./skills/{bucket}/{name}/SKILL.md"
    bucket_link = f"./{name}/SKILL.md"
    docs_path = ROOT / "docs" / bucket / f"{name}.md"

    if root_link not in root_catalog:
        errors.append(f"{relative_skill}: missing from root README catalog")
    if bucket_link not in bucket_catalog:
        errors.append(f"{relative_skill}: missing from {bucket_catalog_path.relative_to(ROOT)}")
    if not docs_path.exists():
        errors.append(f"{relative_skill}: missing {docs_path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    skill_files = sorted((ROOT / "skills").glob("*/*/SKILL.md"))

    if not skill_files:
        errors.append("no skills found")
    for skill_file in skill_files:
        validate_skill(skill_file, errors)
    validate_markdown_links(errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Repository validation passed: {len(skill_files)} skill(s), "
        "catalogs, invocation metadata, package boundaries, and links."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
