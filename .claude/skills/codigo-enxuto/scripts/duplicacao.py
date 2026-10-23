"""Acha blocos de 6+ linhas de código repetidos entre arquivos Python.

Uso:
    python3 -I duplicacao.py <arquivo-novo> [raiz]   # o bloco do arquivo já existe em outro?
    python3 -I duplicacao.py --censo <pasta>         # % de linhas em blocos repetidos

Saída: 0 = nada repetido · 1 = repetição achada · 2 = o autoteste falhou (não confie).
"""

import sys
from pathlib import Path

JANELA = 6
IGNORAR = {".git", ".venv", "__pycache__", "build", "dist"}


def linhas_de_codigo(caminho):
    saida = []
    for numero, linha in enumerate(caminho.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        limpa = linha.strip()
        if limpa and not limpa.startswith("#"):
            saida.append((numero, limpa))
    return saida


def blocos(caminho):
    linhas = linhas_de_codigo(caminho)
    for i in range(len(linhas) - JANELA + 1):
        trecho = linhas[i:i + JANELA]
        if sum(len(t) for _, t in trecho) >= 120:  # ignora blocos triviais (parênteses, imports curtos)
            yield trecho[0][0], "\n".join(t for _, t in trecho)


def arquivos(raiz):
    return [p for p in Path(raiz).rglob("*.py") if not IGNORAR & set(p.parts)]


def repetidos(alvo, raiz):
    indice = {}
    for outro in arquivos(raiz):
        if outro.resolve() != alvo.resolve():
            for linha, texto in blocos(outro):
                indice.setdefault(texto, (outro, linha))
    return [(linha, indice[texto]) for linha, texto in blocos(alvo) if texto in indice]


def censo(pasta):
    vistos, total, repetidas = {}, 0, set()
    for arq in arquivos(pasta):
        total += len(linhas_de_codigo(arq))
        for linha, texto in blocos(arq):
            if texto in vistos:
                repetidas.update((arq, linha + k) for k in range(JANELA))
            vistos.setdefault(texto, (arq, linha))
    return total, len(repetidas)


def autoteste():
    import tempfile
    bloco = "\n".join(f"valor_{i} = calcular_corrente(potencia_{i}, tensao_{i}, fator_{i})" for i in range(7))
    with tempfile.TemporaryDirectory() as d:
        Path(d, "a.py").write_text(bloco)
        Path(d, "b.py").write_text("x = 1\n" + bloco)
        Path(d, "c.py").write_text("y = 2\n")
        return bool(repetidos(Path(d, "b.py"), d)) and not repetidos(Path(d, "c.py"), d)


def main(argv):
    if not autoteste():
        print("autoteste falhou: a régua não acha a cópia plantada", file=sys.stderr)
        return 2
    if argv[:1] == ["--censo"]:
        total, rep = censo(argv[1] if len(argv) > 1 else ".")
        print(f"{rep}/{total} linhas em blocos repetidos ({100 * rep / max(total, 1):.1f}%)")
        return 0
    alvo, raiz = Path(argv[0]), argv[1] if len(argv) > 1 else "."
    achados = repetidos(alvo, raiz)
    for linha, (outro, linha_outro) in achados:
        print(f"{alvo}:{linha} repete {outro}:{linha_outro} → reuse em vez de copiar")
    return 1 if achados else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
