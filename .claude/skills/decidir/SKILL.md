---
name: decidir
description: Pesquisa e compara antes de escolher — quando há duas ou mais formas razoáveis de fazer algo, quando uma tentativa falhou, antes de adicionar dependência, formato de arquivo, padrão de código ou critério de norma. Busca na ordem lição → o que o projeto já faz → o que o FreeCAD/Python já resolve → fonte oficial, compara com evidência e registra a decisão.
when_to_use: bifurcação de desenho; 1ª falha (entender) ou 2ª (pesquisar); antes de dependência, formato, padrão ou critério novo; "qual o melhor jeito de…".
---

# Decidir

Decidir de cabeça é o erro mais caro: a 2ª tentativa sem pesquisa costuma custar horas onde duas
buscas resolviam. Pare assim que a resposta aparecer.

## 1. Já decidimos isto? (segundos)

`git grep -n -i "<conceito>" docs/HISTORICO.md docs/PLANO_DE_DESENVOLVIMENTO.md`.
Decisão registrada com motivo não se reabre sem fato novo.

## 2. Algo já resolve? (minutos)

- O **FreeCAD** já faz? (Part, Draft, BIM/Arch, TechDraw, Spreadsheet, `App::FeaturePython`,
  `Units.Quantity`). Confira no código instalado, não de memória.
- A **biblioteca padrão** do Python 3.11 faz? (`dataclasses`, `enum`, `csv`, `json`, `decimal`).
- O **projeto** já tem a peça? (`git grep`).

## 3. O que a fonte oficial diz (quando 1 e 2 não responderam, ou na 2ª falha)

- Pesquise com versão e ano ("FreeCAD 1.1 FeaturePython onDocumentRestored 2026").
- Fonte primária: wiki.freecad.org e o código do FreeCAD no GitHub, docs.python.org, docs do
  pacote, a própria norma. Fórum e blog são pista, não veredito.
- Dependência: precisa mesmo? Vem dentro do FreeCAD? Licença (MIT, BSD, LGPL ok; GPL não)?
  Manutenção recente? Existe de verdade no PyPI (nome inventado é risco real)?

## 4. Compare com evidência (≥ 2 opções)

| Critério (nesta ordem) | Opção A | Opção B |
|---|---|---|
| correto (inclui casos de borda e a norma) | | |
| seguro para o usuário (não gera projeto errado em silêncio) | | |
| idioma do FreeCAD e do projeto | | |
| linhas e conceitos novos | | |
| custo de desfazer | | |
| evidência (medição, doc oficial, protótipo) | | |

Medir é barato (protótipo de 20 linhas, `timeit`, rodar no `freecadcmd`)? Meça.

## 5. Decida, execute e registre

Decida sem pedir autorização quando for técnico. Pergunte ao dono só o que é escolha dele:
escopo, licença, publicação, nome.

Registro no `docs/HISTORICO.md`, 5 linhas: **contexto · opções · decisão · evidência com data ·
quando reavaliar**.
