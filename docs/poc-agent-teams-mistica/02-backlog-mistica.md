# 02 — Backlog com Mistica Design System

Novo backlog com 12 tasks organizadas em 5 waves. O frontend usa exclusivamente
componentes do Mistica Design System. A **task-11** introduz intencionalmente uma
**falha de seguranca** para demonstrar o fluxo de deteccao e correcao.

---

## Mapa de Waves e Dependencias

```
Wave 1 (paralelo, sem deps)
├── task-01: Modelos Pydantic e Schemas          [backend]
├── task-02: Setup do Banco de Dados              [backend]
└── task-03: Next.js Setup + Mistica Provider     [frontend]

Wave 2 (depende de Wave 1)
├── task-04: Camada de Repositorio CRUD           [backend]  ← deps: 01, 02
└── task-05: Autenticacao JWT                     [backend]  ← deps: 01, 02

Wave 3 (depende de Wave 2)
├── task-06: API Endpoints FastAPI                [backend]  ← deps: 04, 05
├── task-07: Auth UI com Mistica                  [frontend] ← deps: 03, 05
└── task-08: Testes de Integracao E2E             [backend]  ← deps: 06

Wave 4 (depende de Wave 3)
├── task-09: Task Management UI com Mistica       [frontend] ← deps: 03, 06
├── task-10: Dashboard com Mistica                [frontend] ← deps: 07, 09
└── task-11: Endpoint de busca publica [VULN]     [backend]  ← deps: 06

Wave 5 (depende de Wave 4)
└── task-12: Feedback e Notificacoes com Mistica  [frontend] ← deps: 09, 10
```

---

## Tasks Detalhadas

### task-01: Modelos Pydantic e Schemas

**Labels:** `backend`, `ready`, `wave-1`
**Agent:** developer

```markdown
## Descricao
Criar os schemas Pydantic para a TaskFlow API.

## O que criar

### 1. `backend/src/taskflow/schemas.py`
- TaskBase(BaseModel): title (str, min 1, max 200), description (str | None), priority (Literal["low","medium","high"], default "medium")
- TaskCreate(TaskBase): usado para criacao
- TaskUpdate(BaseModel): todos os campos opcionais + status (Literal["todo","in_progress","done"] | None)
- TaskResponse(TaskBase): id (int), status (str), created_at (datetime), updated_at (datetime | None), owner_id (int)
- UserBase(BaseModel): username (str, min 3, max 50), email (EmailStr)
- UserCreate(UserBase): password (str, min 8)
- UserResponse(UserBase): id (int), created_at (datetime)

### 2. `backend/src/taskflow/__init__.py` — Pacote vazio

### 3. `backend/tests/test_schemas.py`
- Testar criacao valida de TaskCreate e UserCreate
- Testar validacoes (titulo vazio, senha curta, email invalido)
- Testar TaskUpdate com campos parciais

## Dependencias
Nenhuma

## Criterios de Aceitacao
- [ ] Schemas Pydantic criados
- [ ] Validacoes funcionando
- [ ] Testes passando
```

---

### task-02: Setup do Banco de Dados

**Labels:** `backend`, `ready`, `wave-1`
**Agent:** developer

```markdown
## Descricao
Configurar SQLAlchemy com SQLite.

## O que criar

### 1. `backend/src/taskflow/database.py`
- Engine SQLite: sqlite:///./taskflow.db
- SessionLocal com autocommit=False, autoflush=False
- Base = declarative_base()
- get_db() com yield pattern
- create_tables()

### 2. `backend/src/taskflow/db_models.py`
- UserModel: id, username (unique, index), email (unique), hashed_password, created_at, tasks relationship
- TaskModel: id, title, description, priority, status, created_at, updated_at, owner_id (FK), owner relationship

### 3. `backend/tests/test_database.py`
- Testar criacao de tabelas
- Testar insercao de User e Task
- Testar relacionamento User <-> Tasks

## Dependencias
Nenhuma

## Criterios de Aceitacao
- [ ] SQLAlchemy configurado
- [ ] Modelos User e Task criados
- [ ] Relacionamentos funcionando
- [ ] Testes passando
```

---

### task-03: Next.js Setup + Mistica ThemeProvider

**Labels:** `frontend`, `ready`, `wave-1`
**Agent:** frontend-developer

```markdown
## Descricao
Criar o projeto Next.js com Mistica Design System configurado.

## O que criar

### 1. Setup do projeto Next.js
- Next.js 14+ com App Router
- TypeScript strict mode
- Instalar @telefonica/mistica

### 2. `frontend/src/app/layout.tsx` — Root Layout
```tsx
import {ThemeContextProvider, getMovistarSkin} from '@telefonica/mistica';
import {MainNavigationBar} from '@telefonica/mistica';

