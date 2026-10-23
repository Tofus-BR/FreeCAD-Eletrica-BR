# Elétrica BR para FreeCAD: plano de desenvolvimento

Projeto independente de Andrew Steven (Tofus Automação), desenvolvido com o Claude.
Versão do plano: 1.1, 22/10/2026 (decisão: projeto 100% livre).

---

## 1. Objetivo

Criar, do zero, uma bancada (addon) livre para o FreeCAD que faça o projeto completo de
**instalações elétricas prediais e de automação residencial pelo padrão brasileiro**:
planta, cálculo, quadro elétrico em 3D, comandos elétricos, cabeamento de rede, automação,
som ambiente e home theater, com documentos prontos (quadro de cargas, unifilar,
lista de materiais, memorial) nas folhas ABNT.

Público principal:

- eletricistas e projetistas de instalações residenciais, comerciais e industriais
  (quadros e comandos de motores, adequações NR-12, como na Elo-Tech);
- **integradores de automação residencial**, que hoje usam três ou quatro
  programas pagos e planilhas para um mesmo projeto;
- estudantes de cursos técnicos e de engenharia.

Princípios:

1. **100% livre e gratuito, multiplataforma** (Windows, macOS, Linux), licença LGPL-3.0, igual ao FreeCAD.
2. **Núcleo de cálculo separado da interface**: Python puro, testável e usável fora do FreeCAD.
3. **Tudo rastreável**: cada resultado mostra a fórmula, os dados e o item da norma usado.
4. **Ferramenta de apoio**: a responsabilidade técnica é do projetista com ART. O programa
   deixa isso claro no memorial.
5. **Feito por etapas publicáveis**: cada etapa vira uma versão útil sozinha.

---

## 2. O que existe no mercado e o que vamos aproveitar (ideias)

### 2.1 Instalações elétricas prediais

| Programa | Melhor ideia para copiar |
|---|---|
| AltoQi Builder Elétrico | Dimensiona fios, eletrodutos e proteção enquanto se desenha; quadro de cargas e unifilar/multifilar automáticos; sugere o melhor local do quadro pelo centro de cargas; lista de materiais por pavimento, circuito ou quadro; IFC (OpenBIM) |
| PRO-Elétrica (Multiplus) | Queda de tensão, curto-circuito, eletrocalha, ar-condicionado; orçamento com preços em planilha; simbologia NBR 5444 e IEC 60617; padrões de entrada das concessionárias (PRODIST) |
| Lumine | Fluxo simples para projeto residencial, muito usado em escritórios e TCCs |

Ponto fraco de todos: pagos, só Windows ou presos ao AutoCAD/Revit.

### 2.2 Quadros e comandos elétricos

| Programa | Melhor ideia |
|---|---|
| EPLAN / SEE Electrical / AutoCAD Electrical | Referência cruzada automática (bobina do contator aponta para os contatos), numeração de fios e bornes, lista de bornes, layout do painel a partir do esquema |
| CADe SIMU | Simula o comando (liga, desliga, intertravamento) para ensino e conferência |
| QElectroTech (livre) | Biblioteca enorme de símbolos (CC-BY 3.0) e esquema 2D organizado por folhas |

### 2.3 Instalação 3D no FreeCAD

| Projeto | Ideia |
|---|---|
| Cables Workbench (SargoDevel, LGPL-3.0, ativo) | Rota do cabo por pontos de apoio, cabos com perfil e cores, eletrodutos, caixas, conectores e componentes a partir de STEP com bornes marcados |

Lições do tópico do Cables no fórum:

- bibliotecas do usuário fora da pasta Mod, para não sumirem na atualização;
- editar componentes por planilha CSV é difícil: fazer isso por interface gráfica;
- falta lista de compra de cabos;
- arquivos STEP de fabricante não podem ser redistribuídos sem licença.

### 2.4 Automação residencial, redes e AV

| Programa | Melhor ideia |
|---|---|
| D-Tools System Integrator / Portal.io | Projeto, orçamento e proposta de integradores AV/automação num só lugar; lista de equipamentos ligada à planta e ao rack |
| KNX ETS / Loxone Config | Planejamento por cômodo e função (luz, persiana, clima, cena), endereçamento dos dispositivos, documentação de comissionamento |
| Ekahau / NetSpot | Mapa de cobertura Wi-Fi sobre a planta e posição ideal dos access points |
| Calculadoras Dolby Atmos / guias Dolby | Posição das caixas pelo ângulo em relação ao assento (layouts 5.1.2, 7.1.4 etc.) |
| EASE / ferramentas de acústica | Cobertura de som ambiente e nível sonoro por área |

