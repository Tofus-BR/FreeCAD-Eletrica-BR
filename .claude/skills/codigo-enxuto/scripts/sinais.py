"""Sinais de código apressado que o Ruff não cobre.

Uso: python3 -I sinais.py <arquivo.py> [...]
Saída: 0 = limpo · 1 = há ERRO · 2 = o autoteste falhou (não confie).
Cada regra tem um caso com defeito e um correto em CASOS; o autoteste roda os dois.
"""

import ast
import re
import sys
from pathlib import Path

NARRATIVO = re.compile(
    r"#\s*(agora|aqui (nós|eu)|primeiro,|em seguida|vamos|isso (faz|garante)|now we|here we|"
    r"this (function|code) (will|does)|step \d|passo \d)", re.I)
TEMPORARIO = re.compile(r"#\s*(TODO|FIXME|XXX|HACK)\b(?!.*#\d+)")  # TODO sem issue vinculada


def sinais(fonte, nome="<texto>"):
    achados = []
    for n, linha in enumerate(fonte.splitlines(), 1):
        if NARRATIVO.search(linha):
            achados.append((n, "AVISO", "comentario-narrativo", "diga o porquê, não a história"))
        if TEMPORARIO.search(linha):
            achados.append((n, "AVISO", "todo-sem-issue", "abra issue e cite #N, ou resolva"))
    try:
        arvore = ast.parse(fonte, nome)
    except SyntaxError as e:
        return [(e.lineno or 0, "ERRO", "sintaxe", str(e.msg))]
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call) and isinstance(no.func, ast.Name) and no.func.id in {"print", "breakpoint"}:
            achados.append((no.lineno, "ERRO", "debug-esquecido", f"{no.func.id}() em código de produto"))
        if isinstance(no, ast.ExceptHandler):
            if no.type is None:
                achados.append((no.lineno, "ERRO", "except-nu", "capture a exceção esperada"))
            elif len(no.body) == 1 and isinstance(no.body[0], ast.Pass):
                achados.append((no.lineno, "ERRO", "erro-engolido", "except com pass esconde falha"))
        if isinstance(no, ast.FunctionDef) and not no.name.startswith("_"):
            if not ast.get_docstring(no) and len(no.body) > 15:
                achados.append((no.lineno, "AVISO", "funcao-publica-sem-doc", "diga o que entra, sai e a norma"))
    return sorted(achados)


CASOS = [
    ("x = 1\nprint(x)\n", "debug-esquecido", True),
    ("import logging\nlogging.getLogger(__name__).info('x')\n", "debug-esquecido", False),
    ("try:\n    f()\nexcept:\n    raise\n", "except-nu", True),
    ("try:\n    f()\nexcept ValueError:\n    raise\n", "except-nu", False),
    ("try:\n    f()\nexcept ValueError:\n    pass\n", "erro-engolido", True),
    ("# agora vamos calcular a corrente\nx = 1\n", "comentario-narrativo", True),
    ("# NBR 5410 6.2.7: queda máxima de 4 % no circuito terminal\nx = 1\n", "comentario-narrativo", False),
    ("x = 1  # TODO arrumar\n", "todo-sem-issue", True),
    ("x = 1  # TODO arrumar #12\n", "todo-sem-issue", False),
]


def autoteste():
    for fonte, regra, deve in CASOS:
        if any(r == regra for _, _, r, _ in sinais(fonte)) != deve:
            print(f"autoteste: regra {regra} errou no caso {fonte!r}", file=sys.stderr)
            return False
    return True


def main(argv):
    if not autoteste():
        return 2
    erro = False
    for caminho in argv:
        for linha, nivel, regra, dica in sinais(Path(caminho).read_text(encoding="utf-8"), caminho):
            print(f"{caminho}:{linha} {nivel} {regra}: {dica}")
            erro |= nivel == "ERRO"
    return 1 if erro else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
