# Como contribuir

Obrigado pelo interesse no Elétrica BR.

## Antes de começar

1. Abra uma issue descrevendo o problema ou a proposta. Mudança grande sem conversa prévia pode
   não ser aceita.
2. Leia o [plano de desenvolvimento](docs/PLANO_DE_DESENVOLVIMENTO.md) e as regras do
   [CLAUDE.md](CLAUDE.md), que valem para qualquer contribuição (arquitetura, nomes, tamanho,
   testes e licença).

## Padrão do código

- Python 3.11, `uv run ruff check .` e `uv run ruff format .` limpos.
- Cálculo em `eletrica_br/nucleo`, sem importar o FreeCAD, com teste de caso de referência que
  cite a fonte (livro, norma ou exemplo publicado).
- Texto de interface traduzível (`translate("EletricaBR", ...)`).
- Nada de tabela copiada de norma, nem modelo 3D ou símbolo sem licença compatível.

## Pull requests

- Uma mudança por PR, com testes.
- Descreva o que muda, como testou e o caso de referência usado.
- Se usou ferramentas de IA para gerar parte do código, diga no PR; a responsabilidade pelo
  código continua sendo de quem envia.

## Termo de cessão de direitos (CLA)

Para que o projeto possa ser mantido e relicenciado no futuro sem depender de cada colaborador,
toda contribuição exige concordar com o termo abaixo. Ao abrir um PR, inclua na descrição a
frase: **"Li e concordo com o termo de cessão do CONTRIBUTING.md."**

> Cedo ao mantenedor do projeto, Andrew Steven, de forma gratuita, irrevogável e mundial, os
> direitos patrimoniais de autor sobre a minha contribuição, incluindo o direito de distribuí-la
> sob a licença do projeto ou sob outra licença. Declaro que a contribuição é obra minha ou que
> tenho direito de cedê-la, e que ela não contém material de terceiros sem licença compatível. O
> que já foi publicado sob licença livre continua disponível sob essa licença.

Este termo é um modelo; o mantenedor pode substituí-lo por versão revisada por advogado, e a
versão vigente é a que estiver neste arquivo na data do PR.
