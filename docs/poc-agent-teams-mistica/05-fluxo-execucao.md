# 05 — Fluxo de Execucao Detalhado

Passo a passo de cada wave, com o que cada ator faz, o que esperar e como reagir.

---

## Diagrama Geral

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  WAVE 1  │────>│  WAVE 2  │────>│  WAVE 3  │────>│  WAVE 4  │────>│  WAVE 5  │
│ 3 tasks  │     │ 2 tasks  │     │ 3 tasks  │     │ 3 tasks  │     │ 1 task   │
│ paralelo │     │ paralelo │     │ paralelo │     │ paralelo │     │ serial   │
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
    ↓                 ↓                ↓                 ↓                ↓
  MERGE             MERGE           MERGE             MERGE            MERGE
 (humano)          (humano)        (humano)          (humano)         (humano)
```

---

## WAVE 1 — Setup Base (3 tasks em paralelo)

### O que acontece

| Teammate | Task | Agent | Arquivos | Tempo Est. |
|----------|------|-------|----------|-----------|
| backend-dev-1 | 01: Schemas | developer | schemas.py, __init__.py, test_schemas.py | 3-5 min |
| backend-dev-2 | 02: Database | developer | database.py, db_models.py, test_database.py | 3-5 min |
| frontend-dev | 03: Next.js+Mistica | frontend-developer | layout.tsx, page.tsx, api.ts, next.config.ts, package.json | 5-8 min |

### Fluxo do Lead

1. **Cria equipe** com TeamCreate
2. **Spawna 3 teammates** em paralelo com Agent tool
3. **Atualiza labels**: `gh issue edit 1,2,3 --add-label "in-progress" --remove-label "ready"`
4. **Monitora** mensagens dos teammates
5. Quando um teammate abre PR:
   - Atualiza label para "pr-open"
   - **Lanca 3 reviewers LOCALMENTE em paralelo** (security, quality, test)
   - Cada reviewer: le diff com `gh pr diff <PR>` → analisa → posta comentario via `gh pr comment <PR>`
   - Lead posta comentario consolidado no PR
6. Se reviews OK: informa humano "PRs prontos para merge"
7. Se review detecta problema: notifica teammate → corrige → re-review

### O que o humano faz

```bash
# Ver PRs abertos (ja terao comentarios dos reviewers)
gh pr list

# Ver comentarios dos reviewers em um PR
gh pr view <PR> --comments

