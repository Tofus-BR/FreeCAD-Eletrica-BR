---
name: revisao
description: Revisão de código deste projeto (Python 3.11 dentro do FreeCAD 1.1, núcleo de cálculo NBR 5410, interface PySide6, TechDraw) por dimensão — desenho, correção do cálculo, comportamento no FreeCAD, testes, simplicidade e nomes. Use antes de dizer "pronto", antes de commit de feature ou quando pedirem "revisar", "review", "está bom?", "pode subir?".
when_to_use: antes de "pronto" ou commit; revisão de diff ou de branch; depois de um lote grande de edições.
---

# Revisão

O hook `ao_editar.py`, o Ruff e o pytest já pegam o que é mecânico. Esta revisão é o que eles não
veem: o **desenho**, o **efeito real dentro do FreeCAD** e o **número certo**.

## 1. Revise nesta ordem

1. **Desenho.** O lugar é este? Cálculo no `nucleo` (sem FreeCAD), objeto paramétrico em
   `freecad/`, documento em `documentos/`. Já existe peça que faz isso? Resolve a causa ou contorna?
2. **Cálculo.** Skill `calculo-normativo`: unidade, fonte, limite, caso de referência, sabotagem.
3. **Funciona no FreeCAD.** Rode de verdade, sem tela:
   ```bash
   /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd testes/freecad/rodar.py
   ```
   Recompute, salvar e reabrir o documento, desfazer/refazer, objeto apagado, documento sem o
   objeto esperado. Interface: abra o FreeCAD e confira o painel (o que a pessoa vê).
4. **Entradas ruins.** Catálogo CSV com coluna faltando, número com vírgula decimal, arquivo
   STEP sem cor ou com várias peças, unidade trocada (mm × m).
5. **Simplicidade.** Skill `codigo-enxuto`: réguas e a tabela do que régua nenhuma vê.
6. **Testes.** O teste falha com a implementação sabotada? Testa o efeito, não o mock? Usa
   invariante em vez de valor cravado sem fonte?
7. **Nomes, textos e tradução.** Nome do domínio em português; texto de interface passa por
   `translate()` (vai para o Crowdin); comentário diz o porquê em até 3 linhas.
8. **Licença.** Código, símbolo ou modelo de terceiro? Licença compatível (MIT, BSD, LGPL, CC-BY)
   e crédito no `THIRD_PARTY.md`. Na dúvida, não entra.

## 2. Relate cada achado assim

`arquivo:linha` · **o que quebra** (entrada concreta → saída errada) · severidade (🔴 resultado
errado ou perda de dado · 🟠 degrada · 🟡 dívida) · **como medi** · conserto em uma frase.
Achado sem cenário de falha concreto é opinião: não reporte, ou marque como pergunta.

## 3. Segunda opinião

Diff que mexe em fórmula, critério de norma, arredondamento ou leitura de catálogo: chame o
subagente `revisor-independente` passando só o diff, os arquivos vizinhos e o objetivo, nunca o
seu raciocínio. Reproduza cada achado dele (teste ou comando) antes de aceitar.

## 4. Feche

Conserte o que é seu e meça de novo. O que é decisão do dono (escopo, publicação, licença) vai
como pergunta. Fechamento: skill `rotina`, fases 3 a 5.