const misticaTheme = {
  skin: getMovistarSkin(),
  i18n: {locale: 'pt-BR', phoneNumberFormattingRegionCode: 'BR'},
};
```
- ThemeContextProvider envolvendo toda a app
- MainNavigationBar com logo "TaskFlow" e links (Dashboard, Tasks)
- Sections: topFixed (navbar), content (children)

### 3. `frontend/src/app/page.tsx` — Home
- Hero section usando Stack, Title1, Text2
- ButtonPrimary: "Ir ao Dashboard"
- ButtonSecondary: "Criar conta"
- ResponsiveLayout para container

### 4. `frontend/src/lib/api.ts` — API Client
- Base URL via NEXT_PUBLIC_API_URL (default: http://localhost:8000)
- Funcoes tipadas: apiGet, apiPost, apiPut, apiDelete
- getAuthHeaders() com Bearer token do localStorage
- Interceptor de 401 → redirect /login

### 5. `frontend/next.config.ts`
```ts
const nextConfig = {
  experimental: {
    optimizePackageImports: ['@telefonica/mistica'],
  },
};
```

## Dependencias
Nenhuma

## Criterios de Aceitacao
- [ ] Next.js rodando com Mistica
- [ ] ThemeContextProvider no root layout
- [ ] MainNavigationBar funcionando
- [ ] Home page com componentes Mistica
- [ ] API client tipado
- [ ] `npm run build` sem erros
```

---

### task-04: Camada de Repositorio CRUD

**Labels:** `backend`, `blocked`, `wave-2`
**Agent:** developer

```markdown
## Descricao
Criar repositorios CRUD para Tasks e Users.

## O que criar

### 1. `backend/src/taskflow/repositories.py`
**TaskRepository:**
- create(db, task, owner_id) -> TaskModel
- get_by_id(db, task_id) -> TaskModel | None
- list_all(db, skip=0, limit=100) -> list[TaskModel]
- list_by_owner(db, owner_id) -> list[TaskModel]
- update(db, task_id, task) -> TaskModel | None
- delete(db, task_id) -> bool

**UserRepository:**
- create(db, user) -> UserModel (hash com passlib)
- get_by_id(db, user_id) -> UserModel | None
- get_by_username(db, username) -> UserModel | None
- verify_password(plain, hashed) -> bool

### 2. `backend/tests/test_repositories.py`
- CRUD completo de Task
- Criacao de User com senha hasheada
- Busca por username

## Dependencias
- task-01 (schemas)
- task-02 (database e db_models)

## Criterios de Aceitacao
- [ ] TaskRepository com 6 metodos
- [ ] UserRepository com 4 metodos
- [ ] Senhas hasheadas
- [ ] Testes passando
```

---

### task-05: Autenticacao JWT

**Labels:** `backend`, `blocked`, `wave-2`
**Agent:** developer

```markdown
## Descricao
Implementar autenticacao JWT.

## O que criar

### 1. `backend/src/taskflow/auth.py`
- SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
- ALGORITHM = "HS256", ACCESS_TOKEN_EXPIRE_MINUTES = 30
- create_access_token(data, expires_delta) -> str
- decode_access_token(token) -> dict (HTTPException 401 se invalido)
- get_current_user(token, db) -> UserModel via OAuth2PasswordBearer

### 2. `backend/src/taskflow/auth_router.py`
- POST /auth/register → UserResponse
- POST /auth/login → {access_token, token_type}

### 3. `backend/tests/test_auth.py`
- Token create/decode
- Token expirado
- Registro e login via API

## Dependencias
- task-01, task-02

## Criterios de Aceitacao
- [ ] JWT funcionando
- [ ] Registro e login
- [ ] get_current_user extraindo user do token
- [ ] Testes passando
```

---

### task-06: API Endpoints FastAPI

**Labels:** `backend`, `blocked`, `wave-3`
**Agent:** developer

```markdown
## Descricao
Criar endpoints REST e app principal.

## O que criar

### 1. `backend/src/taskflow/task_router.py`
- GET /tasks — lista paginada
- GET /tasks/{task_id} — busca por ID (404)
- POST /tasks — cria (auth, owner_id = current_user)
- PUT /tasks/{task_id} — atualiza (owner only, 403)
- DELETE /tasks/{task_id} — deleta (owner only, 403)

### 2. `backend/src/taskflow/app.py`
- FastAPI app com title, version
- Include auth_router e task_router
- CORS para localhost:3000
- Startup: create_tables()
- GET / com info da API

## Dependencias
- task-04 (repositories)
- task-05 (auth)

## Criterios de Aceitacao
- [ ] 5 endpoints de tasks
- [ ] CORS configurado
- [ ] Rotas protegidas
- [ ] /docs com OpenAPI
```

