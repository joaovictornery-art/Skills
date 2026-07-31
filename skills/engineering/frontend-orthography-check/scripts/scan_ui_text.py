#!/usr/bin/env python3
"""Find deterministic orthography candidates in changed frontend files."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


UI_SUFFIXES = {
    ".astro", ".html", ".htm", ".js", ".jsx", ".json", ".mdx",
    ".svelte", ".ts", ".tsx", ".vue",
}
EXCLUDED_PARTS = {
    ".git", ".next", ".nuxt", "__tests__", "build", "coverage", "dist",
    "generated", "node_modules", "out", "storybook-static",
}
EXCLUDED_NAME_RE = re.compile(r"(?:\.test|\.spec|\.snap)\.[^.]+$", re.IGNORECASE)
MOJIBAKE_RE = re.compile(r"(?:Ã.|Â.|â€.|ï¿½|�)")

WORD_SUGGESTIONS = {
    "acao": "ação", "acoes": "ações", "alteracao": "alteração",
    "alteracoes": "alterações", "antecedencia": "antecedência",
    "atualizacao": "atualização", "atualizacoes": "atualizações",
    "comparacao": "comparação", "comparacoes": "comparações",
    "comunicacao": "comunicação", "comunicacoes": "comunicações",
    "configuracao": "configuração", "configuracoes": "configurações",
    "conteudo": "conteúdo", "conteudos": "conteúdos",
    "correcao": "correção", "correcoes": "correções",
    "criacao": "criação", "descricao": "descrição",
    "descricoes": "descrições", "disponivel": "disponível",
    "disponiveis": "disponíveis", "edicao": "edição",
    "edicoes": "edições", "endereco": "endereço",
    "elegivel": "elegível", "elegiveis": "elegíveis",
    "exibicao": "exibição", "ha": "há", "historico": "histórico",
    "horario": "horário", "horarios": "horários",
    "informacao": "informação",
    "informacoes": "informações", "invalida": "inválida",
    "invalidas": "inválidas", "invalido": "inválido",
    "invalidos": "inválidos", "nao": "não",
    "notificacao": "notificação", "notificacoes": "notificações",
    "observacao": "observação", "observacoes": "observações",
    "opcao": "opção", "opcoes": "opções", "operacao": "operação",
    "operacoes": "operações", "pagina": "página", "paginas": "páginas",
    "periodo": "período", "periodos": "períodos",
    "permissao": "permissão", "permissoes": "permissões",
    "possivel": "possível", "proprietario": "proprietário",
    "proprietarios": "proprietários", "publicacao": "publicação",
    "publicacoes": "publicações", "rapida": "rápida",
    "rapidas": "rápidas", "rapido": "rápido", "rapidos": "rápidos",
    "relatorio": "relatório", "relatorios": "relatórios",
    "reune": "reúne", "revisao": "revisão", "seguranca": "segurança",
    "titulo": "título", "titulos": "títulos", "traducao": "tradução",
    "validacao": "validação", "validacoes": "validações",
    "traducoes": "traduções", "unica": "única", "unicas": "únicas",
    "unico": "único", "unicos": "únicos", "versao": "versão",
    "versoes": "versões", "visao": "visão", "visualizacao": "visualização",
    "visualizacoes": "visualizações", "visivel": "visível",
    "visiveis": "visíveis", "voce": "você", "ja": "já",
    "consolidacao": "consolidação", "decisao": "decisão",
    "decisoes": "decisões", "atribuida": "atribuída",
    "atribuidas": "atribuídas", "aparecerao": "aparecerão",
    "proxima": "próxima", "proximas": "próximas",
    # Common Spanish UI copy.
    "comparacion": "comparación", "descripcion": "descripción",
    "mas": "más", "operacion": "operación", "traduccion": "traducción",
    "vision": "visión",
}
WORD_RE = re.compile(
    r"\b(" + "|".join(sorted(map(re.escape, WORD_SUGGESTIONS), key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)
AUXILIARY_RULES = (
    (
        re.compile(
            r"\besta\b(?=\s+(?:agendad[oa]s?|publicad[oa]s?|dispon[ií]ve(?:l|is)|pront[oa]s?))",
            re.IGNORECASE,
        ),
        "está",
        "auxiliary-estar",
    ),
    (
        re.compile(
            r"\be\b(?=\s+(?:compartilhad[oa]s?|obrigat[oó]ri[oa]s?|opciona(?:l|is)))",
            re.IGNORECASE,
        ),
        "é",
        "copula-ser",
    ),
)


@dataclass(frozen=True)
class Candidate:
    path: str
    line: int
    column: int
    matched: str
    suggestion: str
    rule: str
    text: str


def preserve_case(source: str, suggestion: str) -> str:
    if source.isupper():
        return suggestion.upper()
    if source[:1].isupper():
        return suggestion[:1].upper() + suggestion[1:]
    return suggestion


def scan_line(path: str, line_number: int, line: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    seen: set[tuple[int, int, str]] = set()

    def add(
        match: re.Match[str],
        suggestion: str,
        rule: str,
        preserve_source_case: bool = True,
    ) -> None:
        replacement = (
            preserve_case(match.group(0), suggestion)
            if preserve_source_case
            else suggestion
        )
        key = (match.start(), match.end(), replacement)
        if key in seen:
            return
        seen.add(key)
        candidates.append(Candidate(
            path=path,
            line=line_number,
            column=match.start() + 1,
            matched=match.group(0),
            suggestion=replacement,
            rule=rule,
            text=line.strip(),
        ))

    for match in WORD_RE.finditer(line):
        add(match, WORD_SUGGESTIONS[match.group(0).lower()], "missing-diacritic")
    for pattern, suggestion, rule in AUXILIARY_RULES:
        for match in pattern.finditer(line):
            add(match, suggestion, rule)
    for match in MOJIBAKE_RE.finditer(line):
        add(match, "inspect encoding", "mojibake", preserve_source_case=False)

    return sorted(candidates, key=lambda item: item.column)


def run_git(repo: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    return [line for line in result.stdout.splitlines() if line]


def default_base(repo: Path) -> str:
    for candidate in ("origin/main", "origin/master", "main", "master"):
        try:
            run_git(repo, "rev-parse", "--verify", candidate)
            return candidate
        except subprocess.CalledProcessError:
            continue
    raise RuntimeError("Could not resolve a default branch; pass --base explicitly.")


def changed_paths(repo: Path, base: str) -> list[Path]:
    merge_base = run_git(repo, "merge-base", "HEAD", base)[0]
    tracked = run_git(repo, "diff", "--name-only", "--diff-filter=ACMR", merge_base, "--")
    untracked = run_git(repo, "ls-files", "--others", "--exclude-standard")
    return [repo / value for value in dict.fromkeys([*tracked, *untracked])]


def explicit_paths(repo: Path, values: Iterable[str]) -> list[Path]:
    selected: list[Path] = []
    for value in values:
        path = (repo / value).resolve()
        if path.is_dir():
            selected.extend(candidate for candidate in path.rglob("*") if candidate.is_file())
        elif path.is_file():
            selected.append(path)
    return selected


def eligible(path: Path) -> bool:
    return (
        path.suffix.lower() in UI_SUFFIXES
        and not EXCLUDED_NAME_RE.search(path.name)
        and not any(part.lower() in EXCLUDED_PARTS for part in path.parts)
    )


def scan_files(repo: Path, paths: Iterable[Path]) -> list[Candidate]:
    results: list[Candidate] = []
    for path in sorted({item.resolve() for item in paths if eligible(item)}):
        try:
            relative = path.relative_to(repo.resolve()).as_posix()
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError, ValueError):
            continue
        for number, line in enumerate(lines, start=1):
            results.extend(scan_line(relative, number, line))
    return results


def self_test() -> None:
    cases = {
        "A release nao esta agendada.": {"não", "está"},
        "O endereco e compartilhado.": {"endereço", "é"},
        "La operacion es rapida.": {"operación", "rápida"},
        "Ha alteracoes ja visiveis.": {"Há", "alterações", "já", "visíveis"},
        "La vision es mas clara.": {"visión", "más"},
        "NotificaÃ§Ã£o": {"inspect encoding"},
        "Publica esta release.": set(),
        "Publicação correta.": set(),
    }
    for text, expected in cases.items():
        actual = {item.suggestion for item in scan_line("fixture.tsx", 1, text)}
        if actual != expected:
            raise AssertionError(f"{text!r}: expected {expected}, got {actual}")
    print(f"Self-test passed: {len(cases)} cases.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Files or directories relative to --repo")
    parser.add_argument("--repo", default=".", help="Target Git repository")
    parser.add_argument("--base", help="Comparison ref; defaults to the detected default branch")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--self-test", action="store_true", help="Run built-in scanner tests")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    repo = Path(args.repo).resolve()
    try:
        paths = explicit_paths(repo, args.paths) if args.paths else changed_paths(
            repo, args.base or default_base(repo)
        )
        candidates = scan_files(repo, paths)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"scan failed: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([asdict(item) for item in candidates], ensure_ascii=False, indent=2))
    else:
        for item in candidates:
            print(
                f"{item.path}:{item.line}:{item.column}: "
                f"[{item.matched} -> {item.suggestion}; {item.rule}] {item.text}"
            )
        print(f"Candidates: {len(candidates)} across {len({item.path for item in candidates})} file(s).")
    return 1 if candidates else 0


if __name__ == "__main__":
    sys.exit(main())
