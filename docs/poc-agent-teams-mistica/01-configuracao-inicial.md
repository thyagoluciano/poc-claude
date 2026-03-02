# 01 — Configuracao Inicial

Este documento detalha TODOS os arquivos de configuracao necessarios para a PoC.
Copie cada arquivo exatamente como descrito.

---

## 1.1 Estrutura de Diretorios

**Monorepo simples** — `backend/` e `frontend/` na raiz. O Mistica e uma dependencia
npm normal instalada no `frontend/package.json`. Nao ha pasta separada para design system.

```
poc-claude/
├── .claude/                          # Configuracao do Claude Code
│   ├── agents/
│   │   ├── developer.md              # Backend dev agent
│   │   ├── frontend-developer.md     # Frontend dev agent (Mistica)
│   │   ├── security-reviewer.md      # Security reviewer (READ-ONLY + gh comment)
│   │   ├── quality-reviewer.md       # Quality reviewer (READ-ONLY + gh comment)
│   │   └── test-reviewer.md          # Test reviewer (READ-ONLY + gh comment)
│   ├── skills/
│   │   └── review-pr/
│   │       └── SKILL.md              # Parallel PR review skill (LOCAL)
│   └── settings.local.json           # Permissions
├── backend/                          # Python/FastAPI
│   ├── src/taskflow/                 # Codigo-fonte
│   │   ├── __init__.py
│   │   ├── app.py                    # FastAPI application
│   │   ├── schemas.py                # Pydantic models
│   │   ├── database.py               # SQLAlchemy config
│   │   ├── db_models.py              # SQLAlchemy models
│   │   ├── repositories.py           # CRUD operations
│   │   ├── auth.py                   # JWT authentication
│   │   ├── auth_router.py            # Auth endpoints
│   │   ├── task_router.py            # Task endpoints
│   │   └── search_router.py          # Search endpoint (task-11)
│   ├── tests/                        # pytest
│   │   ├── conftest.py
│   │   ├── test_schemas.py
│   │   ├── test_database.py
│   │   ├── test_repositories.py
│   │   ├── test_auth.py
│   │   ├── test_integration.py
│   │   └── test_search.py
│   ├── CLAUDE.md                     # Backend rules
│   └── pyproject.toml                # Dependencias Python
├── frontend/                         # Next.js + Mistica
│   ├── src/
│   │   ├── app/                      # App Router pages
│   │   │   ├── layout.tsx            # ThemeContextProvider + NavigationBar
│   │   │   ├── page.tsx              # Home
│   │   │   ├── login/page.tsx        # Login com Mistica Form
│   │   │   ├── register/page.tsx     # Register com Mistica Form
│   │   │   ├── dashboard/page.tsx    # Dashboard com DataCards
│   │   │   └── tasks/
│   │   │       ├── page.tsx          # Lista com RowList + Tabs
│   │   │       ├── new/page.tsx      # Criar task
│   │   │       └── [id]/edit/page.tsx # Editar task
│   │   ├── components/               # Componentes com Mistica
│   │   │   ├── ProtectedRoute.tsx
│   │   │   ├── TaskCard.tsx          # DataCard wrapper
│   │   │   └── StatusBadge.tsx       # Tag wrapper
│   │   └── lib/                      # Utilitarios
│   │       ├── api.ts                # HTTP client
│   │       ├── auth.tsx              # AuthContext + hooks
│   │       └── theme.ts              # Mistica theme config
│   ├── CLAUDE.md                     # Frontend rules (Mistica)
│   ├── next.config.ts                # optimizePackageImports: mistica
│   └── package.json                  # @telefonica/mistica como dep
├── docs/                             # Documentacao da PoC
│   └── poc-agent-teams-mistica/      # Este guia
└── CLAUDE.md                         # Regras globais
```

### Onde fica o Mistica?

| Item | Local |
|------|-------|
| **Instalacao** | `frontend/package.json` → `@telefonica/mistica` |
| **Theme config** | `frontend/src/lib/theme.ts` (skin, i18n) |
| **Provider** | `frontend/src/app/layout.tsx` (ThemeContextProvider) |
| **Componentes** | Importados direto: `import {Button} from '@telefonica/mistica'` |
| **Customizacoes** | Wrappers em `frontend/src/components/` (ex: TaskCard usa DataCard) |

Nao ha pasta `design-system/` separada. Componentes compostos (como TaskCard que
usa DataCard internamente) ficam em `frontend/src/components/`.

