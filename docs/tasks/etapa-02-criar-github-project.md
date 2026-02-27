# Etapa 02 — Criar GitHub Project Board

## O que faz

Cria um board no GitHub Projects para o repositorio `poc-claude`, com 10 issues representando as tasks do backlog, labels de classificacao e campos customizados. O board sera o painel de controle visual da POC — onde acompanhamos o progresso de cada task e o fluxo da squad hibrida.

## Por que

O GitHub Projects funciona como o "kanban da squad". Cada issue e uma task do backlog. As labels indicam estado (ready, in-progress, pr-open, blocked) e tipo (backend, frontend, ai-agent). Durante a demo, o board mostra visualmente como os agentes pegam tasks, criam PRs e progridem — essencial para a narrativa da apresentacao.

## Roteiro (para gravacao)

> **Cena 1 — Criando o projeto (30s)**
> "Agora vamos criar o board no GitHub Projects. Ele vai ser o nosso kanban. Cada card e uma task do backlog, com descricao completa, criterios de aceitacao e dependencias."

> **Cena 2 — Criando as issues (2min)**
> "Vou criar as 10 issues automaticamente via CLI. Cada issue tem o corpo completo com descricao tecnica, arquivos que devem ser criados, dependencias e criterios de aceitacao. Isso e importante porque os agentes vao ler essas informacoes."

> **Cena 3 — Labels e organizacao (1min)**
> "Agora crio as labels: ai-agent para tasks executadas por agentes, backend e frontend para classificacao, e estados como ready, in-progress, pr-open e blocked. Essas labels vao nos ajudar a visualizar o fluxo."

> **Cena 4 — Board final (30s)**
> "Pronto — temos o board com 10 cards organizados. As tasks da Wave 1 (sem dependencias) ja estao como 'ready'. Vamos ver como fica no GitHub."

---

## Script / Comandos

### 1. Criar Labels no Repositorio

```bash
cd ~/Developer/projetos/poc-claude

# Labels de tipo
gh label create "ai-agent" --color "7057ff" --description "Task executada por agente IA"
gh label create "backend" --color "0075ca" --description "Task de backend (Python/FastAPI)"
gh label create "frontend" --color "e4e669" --description "Task de frontend (Next.js/React)"

# Labels de estado
gh label create "ready" --color "0e8a16" --description "Task pronta para ser iniciada (deps resolvidas)"
gh label create "in-progress" --color "fbca04" --description "Task em andamento por um agente"
gh label create "pr-open" --color "1d76db" --description "PR aberto aguardando review/merge"
gh label create "blocked" --color "d93f0b" --description "Task bloqueada por dependência"

# Remover labels padrão que não usaremos (opcional)
gh label delete "bug" --yes 2>/dev/null
gh label delete "documentation" --yes 2>/dev/null
gh label delete "duplicate" --yes 2>/dev/null
gh label delete "enhancement" --yes 2>/dev/null
gh label delete "good first issue" --yes 2>/dev/null
gh label delete "help wanted" --yes 2>/dev/null
gh label delete "invalid" --yes 2>/dev/null
gh label delete "question" --yes 2>/dev/null
gh label delete "wontfix" --yes 2>/dev/null
```

### 2. Criar as 10 Issues

