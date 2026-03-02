# 06 — Cenario de Falha de Seguranca

Este documento detalha o cenario intencional de vulnerabilidade na task-11 e todo o
fluxo de deteccao, notificacao e correcao.

---

## 6.1 A Vulnerabilidade Planejada

A **task-11** pede a criacao de um endpoint de busca publica de tasks. O texto da issue
instrui o desenvolvedor a:

1. Criar `GET /search/tasks?q={query}` **SEM autenticacao**
2. Retornar dados incluindo **owner username e email**

Isso introduz DUAS vulnerabilidades OWASP:

### Vulnerabilidade 1: Sensitive Data Exposure (OWASP A3:2017 / A02:2021)

```python
# O que o developer vai implementar (vulneravel):
@router.get("/search/tasks")
def search_tasks(q: str, db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).filter(TaskModel.title.contains(q)).all()
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "owner_id": task.owner_id,
            "owner_username": task.owner.username,
            "owner_email": task.owner.email,        # <-- EXPOSICAO DE DADOS
        }
        for task in tasks
    ]
```

**Risco:** Email de usuarios expostos publicamente. Pode ser usado para phishing,
spam ou enumeracao de usuarios.

### Vulnerabilidade 2: Broken Access Control (OWASP A01:2021)

O endpoint nao requer autenticacao, permitindo que QUALQUER pessoa veja TODAS as
tasks de TODOS os usuarios. Isso viola o principio de menor privilegio.

**Risco:** Informacoes privadas de tasks (descricoes, status, prioridades) acessiveis
sem autenticacao.

---

## 6.2 Fluxo de Deteccao (100% Local)

### Passo 1: Teammate implementa task-11

O developer segue a issue e implementa exatamente como descrito:
- Cria `search_router.py` com o endpoint vulneravel
- Cria testes que PASSAM (testes nao verificam seguranca)
- Faz commit, push e cria PR via `gh pr create`

### Passo 2: Lead lanca reviewers LOCALMENTE

O Lead detecta que o teammate abriu o PR e lanca os 3 reviewers como
subagentes locais em paralelo:

```
# O Lead faz internamente (via Agent tool):
Agent(security-reviewer, "Revise PR #<N>. Use gh pr diff <N>, analise, e poste via gh pr comment <N>")
Agent(quality-reviewer,  "Revise PR #<N>. Use gh pr diff <N>, analise, e poste via gh pr comment <N>")
Agent(test-reviewer,     "Revise PR #<N>. Use gh pr diff <N>, analise, e poste via gh pr comment <N>")
```

Cada reviewer:
1. Executa `gh pr diff <PR_NUMBER>` para ler o diff
2. Le os arquivos modificados para contexto
3. Faz a analise especializada
4. **Posta comentario diretamente no PR** via `gh pr comment <PR> --body "..."`

### Passo 3: Comentarios aparecem no PR do GitHub

**security-reviewer posta no PR:**
```markdown
## 🔒 Security Review

### Vulnerabilidades Encontradas

- **[CRITICA] Sensitive Data Exposure (OWASP A02:2021)**
  - Arquivo: `backend/src/taskflow/search_router.py:15`
  - Risco: O campo `owner_email` expoe o email do usuario sem autenticacao.
    Qualquer pessoa pode coletar emails de todos os usuarios do sistema.
  - Correcao: Remover o campo `owner_email` da resposta.

- **[ALTA] Broken Access Control (OWASP A01:2021)**
  - Arquivo: `backend/src/taskflow/search_router.py:8`
  - Risco: Endpoint sem autenticacao permite acesso a TODAS as tasks.
  - Correcao: Adicionar `Depends(get_current_user)`.

### Veredicto
❌ **Reprovado** — Vulnerabilidades criticas encontradas
```

**quality-reviewer posta no PR:**
```markdown
## 📋 Quality Review

### Problemas
- **[Media]** Falta schema Pydantic de resposta para o endpoint de busca.
  Usar schema garante que campos sensiveis nao vazem acidentalmente.

### Veredicto
⚠️ **Aprovado com ressalvas**
```

