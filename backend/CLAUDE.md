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