```bash
cd ~/Developer/projetos/poc-claude

# ============================================================
# TASK 01 — Modelos Pydantic e Schemas
# ============================================================
gh issue create \
  --title "task-01: Modelos Pydantic e Schemas" \
  --label "ai-agent,backend,ready" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Criar os schemas Pydantic para a TaskFlow API.

## O que criar

### 1. `backend/src/taskflow/schemas.py` — Schemas Pydantic
- `TaskBase(BaseModel)`: title (str, min 1, max 200), description (str | None), priority (Literal["low","medium","high"], default "medium")
- `TaskCreate(TaskBase)`: usado para criação
- `TaskUpdate(BaseModel)`: todos os campos opcionais + status (Literal["todo","in_progress","done"] | None)
- `TaskResponse(TaskBase)`: id (int), status (str), created_at (datetime), updated_at (datetime | None), owner_id (int)
- `UserBase(BaseModel)`: username (str, min 3, max 50), email (EmailStr)
- `UserCreate(UserBase)`: password (str, min 8)
- `UserResponse(UserBase)`: id (int), created_at (datetime)

### 2. `backend/src/taskflow/__init__.py` — Pacote vazio

### 3. `backend/tests/test_schemas.py` — Testes unitários
- Testar criação válida de TaskCreate e UserCreate
- Testar validações (título vazio, senha curta, email inválido)
- Testar TaskUpdate com campos parciais

## Nota
- O `backend/pyproject.toml` já foi criado no setup do repo com todas as dependências necessárias.

## Dependências
Nenhuma — pode iniciar imediatamente.

## Wave
Wave 1 (paralelo com task-02 e task-07)

## Critérios de Aceitação
- [ ] Schemas Pydantic criados em `backend/src/taskflow/schemas.py`
- [ ] Validações funcionando (min/max length, email, etc)
- [ ] Testes em `backend/tests/test_schemas.py` passando
- [ ] `backend/pyproject.toml` configurado

## Arquivos a criar
- `backend/src/taskflow/__init__.py`
- `backend/src/taskflow/schemas.py`
- `backend/tests/test_schemas.py`
ISSUE_EOF
)"

# ============================================================
# TASK 02 — Setup do Banco de Dados
# ============================================================
gh issue create \
  --title "task-02: Setup do Banco de Dados" \
  --label "ai-agent,backend,ready" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Configurar SQLAlchemy com SQLite para a TaskFlow API.

## O que criar

### 1. `backend/src/taskflow/database.py` — Configuração do banco
- Engine SQLite: `sqlite:///./taskflow.db`
- SessionLocal com autocommit=False, autoflush=False
- Base = declarative_base()
- Função `get_db()` com yield pattern (FastAPI dependency)
- Função `create_tables()` que cria todas as tabelas

### 2. `backend/src/taskflow/db_models.py` — Modelos SQLAlchemy
- `UserModel(Base)`: table "users"
  - id: Integer, primary_key, autoincrement
  - username: String(50), unique, index
  - email: String(100), unique
  - hashed_password: String(255)
  - created_at: DateTime, default=utcnow
  - tasks: relationship("TaskModel", back_populates="owner")
- `TaskModel(Base)`: table "tasks"
  - id: Integer, primary_key, autoincrement
  - title: String(200)
  - description: Text, nullable
  - priority: String(10), default="medium"
  - status: String(20), default="todo"
  - created_at: DateTime, default=utcnow
  - updated_at: DateTime, nullable, onupdate=utcnow
  - owner_id: Integer, ForeignKey("users.id")
  - owner: relationship("UserModel", back_populates="tasks")

### 3. `backend/tests/test_database.py` — Testes
- Testar criação de tabelas
- Testar inserção de User e Task
- Testar relacionamento User <-> Tasks

## Nota
- O `backend/pyproject.toml` e `backend/src/taskflow/__init__.py` já foram criados no setup do repo.

## Dependências
Nenhuma — pode iniciar imediatamente.

## Wave
Wave 1 (paralelo com task-01 e task-07)

## Critérios de Aceitação
- [ ] SQLAlchemy configurado com SQLite
- [ ] Modelos User e Task criados
- [ ] Relacionamento User-Tasks funcionando
- [ ] Testes passando

## Arquivos a criar
- `backend/src/taskflow/database.py`
- `backend/src/taskflow/db_models.py`
- `backend/tests/test_database.py`
ISSUE_EOF
)"

# ============================================================
# TASK 03 — Camada de Repositório CRUD
# ============================================================
gh issue create \
  --title "task-03: Camada de Repositório CRUD" \
  --label "ai-agent,backend,blocked" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Criar a camada de repositório com operações CRUD para Tasks e Users.

## O que criar

### 1. `backend/src/taskflow/repositories.py` — Operações CRUD

**class TaskRepository:**
- `create(db, task: TaskCreate, owner_id: int) -> TaskModel`
- `get_by_id(db, task_id: int) -> TaskModel | None`
- `list_all(db, skip=0, limit=100) -> list[TaskModel]`
- `list_by_owner(db, owner_id: int) -> list[TaskModel]`
- `update(db, task_id: int, task: TaskUpdate) -> TaskModel | None`
- `delete(db, task_id: int) -> bool`