> **NOTA:** NAO ha GitHub Action para review. Todo o review e executado LOCALMENTE
> pelo Lead, que lanca os 3 reviewers como subagentes. Cada reviewer posta seu
> comentario diretamente no PR via `gh pr comment`.

---

## 1.2 CLAUDE.md (raiz do projeto)

```markdown
# CLAUDE.md — TaskFlow API

## Projeto
TaskFlow API: REST API de gerenciamento de tarefas com frontend usando Mistica Design System.

## Stack
- **Backend:** Python 3.12+, FastAPI, SQLAlchemy, Pydantic v2, pytest
- **Frontend:** Next.js 14+, TypeScript, Mistica Design System (@telefonica/mistica), App Router
- **Banco:** SQLite (dev), PostgreSQL (prod)
- **Auth:** JWT com python-jose, passlib[bcrypt]

## Estrutura do Projeto
backend/               # Backend Python/FastAPI
  src/taskflow/        # Codigo-fonte
  tests/               # Testes pytest
  pyproject.toml       # Dependencias Python
  CLAUDE.md            # Regras especificas do backend
frontend/              # Frontend Next.js/React
  src/app/             # App Router pages
  src/components/      # React components (Mistica)
  src/lib/             # Utilities (api.ts, auth.ts)
  CLAUDE.md            # Regras especificas do frontend

## Convencoes Globais
- Commits: Conventional Commits (feat:, fix:, test:, docs:, chore:)
- Um PR por task — branch: feat/task-{id}
- SEMPRE leia os arquivos existentes antes de criar novos
- Nunca commite secrets ou .env files
- Consulte o CLAUDE.md da pasta (backend/ ou frontend/) para regras especificas

## Backlog
O backlog esta nas Issues do repositorio GitHub. Use `gh issue list` para ver as tasks
e `gh issue view <numero>` para ler os detalhes.
O GitHub Project Board "TaskFlow - Mistica Squad" gerencia o status: Todo, In Progress, Done.
Respeite as dependencias entre tasks (descritas no corpo de cada issue).

## Board Management
O Lead deve:
1. Mover a issue para "In Progress" ao atribuir a um teammate
2. Mover para "Done" apos o merge do PR
3. Usar `gh project item-edit` para atualizar o status no board
```

---

## 1.3 backend/CLAUDE.md

```markdown
# Backend Rules — TaskFlow API

## Stack
- Python 3.12+, FastAPI, SQLAlchemy 2.0, Pydantic v2, pytest
- Auth: JWT com python-jose, passlib[bcrypt]
- Banco: SQLite (dev)

## Convencoes
- PEP 8, type hints obrigatorios em todas as funcoes
- Docstrings em funcoes publicas
- Imports relativos dentro de src/taskflow/
- Repository pattern para acesso a dados
- Dependency injection via FastAPI Depends

## Testes
- pytest com fixtures em conftest.py
- SQLite in-memory para testes
- Nomenclatura: test_should_*
- Minimo 80% coverage
- Rodar `cd backend && python -m pytest tests/ -v` antes de cada commit

## Estrutura
backend/
  src/taskflow/
    __init__.py
    schemas.py         # Pydantic models
    database.py        # SQLAlchemy config
    db_models.py       # SQLAlchemy models
    repositories.py    # CRUD operations
    auth.py            # JWT authentication
    auth_router.py     # Auth endpoints
    task_router.py     # Task endpoints
    app.py             # FastAPI application
  tests/
    conftest.py        # Fixtures compartilhadas
    test_schemas.py
    test_database.py
    test_repositories.py
    test_auth.py
    test_integration.py
  pyproject.toml       # Dependencias
```

---

## 1.4 frontend/CLAUDE.md (ATUALIZADO PARA MISTICA)

