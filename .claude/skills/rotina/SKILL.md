---
name: rotina
description: O ciclo de trabalho deste projeto e as lições já aprendidas — use ao COMEÇAR qualquer tarefa, ao retomar depois de /clear, antes de dizer "pronto/funciona/conferido" e ao fechar um lote. Diz em que momento cada regra do CLAUDE.md morde e onde registrar o erro para não repeti-lo.
when_to_use: início de sessão ou tarefa; "continue"; antes de afirmar um resultado; antes de commit; quando algo falhou uma vez.
---

# Rotina — o ciclo que não repete erro

## 1. Ao começar (ou retomar)

1. Leia `docs/HISTORICO.md`, bloco `▶ RETOMAR AQUI`, e confira contra o DISCO
   (`git status`, `git log -3`), nunca só contra o texto.
2. Busque a lição do tema antes de agir: `git grep -n -i "<tema>" docs/HISTORICO.md`.
3. Leia a etapa atual no `docs/PLANO_DE_DESENVOLVIMENTO.md`. Faça só o que ela pede.
4. Antes de criar função, classe, catálogo ou script: procure o que já existe
   (`git grep -n "def <conceito>"`, a API do FreeCAD, a biblioteca padrão).
5. Duas formas razoáveis, dependência nova ou padrão novo? → skill `decidir` ANTES de escrever.

## 2. Antes de AFIRMAR qualquer coisa

| Vou dizer… | Tenho de ter |
|---|---|
| "funciona" | o efeito medido (teste rodado neste turno, `freecadcmd`, documento salvo e reaberto) |
| "o cálculo está certo" | caso de referência com fonte + sabotagem que o teste pegou (skill `calculo-normativo`) |
| "zero erros / nada repetido" | a régua acertando um caso plantado (saída 2 = não confie) |
| "pronto" | Ruff, pytest e réguas rodados DEPOIS da última mudança, com o número |

Falhou uma vez → pare e entenda o mecanismo (traceback inteiro, log do FreeCAD). Na 2ª, skill
`decidir`. Tentativa às cegas, `sleep` e `try/except` para calar erro são sintoma de não ter entendido.

## 3. Antes de dizer "pronto"

```bash
uv run ruff check eletrica_br testes && uv run ruff format --check eletrica_br testes
uv run pytest
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd testes/freecad/rodar.py
```
Código novo → skills `codigo-enxuto` e `revisao`. Relate: **com que ferramenta · contra o quê ·
o que ela não vê · que caso conhecido ela acertou.**

## 4. Ao commitar

Branch própria por etapa ou tarefa (`etapa-0.1/quadro-de-cargas`), commit pequeno com mensagem
no imperativo em português dizendo o que muda e o número medido ("Calcula queda de tensão
trifásica; 42 testes, 0 falhas"). Publicar release ou abrir PR é decisão do dono.

## 5. Registrar o que aprendeu

Ao fechar um lote, e SEMPRE que um erro custou mais de uma tentativa, em `docs/HISTORICO.md`:

1. **Lição**: o que aconteceu, por quê, como evitar (3 linhas, com data).
2. **Checkpoint** `▶ RETOMAR AQUI`: estado medido, por onde continuar, perguntas para o dono.

**Escada da lição**, texto é a proteção mais fraca:

| Aconteceu | Vira |
|---|---|
| 1× e não muda o futuro | uma linha no checkpoint |
| 1× e muda | lição no HISTORICO |
| de novo | **estrutura**: regra no `sinais.py` (com caso em `CASOS`), regra do Ruff ou teste |
| vale para toda tarefa | linha no pré-voo do CLAUDE.md (avise o dono) |