**class UserRepository:**
- `create(db, user: UserCreate) -> UserModel` (usar passlib para hash)
- `get_by_id(db, user_id: int) -> UserModel | None`
- `get_by_username(db, username: str) -> UserModel | None`
- `verify_password(plain: str, hashed: str) -> bool`

### 2. `backend/tests/test_repositories.py` — Testes
- CRUD completo de Task (create, read, update, delete)
- Criação de User com senha hasheada
- Busca por username
- Fixture com banco SQLite in-memory

## Dependências
- **task-01** (Modelos Pydantic) — precisa dos schemas
- **task-02** (Setup do Banco) — precisa do database e db_models

## Wave
Wave 2 (após Wave 1)

## Critérios de Aceitação
- [ ] TaskRepository com 6 métodos CRUD
- [ ] UserRepository com create, get_by_id, get_by_username, verify_password
- [ ] Senhas hasheadas com passlib
- [ ] Testes com SQLite in-memory passando

## Arquivos a criar
- `backend/src/taskflow/repositories.py`
- `backend/tests/test_repositories.py`
ISSUE_EOF
)"

# ============================================================
# TASK 04 — Autenticação JWT
# ============================================================
gh issue create \
  --title "task-04: Autenticação JWT" \
  --label "ai-agent,backend,blocked" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Implementar autenticação JWT com login e proteção de rotas.

## O que criar

### 1. `backend/src/taskflow/auth.py` — Módulo de autenticação
- SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
- ALGORITHM = "HS256"
- ACCESS_TOKEN_EXPIRE_MINUTES = 30
- `create_access_token(data: dict, expires_delta: timedelta | None) -> str`
- `decode_access_token(token: str) -> dict` (raise HTTPException 401 se inválido)
- `get_current_user(token, db) -> UserModel` com OAuth2PasswordBearer

### 2. `backend/src/taskflow/auth_router.py` — Router FastAPI
- POST `/auth/register` — Cria user, retorna UserResponse
- POST `/auth/login` — OAuth2PasswordRequestForm, retorna access_token

### 3. `backend/tests/test_auth.py` — Testes
- Criação e decodificação de token
- Token expirado
- Registro de usuário via API
- Login com credenciais corretas e incorretas

## Dependências
- **task-01** (Modelos Pydantic) — precisa dos schemas
- **task-02** (Setup do Banco) — precisa do database

## Wave
Wave 2 (paralelo com task-03)

## Critérios de Aceitação
- [ ] JWT token creation e validation funcionando
- [ ] Endpoint de registro criando user
- [ ] Endpoint de login retornando token
- [ ] get_current_user extraindo user do token
- [ ] Testes passando

## Arquivos a criar
- `backend/src/taskflow/auth.py`
- `backend/src/taskflow/auth_router.py`
- `backend/tests/test_auth.py`
ISSUE_EOF
)"

# ============================================================
# TASK 05 — API Endpoints FastAPI
# ============================================================
gh issue create \
  --title "task-05: API Endpoints FastAPI" \
  --label "ai-agent,backend,blocked" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Criar os endpoints REST da API e o app principal FastAPI.

## O que criar

### 1. `backend/src/taskflow/task_router.py` — Router de Tasks
- GET `/tasks` — Lista tasks (paginação: skip, limit)
- GET `/tasks/{task_id}` — Busca por ID (404 se não existe)
- POST `/tasks` — Cria task (requer auth, owner_id = current_user.id)
- PUT `/tasks/{task_id}` — Atualiza (requer auth, só owner)
- DELETE `/tasks/{task_id}` — Deleta (requer auth, só owner)

### 2. `backend/src/taskflow/app.py` — App principal
- FastAPI com title="TaskFlow API", version="1.0.0"
- Incluir auth_router (prefix="/auth", tags=["auth"])
- Incluir task_router (prefix="/tasks", tags=["tasks"])
- Startup event: create_tables()
- GET `/` retornando info da API

## Dependências
- **task-03** (CRUD) — precisa dos repositories
- **task-04** (Auth) — precisa do auth e auth_router

## Wave
Wave 3 (após Wave 2)

## Critérios de Aceitação
- [ ] 5 endpoints de tasks (CRUD + list) funcionando
- [ ] App FastAPI com routers incluídos
- [ ] Rotas protegidas requerem autenticação
- [ ] Documentação OpenAPI em /docs