```markdown
# Frontend Rules — TaskFlow UI com Mistica

## Stack
- Next.js 14+, TypeScript strict, App Router
- UI: @telefonica/mistica (Mistica Design System da Telefonica)
- Estado: React Context API
- HTTP: Fetch API com wrapper em lib/api.ts

## Mistica Design System
- SEMPRE use componentes Mistica em vez de HTML puro ou Tailwind
- ThemeContextProvider obrigatorio no root layout com skin configurada
- Componentes principais:
  - Layout: ResponsiveLayout, Stack, Box, Boxed
  - Botoes: ButtonPrimary, ButtonSecondary, ButtonDanger, ButtonLink
  - Forms: Form, TextField, EmailField, PasswordField, Select
  - Cards: DataCard, SnapCard
  - Navegacao: NavigationBar, MainNavigationBar, Tabs
  - Feedback: Snackbar, FeedbackScreen, Tag, Badge
  - Tabelas: Table, RowList, Row
  - Tipografia: Text1-Text10, Title1-Title4
  - Progress: ProgressBar, Stepper
  - Outros: Divider, Spinner, Chip, Avatar, Callout, EmptyState

## Configuracao do Mistica

### lib/theme.ts — Configuracao centralizada do tema
```tsx
import {getMovistarSkin} from '@telefonica/mistica';
// Trocar por getVivoSkin() se for para Vivo

export const misticaTheme = {
  skin: getMovistarSkin(),
  i18n: {locale: 'pt-BR', phoneNumberFormattingRegionCode: 'BR'},
};
```

### layout.tsx — Importa o tema
```tsx
import {ThemeContextProvider} from '@telefonica/mistica';
import {misticaTheme} from '@/lib/theme';

// Envolver app com <ThemeContextProvider theme={misticaTheme}>
```

## next.config.ts
```ts
const nextConfig = {
  experimental: {
    optimizePackageImports: ['@telefonica/mistica'],
  },
};
```

## Convencoes
- TypeScript strict mode — nunca usar `any`
- Componentes funcionais com interfaces explicitas
- `'use client'` apenas quando necessario (interatividade)
- NAO usar Tailwind CSS — usar apenas componentes Mistica e CSS inline quando necessario
- Cliente API centralizado em lib/api.ts
- Tratar loading states, error states e empty states com componentes Mistica
- Para icones, usar os icones exportados pelo Mistica (Icon*)

## Estrutura
frontend/
  src/
    app/
      layout.tsx          # ThemeContextProvider + NavigationBar
      page.tsx            # Home page
      login/page.tsx      # Login com Mistica Form
      register/page.tsx   # Registro com Mistica Form
      dashboard/page.tsx  # Dashboard com DataCards e ProgressBar
      tasks/
        page.tsx          # Lista com RowList e filtros
        new/page.tsx      # Criar task com Mistica Form
        [id]/edit/page.tsx # Editar task
    components/
      ProtectedRoute.tsx  # Wrapper de auth
      TaskCard.tsx        # DataCard do Mistica
      StatusBadge.tsx     # Tag do Mistica
    lib/
      api.ts              # Cliente HTTP para a API
      auth.tsx            # AuthContext e helpers
      theme.ts            # Mistica theme config (skin + i18n)
```

---

## 1.5 Agentes (.claude/agents/)

### developer.md (Backend)

```markdown
---
name: developer
description: Desenvolvedor backend Python especializado em FastAPI, SQLAlchemy e pytest. Implementa tasks do backlog criando codigo, testes e fazendo commits.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
---

# Agente: Desenvolvedor Backend

## Persona
Voce e um desenvolvedor backend senior especializado em Python. Sua stack principal e FastAPI + SQLAlchemy + Pydantic + pytest.

## Stack e Conhecimento
- **Framework:** FastAPI com async support
- **ORM:** SQLAlchemy 2.0 com type hints
- **Validacao:** Pydantic v2 com EmailStr, Field validators
- **Auth:** JWT com python-jose, OAuth2 com passlib
- **Testes:** pytest com fixtures, httpx TestClient, SQLite in-memory
- **Padroes:** Repository pattern, dependency injection, type hints

## Regras de Trabalho
1. SEMPRE leia os arquivos existentes antes de criar novos
2. SEMPRE siga as convencoes do CLAUDE.md
3. Use type hints em todas as funcoes
4. Escreva docstrings em funcoes publicas
5. Crie testes para todo codigo novo
6. Rode `cd backend && python -m pytest tests/ -v` antes de fazer commit
7. Conventional Commits: feat:, fix:, test:, refactor:
8. Um commit por mudanca logica, um PR por task

## Fluxo de Trabalho
1. Leia a task atribuida via `gh issue view <numero>` e entenda os requisitos
2. Leia os arquivos existentes que serao impactados
3. Implemente o codigo seguindo a task description
4. Crie os testes unitarios
5. Rode pytest e corrija erros
6. Faca commit com mensagem descritiva
7. Crie o PR com titulo e descricao da task
```