---

## 3. Normas e referências técnicas

Elétrica:

- **ABNT NBR 5410**: instalações elétricas de baixa tensão (previsão de cargas, dimensionamento,
  proteção, DR, DPS, eletrodutos).
- **ABNT NBR 5419**: proteção contra descargas atmosféricas (SPDA), módulo futuro.
- **ABNT NBR ISO 8995-1**: iluminação de ambientes de trabalho.
- **NBR 5444** (cancelada, ainda usada no mercado) e **IEC 60617**: simbologia. O programa oferece
  as duas.
- **ABNT NBR 14136**: plugues e tomadas.
- **ABNT NBR IEC 61439**: conjuntos de manobra e controle (quadros).
- **PRODIST (ANEEL)** e normas de cada concessionária: padrão de entrada.
- **ABNT NBR 16752**: folhas de desenho (já temos os modelos ABNT publicados).

Redes e automação:

- **ABNT NBR 14565** e **ABNT NBR 16264**: cabeamento estruturado (a 16264 trata do residencial).
- Protocolos: Wi-Fi (802.11), Zigbee, Z-Wave, Thread/Matter, Bluetooth, KNX, Modbus/RS-485, DALI,
  DMX, IR/RS-232 para AV.

AV:

- Guias de instalação Dolby Atmos para home theater; ITU-R BS.775 (5.1).

### 3.1 Tabelas de cálculo e direitos autorais

- O TRF-3 decidiu em 2014 (Apelação 0010071-65.2006.4.03.6100) que norma técnica é conhecimento
  técnico e não obra protegida (Lei 9.610/98). A ABNT discorda, e não confirmamos se a decisão é
  definitiva.
- Estratégia adotada, segura nos dois cenários:
  1. **Cálculo próprio**: capacidade de corrente dos condutores calculada por física de troca de
     calor (método Neher-McGrath, 1957, domínio público), que é a base das tabelas IEC/NBR.
  2. **Regras da norma** (queda de tensão máxima, coordenação disjuntor e cabo, previsão mínima de
     pontos, taxa de ocupação de eletroduto) implementadas como critérios, citando o item.
  3. **Tabela do usuário**: quem tem a NBR 5410 pode carregar a tabela dela; o programa compara com
     o cálculo próprio e avisa diferenças.
  4. **Conferência** com projetos livres existentes (sclab-dimcabos, LGPL-3.0; dimensionador-nbr5410,
     MIT) nos testes automáticos.

---

## 4. Bibliotecas e recursos que vamos reaproveitar

| Recurso | Licença | Uso |
|---|---|---|
| FreeCAD (Part, Draft, BIM, TechDraw, Spreadsheet) | LGPL | base de geometria, planta, IFC e folhas |
| Cables Workbench | LGPL-3.0 | ideias e, se fizer sentido, compatibilidade (importar rotas/cabos) |
| QElectroTech, coleção de símbolos | CC-BY 3.0 | símbolos de comando e força, com crédito |
| sclab-dimcabos | LGPL-3.0 | conferência de resultados |
| Modelos ABNT para TechDraw (nosso) | CC0 | folhas dos documentos |
| STEP de fabricantes (WEG, Schneider, Siemens, ABB, Steck, Legrand, Tramontina, Sonoff, Aqara, Intelbras etc.) | termos de cada fabricante | **o usuário baixa e importa**; o programa só guarda o caminho e os dados que ele cadastrar |
| ezdxf | MIT | importar planta em DXF |
| ifcopenshell (já vem no FreeCAD) | LGPL | exportação IFC |

---

## 5. Arquitetura

```
FreeCAD-Eletrica-BR/
  eletrica_br/
    nucleo/            # Python puro, sem FreeCAD (cálculo e regras)
      cargas.py        # previsão de cargas, demanda
      condutores.py    # capacidade de corrente (cálculo próprio), queda de tensão
      protecao.py      # disjuntor, DR, DPS, coordenação, curto-circuito
      eletrodutos.py   # taxa de ocupação, dimensionamento
      rede.py          # cabeamento estruturado, orçamento de portas, PoE
      sem_fio.py       # cobertura Wi-Fi, malha Zigbee/Thread
      audio.py         # som ambiente e home theater
      memorial.py      # texto do memorial com fórmulas e itens da norma
    dados/             # catálogos em JSON/CSV (nossos, livres)
    biblioteca/        # componentes 3D e símbolos próprios (CC-BY)
    freecad/           # interface: comandos, objetos paramétricos, painéis
    documentos/        # geração de quadro de cargas, unifilar, listas no TechDraw
  testes/              # pytest: casos de referência e conferências
  docs/
```

