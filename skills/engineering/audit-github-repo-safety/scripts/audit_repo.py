#!/usr/bin/env python3
"""Read-only repository safety scanner.

Findings are deliberately redacted. The script detects candidates; the skill
workflow supplies the required contextual and visual review.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Iterable


SKIP_DIRS = {
    ".git",
    "node_modules",
    ".npm-cache",
    ".pnpm-store",
    ".yarn",
    ".venv",
    "venv",
    "__pycache__",
}

TEXT_LIMIT = 2 * 1024 * 1024
VISUAL_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".pdf",
    ".mp4",
    ".mov",
    ".webm",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}
SENSITIVE_NAMES = {
    ".env",
    "credentials.json",
    "service-account.json",
    "serviceaccount.json",
    "firebase-adminsdk.json",
    "id_rsa",
    "id_ed25519",
}

TOKEN_PATTERNS = [
    ("private-key", "critical", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("github-token", "critical", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("openai-style-key", "critical", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("aws-access-key", "critical", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("google-api-key", "medium", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("stripe-live-key", "critical", re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{16,}\b")),
    ("slack-token", "critical", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
]

GENERIC_SECRET = re.compile(
    r"(?i)\b(api[_-]?key|client[_-]?secret|secret|token|password|private[_-]?key)\b"
    r"\s*[:=]\s*[\"']?([^\s\"'#;,]{8,})"
)
IDENTIFIER_CANDIDATE = re.compile(r"(?<!\d)(?:\d[.\s/-]?){10,14}(?!\d)")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
DUMMY_MARKERS = {
    "example",
    "placeholder",
    "changeme",
    "replace-me",
    "replace_me",
    "your-key",
    "your_key",
    "dummy",
    "fake",
    "test-token",
}


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=check,
    )


def digits(value: str) -> str:
    return "".join(character for character in value if character.isdigit())


def valid_cpf(value: str) -> bool:
    number = digits(value)
    if len(number) != 11 or len(set(number)) == 1:
        return False
    for position in (9, 10):
        total = sum(int(number[index]) * (position + 1 - index) for index in range(position))
        check_digit = (total * 10 % 11) % 10
        if check_digit != int(number[position]):
            return False
    return True


def valid_cnpj(value: str) -> bool:
    number = digits(value)
    if len(number) != 14 or len(set(number)) == 1:
        return False
    weights = ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    for position, weight in zip((12, 13), weights):
        total = sum(int(number[index]) * weight[index] for index in range(position))
        remainder = total % 11
        check_digit = 0 if remainder < 2 else 11 - remainder
        if check_digit != int(number[position]):
            return False
    return True


def looks_dummy(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in DUMMY_MARKERS)


def finding(severity: str, kind: str, location: str, message: str) -> dict[str, str]:
    return {
        "severity": severity,
        "kind": kind,
        "location": location,
        "message": message,
    }


def scan_text(
    text: str,
    location: str,
    *,
    scan_generic: bool = True,
    private_terms: Iterable[str] = (),
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    seen: set[tuple[str, int]] = set()

    for kind, severity, pattern in TOKEN_PATTERNS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            if (kind, line) in seen:
                continue
            seen.add((kind, line))
            findings.append(
                finding(severity, kind, f"{location}:{line}", "Potential secret detected; value redacted.")
            )

    if scan_generic:
        for match in GENERIC_SECRET.finditer(text):
            value = match.group(2)
            if (
                looks_dummy(value)
                or value.startswith(("${", "process.env", "import.meta.env", "os.environ"))
                or re.fullmatch(r"[A-Z][A-Z0-9_]+", value)
                or re.match(r"^[A-Za-z_$][A-Za-z0-9_.$]*\(", value)
            ):
                continue
            line = text.count("\n", 0, match.start()) + 1
            kind = "generic-secret-assignment"
            if (kind, line) not in seen:
                seen.add((kind, line))
                findings.append(
                    finding("high", kind, f"{location}:{line}", "Non-placeholder secret-like assignment; value redacted.")
                )

    for match in IDENTIFIER_CANDIDATE.finditer(text):
        candidate = match.group(0)
        kind = None
        if valid_cpf(candidate):
            kind = "brazilian-cpf"
        elif valid_cnpj(candidate):
            kind = "brazilian-cnpj"
        if kind:
            line = text.count("\n", 0, match.start()) + 1
            if (kind, line) not in seen:
                seen.add((kind, line))
                findings.append(
                    finding("high", kind, f"{location}:{line}", "Valid personal/company identifier detected; value redacted.")
                )

    for match in EMAIL_PATTERN.finditer(text):
        address = match.group(0).lower()
        if address.endswith(("@example.com", "@example.org", "@test.com")):
            continue
        line = text.count("\n", 0, match.start()) + 1
        kind = "email-address"
        if (kind, line) not in seen:
            seen.add((kind, line))
            findings.append(
                finding("low", kind, f"{location}:{line}", "Email address requires intentional-publication review; value redacted.")
            )

    for term in private_terms:
        normalized = term.strip()
        if not normalized:
            continue
        for match in re.finditer(re.escape(normalized), text, flags=re.IGNORECASE):
            line = text.count("\n", 0, match.start()) + 1
            kind = "configured-private-term"
            if (kind, line) not in seen:
                seen.add((kind, line))
                findings.append(
                    finding("high", kind, f"{location}:{line}", "Configured private term detected; value redacted.")
                )

    return findings


def iter_files(root: Path) -> Iterable[Path]:
    for current_root, directory_names, file_names in os.walk(root):
        directory_names[:] = [name for name in directory_names if name not in SKIP_DIRS]
        for name in file_names:
            yield Path(current_root) / name


def read_text_candidate(path: Path) -> str | None:
    try:
        if path.stat().st_size > TEXT_LIMIT:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data:
        return None
    return data.decode("utf-8", errors="replace")


def scan_worktree(root: Path, private_terms: Iterable[str]) -> tuple[list[dict[str, str]], list[str]]:
    findings: list[dict[str, str]] = []
    visuals: list[str] = []
    for path in iter_files(root):
        relative = path.relative_to(root).as_posix()
        lowered_name = path.name.lower()
        if path.suffix.lower() in VISUAL_SUFFIXES:
            visuals.append(relative)
        if lowered_name in SENSITIVE_NAMES or path.suffix.lower() in SENSITIVE_SUFFIXES:
            severity = "medium" if lowered_name.endswith(".example") else "high"
            findings.append(
                finding(severity, "sensitive-file", relative, "Sensitive filename requires review and should normally remain untracked.")
            )
        text = read_text_candidate(path)
        if text is not None:
            generated_bundle = relative.startswith(("dist/assets/", "build/assets/"))
            findings.extend(
                scan_text(
                    text,
                    relative,
                    scan_generic=not generated_bundle,
                    private_terms=private_terms,
                )
            )
    return findings, visuals


HISTORY_GREP = (
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----|"
    r"gh[pousr]_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9_-]{20,}|"
    r"(AKIA|ASIA)[0-9A-Z]{16}|"
    r"AIza[0-9A-Za-z_-]{30,}|"
    r"(sk|rk)_live_[0-9A-Za-z]{16,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"[0-9][0-9. /-]{9,17}[0-9]|"
    r"(api[_-]?key|client[_-]?secret|secret|token|password)[[:space:]]*[:=]"
)


def scan_history(
    root: Path,
    max_commits: int,
    private_terms: Iterable[str],
) -> tuple[list[dict[str, str]], bool]:
    findings: list[dict[str, str]] = []
    private_terms = tuple(term.strip() for term in private_terms if term.strip())
    commits_result = run(["git", "rev-list", "--all"], root)
    commits = [line for line in commits_result.stdout.splitlines() if line]
    truncated = len(commits) > max_commits
    commits = commits[:max_commits]
    dedupe: set[tuple[str, str]] = set()
    grep_patterns = ["-e", HISTORY_GREP]
    for term in private_terms:
        grep_patterns.extend(["-e", re.escape(term)])

    for commit in commits:
        result = run(
            ["git", "grep", "-I", "-n", "-i", "-E", *grep_patterns, commit, "--"],
            root,
            check=False,
        )
        if result.returncode not in (0, 1):
            continue
        for raw_line in result.stdout.splitlines():
            parts = raw_line.split(":", 3)
            if len(parts) != 4:
                continue
            _, path, line_number, content = parts
            location = f"history:{path}@{commit[:8]}"
            for item in scan_text(content, location, private_terms=private_terms):
                item["location"] = f"{location}:{line_number}"
                key = (item["kind"], path)
                if key in dedupe:
                    continue
                dedupe.add(key)
                findings.append(item)
                if len(findings) >= 200:
                    return findings, True

    names = run(["git", "log", "--all", "--name-only", "--pretty=format:"], root).stdout.splitlines()
    for path in sorted(set(name.strip() for name in names if name.strip())):
        candidate = Path(path)
        if candidate.name.lower() in SENSITIVE_NAMES or candidate.suffix.lower() in SENSITIVE_SUFFIXES:
            key = ("historical-sensitive-file", path)
            if key not in dedupe:
                dedupe.add(key)
                findings.append(
                    finding("high", "historical-sensitive-file", f"history:{path}", "Sensitive filename exists in reachable Git history.")
                )
        if candidate.suffix.lower() in VISUAL_SUFFIXES:
            key = ("historical-visual-file", path)
            if key not in dedupe:
                dedupe.add(key)
                removed = not (root / candidate).exists()
                findings.append(
                    finding(
                        "high" if removed else "medium",
                        "historical-visual-file",
                        f"history:{path}",
                        "Removed visual remains in reachable history and requires manual review."
                        if removed
                        else "Visual file exists in reachable history and requires manual review.",
                    )
                )

    return findings, truncated


def find_gh() -> str | None:
    executable = shutil.which("gh")
    if executable:
        return executable
    if os.name == "nt":
        candidate = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "GitHub CLI" / "gh.exe"
        if candidate.exists():
            return str(candidate)
    return None


def github_visibility(root: Path) -> dict[str, object] | None:
    executable = find_gh()
    if not executable:
        return None
    result = run(
        [executable, "repo", "view", "--json", "nameWithOwner,visibility,isPrivate,url"],
        root,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def severity_key(item: dict[str, str]) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(item["severity"], 4)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Git repository safety scan")
    parser.add_argument("--repo", default=".", help="Path inside the Git repository")
    parser.add_argument("--history", action="store_true", help="Scan reachable Git history")
    parser.add_argument("--max-history-commits", type=int, default=500)
    parser.add_argument(
        "--private-term",
        action="append",
        default=[],
        help="Known confidential name or alias to find without echoing its value",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    requested = Path(args.repo).expanduser().resolve()
    if not requested.is_dir():
        print("Repository path is not an accessible directory", file=sys.stderr)
        return 3
    result = run(["git", "rev-parse", "--show-toplevel"], requested, check=False)
    if result.returncode != 0:
        print("Not a Git repository", file=sys.stderr)
        return 3
    root = Path(result.stdout.strip()).resolve()

    findings, visuals = scan_worktree(root, args.private_term)
    history_truncated = False
    if args.history:
        history_findings, history_truncated = scan_history(
            root,
            args.max_history_commits,
            args.private_term,
        )
        findings.extend(history_findings)

    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for item in findings:
        unique[(item["severity"], item["kind"], item["location"])] = item
    findings = sorted(unique.values(), key=lambda item: (severity_key(item), item["location"]))

    status = run(["git", "status", "--short"], root).stdout.splitlines()
    remote = run(["git", "remote", "get-url", "origin"], root, check=False).stdout.strip() or None
    visibility = github_visibility(root)
    counts = {level: sum(item["severity"] == level for item in findings) for level in ("critical", "high", "medium", "low")}

    report = {
        "repository": str(root),
        "remote": remote,
        "github": visibility,
        "working_tree_changes": status,
        "history_scanned": bool(args.history),
        "history_scan_truncated": history_truncated,
        "configured_private_term_count": len(args.private_term),
        "counts": counts,
        "findings": findings,
        "visual_files_for_manual_review": sorted(visuals),
        "manual_review_required": [
            "Real names, brands, customers, internal URLs and proprietary terminology",
            "Screenshots, PDFs, recordings, logs, fixtures, seeds and built client assets",
            "README claims about sanitization, security, production, AI, ownership and impact",
            "GitHub issues, PRs, releases, artifacts, Pages deployments, forks and caches",
        ],
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Repository: {root}")
        print(f"Remote: {remote or 'not configured'}")
        if visibility:
            print(f"GitHub: {visibility.get('nameWithOwner')} ({visibility.get('visibility')})")
        print("Findings: " + ", ".join(f"{level}={counts[level]}" for level in counts))
        for item in findings:
            print(f"[{item['severity'].upper()}] {item['kind']} | {item['location']} | {item['message']}")
        if visuals:
            print("Manual visual review:")
            for path in sorted(visuals):
                print(f"- {path}")
        if history_truncated:
            print("[MEDIUM] History scan was truncated; increase --max-history-commits.")

    if counts["critical"] or counts["high"]:
        return 2
    if counts["medium"] or counts["low"] or history_truncated:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