---

### task-07: Auth UI com Mistica

**Labels:** `frontend`, `blocked`, `wave-3`
**Agent:** frontend-developer

```markdown
## Descricao
Criar UI de autenticacao usando componentes Mistica.

## O que criar

### 1. `frontend/src/lib/auth.tsx` — AuthContext
- Context com user, token, isAuthenticated, isLoading
- login(username, password), register(username, email, password), logout()
- Token em localStorage, auto-load no mount

### 2. `frontend/src/app/login/page.tsx`
- Usar Mistica: ResponsiveLayout, Stack, Title1, Form, TextField, PasswordField, ButtonPrimary, ButtonLink
- Formulario com username e password
- Loading state com Spinner
- Redirect para /dashboard apos login

### 3. `frontend/src/app/register/page.tsx`
- Usar Mistica: ResponsiveLayout, Stack, Title1, Form, TextField, EmailField, PasswordField, ButtonPrimary
- Formulario com username, email, password
- Validacao client-side
- Redirect para /login apos registro

### 4. `frontend/src/components/ProtectedRoute.tsx`
- Verifica isAuthenticated
- Loading com Spinner
- Redirect /login se nao autenticado

## Dependencias
- task-03 (Next.js + Mistica setup)
- task-05 (Auth JWT endpoints)

## Criterios de Aceitacao
- [ ] Login com componentes Mistica
- [ ] Registro com componentes Mistica
- [ ] AuthContext gerenciando JWT
- [ ] ProtectedRoute funcionando
- [ ] Build passando
```

---

### task-08: Testes de Integracao E2E

**Labels:** `backend`, `blocked`, `wave-3`
**Agent:** developer

```markdown
## Descricao
Testes de integracao end-to-end para a API.

## O que criar

### 1. `backend/tests/conftest.py`
- Fixture test_db: SQLite in-memory
- Fixture client: TestClient com override
- Fixture auth_headers: registra + login + headers
- Fixture other_auth_headers: segundo user

### 2. `backend/tests/test_integration.py`
- test_health_check: GET / retorna 200
- test_full_task_lifecycle: create → list → get → update → delete → 404
- test_unauthorized_access: 401 sem token
- test_only_owner_can_modify: 403 para non-owner

## Dependencias
- task-06 (API completa)

## Criterios de Aceitacao
- [ ] Fixtures reutilizaveis
- [ ] Ciclo completo testado
- [ ] Auth 401 e authz 403 testados
- [ ] Todos os testes passando
```

---

### task-09: Task Management UI com Mistica

**Labels:** `frontend`, `blocked`, `wave-4`
**Agent:** frontend-developer

```markdown
## Descricao
UI de gerenciamento de tasks com componentes Mistica.

## O que criar

### 1. `frontend/src/app/tasks/page.tsx` — Lista
- RowList com Row para cada task
- Filtros usando Tabs (All, Todo, In Progress, Done)
- Select para filtro de prioridade
- ButtonPrimary "Nova Task" linkando para /tasks/new
- EmptyState quando nao ha tasks
- Spinner durante loading

### 2. `frontend/src/app/tasks/new/page.tsx` — Criar
- Form com TextField (title), TextArea/TextField (description), Select (priority)
- ButtonPrimary "Criar" + ButtonSecondary "Cancelar"
- Redirect para /tasks

### 3. `frontend/src/app/tasks/[id]/edit/page.tsx` — Editar
- Form preenchido com dados da task
- Campos: title, description, priority, status
- ButtonDanger "Excluir" com confirmacao (useDialog)
- Redirect para /tasks

### 4. `frontend/src/components/TaskCard.tsx`
- DataCard do Mistica com title, subtitle (description truncada)
- Tag para status (cores: todo=gray, in_progress=blue, done=green)
- Tag para priority (cores: low=blue, medium=orange, high=red)
- Link para /tasks/{id}/edit

### 5. `frontend/src/components/StatusBadge.tsx`
- Wrapper sobre Tag do Mistica
- Props: type ("status" | "priority"), value
- Mapeamento de cores

## Dependencias
- task-03 (Next.js + Mistica)
- task-06 (API endpoints)

## Criterios de Aceitacao
- [ ] Lista com filtros via Tabs
- [ ] Criar/editar task com Mistica Form
- [ ] Delete com confirmacao
- [ ] Tags coloridas para status/prioridade
- [ ] Build passando
```

---

### task-10: Dashboard com Mistica

**Labels:** `frontend`, `blocked`, `wave-4`
**Agent:** frontend-developer

