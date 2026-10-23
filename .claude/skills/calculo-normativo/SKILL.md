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

## 4. Antes de dizer "está certo"

Diga **com que caso conhecido** conferiu, **contra que fonte**, **o que o teste não cobre** e
**qual sabotagem ele pegou**. Sem isso, o cálculo está "implementado", não "conferido".
