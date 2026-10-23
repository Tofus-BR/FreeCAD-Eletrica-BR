---
name: freecad-addon
description: Como escrever a parte FreeCAD deste addon do jeito que o próprio FreeCAD espera — bancada (InitGui), comandos, objetos paramétricos FeaturePython e ViewProvider, propriedades com unidade, salvar e reabrir, tradução, ícones, package.xml e compatibilidade entre versões. Use ao criar ou mudar qualquer coisa em eletrica_br/freecad, eletrica_br/documentos, InitGui.py, Init.py ou package.xml.
when_to_use: novo comando, objeto, painel ou documento; mudança em propriedade salva no arquivo; antes de publicar versão no Addon Manager.
---

# Addon do FreeCAD

Fonte primária, nesta ordem: o código do FreeCAD instalado (`/Applications/FreeCAD.app/Contents/
Resources/Mod`), a wiki (wiki.freecad.org: "Workbench creation", "FeaturePython Objects",
"Package Metadata", "Translating an external workbench") e addons maduros (BIM, Draft). Confira
na versão instalada antes de usar uma API; não use de memória.

## 1. Estrutura

- `InitGui.py`: só a classe da bancada (`Gui.Workbench`) e o registro. **Importação preguiçosa**:
  nada pesado no topo; os módulos são importados dentro de `Initialize()` e dos comandos. Bancada
  que atrasa a abertura do FreeCAD é rejeitada pelos usuários.
- Comandos: uma classe por comando com `GetResources()` (ícone, texto e dica traduzidos),
  `IsActive()` barato e `Activated()`. Registro com `Gui.addCommand("EletricaBR_<Nome>", ...)`.
- Interface separada do núcleo: o comando lê o documento, chama `eletrica_br.nucleo` e escreve o
  resultado. Cálculo nunca dentro de comando, painel ou ViewProvider.

## 2. Objetos paramétricos (FeaturePython)

- Proxy do objeto (dados e `execute`) separado do ViewProvider (aparência, ícone, menu de contexto).
- Propriedades com tipo de unidade quando houver (`App::PropertyLength`, `PropertyArea`,
  `PropertyElectricPotential`, `PropertyPower` etc.), grupo e dica traduzida com
  `QT_TRANSLATE_NOOP("App::Property", "...")`.
- Salvar e reabrir: o proxy implementa `dumps`/`loads` (retornando `None` quando não há estado
  próprio) e `onDocumentRestored` para **migrar propriedade nova** em arquivo antigo
  (`if not hasattr(obj, "NovaProp"): obj.addProperty(...)`). Arquivo de versão anterior tem de abrir.
- `execute` não chama `recompute`, não abre janela e não depende da interface (precisa rodar no
  `freecadcmd`).
- Nome interno estável (`Type`), texto visível traduzido.

## 3. Dados e arquivos do usuário

- Catálogos, tabelas carregadas e bibliotecas do usuário em `~/FreeCAD-Eletrica-BR/` (ou
  `App.getUserAppDataDir()`), **nunca** dentro da pasta do addon: a atualização apaga o que estiver lá.
- Catálogo do usuário sobrescreve o padrão pelo identificador; o padrão vem com o addon.

## 4. Tradução e textos

- Todo texto visível por `translate("EletricaBR", "...")` ou `QT_TRANSLATE_NOOP`.
- Arquivos `.ts` em `eletrica_br/traducoes/`, gerados com `lupdate`; textos em português na
  origem e inglês como primeira tradução.

## 5. Ícones

SVG 64×64 próprios (ou CC-BY com crédito em `THIRD_PARTY.md`), sem texto dentro do ícone, com
`font-family` existente (evite `sans-serif` genérico, que gera aviso de fonte no macOS).

## 6. package.xml e publicação

- `package.xml` com nome, descrição, versão (igual ao `__version__`), data, mantenedor, licença
  `LGPL-3.0-or-later`, URLs (repositório, issues, documentação), ícone, `<workbench>` com `classname`
  e `subdirectory`, e `freecadmin` da menor versão testada.
- Antes de pedir inclusão no Addon Manager: release com tag, README com imagem, tópicos `freecad`
  e `addon` no GitHub, testado na versão estável atual e na próxima (release candidate).

## 7. Compatibilidade

- Teste na versão estável instalada (1.1.x) e, antes de cada release, na próxima (26.x RC).
  O Cables quebrou na 26.3 (ícones e hierarquia perdidos): objeto que perde o ViewProvider ao
  reabrir é o primeiro sinal; o teste de salvar/reabrir no `freecadcmd` precisa cobrir isso.
- Nada de API privada (`_algo`) do FreeCAD.