**test-reviewer posta no PR:**
```markdown
## 🧪 Test Review

### Gaps
- Falta teste que verifique que dados sensiveis NAO sao retornados
- Falta teste de acesso sem autenticacao (401)

### Veredicto
⚠️ **Aprovado com ressalvas**
```

### Passo 4: Lead posta consolidado no PR

O Lead posta um comentario final consolidado no PR:

```bash
gh pr comment <PR> --body "$(cat <<'EOF'
# 📋 Review Consolidado

## 🔒 Seguranca: ❌ REPROVADO
- CRITICA: Sensitive Data Exposure — email exposto sem auth
- ALTA: Broken Access Control — endpoint publico

## 📐 Qualidade: ⚠️ RESSALVAS
- Falta schema Pydantic para response

## 🧪 Testes: ⚠️ RESSALVAS
- Falta teste de dados sensiveis e auth

## Veredicto Final
❌ **Precisa de ajustes**

### Acoes Necessarias
1. [CRITICA] Remover owner_email da resposta
2. [ALTA] Adicionar autenticacao ao endpoint
3. [MEDIA] Criar schema TaskSearchResponse
4. [MEDIA] Adicionar testes de seguranca
EOF
)"
```

> **O humano pode ver TODOS esses comentarios no PR do GitHub**, mesmo antes de
> o developer corrigir. Isso da visibilidade total do processo de review.

---

## 6.3 Fluxo de Correcao

### Passo 5: Lead notifica o teammate

O Lead envia mensagem ao teammate backend-dev que implementou task-11 (via SendMessage):

```
O review de seguranca do PR da task-11 encontrou vulnerabilidades criticas:

1. CRITICA — Sensitive Data Exposure: O endpoint /search/tasks retorna
   owner_email sem autenticacao. Remova o campo email da resposta.

2. ALTA — Broken Access Control: O endpoint nao requer autenticacao,
   expondo tasks de todos os usuarios. Adicione Depends(get_current_user)
   para requerer auth.

3. MEDIA — Crie um schema Pydantic SearchResponse para controlar
   explicitamente quais campos sao retornados.

Corrija esses problemas, rode os testes e atualize o PR.
```

### Passo 6: Teammate corrige

O developer vai:

1. **Criar schema** `SearchResponse`:
```python
# schemas.py (adicionar)
class TaskSearchResponse(BaseModel):
    """Schema para resultados de busca — sem dados sensiveis."""
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
```

2. **Adicionar autenticacao** ao endpoint:
```python
# search_router.py (corrigido)
from .auth import get_current_user
from .schemas import TaskSearchResponse

@router.get("/search/tasks", response_model=list[TaskSearchResponse])
def search_tasks(
    q: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),  # <-- AUTH
):
    tasks = db.query(TaskModel).filter(TaskModel.title.contains(q)).all()
    return tasks  # Schema controla os campos retornados
```

3. **Atualizar testes** para incluir autenticacao:
```python
# test_search.py (corrigido)
def test_search_tasks_requires_auth(client):
    """Busca sem token retorna 401."""
    response = client.get("/search/tasks?q=test")
    assert response.status_code == 401

def test_search_tasks_by_title(client, auth_headers):
    """Busca autenticada retorna tasks sem dados sensiveis."""
    # Criar task
    client.post("/tasks/", json={"title": "Test Task"}, headers=auth_headers)
    # Buscar
    response = client.get("/search/tasks?q=Test", headers=auth_headers)
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "Test Task"
    assert "email" not in results[0]          # <-- Verifica que email NAO aparece
    assert "owner_email" not in results[0]    # <-- Verifica que email NAO aparece
```

4. **Commit e push**:
```bash
git add -A
git commit -m "fix: add auth and remove sensitive data from search endpoint"
git push
```

### Passo 7: Lead re-lanca reviewers LOCALMENTE

O Lead lanca novamente os 3 reviewers no PR atualizado (mesmo processo do Passo 2).
Cada reviewer:
1. Le o novo diff com `gh pr diff <PR>`
2. Analisa as correcoes
3. **Posta NOVO comentario no PR** confirmando a correcao

