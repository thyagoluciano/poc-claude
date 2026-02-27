# Etapa 01 — Setup do Repositorio `poc-claude`

## O que faz

Prepara o repositorio `thyagoluciano/poc-claude` do zero com toda a estrutura de diretorios, arquivos de configuracao do Claude Code (CLAUDE.md, agents, skills, workflow) e o backlog de produto. Ao final, o repo estara pronto para receber os agentes da squad hibrida.

## Por que

Sem essa base, os agentes nao sabem como se comportar, quais regras seguir, nem qual backlog executar. O `CLAUDE.md` e o "cerebro" do projeto — ele dita convencoes, stack e fluxo de trabalho. Os agents e skills definem os papeis da squad. O workflow habilita review automatico via `@claude` nos PRs.

## Roteiro (para gravacao)

> **Cena 1 — Intro (30s)**
> "Vamos comecar pelo setup do repositorio. Esse repo vai ser o workspace da nossa squad hibrida. Vou criar toda a estrutura que o Claude Code precisa para operar: o CLAUDE.md com as regras do projeto, os agentes especializados, a skill de review e o backlog de produto."

> **Cena 2 — Clone e estrutura (1min)**
> "Primeiro, clono o repo — ou reseto se ja existir. Depois crio a arvore de diretorios. Reparem na pasta `.claude/` — ela e especial pro Claude Code. Dentro dela ficam os agents e skills."

> **Cena 3 — Arquivos de configuracao (2min)**
> "Agora copio os arquivos pre-configurados. O CLAUDE.md na raiz define regras globais. Os agents definem personas com diferentes especializacoes. A skill review-pr orquestra reviews paralelos. E o workflow do GitHub Actions conecta tudo ao fluxo de PR."

> **Cena 4 — Push e verificacao (30s)**
> "Commit inicial, push, e o repo esta pronto. Vamos verificar no GitHub se tudo subiu corretamente."

---

## Estrutura de Diretorios Esperada

```
poc-claude/
├── CLAUDE.md                          # Regras globais do Claude Code
├── product_backlog.yaml               # Backlog com 10 tasks e dependencias
├── .claude/
│   ├── agents/
│   │   ├── developer.md               # Agente dev backend
│   │   ├── frontend-developer.md      # Agente dev frontend
│   │   ├── security-reviewer.md       # Agente reviewer seguranca (read-only)
│   │   ├── quality-reviewer.md        # Agente reviewer qualidade (read-only)
│   │   └── test-reviewer.md           # Agente reviewer testes (read-only)
│   └── skills/
│       └── review-pr/
│           └── SKILL.md               # Skill de review paralelo
├── .github/
│   └── workflows/
│       └── claude-review.yml          # GitHub Action para @claude review
├── backend/                           # Backend Python/FastAPI
│   ├── CLAUDE.md                      # Regras especificas do backend
│   ├── pyproject.toml                 # Dependencias Python (criado no setup)
│   ├── src/
│   │   └── taskflow/                  # (sera populado pelos agentes)
│   │       └── __init__.py
│   └── tests/                         # (sera populado pelos agentes)
│       └── __init__.py
└── frontend/                          # Frontend Next.js/React
    └── CLAUDE.md                      # Regras especificas do frontend
```

---

## Script / Comandos

### 1. Clone ou reset do repositorio

```bash
# Se o repo ja existe localmente, remova e clone novamente
cd ~/Developer/projetos
rm -rf poc-claude
git clone https://github.com/thyagoluciano/poc-claude.git
cd poc-claude

# Se o repo esta vazio no GitHub, crie-o primeiro:
# gh repo create thyagoluciano/poc-claude --public --clone
```

### 2. Limpar o repo (se necessario)

```bash
# Se o repo tem conteudo anterior e voce quer resetar:
cd ~/Developer/projetos/poc-claude
git checkout main
rm -rf *
rm -rf .claude .github
git add -A
git commit -m "chore: reset repo for POC Hybrid Squad"
git push origin main
```

### 3. Criar a estrutura de diretorios

```bash
cd ~/Developer/projetos/poc-claude

# Diretorios do Claude Code
mkdir -p .claude/agents
mkdir -p .claude/skills/review-pr

# Diretorio do GitHub Actions
mkdir -p .github/workflows

# Diretorios do backend
mkdir -p backend/src/taskflow
mkdir -p backend/tests

# Diretorio do frontend (placeholder — sera criado pelo agent na task-07)
mkdir -p frontend

# Criar __init__.py vazios
touch backend/src/taskflow/__init__.py
touch backend/tests/__init__.py
```

### 4. Copiar arquivos de configuracao

> **Nota:** Os arquivos fonte estao em `~/Developer/projetos/zup/ppt/docs/poc-config/`.
> Se voce preferir, pode criar cada arquivo manualmente com os conteudos das etapas 04, 05, 03 e 07.

```bash
cd ~/Developer/projetos/poc-claude

# CLAUDE.md — criar na raiz (regras globais)
cat > CLAUDE.md << 'CLAUDE_EOF'
# CLAUDE.md — TaskFlow API

## Projeto
TaskFlow API: REST API de gerenciamento de tarefas com frontend.

## Stack
- **Backend:** Python 3.12+, FastAPI, SQLAlchemy, Pydantic v2, pytest
- **Frontend:** Next.js 14+, TypeScript, Tailwind CSS, App Router
- **Banco:** SQLite (dev), PostgreSQL (prod)
- **Auth:** JWT com python-jose, passlib[bcrypt]

## Estrutura do Projeto
```
backend/               # Backend Python/FastAPI
  src/taskflow/        # Código-fonte
  tests/               # Testes pytest
  pyproject.toml       # Dependências Python
  CLAUDE.md            # Regras específicas do backend
