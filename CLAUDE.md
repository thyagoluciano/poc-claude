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