## Arquivos a criar
- `backend/src/taskflow/task_router.py`
- `backend/src/taskflow/app.py`
ISSUE_EOF
)"

# ============================================================
# TASK 06 — Testes de Integração E2E
# ============================================================
gh issue create \
  --title "task-06: Testes de Integração End-to-End" \
  --label "ai-agent,backend,blocked" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Criar testes de integração completos que testam o fluxo inteiro da API.

## O que criar

### 1. `backend/tests/conftest.py` — Fixtures compartilhadas
- Fixture `test_db`: banco SQLite in-memory com sessão
- Fixture `client`: TestClient do FastAPI com override de get_db
- Fixture `auth_headers`: registra user, faz login, retorna headers com token

### 2. `backend/tests/test_integration.py` — Testes E2E
- `test_health_check`: GET / retorna 200
- `test_full_task_lifecycle`: registro → login → criar → listar → buscar → atualizar → deletar → 404
- `test_unauthorized_access`: POST /tasks sem token = 401
- `test_create_multiple_tasks`: criar 3 tasks, verificar listagem
- `test_update_task_status`: criar task, atualizar status para "done"
- `test_only_owner_can_modify`: User A cria, User B tenta deletar = 403

## Dependências
- **task-05** (API Endpoints) — precisa da API completa

## Wave
Wave 4 (após Wave 3)

## Critérios de Aceitação
- [ ] conftest.py com fixtures reutilizáveis
- [ ] Testes cobrindo ciclo completo da API
- [ ] Teste de autenticação (401 sem token)
- [ ] Teste de autorização (403 para non-owner)
- [ ] Todos os testes passando com pytest

## Arquivos a criar
- `backend/tests/conftest.py`
- `backend/tests/test_integration.py`
ISSUE_EOF
)"

# ============================================================
# TASK 07 — Next.js Setup + Layout Base
# ============================================================
gh issue create \
  --title "task-07: Next.js Setup + Layout Base" \
  --label "ai-agent,frontend,ready" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Criar o projeto Next.js com TypeScript, Tailwind CSS, App Router, layout base e cliente API.

## O que criar

### 1. Setup do projeto
```bash
npx create-next-app@latest frontend --typescript --tailwind --app --src-dir --eslint
```

### 2. `frontend/src/lib/api.ts` — Cliente API
- Base URL configurável via env (NEXT_PUBLIC_API_URL)
- Funções: apiGet, apiPost, apiPut, apiDelete
- Interceptor para incluir JWT token do localStorage
- Tratamento de erros (401 → redirect login)

### 3. `frontend/src/app/layout.tsx` — Layout base
- Navbar com logo "TaskFlow", links (Dashboard, Tasks), botão Login/Logout
- Footer simples
- Providers wrapper (AuthContext placeholder)

### 4. `frontend/src/app/page.tsx` — Home page
- Hero section com descrição da TaskFlow API
- Botão CTA para Dashboard

## Dependências
Nenhuma — pode iniciar imediatamente.

## Wave
Wave 1 (paralelo com task-01 e task-02)

## Critérios de Aceitação
- [ ] Next.js rodando com `npm run dev`
- [ ] Layout base com navbar e footer
- [ ] Cliente API em `lib/api.ts` configurado
- [ ] TypeScript strict mode ativo
- [ ] Tailwind CSS funcionando

## Arquivos a criar
- `frontend/` (todo o projeto Next.js)
- `frontend/src/lib/api.ts`
- `frontend/src/app/layout.tsx` (customizado)
- `frontend/src/app/page.tsx` (customizado)
ISSUE_EOF
)"

# ============================================================
# TASK 08 — Auth UI - Login/Register
# ============================================================
gh issue create \
  --title "task-08: Auth UI - Login/Register" \
  --label "ai-agent,frontend,blocked" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Criar as páginas de login e registro, AuthContext com JWT e wrapper de rotas protegidas.

## O que criar

### 1. `frontend/src/lib/auth.ts` — AuthContext
- AuthContext com React Context API
- Estado: user, token, isAuthenticated, isLoading
- Funções: login(username, password), register(username, email, password), logout()
- Persistência do token no localStorage
- Auto-login ao carregar (verificar token existente)

