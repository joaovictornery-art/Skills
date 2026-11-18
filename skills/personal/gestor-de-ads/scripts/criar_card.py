"""Exporta um card tipográfico da marca em HTML editável e PNG, sem acesso à rede."""

import argparse
import base64
from html import escape
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile


FORMATOS = {"feed": (1080, 1350), "vertical": (1080, 1920), "quadrado": (1080, 1080)}


def navegador():
    for raiz in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA"):
        pasta = Path(os.environ.get(raiz, ""))
        for nome in ("Microsoft/Edge/Application/msedge.exe", "Google/Chrome/Application/chrome.exe"):
            if (pasta / nome).is_file():
                return str(pasta / nome)
    for nome in ("chromium", "google-chrome", "microsoft-edge"):
        if caminho := shutil.which(nome):
            return caminho
    raise SystemExit("Instale o Microsoft Edge ou Google Chrome para exportar o PNG.")


def cor_hexadecimal(valor):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", valor):
        raise argparse.ArgumentTypeError("Use uma cor no formato #RRGGBB.")
    return valor


def pagina(titulo, corpo, chamada, largura, altura, svg, fundo, texto, destaque):
    logo = base64.b64encode(svg).decode("ascii")
    rodape = f"<footer>{escape(chamada)}</footer>" if chamada else ""
    margem_vertical = 260 if altura == 1920 else 88
    return f"""<!doctype html>
<html lang="pt-BR"><meta charset="utf-8"><title>{escape(titulo)}</title>
<style>
* {{ box-sizing: border-box }}
body {{ margin: 0; background: {fundo}; color: {texto} }}
main {{ width: {largura}px; height: {altura}px; padding: {margem_vertical}px 90px;
  display: grid; grid-template-rows: auto 1fr auto; gap: 46px; --escala: 1 }}
header img {{ width: 290px; display: block }}
section {{ align-self: center; min-width: 0; overflow-wrap: anywhere }}
h1 {{ margin: 0; text-wrap: balance; font: 500 calc(102px * var(--escala))/1.03 Fraunces, Georgia, serif }}
p,footer {{ font-family: Figtree, "Segoe UI", sans-serif; white-space: pre-line }}
p {{ font-size: calc(46px * var(--escala)); line-height: 1.34; margin: 36px 0 0 }}
footer {{ border-top: 3px solid {destaque}; padding-top: 25px;
  font-size: calc(37px * var(--escala)); overflow-wrap: anywhere }}
</style>
<main><header><img alt="Logo da marca" src="data:image/svg+xml;base64,{logo}"></header>
<section><h1>{escape(titulo)}</h1>{f"<p>{escape(corpo)}</p>" if corpo else ""}</section>{rodape}</main>
<script>
const quadro = document.querySelector('main');
function ajustar() {{
  for (let escala = 100; escala >= 72; escala -= 2) {{
    quadro.style.setProperty('--escala', escala / 100);
    const fim = quadro.lastElementChild.getBoundingClientRect().bottom;
    if (fim <= {altura - margem_vertical + 1} && quadro.scrollWidth <= {largura}) {{
      quadro.dataset.ajuste = "ok";
      return;
    }}
  }}
}}
document.fonts.ready.then(ajustar);
</script></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destino", type=Path, help="Pasta nova para a versão da peça")
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--logo", required=True, type=Path, help="Arquivo SVG original da marca")
    parser.add_argument("--fundo", required=True, type=cor_hexadecimal)
    parser.add_argument("--texto", required=True, type=cor_hexadecimal)
    parser.add_argument("--destaque", required=True, type=cor_hexadecimal)
    parser.add_argument("--corpo", default="")
    parser.add_argument("--chamada", default="", help="Texto opcional de rodapé")
    parser.add_argument("--formato", choices=FORMATOS, default="feed")
    args = parser.parse_args()
    if not args.titulo.strip():
        parser.error("Informe um título.")
    if not args.logo.is_file() or args.logo.suffix.lower() != ".svg":
        parser.error("Informe um arquivo SVG existente para o logo.")
    destino = args.destino.resolve()
    if destino.exists():
        parser.error("A pasta já existe. Use uma nova versão para preservar os ajustes.")
    largura, altura = FORMATOS[args.formato]
    executavel = navegador()
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destino.parent) as temporaria:
        base = Path(temporaria)
        entrega = base / "entrega"
        entrega.mkdir()
        html, png = entrega / "card.html", entrega / "card.png"
        conteudo = pagina(args.titulo, args.corpo, args.chamada, largura, altura,
                          args.logo.read_bytes(), args.fundo, args.texto, args.destaque)
        html.write_text(conteudo, encoding="utf-8")
        opcoes = [executavel, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                  "--disable-background-networking", "--no-first-run", "--force-device-scale-factor=1",
                  f"--user-data-dir={base / 'perfil'}", f"--window-size={largura},{altura}"]
        dom = subprocess.run([*opcoes, "--dump-dom", html.as_uri()], check=True, capture_output=True, timeout=45)
        if b'data-ajuste="ok"' not in dom.stdout:
            parser.error("O texto ultrapassa o espaço do card. Encurte ou divida em duas páginas.")
        subprocess.run([*opcoes, f"--screenshot={png}", html.as_uri()], check=True, capture_output=True, timeout=45)
        with png.open("rb") as imagem:
            cabecalho = imagem.read(24)
        if cabecalho[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", cabecalho[16:24]) != (largura, altura):
            raise SystemExit("A exportação gerou um PNG fora das dimensões solicitadas.")
        entrega.rename(destino)
    print(destino / "card.png")


if __name__ == "__main__":
    main()
