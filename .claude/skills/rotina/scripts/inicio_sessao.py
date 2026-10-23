"""Hook SessionStart: põe no contexto o estado medido do disco e o checkpoint do HISTORICO.

Frases factuais, curtas (o campo tem teto). Falha do git não derruba a sessão: sai 0 e diz o que
não mediu.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROJETO = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))


def git(*args):
    r = subprocess.run(["git", *args], cwd=PROJETO, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def estado_git():
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if not branch:
        return "Estado do git NÃO medido (git falhou neste diretório)."
    sujos = len([linha for linha in (git("status", "--porcelain") or "").splitlines() if linha])
    remoto = git("rev-list", "--left-right", "--count", "@{u}...HEAD")
    sync = f"remoto: {remoto.split()[1]} a enviar, {remoto.split()[0]} a puxar" if remoto else "sem upstream"
    arvore = f"{sujos} arquivo(s) não commitados" if sujos else "árvore limpa"
    return f"Estado medido no início da sessão: branch `{branch}`; {sync}; {arvore}."


def checkpoint():
    hist = PROJETO / "docs" / "HISTORICO.md"
    if not hist.exists():
        return "docs/HISTORICO.md não encontrado."
    texto = hist.read_text(encoding="utf-8")
    bloco = re.search(r"## ▶ RETOMAR AQUI\n(.*?)(?=\n## )", texto, re.S)
    if not bloco:
        return "Bloco '▶ RETOMAR AQUI' não encontrado no docs/HISTORICO.md."
    return "Checkpoint do docs/HISTORICO.md:\n" + bloco.group(1).strip()[:2500]


def main():
    linhas = [
        estado_git(),
        checkpoint(),
        "Documentos vivos: docs/PLANO_DE_DESENVOLVIMENTO.md (etapas e decisões) e docs/HISTORICO.md "
        "(checkpoint, sessões, decisões, lições). Skills: rotina, calculo-normativo, freecad-addon, "
        "codigo-enxuto, revisao, decidir.",
    ]
    saida = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(linhas)}}
    json.dump(saida, sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