# Merge (3 PRs)
gh pr merge <PR_1> --merge
gh pr merge <PR_2> --merge
gh pr merge <PR_3> --merge
```

### Retomar

```
Os 3 PRs da Wave 1 foram merged (task-01, task-02, task-03).
Feche as issues, atualize o board e distribua a Wave 2.
```

---

## WAVE 2 — Core Backend (2 tasks em paralelo)

### O que acontece

| Teammate | Task | Agent | Arquivos | Tempo Est. |
|----------|------|-------|----------|-----------|
| backend-dev-1 | 04: CRUD | developer | repositories.py, test_repositories.py | 5-7 min |
| backend-dev-2 | 05: Auth JWT | developer | auth.py, auth_router.py, test_auth.py | 5-7 min |
| frontend-dev | (idle) | - | - | - |

### Nota
O frontend-dev fica idle porque nenhuma task frontend esta READY ainda.
O Lead pode usar esse tempo para fazer o frontend-dev revisar o codigo
existente ou preparar o terreno.

### O que o Lead faz

1. **Puxa main** nos teammates: cada um faz `git pull origin main`
2. **Distribui** task-04 e task-05
3. **Atualiza labels**: mover 04 e 05 para "in-progress"
4. Aguarda PRs e executa reviews

### Merge pelo humano

```bash
gh pr merge <PR_04> --merge
gh pr merge <PR_05> --merge
```

### Retomar

```
PRs da Wave 2 merged (task-04, task-05).
Distribua a Wave 3.
```

---

## WAVE 3 — API + Auth UI + Testes (3 tasks)

### O que acontece

| Teammate | Task | Agent | Arquivos | Deps | Tempo Est. |
|----------|------|-------|----------|------|-----------|
| backend-dev-1 | 06: API Endpoints | developer | task_router.py, app.py | 04, 05 | 5-7 min |
| frontend-dev | 07: Auth UI Mistica | frontend-developer | auth.tsx, login/page.tsx, register/page.tsx, ProtectedRoute.tsx | 03, 05 | 7-10 min |
| backend-dev-2 | 08: Testes E2E | developer | conftest.py, test_integration.py | 06 | 5-7 min |

### Ordem de dependencia
- task-06 e task-07 podem comecar imediatamente (deps satisfeitas)
- task-08 depende de task-06, entao **backend-dev-2 comeca DEPOIS que task-06 gera PR**

O Lead pode:
1. Distribuir task-06 e task-07 imediatamente
2. Aguardar task-06 ter PR → distribuir task-08
3. OU esperar o merge de task-06 para garantir

### Componentes Mistica usados na task-07

```
Form, TextField, PasswordField, EmailField
ResponsiveLayout, Stack, Boxed
Title1, Text2
ButtonPrimary, ButtonLink
Spinner
```

---

## WAVE 4 — UI + Dashboard + VULNERABILIDADE (3 tasks)

### O que acontece

| Teammate | Task | Agent | Arquivos | Deps | Tempo Est. |
|----------|------|-------|----------|------|-----------|
| frontend-dev | 09: Task UI | frontend-developer | tasks/page.tsx, new/page.tsx, [id]/edit/page.tsx, TaskCard.tsx, StatusBadge.tsx | 03, 06 | 10-12 min |
| backend-dev-1 | 11: Search [VULN] | developer | search_router.py, test_search.py | 06 | 5-7 min |
| backend-dev-2 | (aguarda) | - | - | - | - |

> **task-10** (Dashboard) depende de task-07 E task-09. So pode comecar depois que
> ambas estejam merged. Pode ser feita nesta wave se 09 terminar rapido, ou na Wave 5.

### CENARIO DE SEGURANCA (task-11)

Este e o momento critico da demo. Veja [06-cenario-seguranca.md](./06-cenario-seguranca.md) para detalhes.

**O que acontece:**
1. backend-dev-1 implementa task-11 (endpoint /search/tasks sem auth, retornando email)
2. Cria PR normalmente
3. Lead **lanca os 3 reviewers LOCALMENTE** no PR da task-11:
   - Cada reviewer executa `gh pr diff <PR>` para ler as mudancas
   - Cada reviewer posta seu comentario no PR via `gh pr comment <PR> --body "..."`
4. security-reviewer POSTA no PR que detectou:
   - Sensitive Data Exposure: endpoint retorna email do owner sem auth
   - Broken Access Control: todas as tasks visiveis sem auth
5. Lead POSTA comentario consolidado no PR com veredicto ❌
6. Lead NOTIFICA backend-dev-1 via SendMessage com os problemas encontrados
7. backend-dev-1 CORRIGE no codigo, commit + push (PR atualiza automaticamente)
8. Lead **re-lanca os reviewers** no PR atualizado
9. Reviewers postam novos comentarios confirmando correcao ✅
10. Lead informa humano que PR esta pronto para merge

### Componentes Mistica usados na task-09

```
RowList, Row, DataCard, SnapCard
Tabs (filtros de status)
Form, TextField, Select
Tag (status badge, priority badge)
EmptyState, Spinner
ButtonPrimary, ButtonSecondary, ButtonDanger
useDialog (confirmacao de delete)
```

---

## WAVE 5 — Feedback + Dashboard (1-2 tasks)

### O que acontece

| Teammate | Task | Agent | Arquivos | Deps | Tempo Est. |
|----------|------|-------|----------|------|-----------|
| frontend-dev | 10: Dashboard | frontend-developer | dashboard/page.tsx | 07, 09 | 7-10 min |
| frontend-dev | 12: Feedback | frontend-developer | (modifica paginas existentes) | 09, 10 | 5-7 min |

> Se task-10 nao coube na Wave 4, ela e feita aqui junto com task-12.
> task-12 depende de 09 e 10, entao executa apos task-10.

### Componentes Mistica na task-10

```
DataCard (stats)
ProgressBar (% conclusao)
RowList, Row (tasks recentes)
Tag (status)
Callout (dica do dia)
Title1, Text2
Spinner
```

### Componentes Mistica na task-12

```
useSnackbar() — feedback de acoes CRUD
SuccessFeedbackScreen — apos registro
ErrorFeedbackScreen — erros de API
EmptyState — listas vazias
Spinner — loading global
SkeletonRectangle — skeleton loading
```

---

## Timeline Estimada

| Fase | Duracao | Acumulado |
|------|---------|-----------|
| Pre-flight + Prompt | 3 min | 3 min |
| Wave 1 (3 tasks) | 8-10 min | 13 min |
| Review + Merge W1 | 3 min | 16 min |
| Wave 2 (2 tasks) | 7-8 min | 24 min |
| Review + Merge W2 | 3 min | 27 min |
| Wave 3 (3 tasks) | 10-12 min | 39 min |
| Review + Merge W3 | 3 min | 42 min |
| Wave 4 (3 tasks + correcao seg.) | 12-15 min | 57 min |
| Review + Merge W4 | 5 min | 62 min |
| Wave 5 (1-2 tasks) | 10-12 min | 74 min |
| Review + Merge W5 | 3 min | 77 min |
| **TOTAL** | **~70-80 min** | |

---

## Monitoramento em Tempo Real

### Terminal split recomendado

```
┌─────────────────────────────────┬──────────────────────────┐
│                                 │  gh pr list --watch      │
│   Claude Code (Lead)            │  (atualiza a cada 5s)    │
│                                 ├──────────────────────────┤
│                                 │  gh issue list           │
│                                 │  --label "in-progress"   │
└─────────────────────────────────┴──────────────────────────┘
```

### Comandos uteis durante a execucao

```bash
# PRs abertos
gh pr list

# Issues em progresso
gh issue list --label "in-progress"

# Issues com PR aberto
gh issue list --label "pr-open"

# Ver branches
git fetch && git branch -r

# Merge rapido via CLI
gh pr merge <N> --merge
```

---

Proximo: [06 — Cenario de Falha de Seguranca](./06-cenario-seguranca.md)
