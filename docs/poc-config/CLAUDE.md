# TaskFlow API — Projeto da POC Squad Híbrida

## Sobre
API REST de gerenciamento de tarefas construída autonomamente por uma squad híbrida (Humanos + IA Agents).

## Stack
### Backend
- Python 3.12+
- FastAPI para API REST
- SQLAlchemy com SQLite
- Pydantic v2 para schemas e validação
- python-jose[cryptography] para JWT
- passlib[bcrypt] para hashing de senhas
- pytest + httpx para testes

### Frontend
- Next.js 14+ (App Router)
- React 18+ com hooks
- TypeScript (strict mode)
- Tailwind CSS para estilização
- Fetch API para comunicação com backend

## Estrutura do Projeto
```
src/
├── taskflow/          # Backend Python
│   ├── __init__.py
│   ├── app.py         # FastAPI application
│   ├── schemas.py     # Pydantic models
│   ├── db_models.py   # SQLAlchemy models
│   ├── database.py    # Database setup
│   ├── repositories.py # CRUD operations
│   ├── auth.py        # JWT auth logic
│   ├── auth_router.py # Auth endpoints
│   └── task_router.py # Task endpoints
├── frontend/          # Next.js App
│   ├── src/app/       # App Router pages
│   ├── src/lib/       # API client, auth context
│   └── src/components/ # React components
tests/                 # Backend tests
```

## Regras de Desenvolvimento
- Type hints obrigatórios em todo código Python
- TypeScript strict mode no frontend
- Testes para toda funcionalidade nova (backend: pytest, frontend: build check)
- Commit message: `[task-XX-name] Descrição curta`
- Rodar `python -m pytest tests/ -v` antes de finalizar tasks backend
- Rodar `cd src/frontend && npm run build` antes de finalizar tasks frontend
- NÃO modificar arquivos de outras tasks (cada task tem escopo definido)
- Usar imports relativos dentro do pacote taskflow
- Backend roda na porta 8000, Frontend na porta 3000
- CORS deve estar configurado para permitir localhost:3000

## Regras de Code Review
- Security: verificar OWASP Top 10, injection, auth bypass, secrets
- Quality: SOLID, DRY, clean code, naming conventions
- Tests: cobertura, edge cases, assertions claras
