# Histórico de desenvolvimento

## ▶ RETOMAR AQUI

22/10/2026: plano (v1.1), CLAUDE.md, skills (`rotina`, `codigo-enxuto`, `revisao`, `decidir`,
`calculo-normativo`), subagente `revisor-independente`, hook de edição e `pyproject.toml` criados.
Réguas `sinais.py`, `duplicacao.py` e `ao_editar.py` conferidas com casos plantados (defeito → saída
1/2; código limpo → 0). Ainda sem código do núcleo e sem repositório no GitHub.

23/10/2026: repositório público `Tofus-BR/FreeCAD-Eletrica-BR` criado com LGPL-3.0 (COPYING e
COPYING.LESSER), README, CONTRIBUTING com termo de cessão, THIRD_PARTY, modelos de issue e PR, CI no
GitHub Actions (Ruff, réguas, pytest em Python 3.11 via uv) e skill nova `freecad-addon`. Ambiente
local com `uv` (Python 3.11.16, igual ao do FreeCAD): Ruff limpo, pytest 2/2, freecadcmd 1/1.

Próximo: etapa 0.1, começando pela previsão de cargas (skill `calculo-normativo`). O
`package.xml` entra quando existir a primeira bancada (`InitGui.py`).

## Decisões

- 22/10/2026 · **Projeto 100% livre** (LGPL-3.0) com CLA · opções: livre, misto, pago · decisão:
  livre, custo quase zero, retorno indireto · evidência: custos levantados (GitHub, Crowdin e Addon
  Manager gratuitos) · reavaliar se surgir módulo novo voltado a empresas.
- 22/10/2026 · **Tabelas da norma fora do código** · cálculo próprio (Neher-McGrath) + tabela do
  usuário · evidência: TRF-3 2014 a favor do uso, ABNT discorda · reavaliar com parecer jurídico.

## Lições

(vazio)