Objetos paramétricos principais (FeaturePython):

- Ambiente (cômodo, área, perímetro, uso), Ponto (tomada TUG/TUE, luz, interruptor, dado, som,
  sensor), Circuito, Quadro, Dispositivo (disjuntor, DR, DPS, contator...), Eletroduto, Condutor,
  Rack, Equipamento de rede, Dispositivo de automação, Caixa de som.

Dados do usuário ficam em `~/FreeCAD-Eletrica-BR/` (fora da pasta Mod), para não se perderem nas
atualizações.

---

## 6. Módulos e etapas

### Etapa 0.1: núcleo de cálculo e quadro de cargas (primeira entrega)

- Cadastro de ambientes (área, perímetro, tipo) por formulário ou planilha.
- Previsão mínima de iluminação e tomadas por cômodo (NBR 5410 9.5.2).
- Cargas específicas (chuveiro, ar-condicionado, forno etc.) com catálogo editável.
- Divisão em circuitos, balanceamento de fases.
- Demanda e corrente de projeto.
- Condutor por capacidade de corrente (cálculo próprio + tabela do usuário) e por queda de tensão.
- Disjuntor (coordenação Ib ≤ In ≤ Iz), indicação de DR e DPS.
- Saída: quadro de cargas e memorial de cálculo (Spreadsheet + PDF na folha ABNT).
- Testes automáticos com casos resolvidos de livros e TCCs.

### Etapa 0.2: planta e simbologia

- Inserir pontos sobre a planta (BIM do FreeCAD, DXF importado ou imagem em escala).
- Simbologia NBR 5444 e IEC 60617, legenda automática.
- Desenho de eletrodutos e circuitos na planta, numeração automática.
- Comprimento real dos circuitos vindo da planta, alimentando o cálculo da queda de tensão.
- Sugestão do local do quadro pelo centro de cargas.

### Etapa 0.3: documentos completos

- Diagrama unifilar e multifilar automáticos no TechDraw.
- Lista de materiais por circuito, quadro e pavimento, com exportação CSV/XLSX.
- Orçamento com tabela de preços do usuário.
- Prancha completa nas folhas ABNT com carimbo preenchido.

### Etapa 0.4: quadro elétrico em 3D

- Trilho DIN, disjuntores, DR, DPS, barramentos, canaletas e bornes paramétricos (nossos).
- Importação de STEP de fabricante com cadastro dos bornes por clique (sem editar CSV).
- Layout do quadro gerado a partir do unifilar; verificação de espaço (módulos DIN).
- Etiquetas e identificação de circuitos.

### Etapa 0.5: comandos elétricos

- Esquema de força e comando em 2D com símbolos do QElectroTech (CC-BY).
- Referência cruzada bobina/contatos, numeração de fios e bornes, lista de bornes.
- Circuitos prontos: partida direta, reversão, estrela-triângulo, intertravamentos.
- Simulação simples do comando (inspirada no CADe SIMU).
- Importação/exportação com o QElectroTech.

### Etapa 0.6: instalação 3D e BIM

- Rota 3D de eletrodutos, eletrocalhas e cabos com o comprimento real.
- Lista de compra de cabos por tipo e bitola (o que falta no Cables).
- Detecção de interferência com estrutura e tubulações.
- Exportação IFC (IfcCableSegment, IfcCableCarrierSegment, IfcElectricDistributionBoard etc.).

### Etapa 0.7: automação residencial e redes (módulo para integradores)

**Planejamento por cômodo e função** (estilo KNX ETS / Loxone):

- Para cada ambiente: iluminação (on/off, dimmer, RGB/CCT, DALI), persianas e cortinas,
  climatização, tomadas inteligentes, sensores (presença, porta/janela, temperatura, umidade,
  fumaça, vazamento), fechaduras, interfone, câmeras, cenas.
- Escolha do protocolo por dispositivo: Wi-Fi, Zigbee, Z-Wave, Thread/Matter, KNX, RS-485/Modbus,
  DALI, com regras de compatibilidade e de neutro na caixa (interruptores inteligentes).