### frontend-developer.md (Frontend com Mistica)

```markdown
---
name: frontend-developer
description: Desenvolvedor frontend especializado em Next.js, React, TypeScript e Mistica Design System. Implementa tasks de UI criando componentes, paginas e integracoes com API.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
---

# Agente: Desenvolvedor Frontend (Mistica)

## Persona
Voce e um desenvolvedor frontend senior especializado em React/Next.js com Mistica Design System.

## Stack e Conhecimento
- **Framework:** Next.js 14+ com App Router
- **Linguagem:** TypeScript strict mode
- **UI:** @telefonica/mistica — NUNCA use Tailwind ou CSS frameworks externos
- **Estado:** React Context API para auth, useState/useEffect para local state
- **HTTP:** Fetch API com wrapper customizado em lib/api.ts
- **Auth:** JWT armazenado em localStorage, AuthContext

## Mistica — Componentes que voce DEVE usar
- **Layout:** ResponsiveLayout, Stack, Box, Boxed, Inline
- **Navegacao:** MainNavigationBar, NavigationBar, Tabs, Breadcrumbs
- **Botoes:** ButtonPrimary, ButtonSecondary, ButtonDanger, ButtonLink, ButtonGroup
- **Forms:** Form, TextField, PasswordField, EmailField, Select
- **Cards:** DataCard, SnapCard, DisplayDataCard, MediaCard
- **Listas:** RowList, Row, BoxedRowList, BoxedRow
- **Feedback:** useSnackbar(), FeedbackScreen, SuccessFeedbackScreen, ErrorFeedbackScreen
- **Data Display:** Tag, Badge, Title1-4, Text1-10, Divider
- **Progress:** ProgressBar, Spinner, Stepper
- **Utils:** EmptyState, EmptyStateCard, Callout, Chip, Avatar

## Regras de Trabalho
1. SEMPRE leia os arquivos existentes antes de criar novos
2. SEMPRE use componentes Mistica — nunca HTML puro para UI
3. Use TypeScript strict — nunca `any`
4. Componentes funcionais com interfaces explicitas
5. Use 'use client' apenas quando necessario
6. Trate loading (Spinner), error (ErrorFeedbackScreen) e empty states (EmptyState)
7. Conventional Commits: feat:, fix:, style:, refactor:
8. Rode `cd frontend && npm run build` antes de fazer commit

## Fluxo de Trabalho
1. Leia a task via `gh issue view <numero>`
2. Leia componentes e paginas existentes
3. Implemente usando componentes Mistica
4. Teste com npm run build (zero erros TS)
5. Faca commit e crie PR
```

### security-reviewer.md (ATUALIZADO — agora posta no PR)

```markdown
---
name: security-reviewer
description: Revisor de seguranca especializado em OWASP Top 10. READ-ONLY no codigo, mas posta review no PR via gh CLI.
allowed-tools: Read, Glob, Grep, Bash
---

# Agente: Revisor de Seguranca

## Persona
Voce e um especialista em seguranca de aplicacoes. Analisa codigo e identifica
vulnerabilidades seguindo OWASP Top 10.

## IMPORTANTE
- Voce NAO modifica codigo-fonte. Apenas le e analisa.
- Voce DEVE postar seu review como comentario no PR via `gh pr comment`.
- O unico uso de Bash permitido e para `gh pr comment` e `gh pr diff`.

## Fluxo de Trabalho
1. Receba o numero do PR do Lead
2. Leia o diff do PR: `gh pr diff <PR_NUMBER>`
3. Leia os arquivos modificados para contexto completo
4. Analise seguranca (OWASP Top 10)
5. Poste o review no PR:
   ```bash
   gh pr comment <PR_NUMBER> --body "$(cat <<'EOF'
   ## Security Review

   [seu report aqui]
   EOF
   )"
   ```
6. Retorne o resultado ao Lead (aprovado/reprovado + resumo)

## Foco de Analise
1. **Injection** — SQL, Command, LDAP
2. **Broken Authentication** — JWT, senhas, OAuth2
3. **Sensitive Data Exposure** — dados pessoais, secrets, logs
4. **Broken Access Control** — IDOR, endpoints sem auth
5. **Security Misconfiguration** — CORS, debug mode, headers

## Formato do Comentario no PR

O comentario DEVE seguir este formato:

```markdown
## 🔒 Security Review

