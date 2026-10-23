---
name: calculo-normativo
description: Regras para escrever e testar cálculo de engenharia elétrica (NBR 5410 e correlatas) que vai para memorial e ART — unidade explícita, fonte de cada número, caso de referência resolvido à mão, sabotagem do teste e limite de aplicação. Use ao criar ou mudar qualquer coisa em eletrica_br/nucleo/, tabela de catálogo, critério de norma ou texto de memorial.
when_to_use: novo cálculo ou critério; mudança em fórmula, tabela, fator de correção ou arredondamento; antes de afirmar que um resultado está certo.
---

# Cálculo normativo

Um erro aqui vira cabo subdimensionado numa casa. Cálculo só está pronto quando outra pessoa
consegue refazer cada número com papel e a norma na mão.

## 1. Antes de escrever

1. Qual item da norma ou fonte técnica? Escreva no docstring: `NBR 5410:2004 6.2.7.1` ou
   `Neher, McGrath, AIEE 1957`. Sem fonte, não escreve.
2. Qual a unidade de cada entrada e saída? (A, V, W, VA, mm², m, °C, %). Unidade vai no nome
   (`comprimento_m`, `secao_mm2`) ou no tipo, nunca só na cabeça.
3. Qual o limite de aplicação? (baixa tensão até 1000 V CA, cobre/alumínio, PVC/EPR/XLPE,
   temperatura ambiente). Fora do limite: erro claro, nunca resultado silencioso.

## 1.1 Biblioteca de referência (app Livros do dono, coleção ELETRICA E CLP)

Antes de implementar um critério, confira-o em pelo menos um livro e cite página ou seção no teste:

```bash
L=.claude/skills/calculo-normativo/scripts/livro.py
python3 -I $L listar "5410|creder|cotrim|mamede"         # acha o arquivo
python3 -I $L buscar "<arquivo.pdf>" "queda de tens" 2     # baixa do iCloud, converte e busca
```

| Assunto | Livros (nome do arquivo no app) |
|---|---|
| Base de projeto residencial e predial | `Livro Instalacoes Eletricas - 16 ed. - Helio Creder.pdf`, `Instalações_Eletricas_5ª_Edição_Ademaro_A_M_B_Cotrim.pdf`, `instalacoes eletrica - 4 edicao - julio niskier.pdf` |
| Dimensionamento de condutores e disjuntores (NBR 5410) | `666867388-Manual-do-dimensionamento-de-condutores-eletricos-e-disjuntores-de-acordo-com-a-NBR-5410-Prof-Eng-Lincoln-Costa.pdf` |
| Industrial, curto-circuito, proteção | `Instalações_Elétricas_Industriais_João_Mamede_Filho_9ed_1.pdf`, `Protecao_de_sistemas_eletricos_de_potencia_2_ed_Mamede_Filho_2.pdf` |
| Memorial e projeto predial | `609836052-Memorial-Descritivo-Instalacoes-Eletricas.pdf`, `Projeto de sistemas eletricos prediais.pdf` |
| Aterramento e DR/DPS | `51409284-Esquemas-eletricos-de-aterramento.pdf`, `535206799-Dispositivos-de-protecao-eletrica.pdf` |
| Comandos elétricos (etapa 0.5) | `633262135-Manual-comando-eletrico-weg-pdf.pdf`, `Comandos Elétricos Teoria e Atividades - Claiton Moro Franch.pdf` |
| Automação e redes (etapa 0.7) | `331345614-eBook-Eletrico-Automacao-Residencial 1.pdf`, `682500048-ebook-AUTOMACAO-RESIDENCIAL-POR-WIFI.pdf`, `652529862-Guia-completo-cabeamento-de-rede-Pinheiro.pdf` |
| Simbologia | `Simbologia elétrica.pdf`, `Simbologia eletrica PROF LUIZ FERNANDO GONCALVES.pdf` |

Normas (licença do dono, **só consulta**, regra 11 do CLAUDE.md). Confira a vigência antes de usar:

| Norma | Arquivo | Situação conferida |
|---|---|---|
| NBR 5410:2004 corr. 2008 | `733208582-ABNT-NBR-5410-2004-Versao-Corrigida-2008 1.pdf` | vigente; revisão prevista para o fim de 2026 |
| NBR 5419-1 e -2:2026 | `1024862935-NBR-5419-1-2026-...pdf`, `1024862639-NBR-5419-2-2026-...pdf` | 2ª edição de 10/03/2026; existe versão corrigida posterior. A de 2015 não serve para projeto novo |
| NBR NM 60898:2004, NBR IEC 60898-2 | `675069717-ABNT-NBR-NM-60898-...pdf`, `849551707-ABNT-NBR-IEC-60898-2.pdf` | conferir vigência no catálogo ABNT |
| NBR IEC 61643-1 (DPS) | `596101700-NBR-IEC-61643-1-...pdf` | edição antiga; a família atual é a IEC 61643-11. Conferir |
| DR: BS EN e UNE EN 61008-1 | `784139129-BS-EN-61008-1-2012.pdf` | europeias, só referência; a brasileira é a NBR NM 61008-1 |
| NBR IEC 61439-1, -3, -5, -6 | `546666931-ABNT-NBR-IEC-61439-1-2017.pdf`, `713023951-ABNT-NBR-IEC-61439-3-2017.pdf` | quadros, etapa 0.4 |
| NBR 14136 + emenda 1 | `109355423-ABNT-NBR-14136-...pdf`, `176961929-Abnt-Nbr-14136-Emenda-01.pdf` | tomadas |
| NBR 14565:2019 | `705758660-ABNT-NBR-14565-2019.pdf` | redes, etapa 0.7 |
| NBR ISO/CIE 8995-1:2013 | `257395363-NBR-ISO-CIE-8995-1-2013-...pdf` | iluminação |
| IEC 60617 | `666911398-IEC-60617.pdf` | simbologia |
| NR-10, NR-12 | `731851461-NR-10.pdf`, `422624068-NR-12.pdf` | conferir a redação atual no site do MTE |
| CPFL | `199051653-Norma-Cpfl.pdf` (micro e minigeração), `682846855-guia-cpfl.pdf` (2006) | falta o padrão de entrada atual (GED 13) |
| NBR 17019 | `727885583-NBR-17019-2022 1.pdf` | é resumo em Word, não a norma |

Regras: livro é fonte de **método e de exemplo resolvido**; norma vale só a **versão vigente**
(muitos livros citam normas antigas ou canceladas). O texto convertido fica em
`~/FreeCAD-Eletrica-BR/referencias`, **fora do repositório**: livro nunca vai para o GitHub, nem
trecho longo copiado para o código ou para os testes (cite seção e página).

## 2. Regras de código

- **Núcleo em Python puro** (`eletrica_br/nucleo`), sem importar FreeCAD. Função pura: entra dado,
  sai resultado; nada de estado global.
- **Constante com nome, unidade e fonte**: `QUEDA_MAX_TERMINAL_PCT = 4.0  # NBR 5410 6.2.7.1`.
- **Tabelas da norma não ficam no código.** Capacidade de corrente vem do cálculo próprio
  (`condutores.py`) ou da tabela carregada pelo usuário. Ver plano, seção 3.1.
- **Arredondamento só no fim** e no sentido da segurança (seção comercial imediatamente superior,
  disjuntor imediatamente inferior a Iz). Documente o sentido.
- **Resultado traz o caminho**: cada função de dimensionamento devolve o valor e a lista de
  passos (fórmula, valores, item da norma) que o memorial imprime.
- Entrada inválida (potência negativa, tensão zero, comprimento fora da faixa) levanta
  `ValueError` com mensagem em português que diga o campo e a faixa aceita.

## 3. Testes obrigatórios (pytest, em testes/nucleo)

| Teste | O que prova |
|---|---|
| Caso de referência resolvido à mão (livro, TCC, exemplo publicado), com a fonte no teste | o número bate com o mundo, não com o próprio código |
| Conferência cruzada (sclab-dimcabos ou outro programa) quando houver | outro método chega ao mesmo resultado |
| Invariante (corrente cresce com a potência; seção nunca diminui quando o comprimento aumenta) | o comportamento, não um valor cravado |
| Borda (limite exato da queda, 0 e máximo da faixa, monofásico e trifásico) | não erra no limite |
| Entrada inválida → `ValueError` | não devolve número quando deveria recusar |
| **Sabotagem**: troque o sinal, o fator ou o arredondamento e rode — o teste TEM de falhar | o teste testa de verdade |

Tolerância numérica explícita (`pytest.approx(rel=1e-3)`) e justificada.

Sabotagem automática: liste as mutações em `testes/nucleo/sabotagens_<modulo>.json`
(`[trecho original, trecho sabotado]`) e rode
`python3 -I .claude/skills/calculo-normativo/scripts/sabotar.py eletrica_br/nucleo/<modulo>.py testes/nucleo/sabotagens_<modulo>.json`.
Saída 0 = todas pegas. Mutação que "escapa" ou é defeito do teste, ou é equivalente (não muda
resultado nenhum): no segundo caso, troque por uma que mude.

## 4. Antes de dizer "está certo"

Diga **com que caso conhecido** conferiu, **contra que fonte**, **o que o teste não cobre** e
**qual sabotagem ele pegou**. Sem isso, o cálculo está "implementado", não "conferido".
