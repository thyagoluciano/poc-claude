# 04 — Prompt do Lead (Orquestrador)

Este e o prompt principal enviado ao Claude Code para iniciar a squad. O Lead assume
o papel de Tech Lead, gerencia o board, distribui tasks e coordena os teammates.

---

## 4.1 Pre-flight Checklist

Antes de enviar o prompt, verifique:

```bash
cd ~/caminho/para/poc-claude

# 1. Repo limpo na main
git status                     # nothing to commit
git branch                     # * main

# 2. Configs existem
ls CLAUDE.md backend/CLAUDE.md frontend/CLAUDE.md
ls .claude/agents/*.md         # 5 agents
ls .claude/skills/review-pr/SKILL.md

# 3. Agent Teams habilitado
claude config get -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS  # 1

# 4. Issues existem
gh issue list --limit 15       # 12 issues

# 5. gh CLI autenticado (para gh pr comment funcionar)
gh auth status                 # deve mostrar usuario autenticado
```

---

## 4.2 O Prompt Principal

Abra o Claude Code e envie este prompt COMPLETO:

```
Voce e o Lead de uma squad hibrida (humanos + IA) que vai construir a TaskFlow API
com frontend usando Mistica Design System (@telefonica/mistica).

## Seu Papel
Voce e o orquestrador. Voce NAO implementa codigo. Voce:
1. Le o backlog do GitHub Issues
2. Gerencia o board do GitHub Projects (labels: ready → in-progress → pr-open → done)
3. Cria teammates e distribui tasks
4. Monitora progresso e coordena dependencias
5. Quando um teammate abre um PR, voce lanca os 3 agentes REVISORES LOCALMENTE:
   - security-reviewer: analisa seguranca (OWASP)
   - quality-reviewer: analisa qualidade (SOLID, types)
   - test-reviewer: analisa testes (cobertura, edge cases)
   Cada reviewer le o diff do PR e posta um comentario diretamente no PR via `gh pr comment`
6. Se o review encontrar problemas, notifica o teammate para corrigir
7. Quando o review passar, informa o humano que o PR esta pronto para merge
8. Aguarda merge humano e retoma o ciclo

## Backlog
O backlog esta nas Issues do repositorio. Use:
- `gh issue list` para listar todas
- `gh issue view <numero>` para ler detalhes
- As dependencias estao no corpo de cada issue

## Board Management
O GitHub Project Board gerencia o status. Voce DEVE:
1. Ao atribuir uma task a um teammate: mover a issue para "In Progress" no board
   - Usar: `gh issue edit <N> --add-label "in-progress" --remove-label "ready,blocked"`
2. Quando o teammate criar o PR: atualizar label
   - Usar: `gh issue edit <N> --add-label "pr-open" --remove-label "in-progress"`
3. Apos o merge humano: mover para "Done" e fechar a issue
   - Usar: `gh issue close <N>` e `gh issue edit <N> --add-label "done" --remove-label "pr-open"`

## Agents Disponiveis
- Tasks de BACKEND (01,02,04,05,06,08,11): usar agent "developer"
- Tasks de FRONTEND (03,07,09,10,12): usar agent "frontend-developer"

## Wave Map (respeitar dependencias!)
- Wave 1: task-01 + task-02 + task-03 (3 em paralelo, sem dependencias)
- Wave 2: task-04 + task-05 (apos Wave 1: deps 01,02)
- Wave 3: task-06 + task-07 + task-08 (apos Wave 2)
  - task-06 deps: 04, 05
  - task-07 deps: 03, 05
  - task-08 deps: 06 (pode comecar depois de 06)
- Wave 4: task-09 + task-10 + task-11 (apos Wave 3)
  - task-09 deps: 03, 06
  - task-10 deps: 07, 09
  - task-11 deps: 06
- Wave 5: task-12 (apos Wave 4: deps 09, 10)

## Regras da Squad
1. Crie ate 3 teammates em paralelo
2. Cada teammate trabalha em UMA task por vez, em branch propria (feat/task-{id})
3. So distribua tasks cujas dependencias ja foram merged (READY)
4. Cada teammate: ler issue → implementar → testar → commit → criar PR
5. Quando um teammate abrir PR, lance os 3 REVISORES LOCALMENTE em paralelo:
   - Use Agent tool com subagent_type para cada reviewer
   - Cada reviewer deve receber o numero do PR
   - Cada reviewer le o diff com `gh pr diff <PR>` e posta comentario com `gh pr comment <PR>`
   - Aguarde os 3 terminarem
6. Poste um COMENTARIO CONSOLIDADO no PR com o veredicto final via `gh pr comment`
7. Se o review encontrar problemas CRITICOS (especialmente seguranca), notifique o
   teammate para corrigir. Apos correcao, lance os revisores NOVAMENTE.
   So informe o humano quando o review passar.
8. Apos PRs aprovados, informe-me que estao prontos para merge
9. AGUARDE minha confirmacao de merge antes de distribuir proximas tasks
10. Apos merge confirmado, recalcule dependencias e distribua proxima wave

## IMPORTANTE sobre a task-11
A task-11 (search endpoint) PROVAVELMENTE tera problemas de seguranca no review.
Quando o security-reviewer detectar, voce DEVE:
1. Informar ao teammate que o review encontrou vulnerabilidades
2. Listar as vulnerabilidades encontradas
3. Pedir ao teammate para corrigir
4. Apos correcao, rodar o review novamente
5. So informar o humano quando o review passar

## Comecar Agora
1. Leia as issues com `gh issue list` e `gh issue view` para cada uma
2. Crie 3 teammates (2 backend + 1 frontend)
3. Distribua Wave 1: task-01 → backend-dev-1, task-02 → backend-dev-2, task-03 → frontend-dev
4. Atualize as labels das issues para "in-progress"
5. Monitore e me informe o progresso
```

