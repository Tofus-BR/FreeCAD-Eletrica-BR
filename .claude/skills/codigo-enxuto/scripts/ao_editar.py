"""Hook PostToolUse do Claude Code: roda as réguas no arquivo .py que acabou de ser editado.

Recebe o JSON do hook na entrada padrão. Sai com 2 quando há ERRO, para o Claude corrigir na hora.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).parent


def rodar(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    dados = json.load(sys.stdin)
    caminho = (dados.get("tool_input") or {}).get("file_path", "")
    if not caminho.endswith(".py") or "/.claude/" in caminho:
        return 0
    raiz = Path(dados.get("cwd") or ".")
    comandos = [
        (sys.executable, "-I", str(AQUI / "sinais.py"), caminho),
        (sys.executable, "-I", str(AQUI / "duplicacao.py"), caminho, str(raiz / "eletrica_br")),
    ]
    if shutil.which("ruff"):
        comandos.insert(0, ("ruff", "check", "--quiet", caminho))
    saidas, erro = [], False
    for cmd in comandos:
        codigo, texto = rodar(*cmd)
        if codigo == 0 or not texto:
            continue
        saidas.append(texto)
        regua_quebrada = codigo == 2 and cmd[0] != "ruff"
        erro |= regua_quebrada or cmd[0] == "ruff" or " ERRO " in texto or " repete " in texto
    if saidas:
        print("\n".join(saidas), file=sys.stderr)
    return 2 if erro else 0


if __name__ == "__main__":
    sys.exit(main())