- Catálogo de dispositivos editável (Sonoff, Tuya, Aqara, Shelly, Intelbras, Philips Hue, KNX etc.),
  com consumo, protocolo, tamanho de caixa e necessidade de neutro.

**Redes sem fio:**

- Mapa de cobertura Wi-Fi sobre a planta com perdas por parede (alvenaria, drywall, laje, vidro),
  sugestão de posição de access points (estilo Ekahau/NetSpot, simplificado).
- Malha Zigbee/Thread: distância entre roteadores (dispositivos ligados na rede elétrica), alerta de
  dispositivos sem rota, posição do coordenador/hub.
- Canais e interferência entre Wi-Fi 2,4 GHz e Zigbee.

**Cabeamento estruturado (NBR 14565 / NBR 16264):**

- Pontos de dados, TV, CFTV e AP por cômodo; distribuidor/rack; comprimento máximo do enlace.
- Rack em 3D: patch panel, switch, roteador, NVR, nobreak, organizadores; cálculo de U.
- Orçamento de portas e de potência PoE do switch.
- Lista de cabos (Cat6/Cat6A, fibra, coaxial) e conectores.

**Documentação para o integrador:**

- Lista de dispositivos com cômodo, protocolo, endereço/ID, circuito elétrico e porta do switch.
- Planilha de comissionamento (endereços KNX, IDs Zigbee, IPs fixos, VLANs).
- Proposta comercial e orçamento (estilo D-Tools/Portal.io) com os preços do integrador.

### Etapa 0.8: som ambiente e home theater

**Som ambiente (multiroom):**

- Caixas de embutir (teto/parede) por ambiente com cobertura pelo ângulo de dispersão e altura do
  forro; espaçamento sugerido.
- Zonas, amplificadores e potência; impedância (8 ohms, 70/100 V para áreas grandes).
- Bitola e comprimento do cabo de caixa de som.
- Streamers e controle (Sonos, WiiM, Denon HEOS etc.) no catálogo.

**Home theater e sala de cinema:**

- Layouts 5.1, 5.1.2, 7.1.4, 9.1.6 com posição das caixas pelos ângulos dos guias Dolby Atmos e
  ITU-R BS.775, a partir da posição do assento principal.
- Distância de visualização e tamanho de tela (ângulo de visão), altura da tela, projetor (throw).
- Subwoofers: posição e alerta de modos da sala (cálculo dos modos axiais pelas dimensões).
- Infraestrutura: tubulação de cabos, pontos elétricos dedicados, rack de AV, ventilação.
- Saída: planta e cortes com a posição de cada caixa e a lista de equipamentos.

### Etapa 0.9+: extras

- SPDA (NBR 5419), iluminação (NBR ISO 8995-1), fotovoltaico, carregador de veículo elétrico.
- Tradução para inglês e espanhol (a base já nasce traduzível, com Crowdin).

---

## 7. Qualidade e engenharia de software (desde o primeiro commit)

Meta: o código entra limpo e certo na primeira vez, para não gastar tempo refazendo.

**Guardas automáticas (já criadas e testadas com defeito plantado):**

| Guarda | O que faz |
|---|---|
| `CLAUDE.md` | Regras curtas e pré-voo: escopo, arquitetura, nomes, tamanho, licença, definição de pronto |
| Hook `PostToolUse` (`.claude/settings.json`) | A cada arquivo `.py` editado roda Ruff + `sinais.py` + `duplicacao.py`; erro bloqueia na hora |
| `pyproject.toml` (Ruff) | Complexidade ≤ 10, função ≤ 50 comandos, ≤ 6 argumentos, `print` proibido, código comentado, except genérico |
| `sinais.py` | Debug esquecido, except nu, erro engolido, comentário narrativo, TODO sem issue (com autoteste) |
| `duplicacao.py` | Bloco de 6+ linhas que já existe em outro arquivo: reusar em vez de copiar (com autoteste) |

**Skills do projeto (`.claude/skills`):**

| Skill | Quando |
|---|---|
| `rotina` | Início e fim de toda tarefa; antes de afirmar resultado; registro de lições |
| `codigo-enxuto` | Antes de commit: réguas + o que régua nenhuma vê |
| `revisao` | Antes de "pronto": desenho, cálculo, funcionamento no FreeCAD, testes, licença |
| `decidir` | Bifurcação, dependência nova, 2ª tentativa |
| `calculo-normativo` (nova, deste projeto) | Todo cálculo: fonte, unidade, limite, caso de referência, sabotagem do teste |
| subagente `revisor-independente` | Segunda opinião com contexto limpo em fórmula, critério e arredondamento |