### 2. `frontend/src/app/login/page.tsx` — Página de Login
- Formulário com username e password
- Botão de submit com loading state
- Link para registro
- Redirect para /dashboard após login
- Mensagem de erro para credenciais inválidas

### 3. `frontend/src/app/register/page.tsx` — Página de Registro
- Formulário com username, email e password
- Validação client-side (email, senha mínima)
- Redirect para login após registro
- Mensagem de erro para username duplicado

### 4. `frontend/src/components/ProtectedRoute.tsx` — Wrapper
- Verifica se usuário está autenticado
- Redirect para /login se não autenticado
- Loading state enquanto verifica

## Dependências
- **task-04** (Auth JWT) — precisa dos endpoints /auth/login e /auth/register
- **task-07** (Next.js Setup) — precisa do projeto frontend base

## Wave
Wave 3 (paralelo com task-05)

## Critérios de Aceitação
- [ ] Login funcional com JWT
- [ ] Registro funcional
- [ ] AuthContext gerenciando estado de autenticação
- [ ] ProtectedRoute redirecionando usuários não autenticados
- [ ] Integração com POST /auth/login e POST /auth/register

## Arquivos a criar
- `frontend/src/lib/auth.ts`
- `frontend/src/app/login/page.tsx`
- `frontend/src/app/register/page.tsx`
- `frontend/src/components/ProtectedRoute.tsx`
ISSUE_EOF
)"

# ============================================================
# TASK 09 — Task Management UI
# ============================================================
gh issue create \
  --title "task-09: Task Management UI" \
  --label "ai-agent,frontend,blocked" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Criar a interface de gerenciamento de tarefas: listagem com filtros, criação/edição, exclusão e badges de status.

## O que criar

### 1. `frontend/src/app/tasks/page.tsx` — Lista de Tasks
- Listagem de tasks em cards ou tabela
- Filtros por status (todo, in_progress, done) e prioridade (low, medium, high)
- Botão "Nova Task"
- Loading state e empty state

### 2. `frontend/src/app/tasks/new/page.tsx` — Criar Task
- Formulário com title, description, priority (select)
- Validação client-side
- Redirect para /tasks após criação

### 3. `frontend/src/app/tasks/[id]/edit/page.tsx` — Editar Task
- Formulário preenchido com dados da task
- Campos: title, description, priority, status
- Botão salvar e cancelar

### 4. `frontend/src/components/TaskCard.tsx` — Card de Task
- Exibir title, description (truncada), priority badge, status badge
- Botões: Edit, Delete
- Delete com confirmação (modal ou confirm)

### 5. `frontend/src/components/StatusBadge.tsx` — Badge de Status
- Cores: todo (gray), in_progress (yellow), done (green)
- Priority: low (blue), medium (orange), high (red)

## Dependências
- **task-05** (API Endpoints) — precisa dos endpoints GET/POST/PUT/DELETE /tasks
- **task-07** (Next.js Setup) — precisa do projeto frontend base

## Wave
Wave 4 (paralelo com task-06)

## Critérios de Aceitação
- [ ] Lista de tasks com filtros
- [ ] Criação de task funcional
- [ ] Edição de task funcional
- [ ] Exclusão com confirmação
- [ ] Status badges com cores
- [ ] Integração com API de tasks

## Arquivos a criar
- `frontend/src/app/tasks/page.tsx`
- `frontend/src/app/tasks/new/page.tsx`
- `frontend/src/app/tasks/[id]/edit/page.tsx`
- `frontend/src/components/TaskCard.tsx`
- `frontend/src/components/StatusBadge.tsx`
ISSUE_EOF
)"

# ============================================================
# TASK 10 — Dashboard + Integração Final
# ============================================================
gh issue create \
  --title "task-10: Dashboard + Integração Final" \
  --label "ai-agent,frontend,blocked" \
  --body "$(cat <<'ISSUE_EOF'
## Descrição

Criar o dashboard com estatísticas, overview de tasks e verificação final de integração.

## O que criar

### 1. `frontend/src/app/dashboard/page.tsx` — Dashboard
- Stats cards: total de tasks, tasks por status (todo/in_progress/done), tasks por prioridade
- Overview: lista das últimas 5 tasks
- Botão rápido "Nova Task"
- Gráfico simples (barras CSS) de tasks por status