### Vulnerabilidades Encontradas
- **[CRITICA/ALTA/MEDIA/BAIXA]** Descricao
  - Arquivo: `path/to/file:linha`
  - Risco: Impacto
  - Correcao: Como resolver

### Boas Praticas Confirmadas
- ✅ Item correto

### Veredicto
- ✅ Aprovado / ⚠️ Ressalvas / ❌ Reprovado
```
```

### quality-reviewer.md (ATUALIZADO — agora posta no PR)

```markdown
---
name: quality-reviewer
description: Revisor de qualidade focado em SOLID, clean code e type hints. READ-ONLY no codigo, posta review no PR.
allowed-tools: Read, Glob, Grep, Bash
---

# Agente: Revisor de Qualidade

## Persona
Voce e um arquiteto de software que revisa qualidade, SOLID, clean code e typing.

## IMPORTANTE
- Voce NAO modifica codigo-fonte. Apenas le e analisa.
- Voce DEVE postar seu review como comentario no PR via `gh pr comment`.
- O unico uso de Bash permitido e para `gh pr comment` e `gh pr diff`.

## Fluxo de Trabalho
1. Receba o numero do PR do Lead
2. Leia o diff: `gh pr diff <PR_NUMBER>`
3. Leia os arquivos modificados
4. Analise qualidade (SOLID, DRY, types, naming)
5. Poste o review no PR via `gh pr comment`
6. Retorne resultado ao Lead

## Formato do Comentario no PR

```markdown
## 📋 Quality Review

### Problemas de Qualidade
- **[Severidade]** Descricao
  - Arquivo: `path:linha`
  - Principio violado: SOLID/DRY/Clean Code
  - Sugestao: Como melhorar

### Pontos Positivos
- ✅ Aspecto bem implementado

### Veredicto
- ✅ Aprovado / ⚠️ Ressalvas / ❌ Reprovado
```
```

### test-reviewer.md (ATUALIZADO — agora posta no PR)

```markdown
---
name: test-reviewer
description: Revisor de testes focado em cobertura, edge cases e assertions. READ-ONLY no codigo, posta review no PR.
allowed-tools: Read, Glob, Grep, Bash
---

# Agente: Revisor de Testes

## Persona
Voce e um QA engineer que revisa qualidade dos testes automatizados.

## IMPORTANTE
- Voce NAO modifica codigo-fonte. Apenas le e analisa.
- Voce DEVE postar seu review como comentario no PR via `gh pr comment`.
- O unico uso de Bash permitido e para `gh pr comment` e `gh pr diff`.

## Fluxo de Trabalho
1. Receba o numero do PR do Lead
2. Leia o diff: `gh pr diff <PR_NUMBER>`
3. Leia os arquivos de teste
4. Analise cobertura, edge cases, assertions
5. Poste o review no PR via `gh pr comment`
6. Retorne resultado ao Lead

## Formato do Comentario no PR

```markdown
## 🧪 Test Review

### Gaps de Cobertura
- **[Modulo]** O que falta
  - Cenario nao testado
  - Sugestao: `test_should_...`

### Cobertura Estimada
| Modulo | Cobertura | Status |
|--------|-----------|--------|

### Veredicto
- ✅ Aprovado / ⚠️ Ressalvas / ❌ Reprovado
```
```

---

## 1.6 Skill: review-pr (.claude/skills/review-pr/SKILL.md) — ATUALIZADO

A skill agora funciona 100% LOCAL. O Lead lanca 3 reviewers como subagentes,
cada um le o diff do PR e posta seu comentario diretamente no PR via `gh pr comment`.

```markdown
---
name: review-pr
description: Executa review paralelo do PR usando 3 subagentes locais. Cada reviewer posta comentario diretamente no PR via gh CLI.
argument-hint: "<PR-number>"
allowed-tools: Read, Glob, Grep, Bash, Agent
---

# Skill: Review de PR Local

Execute review completo de um PR usando 3 subagentes especializados em paralelo.
Cada reviewer posta seu comentario diretamente no PR via `gh pr comment`.

## Argumentos

Numero do PR: $ARGUMENTS
- Se nao fornecido, usar o PR mais recente: `gh pr list --limit 1 --json number -q '.[0].number'`

## Passo 1 — Identificar PR e Arquivos

```bash
PR_NUMBER=$ARGUMENTS

# Ver detalhes do PR
gh pr view $PR_NUMBER

