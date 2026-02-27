#!/usr/bin/env bash
set -euo pipefail

# Configuration
REPO="thyagoluciano/poc-claude"
PROJECT_TITLE="TaskFlow API — Squad Híbrida"

echo "🚀 Configurando POC Squad Híbrida..."
echo "Repo: $REPO"
echo ""

# 1. Create labels
echo "📌 Criando labels..."
gh label create "ai-agent" --color "7B68EE" --description "Task assigned to AI agent" --repo "$REPO" 2>/dev/null || true
gh label create "backend" --color "3572A5" --description "Backend task (Python)" --repo "$REPO" 2>/dev/null || true
gh label create "frontend" --color "F1E05A" --description "Frontend task (Next.js)" --repo "$REPO" 2>/dev/null || true
gh label create "blocked" --color "D73A4A" --description "Blocked by dependencies" --repo "$REPO" 2>/dev/null || true
gh label create "ready" --color "0E8A16" --description "Ready for development" --repo "$REPO" 2>/dev/null || true
gh label create "in-progress" --color "FBCA04" --description "In progress by agent" --repo "$REPO" 2>/dev/null || true
gh label create "pr-open" --color "6F42C1" --description "PR created, awaiting review" --repo "$REPO" 2>/dev/null || true

# 2. Create issues for each task
echo ""
echo "📝 Criando issues..."

# Task 01 - Models
gh issue create --repo "$REPO" \
  --title "[task-01-models] Modelos Pydantic e Schemas" \
  --label "ai-agent,backend,ready" \
  --body "## Descrição
Criar os schemas Pydantic para a TaskFlow API.

## Critérios de Aceite
- Schemas Pydantic criados em src/taskflow/schemas.py
- Validações funcionando (min/max length, email, etc)
- Testes em tests/test_schemas.py passando

## Dependências
Nenhuma

## Arquivos
- src/taskflow/__init__.py
- src/taskflow/schemas.py
- tests/test_schemas.py
- pyproject.toml"

# Task 02 - Database
gh issue create --repo "$REPO" \
  --title "[task-02-database] Setup do Banco de Dados" \
  --label "ai-agent,backend,ready" \
  --body "## Descrição
Configurar SQLAlchemy com SQLite para a TaskFlow API.

## Critérios de Aceite
- SQLAlchemy configurado com SQLite
- Modelos User e Task criados
- Relacionamento User-Tasks funcionando
- Testes passando

## Dependências
Nenhuma

## Arquivos
- src/taskflow/database.py
- src/taskflow/db_models.py
- tests/test_database.py"

# Task 03 - CRUD
gh issue create --repo "$REPO" \
  --title "[task-03-crud] Camada de Repositório CRUD" \
  --label "ai-agent,backend,blocked" \
  --body "## Descrição
Criar a camada de repositório com operações CRUD para Tasks e Users.

## Critérios de Aceite
- TaskRepository com 6 métodos CRUD
- UserRepository com create, get_by_id, get_by_username, verify_password
- Senhas hasheadas com passlib
- Testes com SQLite in-memory passando

## Dependências
- task-01-models
- task-02-database

## Arquivos
- src/taskflow/repositories.py
- tests/test_repositories.py"

# Task 04 - Auth
gh issue create --repo "$REPO" \
  --title "[task-04-auth] Autenticação JWT" \
  --label "ai-agent,backend,blocked" \
  --body "## Descrição
Implementar autenticação JWT com login e proteção de rotas.

## Critérios de Aceite
- JWT token creation e validation funcionando
- Endpoint de registro criando user
- Endpoint de login retornando token
- get_current_user extraindo user do token
- Testes passando

## Dependências
- task-01-models
- task-02-database

## Arquivos
- src/taskflow/auth.py
- src/taskflow/auth_router.py
- tests/test_auth.py"

# Task 05 - API Endpoints
gh issue create --repo "$REPO" \
  --title "[task-05-api-endpoints] API Endpoints FastAPI" \
  --label "ai-agent,backend,blocked" \
  --body "## Descrição
Criar os endpoints REST da API e o app principal FastAPI.

## Critérios de Aceite
- 5 endpoints de tasks (CRUD + list) funcionando
- App FastAPI com routers incluídos
- Rotas protegidas requerem autenticação
- Documentação OpenAPI disponível em /docs

## Dependências
- task-03-crud
- task-04-auth

## Arquivos
- src/taskflow/task_router.py
- src/taskflow/app.py"

