# Prompt e contexto para continuar no Claude Desktop

Cole o bloco abaixo numa conversa nova do Claude Desktop (de preferência num Projeto chamado
"Elétrica BR") para continuar de onde paramos.

---

## Prompt

Sou o Andrew Steven (Tofus Automação, GitHub Tofus-BR), engenheiro mecatrônico e programador.
Não faço mais parte da KiWi; hoje trabalho na Elo-Tech (equipamentos rotativos, quadros e
comandos, adequações NR-12) e na Tofus Automação. Estou criando, junto com você, um projeto independente e
nosso: um addon livre para o FreeCAD chamado **Elétrica BR**, para projeto de instalações
elétricas prediais e de automação residencial pelo padrão brasileiro (ABNT).

Leia primeiro o plano em `~/Projetos/FreeCAD-Eletrica-BR/docs/PLANO_DE_DESENVOLVIMENTO.md`.

Pedidos originais (nas minhas palavras):

1. "Veja a possibilidade de começar do zero, projeto independente só nosso, eu e você. Pode até
   procurar outras bibliotecas já existentes, ou faremos do zero, com possibilidade de até inserir
   os blocos de componentes de outros fabricantes. Sobre a tabela ABNT de cálculo, acredito que isso
   seja livre pois é matemática, ou faremos o nosso, ou pesquisamos onde tem alguma que podemos usar."
2. "Crie um plano de desenvolvimento e ponha em uma pasta. Acrescente também sistemas e componentes
   para automação residencial: protocolo de rede, Wi-Fi, Zigbee etc., sistema de som ambiente, home
   theater etc., para quem trabalha com automação residencial e precisa muito disso. Pegue o melhor
   de todos os programas que você já pesquisou e ponha no plano."
3. Projetos: tanto ligações elétricas de uma casa, quadro elétrico com disjuntores, comandos
   elétricos, fios, eletrodutos etc.

Decisões já tomadas:

- Projeto do zero, independente, **100% livre e gratuito** (LGPL-3.0), repositório `Tofus-BR/FreeCAD-Eletrica-BR`,
  com termo de cessão (CLA) para colaboradores; retorno indireto (uso na Elo-Tech e na Tofus Automação, cursos, serviços).
- Núcleo de cálculo em Python puro, separado da interface do FreeCAD, com testes automáticos.
- Tabelas: cálculo próprio de capacidade de corrente (Neher-McGrath, domínio público) + regras da
  NBR 5410 como critérios citando o item + opção de o usuário carregar a tabela da norma dele.
  Referência jurídica: TRF-3, 2014, Apelação 0010071-65.2006.4.03.6100.
- Símbolos de comando do QElectroTech (CC-BY 3.0); STEP de fabricantes importados pelo usuário,
  sem redistribuir.
- Folhas ABNT: usar o nosso addon "Modelos ABNT para TechDraw" (github.com/Tofus-BR/FreeCAD-Templates-ABNT).
- Primeira entrega: etapa 0.1 (núcleo de cálculo, quadro de cargas e memorial).

Preferências: responder em português, direto, sem travessão (—), sem frases com cara de IA,
seguindo boas práticas de engenharia de software; testar antes de afirmar.

---

## Situação em 22/10/2026

- Plano de desenvolvimento escrito (este diretório).
- Nada de código ainda; próximo passo: criar o repositório e começar a etapa 0.1.
- Outras frentes paralelas (não misturar): tradução pt-BR do FreeCAD no Crowdin; addon Modelos ABNT
  aguardando revisão (FreeCAD/Addons issue 182); projeto da selagem P-57 (outra sessão do Claude,
  não mexer).
