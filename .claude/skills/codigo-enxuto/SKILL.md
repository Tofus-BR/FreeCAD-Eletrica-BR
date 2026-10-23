---
name: codigo-enxuto
description: Faz o código NOVO chegar ao resultado correto pelo caminho mais curto, no idioma de um bom projeto Python/FreeCAD, sem repetir o que já existe, sem voltas, sem função inchada, sem defesa contra o impossível e sem comentário narrativo. Use antes de commitar, ao revisar um diff ou quando pedirem "limpar", "enxugar", "simplificar", "tirar cara de IA".
when_to_use: antes de commit de código em eletrica_br/ ou testes/; revisão de diff; pedido de limpeza.
---

# Código enxuto

**Prioridade, nesta ordem:** correto → seguro → igual ao idioma do vizinho → menos linhas.
"Menos linhas" só vale com comportamento IGUAL. Nunca troque validação de entrada, unidade ou
item de norma por concisão.

O objetivo é código que um bom engenheiro de software escreveria e manteria: a régua olha o
código, não quem o escreveu. Os vícios típicos de código gerado com pressa (por gente ou por IA)
são **recriar em vez de reusar**, **API antiga**, **pacote inventado** e **comentário que conta a
história**. É isso que as réguas abaixo pegam.

## 1. Meça (réguas com controle; saída 2 = régua quebrada, não confie)

O hook `ao_editar.py` já roda as três no arquivo editado a cada Edit/Write. Antes do commit, rode
à mão sobre tudo o que mudou, inclusive arquivo novo ainda não rastreado:

```bash
S=.claude/skills/codigo-enxuto/scripts
uv run ruff check eletrica_br testes && uv run ruff format --check eletrica_br testes
python3 -I $S/sinais.py <arquivos .py alterados>        # print/breakpoint, except nu, erro engolido, narrativa, TODO sem issue
python3 -I $S/duplicacao.py <arquivo> eletrica_br        # bloco de 6+ linhas que JÁ EXISTE → reuse
python3 -I $S/duplicacao.py --censo eletrica_br          # retrato geral (referência humana: 8 a 13 %)
```

Limites do `pyproject.toml` (o Ruff cobra): complexidade ciclomática ≤ 10 (C901), ≤ 50 comandos
por função (PLR0915), ≤ 6 argumentos (PLR0913), ≤ 300 linhas por arquivo (regra do CLAUDE.md).

## 2. Revise o que régua nenhuma vê

| Vício | Pergunta | Corte típico |
|---|---|---|
| Recriar em vez de reusar | Já existe em `eletrica_br/nucleo`, na API do FreeCAD ou na biblioteca padrão? (`git grep`) | Importe o existente |
| API antiga ou inventada | O método existe na versão do FreeCAD/Python que usamos? | Confirme no código instalado (`freecadcmd -c "help(...)"`) |
| Pacote novo | Precisa mesmo? Vem no FreeCAD? Licença compatível? | Skill `decidir` antes |
| Abstração de uso único | Classe/função com 1 chamador que só repassa? | Inline |
| Defesa contra o impossível | `if x is None` onde o tipo garante, `try` em código que não lança | Apague, **exceto** na fronteira (entrada do usuário, arquivo, catálogo) |
| Tentativa deixada | Flag, ramo ou variável de abordagem abandonada | Apague |
| Comentário narrativo | Conta a história ou repete a linha? | O porquê em até 3 linhas, ou o item da norma |
| Nome genérico ou inchado | `data`, `result`, `helper`, `calcular_valor_final_resultado` | Nome do domínio, curto, em português |
| Número mágico | `0.04`, `1.25` soltos | Constante com nome, unidade e fonte |
| Teste que só mede o mock | Passa com a implementação sabotada? | Teste o efeito; sabote para provar |
| Mudança fora do pedido | Mexe no que ninguém pediu? | Separe ou desfaça |

## 3. O que NÃO cortar

- Validação de dado externo (arquivo, catálogo CSV/JSON, entrada do usuário).
- Unidade e item da norma em constante ou docstring de cálculo.
- Comentário com número medido que impede regressão: encurte, não apague.

## 4. Feche

`pytest` e as réguas DEPOIS do corte. Duplicação tem de cair e nada novo pode subir. Lição que
custou mais de uma tentativa vai para a skill `rotina`, fase 5.