### 2. Integração final
- Verificar que todas as páginas funcionam com a API
- Auth flow: login → dashboard → tasks → CRUD → logout
- Verificar responsividade básica

### 3. Checklist de teste E2E manual
- [ ] Registro de novo usuário
- [ ] Login com credenciais
- [ ] Dashboard mostra estatísticas
- [ ] Criar nova task
- [ ] Editar task existente
- [ ] Alterar status da task
- [ ] Deletar task com confirmação
- [ ] Logout e redirect para login
- [ ] Acesso protegido (redirect sem token)

## Dependências
- **task-08** (Auth UI) — precisa do AuthContext e páginas de auth
- **task-09** (Task Management UI) — precisa da UI de tasks

## Wave
Wave 5 (final)

## Critérios de Aceitação
- [ ] Dashboard com stats cards funcionando
- [ ] Todas as páginas conectadas à API
- [ ] Auth flow completo funcionando
- [ ] E2E manual checklist passando

## Arquivos a criar
- `frontend/src/app/dashboard/page.tsx`
ISSUE_EOF
)"
```

### 3. Criar o GitHub Project

```bash
# Criar o project board
gh project create "TaskFlow - POC Hybrid Squad" \
  --owner thyagoluciano \
  --body "Board de acompanhamento da POC de Squad Híbrida com Claude Code Agent Teams"

# Anotar o número do projeto retornado (ex: 1)
# Substitua PROJECT_NUMBER pelo número retornado
PROJECT_NUMBER=1
```

### 4. Adicionar Issues ao Project

```bash
# Listar as issues para confirmar
gh issue list --repo thyagoluciano/poc-claude

# Adicionar cada issue ao project
for i in $(seq 1 10); do
  gh project item-add $PROJECT_NUMBER \
    --owner thyagoluciano \
    --url "https://github.com/thyagoluciano/poc-claude/issues/$i"
done
```

### 5. Configurar Campos do Project (opcional)

```bash
# Listar campos do projeto
gh project field-list $PROJECT_NUMBER --owner thyagoluciano

# Adicionar campo "Wave" como single select
gh project field-create $PROJECT_NUMBER \
  --owner thyagoluciano \
  --name "Wave" \
  --data-type "SINGLE_SELECT"

# Adicionar campo "Agent" como text
gh project field-create $PROJECT_NUMBER \
  --owner thyagoluciano \
  --name "Agent" \
  --data-type "TEXT"
```

### 6. Verificacao

```bash
# Verificar issues criadas
gh issue list --repo thyagoluciano/poc-claude --limit 15

# Verificar labels
gh label list --repo thyagoluciano/poc-claude

# Abrir o project no browser
gh project view $PROJECT_NUMBER --owner thyagoluciano --web
```

---

## Mapa de Waves e Dependencias

```
Wave 1 (paralelo):
  ├── task-01: Modelos Pydantic       [ready] — sem deps
  ├── task-02: Setup Banco de Dados    [ready] — sem deps
  └── task-07: Next.js Setup           [ready] — sem deps

Wave 2 (após Wave 1):
  ├── task-03: CRUD Repository         [blocked] — deps: 01, 02
  └── task-04: Auth JWT                [blocked] — deps: 01, 02

Wave 3 (após Wave 2):
  ├── task-05: API Endpoints           [blocked] — deps: 03, 04
  └── task-08: Auth UI                 [blocked] — deps: 04, 07

Wave 4 (após Wave 3):
  ├── task-06: Testes E2E Backend      [blocked] — deps: 05
  └── task-09: Task Management UI      [blocked] — deps: 05, 07

Wave 5 (final):
  └── task-10: Dashboard + Integração  [blocked] — deps: 08, 09
```

---

## Checklist de Verificacao

- [ ] 7 labels criadas (ai-agent, backend, frontend, ready, in-progress, pr-open, blocked)
- [ ] 10 issues criadas com body completo
- [ ] Issues 01, 02, 07 com label "ready"
- [ ] Issues 03, 04, 05, 06, 08, 09, 10 com label "blocked"
- [ ] Project board criado no GitHub Projects
- [ ] Todas as issues adicionadas ao project

---

## Proximo Passo

Siga para **Etapa 03** — Configurar GitHub Action para review com `@claude`.
