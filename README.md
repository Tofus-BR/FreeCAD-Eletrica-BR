# Elétrica BR para FreeCAD

Bancada livre para o [FreeCAD](https://www.freecad.org) que faz o projeto de **instalações
elétricas e de automação residencial pelo padrão brasileiro (ABNT)**: quadro de cargas,
dimensionamento pela NBR 5410, unifilar, lista de materiais, quadro elétrico em 3D, comandos
elétricos, cabeamento de rede, automação, som ambiente e home theater.

> **Em desenvolvimento.** A primeira versão (0.1) trará o quadro de cargas e o dimensionamento de
> condutores e proteção com memorial de cálculo. Veja o
> [plano de desenvolvimento](docs/PLANO_DE_DESENVOLVIMENTO.md).

## Princípios

- **Livre e gratuito** (LGPL-3.0), para Windows, macOS e Linux.
- **Cálculo rastreável**: cada número do memorial mostra a fórmula, os dados e o item da norma.
- **Ferramenta de apoio ao projetista**: a responsabilidade técnica é do profissional habilitado
  que assina a ART.

## Desenvolvimento

Requer Python 3.11 e [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run ruff check . && uv run ruff format --check .
uv run pytest
freecadcmd testes/freecad/rodar.py   # testes dentro do FreeCAD
```

Contribuições são bem-vindas: leia o [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

[LGPL-3.0-or-later](COPYING.LESSER). Créditos de terceiros em [THIRD_PARTY.md](THIRD_PARTY.md).

---

# Elétrica BR for FreeCAD (English)

Free FreeCAD workbench for **electrical installation and home automation design following Brazilian
ABNT standards** (NBR 5410). Under development; first release (0.1) will provide load schedules and
conductor/protection sizing with a calculation report. Licensed under LGPL-3.0-or-later.
