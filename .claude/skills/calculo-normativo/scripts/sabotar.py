"""Sabotagem dos testes: aplica cada mutação no arquivo, roda o pytest e exige que ele FALHE.

Uso: python3 -I sabotar.py <arquivo.py> <mutacoes.json>
mutacoes.json: lista de [trecho_original, trecho_sabotado].
Saída: 0 = os testes pegaram todas as sabotagens · 1 = alguma passou despercebida.
O arquivo é sempre restaurado, mesmo com erro.
"""

import json
import subprocess
import sys
from pathlib import Path


def main(arquivo, mutacoes):
    caminho = Path(arquivo)
    original = caminho.read_text(encoding="utf-8")
    escaparam = []
    try:
        for antes, depois in json.loads(Path(mutacoes).read_text(encoding="utf-8")):
            if original.count(antes) != 1:
                escaparam.append(antes)
                sys.stdout.write(f"TRECHO NÃO ACHADO (uma única vez): {antes!r}\n")
                continue
            caminho.write_text(original.replace(antes, depois), encoding="utf-8")
            r = subprocess.run(["uv", "run", "pytest", "-q", "-x"], capture_output=True, text=True)
            sys.stdout.write(f"{'pego' if r.returncode else 'ESCAPOU'}: {antes!r} → {depois!r}\n")
            if r.returncode == 0:
                escaparam.append(antes)
    finally:
        caminho.write_text(original, encoding="utf-8")
    return 1 if escaparam else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