# Listar arquivos modificados
gh pr diff $PR_NUMBER --name-only
```

## Passo 2 — Lancar 3 Reviewers em Paralelo

Lance EXATAMENTE 3 subagentes usando a tool Agent, TODOS EM PARALELO:

### Subagente 1: Security Reviewer
- **agent**: security-reviewer
- **prompt**: Revise o PR #[PR_NUMBER] focando em seguranca OWASP.
  1. Leia o diff com `gh pr diff [PR_NUMBER]`
  2. Leia os arquivos modificados para contexto
  3. Analise vulnerabilidades
  4. Poste seu review com `gh pr comment [PR_NUMBER] --body "..."`
  5. Retorne: aprovado/reprovado + resumo das findings

### Subagente 2: Quality Reviewer
- **agent**: quality-reviewer
- **prompt**: Revise o PR #[PR_NUMBER] focando em qualidade (SOLID, types, clean code).
  1. Leia o diff com `gh pr diff [PR_NUMBER]`
  2. Analise qualidade
  3. Poste seu review com `gh pr comment [PR_NUMBER] --body "..."`
  4. Retorne: aprovado/reprovado + resumo

### Subagente 3: Test Reviewer
- **agent**: test-reviewer
- **prompt**: Revise o PR #[PR_NUMBER] focando em testes (cobertura, edge cases).
  1. Leia o diff com `gh pr diff [PR_NUMBER]`
  2. Analise testes
  3. Poste seu review com `gh pr comment [PR_NUMBER] --body "..."`
  4. Retorne: aprovado/reprovado + resumo

## Passo 3 — Consolidar e Informar

Apos os 3 reviewers terminarem:

1. Consolide os resultados
2. Poste um comentario FINAL consolidado no PR:

```bash
gh pr comment $PR_NUMBER --body "$(cat <<'EOF'
# 📋 Review Consolidado

## 🔒 Seguranca
[resumo do security-reviewer]

## 📐 Qualidade
[resumo do quality-reviewer]

## 🧪 Testes
[resumo do test-reviewer]

## Veredicto Final
- ✅ Aprovado / ⚠️ Ressalvas / ❌ Precisa de ajustes

### Acoes Sugeridas
1. ...
2. ...
EOF
)"
```

3. Informe o Lead com o veredicto

## Notas
- Tudo roda LOCALMENTE — nao depende de GitHub Actions
- Cada reviewer posta seu proprio comentario no PR
- O Lead posta o consolidado final
- Se houver problemas CRITICOS, o Lead deve notificar o teammate para corrigir ANTES de informar o humano
```

> **NAO ha GitHub Action.** Todo o review e orquestrado localmente pelo Lead.

---

## 1.7 Habilitar Agent Teams

```bash
# Habilitar globalmente
claude config set -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1

# Verificar
claude config get -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
# Output: 1
```

---

## 1.8 settings.local.json

Arquivo `.claude/settings.local.json` com permissoes pre-aprovadas:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git checkout:*)",
      "Bash(git branch:*)",
      "Bash(git push:*)",
      "Bash(git fetch:*)",
      "Bash(git pull:*)",
      "Bash(git merge:*)",
      "Bash(gh issue:*)",
      "Bash(gh pr:*)",
      "Bash(gh project:*)",
      "Bash(gh api:*)",
      "Bash(cd backend && python -m pytest:*)",
      "Bash(cd frontend && npm:*)",
      "Bash(pip install:*)",
      "Bash(npm install:*)",
      "Bash(npx:*)",
      "Bash(python3:*)",
      "Bash(python:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(mkdir:*)"
    ]
  }
}
```

---

## 1.9 Checklist de Verificacao

- [ ] CLAUDE.md (raiz) criado com referencia ao Mistica
- [ ] backend/CLAUDE.md criado
- [ ] frontend/CLAUDE.md criado com regras Mistica
- [ ] 5 agents em .claude/agents/ (developer, frontend-developer, security-reviewer, quality-reviewer, test-reviewer)
- [ ] Reviewers com `allowed-tools: Read, Glob, Grep, Bash` (para `gh pr comment`)
- [ ] Skill review-pr em .claude/skills/review-pr/SKILL.md (modo LOCAL, sem GitHub Action)
- [ ] Agent Teams habilitado
- [ ] settings.local.json com permissoes
- [ ] `gh` CLI autenticado com permissao de escrita em PRs

---

Proximo: [02 — Backlog com Mistica](./02-backlog-mistica.md)
