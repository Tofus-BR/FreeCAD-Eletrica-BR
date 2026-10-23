# Histórico de desenvolvimento — Elétrica BR

Documento vivo. Ordem: checkpoint → revisão geral → decisões → lições → sessões (mais recente no
topo). Atualizado ao fim de cada lote (skill `rotina`, fase 5). O plano de etapas mora em
`docs/PLANO_DE_DESENVOLVIMENTO.md`; este arquivo diz onde estamos e o que aprendemos.

## ▶ RETOMAR AQUI

**Etapa atual:** 0.1 — núcleo de cálculo, quadro de cargas e memorial.
**Branch:** `etapa-0.1/previsao-de-cargas`.

**Feito:** `eletrica_br/nucleo/previsao.py` — iluminação mínima e TUG (quantidade e potência) por
cômodo. 48 testes verdes, 5 casos de referência publicados, 12/12 sabotagens pegas.

### Por onde continuar

1. TUE e cargas específicas (chuveiro, ar-condicionado, forno) com catálogo editável.
2. Divisão em circuitos e balanceamento de fases.
3. Demanda e corrente de projeto.

### Perguntas para o dono

- Tem o texto da NBR 5410:2004? Serve para conferir as citações dos itens (9.5.2.1, 9.5.2.2.1 e
  9.5.2.2.2) e a nota sobre o cômodo ≤ 2,25 m² (só muda a posição do ponto, não a quantidade).

## 🔎 Revisão geral — o que tem de continuar valendo

| Comportamento | Como medir | Prova esperada |
|---|---|---|
| Núcleo não depende do FreeCAD | `uv run pytest testes/test_pacote.py` | 2/2 verde |
| Pacote importa dentro do FreeCAD | `freecadcmd testes/freecad/rodar.py` | 1/1 ok |
| Réguas pegam defeito plantado | autoteste do `sinais.py` e `duplicacao.py` | saída ≠ 2 |
| Previsão de cargas bate com exemplos publicados | `uv run pytest testes/nucleo` | casos de referência verdes |

## Decisões

- 22/10/2026 · **Projeto 100% livre** (LGPL-3.0) com CLA · opções: livre, misto, pago · decisão:
  livre, custo quase zero, retorno indireto · evidência: GitHub, Crowdin e Addon Manager gratuitos ·
  reavaliar se surgir módulo novo voltado a empresas.
- 22/10/2026 · **Tabelas da norma fora do código** · cálculo próprio (Neher-McGrath) + tabela do
  usuário · evidência: TRF-3 2014 a favor do uso, ABNT discorda · reavaliar com parecer jurídico.
- 23/10/2026 · **Ambiente com uv e Python 3.11** · opções: Python do sistema (3.14), Python do
  FreeCAD, uv · decisão: uv com 3.11, igual ao FreeCAD 1.1 · evidência: pytest ausente no FreeCAD e
  3.14 diferente do alvo · reavaliar quando o FreeCAD mudar de Python.

- 23/10/2026 · **Quadro elétrico: montagem 3D, unifilar e etiquetas no mesmo addon** · opções:
  addon separado ou bancada do Elétrica BR · decisão: bancada do Elétrica BR, etapa 0.4 · evidência:
  o quadro depende dos circuitos e proteções já calculados · reavaliar se surgir uso só de painéis.

- 23/10/2026 · **Normas ABNT só para consulta local** · o dono tem acesso pelo convênio
  Confea/Crea com a ABNT (CREA-SP) e algumas licenciadas no próprio nome · decisão: PDFs em
  `~/FreeCAD-Eletrica-BR/normas`, fora do repo, bloqueados no `.gitignore`; código cita só número,
  edição e item · reavaliar se a ABNT liberar uso público.

- 23/10/2026 · **Redução de potência das TUG com mais de 6 pontos não aplicada** · opções: aplicar
  a redução permitida pela norma ou não · decisão: não aplicar no cálculo por cômodo (sempre do
  lado da segurança) · evidência: a norma diz "admite-se" · reavaliar quando houver quadro de cargas
  do conjunto, onde a redução pode virar opção do projetista.

## Lições

- 23/10/2026 · Sabotagem `<=` → `<` no limite de 6 m² "escapou" porque é equivalente (os dois
  ramos dão 100 VA em 6 m²). Como evitar: mutação que não muda nenhum resultado não prova nada;
  troque por uma que mude.

- 23/10/2026 · O Ruff do projeto pegou 5 problemas no primeiro arquivo de teste (caminhos com
  `os.path`, import fora do topo). Como evitar: rodar `uv run ruff check .` antes de dizer pronto;
  o hook já faz isso a cada edição dentro do Claude Code.

## Sessões

### 23/10/2026 — Biblioteca de livros ligada ao projeto

- Ferramenta `livro.py` (skill `calculo-normativo`): lista a coleção ELETRICA E CLP do app Livros,
  baixa do iCloud, converte com pdftotext para `~/FreeCAD-Eletrica-BR/referencias` e busca.
  Testada com Creder 16ª ed. e o manual do Lincoln Costa.
- `previsao.py` conferido com Creder 16ª ed., 3.3.2 e 3.3.3: regras de iluminação, quantidade e
  potência das TUG batem. Creder acrescenta: subsolo, garagem, sótão e hall com pelo menos 1 TUG
  (já cobertos por "demais cômodos" quando ≤ 6 m²) e 1 ponto acima de cada bancada ≥ 0,30 m
  (posição, não muda a quantidade mínima).

### 23/10/2026 — Etapa 0.1: previsão de cargas

- `previsao.py`: iluminação mínima pela área, quantidade mínima de TUG por tipo de cômodo e
  potência mínima das TUG, com cada resultado trazendo o passo do cálculo e o item da norma.
- Conferido: 5 casos de referência (GESEP/UFV e Voltimum), bordas, invariantes, entradas inválidas;
  48 testes; script `sabotar.py` novo com 12 mutações, todas pegas.

### 23/10/2026 — Ambiente, GitHub e início da etapa 0.1

- Repositório público `Tofus-BR/FreeCAD-Eletrica-BR` com LGPL-3.0, README, CONTRIBUTING com termo
  de cessão, THIRD_PARTY, modelos de issue e PR e CI (Ruff, réguas, pytest em 3.11). CI verde.
- Ambiente local com uv (Python 3.11.16), extensões do Cursor para Python/Ruff/TOML e configuração
  do editor só deste projeto (`.vscode/`). Gemini desligado aqui.
- Skill nova `freecad-addon`; hook `SessionStart` que injeta este checkpoint; HISTORICO neste formato.

### 22/10/2026 — Plano e regras de qualidade

- Plano de desenvolvimento v1.1, CLAUDE.md, skills `rotina`, `codigo-enxuto`, `revisao`,
  `decidir`, `calculo-normativo`, subagente `revisor-independente`, hook de edição e réguas
  (`sinais.py`, `duplicacao.py`) conferidas com defeito plantado.
