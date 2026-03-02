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