**Testes:** pytest no núcleo (casos de referência com fonte, invariantes, bordas, sabotagem),
`freecadcmd` para os objetos dentro do FreeCAD, GitHub Actions a cada push.

**Autoria e uso de IA:** o código segue o padrão de um projeto mantido por gente experiente, e a
responsabilidade técnica é do dono. No repositório próprio, como registrar a ferramenta usada é
decisão do dono. Em contribuição para o repositório do FreeCAD, a política do projeto (jun/2026)
exige declarar o uso de IA na descrição do PR; seguir essa regra.

## 8. Licença, direitos e sustentabilidade

Decisão de 22/10/2026: **todo o projeto é livre e gratuito.**

Motivos:

- custo quase zero para manter (GitHub, Actions, Pages, Addon Manager, fórum e Crowdin são gratuitos
  para projeto livre); o investimento é só tempo;
- sem compromisso de suporte pago: o projeto evolui no ritmo do autor;
- mais usuários, testes, traduções e divulgação.

Regras que deixam opções abertas para o futuro (sem custo):

1. **Licença LGPL-3.0** para todo o código; bibliotecas e símbolos próprios em CC-BY 4.0.
2. **Termo de cessão para colaboradores (CLA)** no repositório: quem contribui cede os direitos ao
   autor. Assim o autor continua dono de todo o código e pode, no futuro, lançar módulos novos com
   outra licença sem depender de terceiros. O que já foi publicado livre continua livre.
3. **Núcleo separado dos módulos** (seção 5), que também é boa prática de engenharia.
4. **Marca "Elétrica BR"**: registro no INPI quando o projeto tiver usuários.

Como o projeto se sustenta (retorno indireto):

| Fonte | Como |
|---|---|
| Uso próprio | A Elo-Tech e a Tofus Automação projetam quadros, comandos, instalações e automação mais rápido, sem licenças pagas |
| Cursos e treinamentos | Online e presenciais, para eletricistas, integradores e escolas técnicas |
| Serviços | Projetos para terceiros, consultoria, personalização para empresas |
| Apoio | GitHub Sponsors, Apoia.se, bolsas da FreeCAD Project Association |
| Parcerias | Fabricantes que fornecem modelos oficiais ou patrocinam conteúdo |
| Reputação | Autor da ferramenta brasileira de elétrica do FreeCAD |

## 9. Publicação e comunidade

- Repositório público `Tofus-BR/FreeCAD-Eletrica-BR` (LGPL-3.0).
- Envio ao Addon Manager a cada etapa estável (como os Modelos ABNT, issue 182).
- Wiki com tutoriais em português e vídeos curtos.
- Tópico no fórum do FreeCAD (seção em português e External Workbenches).
- Contato com o autor do Cables para compatibilidade, sem depender dele.
- Convite a eletricistas, integradores e professores de cursos técnicos para testar.

---

## 10. Cronograma sugerido (ritmo de projeto paralelo)

| Etapa | Entrega | Prazo estimado |
|---|---|---|
| 0.1 | Núcleo de cálculo + quadro de cargas + memorial | 3 a 4 semanas |
| 0.2 | Planta e simbologia | 4 semanas |
| 0.3 | Unifilar, listas e pranchas | 3 semanas |
| 0.4 | Quadro elétrico 3D | 4 semanas |
| 0.5 | Comandos elétricos | 5 semanas |
| 0.6 | Instalação 3D e IFC | 5 semanas |
| 0.7 | Automação e redes | 6 semanas |
| 0.8 | Som ambiente e home theater | 4 semanas |

Os prazos dependem do tempo disponível; cada etapa só é publicada depois de testada.

---

## 11. Próximos passos imediatos

1. Criar o repositório e a estrutura de pastas (seção 5), com LICENSE (LGPL-3.0), CLA e CONTRIBUTING.
2. Reunir 5 a 10 casos resolvidos de projeto residencial para os testes da etapa 0.1.
3. Implementar o cálculo próprio de capacidade de corrente e conferir com sclab-dimcabos.
4. Implementar previsão de cargas, circuitos, condutor, disjuntor e quadro de cargas.
5. Gerar o memorial em PDF na folha ABNT.
6. Testar num projeto real (Elo-Tech ou Tofus Automação) antes de publicar.