# Task 06 - Integration Tests
gh issue create --repo "$REPO" \
  --title "[task-06-integration-tests] Testes de Integração E2E" \
  --label "ai-agent,backend,blocked" \
  --body "## Descrição
Criar testes de integração completos que testam o fluxo inteiro da API.

## Critérios de Aceite
- conftest.py com fixtures reutilizáveis
- Testes cobrindo o ciclo completo da API
- Teste de autenticação (401 sem token)
- Teste de autorização (403 para non-owner)
- Todos os testes passando com pytest

## Dependências
- task-05-api-endpoints

## Arquivos
- tests/conftest.py
- tests/test_integration.py"

# Task 07 - Next.js Setup
gh issue create --repo "$REPO" \
  --title "[task-07-nextjs-setup] Next.js Setup + Layout Base" \
  --label "ai-agent,frontend,ready" \
  --body "## Descrição
Criar o projeto Next.js com layout base, Tailwind CSS e API client.

## Critérios de Aceite
- Projeto Next.js criado com App Router e TypeScript
- Tailwind CSS configurado
- Layout base com navegação
- API client em lib/api.ts
- Build passando sem erros

## Dependências
Nenhuma

## Arquivos
- src/frontend/ (projeto Next.js completo)
- src/frontend/src/lib/api.ts
- src/frontend/src/app/layout.tsx
- src/frontend/src/app/page.tsx"

# Task 08 - Auth UI
gh issue create --repo "$REPO" \
  --title "[task-08-auth-ui] Auth UI - Login/Register" \
  --label "ai-agent,frontend,blocked" \
  --body "## Descrição
Criar páginas de login e registro com context de autenticação.

## Critérios de Aceite
- Página de login com email/username e senha
- Página de registro com username, email e senha
- AuthContext com JWT token storage
- Proteção de rotas (redirect para login se não autenticado)
- Integração com API /auth/login e /auth/register
- Build passando sem erros

## Dependências
- task-04-auth
- task-07-nextjs-setup

## Arquivos
- src/frontend/src/app/login/page.tsx
- src/frontend/src/app/register/page.tsx
- src/frontend/src/lib/auth-context.tsx
- src/frontend/src/components/ProtectedRoute.tsx"

# Task 09 - Task UI
gh issue create --repo "$REPO" \
  --title "[task-09-task-ui] Task Management UI" \
  --label "ai-agent,frontend,blocked" \
  --body "## Descrição
Criar UI de gerenciamento de tasks com CRUD e filtros.

## Critérios de Aceite
- Lista de tasks com filtros por status
- Formulário de criar/editar task
- Delete com confirmação
- Status badges coloridos
- Integração com API /tasks/*
- Build passando sem erros

## Dependências
- task-05-api-endpoints
- task-07-nextjs-setup

## Arquivos
- src/frontend/src/app/tasks/page.tsx
- src/frontend/src/app/tasks/new/page.tsx
- src/frontend/src/app/tasks/[id]/page.tsx
- src/frontend/src/components/TaskCard.tsx
- src/frontend/src/components/TaskForm.tsx"

# Task 10 - Dashboard
gh issue create --repo "$REPO" \
  --title "[task-10-dashboard] Dashboard + Integração Final" \
  --label "ai-agent,frontend,blocked" \
  --body "## Descrição
Criar dashboard com stats e integração final entre frontend e backend.

## Critérios de Aceite
- Dashboard com cards de estatísticas (total tasks, por status, por prioridade)
- Overview de tasks recentes
- Navegação completa entre páginas
- Build passando sem erros
- E2E: registrar user, login, criar task, listar, editar, deletar

## Dependências
- task-08-auth-ui
- task-09-task-ui

## Arquivos
- src/frontend/src/app/dashboard/page.tsx
- src/frontend/src/components/StatsCard.tsx"

echo ""
echo "📋 Criando GitHub Project..."
gh project create --owner thyagoluciano --title "$PROJECT_TITLE" 2>/dev/null || echo "Project may already exist"

echo ""
echo "✅ Setup completo!"
echo ""
echo "Próximos passos:"
echo "1. Adicione as issues ao GitHub Project manualmente (ou via API)"
echo "2. Configure o secret ANTHROPIC_API_KEY: gh secret set ANTHROPIC_API_KEY --repo $REPO"
echo "3. Habilite Agent Teams: claude config set -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1"
echo "4. Inicie a POC com Agent Teams"
