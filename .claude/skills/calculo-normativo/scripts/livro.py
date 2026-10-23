"""Consulta a biblioteca do app Livros (iCloud) do dono, coleção ELETRICA E CLP.

Uso:
    python3 -I livro.py listar [filtro]            # livros da coleção cujo nome casa o filtro
    python3 -I livro.py texto "<arquivo.pdf>"      # baixa do iCloud e converte para texto (cache)
    python3 -I livro.py buscar "<arquivo.pdf>" "<regex>" [contexto]

O texto fica em ~/FreeCAD-Eletrica-BR/referencias (fora do repositório: os livros têm direitos
autorais e não vão para o GitHub). Livro é fonte de MÉTODO e de exemplo resolvido; norma vale só a
versão vigente.
"""

import csv
import re
import subprocess
import sys
import time
from pathlib import Path

ICLOUD = Path.home() / "Library/Mobile Documents/iCloud~com~apple~iBooks/Documents"
INDICE = Path.home() / "PROJETO SELAGEM 2026/ESTUDO/REFERENCIA/BIBLIOTECA-LIVROS.csv"
CACHE = Path.home() / "FreeCAD-Eletrica-BR/referencias"
COLECAO = "ELETRICA E CLP"


def listar(filtro=""):
    with INDICE.open(encoding="utf-8-sig") as f:
        nomes = [linha["arquivo"] for linha in csv.DictReader(f, delimiter=";") if linha["colecao_sugerida"] == COLECAO]
    padrao = re.compile(filtro, re.I)
    return sorted(n for n in nomes if padrao.search(n))


def baixar(arquivo, espera_s=120):
    caminho = ICLOUD / arquivo
    if not caminho.exists():
        raise FileNotFoundError(f"não está no app Livros: {arquivo}")
    if caminho.stat().st_blocks == 0:
        subprocess.run(["brctl", "download", str(caminho)], check=False)
        limite = time.monotonic() + espera_s
        while caminho.stat().st_blocks == 0 and time.monotonic() < limite:
            time.sleep(2)
    if caminho.stat().st_blocks == 0:
        raise TimeoutError(f"o iCloud não baixou em {espera_s} s: {arquivo}")
    return caminho


def texto(arquivo):
    destino = CACHE / (Path(arquivo).stem + ".txt")
    if not destino.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftotext", "-layout", str(baixar(arquivo)), str(destino)], check=True)
    return destino


def buscar(arquivo, regex, contexto=3):
    linhas = texto(arquivo).read_text(encoding="utf-8", errors="ignore").splitlines()
    padrao = re.compile(regex, re.I)
    blocos = []
    for i, linha in enumerate(linhas):
        if padrao.search(linha):
            ini, fim = max(0, i - contexto), min(len(linhas), i + contexto + 1)
            blocos.append("\n".join(f"{n + 1}: {linhas[n]}" for n in range(ini, fim)))
    return blocos


def main(argv):
    comando, *resto = argv or ["listar"]
    if comando == "listar":
        saida = listar(*resto[:1])
    elif comando == "texto":
        saida = [str(texto(resto[0]))]
    elif comando == "buscar":
        saida = buscar(resto[0], resto[1], int(resto[2]) if len(resto) > 2 else 3)
    else:
        sys.stderr.write(__doc__)
        return 2
    sys.stdout.write("\n".join(saida) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