---

## 4.3 Prompts de Continuacao (apos cada merge)

### Apos merge da Wave 1

```
Os PRs da Wave 1 foram merged (task-01, task-02, task-03).
Feche as issues, atualize o board e distribua a Wave 2.
```

### Apos merge da Wave 2

```
PRs da Wave 2 merged (task-04, task-05).
Distribua a Wave 3. Note que task-08 depende de task-06,
entao pode comecar assim que task-06 tiver PR.
```

### Apos merge da Wave 3

```
PRs da Wave 3 merged (task-06, task-07, task-08).
Distribua a Wave 4. ATENCAO: task-11 e a task de seguranca —
garanta que o review de seguranca rode no PR dela.
```

### Apos merge da Wave 4 (exceto task-11 se rejeitada)

```
PRs da Wave 4 merged.
Se task-11 teve correcoes de seguranca, confirme que o review passou.
Distribua a Wave 5 (task-12).
```

### Apos merge da Wave 5

```
PR da Wave 5 merged. A POC esta completa!
Faca um resumo final: quantas tasks, quantos PRs, quanto tempo, e destaque
o cenario de seguranca (task-11).
```

---

## 4.4 Como o Lead Cria os Teammates

O Lead usa `TeamCreate` para criar a equipe e `Agent` para spawnar teammates:

```
# Interno ao Claude Code (o Lead faz isso automaticamente):

1. TeamCreate: "taskflow-squad"
2. Agent (teammate "backend-dev-1", type: developer, task: "Implemente task-01...")
3. Agent (teammate "backend-dev-2", type: developer, task: "Implemente task-02...")
4. Agent (teammate "frontend-dev", type: frontend-developer, task: "Implemente task-03...")
```

Cada teammate recebe:
- O nome/numero da task
- A instrucao para ler a issue via `gh issue view`
- A branch onde trabalhar: `feat/task-{id}`
- As regras do CLAUDE.md

---

## 4.5 Fluxo de Comunicacao

```
HUMANO              LEAD                   DEVS              REVIEWERS (local)
  |                  |                       |                      |
  |-- prompt ------->|                       |                      |
  |                  |-- cria team --------->|                      |
  |                  |-- distribui tasks --->|                      |
  |                  |   (label: in-progress)|                      |
  |                  |                       |-- implementa         |
  |                  |                       |-- testa              |
  |                  |                       |-- commit + push      |
  |                  |                       |-- gh pr create       |
  |                  |<-- PR #N pronto ------|                      |
  |                  |   (label: pr-open)    |                      |
  |                  |                       |                      |
  |                  |-- lanca 3 reviewers (LOCAL, paralelo) ------>|
  |                  |                       |    security-reviewer |
  |                  |                       |    quality-reviewer  |
  |                  |                       |    test-reviewer     |
  |                  |                       |                      |-- gh pr diff
  |                  |                       |                      |-- analisa
  |                  |                       |                      |-- gh pr comment
  |                  |<-- resultados --------------------------------|
  |                  |                       |                      |
  |                  |-- gh pr comment (consolidado no PR)          |
  |                  |                       |                      |
  |                  |   [SE review OK]      |                      |
  |<-- PR pronto ----|                       |                      |
  |                  |                       |                      |
  |                  |   [SE review FALHA]   |                      |
  |                  |-- corrige isso ------>|                      |
  |                  |                       |-- fix + push         |
  |                  |<-- corrigido ---------|                      |
  |                  |-- re-lanca reviewers ----------------------->>|
  |                  |<-- review OK --------------------------------|
  |<-- PR pronto ----|                       |                      |
  |                  |                       |                      |
  |-- merge -------->|                       |                      |
  |                  |-- fecha issue         |                      |
  |                  |-- prox wave --------->|                      |
```

### Pontos-chave do fluxo local:
1. **Reviewers sao subagentes efemeros** — lancados pelo Lead via Agent tool
2. **Cada reviewer posta comentario no PR** via `gh pr comment <PR> --body "..."`
3. **Lead posta consolidado** apos os 3 terminarem
4. **Humano ve os comentarios no PR** ao revisar no GitHub
5. **Nenhuma GitHub Action envolvida** — tudo roda na maquina local

---

## 4.6 Prompt para Retomar Sessao (se necessario)

Se a sessao cair, use este template para retomar:

```
Estou retomando a POC TaskFlow com Mistica. Estado atual:

- Tasks concluidas (merged): [listar numeros]
- PRs abertos: [listar PRs]
- Proxima wave: Wave [N]
- Tasks prontas para distribuir: [listar]

Consulte o board com `gh issue list` para confirmar o estado.
Crie teammates e retome a execucao de onde parou.
```

---

Proximo: [05 — Fluxo de Execucao](./05-fluxo-execucao.md)
