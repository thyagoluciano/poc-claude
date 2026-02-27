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
O backlog está nas Issues do repositório GitHub. Use `gh issue list` para ver as tasks e `gh issue view <número>` para ler os detalhes. Respeite as dependências entre tasks (descritas no corpo de cada issue).
