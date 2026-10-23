# CLAUDE.md — Elétrica BR para FreeCAD

Addon livre (LGPL-3.0) para projeto de instalações elétricas e automação residencial pelo padrão
brasileiro. Dono e responsável: Andrew Steven (Tofus Automação). Plano: `docs/PLANO_DE_DESENVOLVIMENTO.md`.
Estado e lições: `docs/HISTORICO.md`. Este arquivo fica abaixo de ~150 linhas; detalhe vai nas skills.

**Objetivo de qualidade:** o código entra limpo e certo na primeira vez, no padrão de um bom
projeto Python mantido por gente experiente. Refazer custa mais que fazer devagar.

## Pré-voo (cheque ANTES de agir)

| Antes de… | Faça |
|---|---|
| qualquer tarefa | skill `rotina` fase 1: HISTORICO, etapa do plano, o que já existe |
| escrever cálculo | skill `calculo-normativo`: fonte, unidade, limite, caso de referência |
| mexer em comando, objeto, painel ou `package.xml` | skill `freecad-addon` |
| 2ª tentativa do que falhou | PARE e pesquise (skill `decidir`) |
| criar função, classe ou arquivo | `git grep` pelo conceito; reuse |
| adicionar dependência | skill `decidir`; prefira o que vem no FreeCAD e a biblioteca padrão |
| `Write` num caminho | `ls`/`git status` antes, para não sobrescrever |
| afirmar "funciona / certo / pronto" | rode neste turno e diga com que caso conhecido conferiu |

## Regras

1. **Escopo.** Faça só o que a tarefa pede. Melhoria fora do pedido vira sugestão, não diff.
2. **Arquitetura.** `eletrica_br/nucleo` = Python puro, sem FreeCAD, funções puras. `freecad/` =
   objetos e comandos. `documentos/` = TechDraw, planilhas, PDF. Dado do usuário fica em
   `~/FreeCAD-Eletrica-BR/`, nunca dentro da pasta Mod.
3. **Python 3.11** (a versão do FreeCAD 1.1). Tipagem nas funções públicas. `dataclasses` para
   dados. Sem `print`: use `FreeCAD.Console` na interface e `logging` no núcleo.
4. **Tamanho.** ≤ 300 linhas por arquivo, função ≤ 50 comandos e complexidade ≤ 10 (o Ruff
   cobra). Coesão vale mais que contar linhas: não fragmente artificialmente.
5. **Nomes em português**, do domínio (`corrente_projeto_a`, `secao_mm2`, `queda_tensao_pct`).
   Unidade no nome quando a grandeza tem unidade.
6. **Comentário diz o porquê** em até 3 linhas, ou o item da norma. Nunca conta a história do que
   foi feito; isso vai no commit.
7. **Texto de interface** sempre por `translate("EletricaBR", "...")`, para o Crowdin.
8. **Tabelas da norma não entram no código** (plano, seção 3.1).
9. **Licença de terceiros.** Só MIT, BSD, LGPL ou CC-BY, com crédito em `THIRD_PARTY.md`.
   STEP de fabricante nunca é redistribuído.
10. **Teste junto com o código**, no mesmo commit. Teste de cálculo segue `calculo-normativo`.

## Comandos

```bash
uv run ruff check eletrica_br testes && uv run ruff format eletrica_br testes
uv run pytest                                   # núcleo, sem FreeCAD
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd testes/freecad/rodar.py   # dentro do FreeCAD
python3 -I .claude/skills/codigo-enxuto/scripts/sinais.py <arquivos>
python3 -I .claude/skills/codigo-enxuto/scripts/duplicacao.py <arquivo> eletrica_br
```

O hook `PostToolUse` (`.claude/settings.json`) roda Ruff + sinais + duplicação em todo `.py`
editado. ERRO bloqueia e volta para corrigir na hora.

## Definição de pronto

1. Ruff limpo, pytest verde e `freecadcmd` verde, rodados DEPOIS da última mudança.
2. Cálculo: caso de referência com fonte e sabotagem pega pelo teste.
3. Interface: aberta no FreeCAD, documento salvo, fechado e reaberto sem erro.
4. Skills `codigo-enxuto` e `revisao` aplicadas ao diff.
5. Checkpoint no `docs/HISTORICO.md` (skill `rotina` fase 5).

Toda afirmação de pronto diz: **com que ferramenta, contra o quê, o que ela não vê e que caso
conhecido ela acertou.**

## Git

Branch por tarefa, commit pequeno em português no imperativo com o número medido. Push da branch
é livre; release, merge na `main` e publicação no Addon Manager são decisões do dono.