**security-reviewer posta:**
```markdown
## 🔒 Security Re-Review

### Correcoes Verificadas
- ✅ Endpoint agora requer autenticacao (`Depends(get_current_user)`)
- ✅ Email do owner NAO e exposto na resposta
- ✅ Schema `TaskSearchResponse` controla campos retornados

### Veredicto
✅ **Aprovado** — Vulnerabilidades corrigidas
```

**Lead posta consolidado final:**
```markdown
# 📋 Re-Review Consolidado

## Veredicto Final
✅ **Aprovado** — Todas as vulnerabilidades foram corrigidas

- 🔒 Seguranca: ✅ Aprovado
- 📐 Qualidade: ✅ Aprovado
- 🧪 Testes: ✅ Aprovado
```

### Passo 8: Lead informa humano

O Lead informa o humano:

```
O PR da task-11 esta pronto para merge.

Historico do review (visivel nos comentarios do PR):
1. Review inicial detectou 2 vulnerabilidades (Sensitive Data Exposure + Broken Access Control)
2. Developer foi notificado e corrigiu (adicionou auth + removeu email + criou schema)
3. Re-review confirmou que todas as correcoes estao OK

Voce pode ver todos os comentarios dos reviewers diretamente no PR.
```

> O humano pode abrir o PR no GitHub e ver TODA a linha do tempo:
> comentarios dos reviewers, o consolidado, a correcao e o re-review.

---

## 6.4 O que Demonstra

Este cenario demonstra CINCO capacidades:

### 1. Deteccao Automatica de Vulnerabilidades
O security-reviewer (agente local) identifica problemas OWASP sem intervencao humana
e posta diretamente no PR para visibilidade.

### 2. Workflow de Correcao Integrado
O Lead orquestra o ciclo: detectar → notificar → corrigir → re-verificar.
O humano so precisa fazer merge do codigo ja corrigido.

### 3. Seguranca como Parte do Fluxo
A seguranca nao e um gate final — e parte do desenvolvimento continuo.
Problemas sao pegos ANTES do merge, nao em producao.

### 4. Rastreabilidade Completa no PR
Todos os comentarios (review inicial, consolidado, correcao, re-review) ficam
visíveis no PR do GitHub. O humano tem visibilidade TOTAL do processo sem
precisar rodar nada — basta abrir o PR e ler os comentarios.

### 5. Agentes Especializados com Orquestracao Local
Cada agente tem seu papel claro e tudo roda LOCALMENTE:
- **developer**: implementa (pode introduzir vulnerabilidades)
- **security-reviewer**: detecta e POSTA no PR (read-only no codigo, escreve no PR)
- **quality-reviewer**: analisa qualidade e POSTA no PR
- **test-reviewer**: analisa testes e POSTA no PR
- **Lead**: orquestra tudo localmente (lanca reviewers, notifica devs)
- **humano**: valida e merge (decisao final, ve tudo nos comentarios do PR)

---

## 6.5 Pontos de Atencao para a Demo

1. **O developer NAO sabe que a task e vulneravel.** Ele segue a issue ao pe da letra.
   Isso e intencional — demonstra que o review automatico pega o que o dev nao percebeu.

2. **O security-reviewer NAO corrige.** Ele apenas reporta. Isso demonstra
   separation of concerns e o principio de menor privilegio.

3. **O Lead coordena.** Ele e o intermediario entre deteccao e correcao.
   Na vida real, isso seria como um Tech Lead mediando entre SecOps e devs.

4. **O humano faz merge SOMENTE depois da correcao.** Isso demonstra que o
   human-in-the-loop e o checkpoint final de qualidade.

---

## 6.6 Variacao: Se o Review NAO Pegar

Se por algum motivo o security-reviewer nao detectar a vulnerabilidade:

1. O Lead pode apontar manualmente:
   ```
   Revisei o PR da task-11 e percebi que o endpoint /search/tasks expoe
   email sem auth. Execute /review-pr com foco especifico em seguranca.
   ```

2. Ou o Snyk (se configurado) pode pegar via `snyk_code_scan`

3. Ou o humano pode pegar durante o merge review:
   ```
   O PR da task-11 tem problemas de seguranca. Pecam ao developer para
   remover o email da resposta e adicionar autenticacao.
   ```

---

Proximo: [07 — Troubleshooting](./07-troubleshooting.md)