frontend/              # Frontend Next.js/React
  src/app/             # App Router pages
  src/components/      # React components
  src/lib/             # Utilities (api.ts, auth.ts)
  CLAUDE.md            # Regras específicas do frontend
```

## Convenções Globais
- Commits: Conventional Commits (feat:, fix:, test:, docs:, chore:)
- Um PR por task — branch: feat/task-{id}
- SEMPRE leia os arquivos existentes antes de criar novos
- Nunca commite secrets ou .env files
- Consulte o CLAUDE.md da pasta da aplicação (backend/ ou frontend/) para regras específicas

## Backlog
O backlog está em `product_backlog.yaml`. Respeite as dependências entre tasks.
CLAUDE_EOF

# backend/CLAUDE.md — regras especificas do backend
cat > backend/CLAUDE.md << 'BACKEND_CLAUDE_EOF'
# Backend Rules — TaskFlow API

## Stack
- Python 3.12+, FastAPI, SQLAlchemy 2.0, Pydantic v2, pytest
- Auth: JWT com python-jose, passlib[bcrypt]
- Banco: SQLite (dev)

## Convenções
- PEP 8, type hints obrigatórios em todas as funções
- Docstrings em funções públicas
- Imports relativos dentro de src/taskflow/
- Repository pattern para acesso a dados
- Dependency injection via FastAPI Depends

## Testes
- pytest com fixtures em conftest.py
- SQLite in-memory para testes
- Nomenclatura: test_should_*
- Mínimo 80% coverage
- Rodar `cd backend && pytest` antes de cada commit

## Estrutura
```
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
  pyproject.toml       # Dependências
```
BACKEND_CLAUDE_EOF

# frontend/CLAUDE.md — regras especificas do frontend
cat > frontend/CLAUDE.md << 'FRONTEND_CLAUDE_EOF'
# Frontend Rules — TaskFlow UI

## Stack
- Next.js 14+, TypeScript strict, Tailwind CSS, App Router
- Estado: React Context API
- HTTP: Fetch API com wrapper em lib/api.ts

## Convenções
- TypeScript strict mode — nunca usar `any`
- Componentes funcionais com interfaces explícitas
- `'use client'` apenas quando necessário (interatividade)
- Tailwind puro — sem libs de UI externas (shadcn, MUI, etc)
- Cliente API centralizado em lib/api.ts
- Tratar loading states, error states e empty states

## Estrutura
```
frontend/
  src/
    app/
      layout.tsx          # Layout base com navbar
      page.tsx            # Home page
      login/page.tsx      # Login
      register/page.tsx   # Registro
      dashboard/page.tsx  # Dashboard com stats
      tasks/
        page.tsx          # Lista de tasks
        new/page.tsx      # Criar task
        [id]/edit/page.tsx # Editar task
    components/
      ProtectedRoute.tsx  # Wrapper de auth
      TaskCard.tsx        # Card de task
      StatusBadge.tsx     # Badge de status/prioridade
    lib/
      api.ts              # Cliente HTTP para a API
      auth.ts             # AuthContext e helpers
```
FRONTEND_CLAUDE_EOF

# backend/pyproject.toml — criar no setup para evitar conflito na Wave 1
cat > backend/pyproject.toml << 'PYPROJECT_EOF'
[project]
name = "taskflow-api"
version = "0.1.0"
description = "TaskFlow API — REST API de gerenciamento de tarefas"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "pydantic[email]",
    "sqlalchemy",
    "python-jose[cryptography]",
    "passlib[bcrypt]",
    "uvicorn",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "httpx",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
PYPROJECT_EOF

# product_backlog.yaml — copiar o backlog
# (sera criado/atualizado na etapa-07 com todas as 10 tasks)
# Por enquanto, copiar o backlog base com as 6 tasks backend:
cp ~/Developer/projetos/zup/ppt/src/poc_hybrid_squad/product_backlog.yaml ./product_backlog.yaml

# Agents — serao criados na etapa-04
# Skills — serao criados na etapa-05
# Workflow — sera criado na etapa-03
```

### 5. Commit inicial e push

```bash
cd ~/Developer/projetos/poc-claude

git add -A
git commit -m "chore: setup inicial do repositório para POC Hybrid Squad

- CLAUDE.md global + backend/CLAUDE.md + frontend/CLAUDE.md
- Estrutura de diretórios (.claude/, .github/, backend/, frontend/)
- backend/pyproject.toml com dependências Python
- product_backlog.yaml com backlog de produto"

git push origin main
```

### 6. Verificacao

```bash
# Verificar no GitHub
gh repo view thyagoluciano/poc-claude --web

# Verificar estrutura local
tree -a -I '.git|__pycache__|.venv' .
```

---

## Checklist de Verificacao

- [ ] Repo `poc-claude` existe no GitHub
- [ ] `CLAUDE.md` esta na raiz do repo
- [ ] `product_backlog.yaml` esta na raiz do repo
- [ ] Diretorio `.claude/agents/` existe
- [ ] Diretorio `.claude/skills/review-pr/` existe
- [ ] Diretorio `.github/workflows/` existe
- [ ] Diretorios `backend/src/taskflow/` e `backend/tests/` existem com `__init__.py`
- [ ] `backend/pyproject.toml` existe com dependencias
- [ ] `backend/CLAUDE.md` existe com regras Python
- [ ] `frontend/CLAUDE.md` existe com regras Next.js
- [ ] Commit inicial feito e push realizado
- [ ] Repo visivel no GitHub com todos os arquivos

---

## Proximo Passo

Siga para **Etapa 02** — Criar o GitHub Project Board com as 10 issues.
