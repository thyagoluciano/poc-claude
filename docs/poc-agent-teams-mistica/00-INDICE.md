# PoC Agent Teams com Mistica Design System

## Objetivo

Demonstrar o uso de **Claude Code Agent Teams** para construir uma aplicacao full-stack
com um Lead orquestrando agentes desenvolvedores (frontend e backend), agentes de review
(seguranca, qualidade, testes), integracao com GitHub Projects board e human-in-the-loop
para merge de PRs.

O frontend usa o **Mistica Design System** da Telefonica (`@telefonica/mistica`).

Uma task introduz intencionalmente uma **falha de seguranca** para demonstrar que o
review automatizado detecta e notifica o desenvolvedor para corrigir.

## Indice

| # | Documento | Descricao |
|---|-----------|-----------|
| 01 | [Configuracao Inicial](./01-configuracao-inicial.md) | CLAUDE.md, agents, skills, settings |
| 02 | [Backlog com Mistica](./02-backlog-mistica.md) | Novas tasks usando Mistica Design System |
| 03 | [Setup do Board GitHub](./03-setup-board-github.md) | Criar project board, issues e automacoes |
| 04 | [Prompt do Lead](./04-prompt-lead.md) | O prompt que inicia a orquestracao |
| 05 | [Fluxo de Execucao](./05-fluxo-execucao.md) | Passo a passo de cada wave |
| 06 | [Cenario de Falha de Seguranca](./06-cenario-seguranca.md) | Task com vulnerabilidade e fluxo de correcao |
| 07 | [Troubleshooting](./07-troubleshooting.md) | Problemas comuns e solucoes |

## Arquitetura da Squad

```
                    +------------------+
                    |    HUMANO        |
                    |  (merge PRs)     |
                    +--------+---------+
                             |
                    +--------v---------+
                    |     LEAD         |
                    | (orquestrador)   |
                    +--+-----+-----+--+
                       |     |     |
              +--------+  +--+--+  +--------+
              |           |     |           |
     +--------v---+ +----v----+ +---v--------+
     | backend-dev | |front-dev| | reviewers  |
     | (developer) | |(front)  | | (LOCAL)    |
     +-------------+ +---------+ +------------+
                                   - security  → gh pr comment
                                   - quality   → gh pr comment
                                   - tests     → gh pr comment
```

> Tudo roda LOCALMENTE. Os reviewers sao lancados pelo Lead como subagentes
> e postam seus comentarios diretamente no PR via `gh pr comment`.
> Nenhuma GitHub Action e necessaria.

## Pre-requisitos

- Claude Code CLI instalado e autenticado
- `gh` CLI autenticado com acesso ao repositorio
- Node.js 18+ e Python 3.12+ instalados
- Agent Teams habilitado: `claude config set -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1`