```markdown
## Descricao
Dashboard com estatisticas usando componentes Mistica.

## O que criar

### 1. `frontend/src/app/dashboard/page.tsx`
- ProtectedRoute wrapper
- Stats usando DataCard: Total, Todo, In Progress, Done
- ProgressBar mostrando % concluido
- RowList com ultimas 5 tasks
- Callout com dica do dia
- ButtonPrimary "Nova Task"

### 2. Integracao
- Fetch /tasks/ no mount
- Calcular stats a partir dos dados
- Loading com Spinner
- Erro com ErrorFeedbackScreen

## Dependencias
- task-07 (Auth UI)
- task-09 (Task Management UI)

## Criterios de Aceitacao
- [ ] Dashboard com stats em DataCards
- [ ] ProgressBar de conclusao
- [ ] Tasks recentes
- [ ] Build passando
```

---

### task-11: Endpoint de busca publica de tasks [VULNERABILIDADE INTENCIONAL]

**Labels:** `backend`, `blocked`, `wave-4`, `security-test`
**Agent:** developer

```markdown
## Descricao
Criar endpoint de busca publica de tasks por titulo.

IMPORTANTE: Este endpoint deve permitir busca por titulo SEM autenticacao,
para facilitar a integracao com outros servicos.

## O que criar

### 1. `backend/src/taskflow/search_router.py`
- GET /search/tasks?q={query} — Busca tasks por titulo
- SEM autenticacao (publico)
- Retornar: id, title, description, status, priority, owner_id, owner username e email

### 2. Registrar no app.py
- Include search_router com prefix="/search"

### 3. `backend/tests/test_search.py`
- test_search_tasks_by_title: busca por titulo
- test_search_empty_query: query vazia retorna vazio

## Dependencias
- task-06 (API)

## Criterios de Aceitacao
- [ ] Endpoint /search/tasks funcional
- [ ] Busca por titulo implementada
- [ ] Testes passando
```

> **NOTA PARA A POC:** Esta task introduz INTENCIONALMENTE duas vulnerabilidades:
> 1. **Sensitive Data Exposure (OWASP A3):** O endpoint retorna email e dados do owner sem autenticacao
> 2. **Broken Access Control (OWASP A1):** Qualquer pessoa pode ver todas as tasks de todos os usuarios
>
> O security-reviewer DEVE detectar isso durante o review do PR.
> O fluxo de correcao esta documentado em [06-cenario-seguranca.md](./06-cenario-seguranca.md).

---

### task-12: Feedback e Notificacoes com Mistica

**Labels:** `frontend`, `blocked`, `wave-5`
**Agent:** frontend-developer

```markdown
## Descricao
Adicionar feedback visual com Snackbar e FeedbackScreen do Mistica.

## O que criar

### 1. Snackbar para acoes
- Apos criar task: Snackbar "Task criada com sucesso"
- Apos editar task: Snackbar "Task atualizada"
- Apos deletar task: Snackbar "Task excluida"
- Erro de API: Snackbar de erro

### 2. FeedbackScreen para estados
- SuccessFeedbackScreen apos registro
- ErrorFeedbackScreen para erros de API
- EmptyState para listas vazias

### 3. Loading states
- Spinner durante carregamento
- Skeleton para cards (SkeletonRectangle)

## Dependencias
- task-09 (Task UI)
- task-10 (Dashboard)

## Criterios de Aceitacao
- [ ] Snackbar em todas as acoes CRUD
- [ ] FeedbackScreens para sucesso/erro
- [ ] Loading com Spinner/Skeleton
- [ ] Build passando
```

---

## Resumo de Tasks por Tipo

| Wave | Task | Tipo | Agent | Deps |
|------|------|------|-------|------|
| 1 | 01 - Schemas Pydantic | backend | developer | - |
| 1 | 02 - Setup Database | backend | developer | - |
| 1 | 03 - Next.js + Mistica | frontend | frontend-developer | - |
| 2 | 04 - CRUD Repository | backend | developer | 01, 02 |
| 2 | 05 - Auth JWT | backend | developer | 01, 02 |
| 3 | 06 - API Endpoints | backend | developer | 04, 05 |
| 3 | 07 - Auth UI Mistica | frontend | frontend-developer | 03, 05 |
| 3 | 08 - Testes E2E | backend | developer | 06 |
| 4 | 09 - Task UI Mistica | frontend | frontend-developer | 03, 06 |
| 4 | 10 - Dashboard Mistica | frontend | frontend-developer | 07, 09 |
| 4 | 11 - Search [VULN] | backend | developer | 06 |
| 5 | 12 - Feedback Mistica | frontend | frontend-developer | 09, 10 |

---

Proximo: [03 — Setup do Board GitHub](./03-setup-board-github.md)
