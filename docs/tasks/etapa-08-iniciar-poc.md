# Etapa 08 — Iniciar a POC com Agent Teams

## O que faz

Inicia a execucao da POC: abre o Claude Code no repositorio `poc-claude` com Agent Teams habilitado e envia o prompt que cria a squad hibrida. O Claude Code assume o papel de lider da equipe, cria 3 teammates desenvolvedores e distribui as tasks da Wave 1 em paralelo. A partir dai, o ciclo se repete: implementar, testar, commit, PR, merge humano, liberar proxima wave.

## Por que

Essa e a etapa principal da demo. Tudo o que fizemos ate aqui (repo, board, action, agents, skills, teams, backlog) converge nesse momento. O humano da um unico prompt e o Claude Code orquestra toda a squad. E a prova de conceito de que agentes IA podem funcionar como membros de uma equipe de desenvolvimento.

## Roteiro (para gravacao)

> **Cena 1 — Pre-flight (30s)**
> "Antes de comecar, vou verificar que tudo esta pronto: repo limpo, project board com 10 issues, API key configurada, Agent Teams habilitado. Tudo verde — vamos iniciar."

> **Cena 2 — O prompt (1min)**
> "Agora vou enviar UM unico prompt para o Claude Code. Esse prompt define o papel do lider, as regras da squad, o backlog e a estrategia de execucao. Observem — eu nao vou dizer COMO implementar cada task. Eu digo O QUE precisa ser feito e o Claude Code organiza a execucao."

> **Cena 3 — Criacao dos teammates (1min)**
> "Olha — o Claude Code esta criando 3 teammates. Cada um vai receber uma task da Wave 1. O teammate 1 vai trabalhar nos schemas Pydantic, o teammate 2 no setup do banco de dados, e o teammate 3 no projeto Next.js. Tudo em paralelo."

> **Cena 4 — Desenvolvimento paralelo (2-3min)**
> "Agora os 3 estao trabalhando simultaneamente. Cada um em sua branch. Podemos ver a atividade nos 3 paineis. O teammate 1 esta criando schemas.py... o teammate 2 esta configurando o SQLAlchemy... o teammate 3 esta rodando npx create-next-app."

> **Cena 5 — Testes e PRs (1min)**
> "Os teammates estao rodando testes. Quando passam, eles fazem commit e criam PRs. Vejam no GitHub — 3 PRs abertos. O @claude review ja esta rodando automaticamente."

> **Cena 6 — Merge humano (1min)**
> "Agora e a minha vez. Vou revisar os PRs, olhar o review do @claude e fazer merge. Esse e o checkpoint humano — o ponto onde o humano valida o trabalho dos agentes."

> **Cena 7 — Proxima wave (1min)**
> "Apos os merges, informo ao Claude Code que os PRs foram merged. Ele recalcula as dependencias e distribui as tasks da Wave 2: CRUD e Auth, agora em paralelo. O ciclo se repete."

---

## Pre-flight Checklist

Antes de iniciar, verifique TODOS estes itens:

```bash
cd ~/Developer/projetos/poc-claude

# 1. Repo está limpo e na main
git status                    # deve mostrar "nothing to commit"
git branch                    # deve estar em "main"

# 2. Todos os arquivos de config existem
ls CLAUDE.md                  # deve existir
ls backend/CLAUDE.md          # deve existir
ls backend/pyproject.toml     # deve existir
ls frontend/CLAUDE.md         # deve existir
ls .claude/agents/*.md        # deve listar 5 agents
ls .claude/skills/review-pr/SKILL.md  # deve existir
ls .github/workflows/claude-review.yml # deve existir

# 3. API key está configurada
gh secret list --repo thyagoluciano/poc-claude  # deve mostrar ANTHROPIC_API_KEY

# 4. Agent Teams está habilitado
claude config get -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS  # deve retornar "1"

# 5. Issues e project board existem
gh issue list --repo thyagoluciano/poc-claude --limit 15  # deve listar 10 issues
```

---

## Setup do Terminal

### Opcao 1: tmux (recomendado)

```bash
# Criar sessão tmux com painel grande
tmux new-session -s poc

# O painel principal será o Claude Code
# Painéis secundários podem mostrar:
# - gh pr list --watch
# - tail de logs
# - htop para monitorar recursos

# Atalhos tmux úteis:
# Ctrl+B " = split horizontal
# Ctrl+B % = split vertical
# Ctrl+B [arrow] = navegar entre painéis
```

### Opcao 2: iTerm2 com split panes

- Abra iTerm2
- Cmd+D para split vertical (2 colunas)
- Cmd+Shift+D para split horizontal no painel direito
- Painel esquerdo (grande): Claude Code
- Painel direito superior: `watch -n 5 'gh pr list --repo thyagoluciano/poc-claude'`
- Painel direito inferior: `watch -n 5 'gh issue list --repo thyagoluciano/poc-claude --label in-progress'`

### Configuracao do terminal para gravacao

```bash
# Fonte grande para legibilidade
# iTerm2: Preferences > Profiles > Text > Font Size: 16-18pt

# Tema escuro com bom contraste
# iTerm2: Preferences > Profiles > Colors > Color Presets: Solarized Dark ou Dracula

# Limpar o terminal antes de começar
clear
```

---

## O Prompt para o Claude Code

Abra o Claude Code no diretorio do repo e envie este prompt:

```bash
cd ~/Developer/projetos/poc-claude
claude
```

### Prompt Inicial (copiar e colar integralmente):

```
Você é o líder de uma squad híbrida que vai construir a TaskFlow API.

O backlog está nas Issues do repositório GitHub. Use `gh issue list` para ver todas
as tasks e `gh issue view <número>` para ler os detalhes de cada uma.
As tasks estão organizadas em 5 waves com dependências explícitas no corpo de cada issue.

Regras da Squad:
1. Crie 3 teammates desenvolvedores para trabalhar em paralelo
2. Cada teammate trabalha em UMA task por vez, em sua própria branch (feat/task-{id})
3. Distribua apenas tasks READY — ou seja, tasks cujas dependências já foram concluídas (merged)
4. Cada teammate deve seguir este fluxo: ler task via `gh issue view` → implementar → rodar testes → commit → criar PR
5. Quando uma task gera PR, ela fica em status "PR_OPEN" — aguardar merge humano
6. Após eu confirmar que fiz merge, recalcule dependências e distribua novas tasks READY
7. Os teammates só param quando não há tasks READY disponíveis
8. Use os agents definidos em .claude/agents/ para os teammates:
   - Tasks de backend (01-06): usar agent "developer"
   - Tasks de frontend (07-10): usar agent "frontend-developer"

Wave Map:
- Wave 1: task-01 + task-02 + task-07 (3 em paralelo, sem dependências)
- Wave 2: task-03 + task-04 (após Wave 1)
- Wave 3: task-05 + task-08 (após Wave 2)
- Wave 4: task-06 + task-09 (após Wave 3)
- Wave 5: task-10 (após Wave 4)

Comece agora:
1. Leia as issues do backlog com `gh issue list` e `gh issue view`
2. Crie 3 teammates
3. Distribua task-01, task-02 e task-07 (Wave 1) — um para cada teammate
4. Acompanhe o progresso e me informe quando os PRs estiverem prontos para review
```

---

## Fluxo Esperado — Cena por Cena

### Fase 1: Inicializacao (1-2 minutos)

**O que o Claude Code faz:**
1. Le as issues do GitHub (`gh issue list`) e o `CLAUDE.md`
2. Analisa as 10 tasks e suas dependencias
3. Identifica as 3 tasks da Wave 1 (sem deps): task-01, task-02, task-07
4. Cria 3 teammates:
   - Teammate 1: agent `developer` → task-01 (schemas)
   - Teammate 2: agent `developer` → task-02 (database)
   - Teammate 3: agent `frontend-developer` → task-07 (next.js)

**O que mostrar na camera:**
- O prompt sendo enviado
- O Claude Code lendo os arquivos
- A mensagem de criacao dos teammates

### Fase 2: Desenvolvimento Paralelo da Wave 1 (5-10 minutos)

**O que cada teammate faz:**

| Teammate | Task | Acoes | Arquivos criados |
|----------|------|-------|-----------------|
| 1 | task-01 schemas | Cria schemas.py, test_schemas.py em backend/, roda pytest | 2 arquivos |
| 2 | task-02 database | Cria database.py, db_models.py, test_database.py em backend/, roda pytest | 3 arquivos |
| 3 | task-07 next.js | Roda npx create-next-app em frontend/, cria api.ts, customiza layout, page | ~20 arquivos |

**O que mostrar na camera:**
- Split screen com atividade dos 3 teammates
- Codigo sendo escrito em tempo real
- Testes rodando e passando
- Commits sendo feitos

### Fase 3: PRs da Wave 1 (2-3 minutos)

**O que acontece:**
1. Cada teammate faz `git push` e cria PR com `gh pr create`
2. O GitHub Action `claude-review.yml` dispara automaticamente
3. O Claude Code informa: "3 PRs prontos para review"

**O que mostrar na camera:**
- PRs aparecendo no GitHub
- Review automatico do @claude sendo postado
- O board atualizado com labels "pr-open"

### Fase 4: Merge Humano (1-2 minutos)

**O que o humano faz:**
1. Abre cada PR no GitHub (ou via CLI)
2. Le o review do @claude
3. Opcionalmente comenta `@claude` para perguntas adicionais
4. Faz merge de cada PR

```bash
# Via CLI (mais rápido para demo):
gh pr merge 1 --merge --repo thyagoluciano/poc-claude
gh pr merge 2 --merge --repo thyagoluciano/poc-claude
gh pr merge 3 --merge --repo thyagoluciano/poc-claude
```

**O que mostrar na camera:**
- Review do @claude em um dos PRs
- O merge sendo feito
- O board atualizando

### Fase 5: Informar o Claude Code e iniciar Wave 2

**O que dizer ao Claude Code:**

```
Os 3 PRs da Wave 1 foram merged (task-01, task-02, task-07).
Recalcule as dependências e distribua as tasks da Wave 2.
```

**O que o Claude Code faz:**
1. Atualiza o estado: task-01, task-02, task-07 = DONE
2. Verifica quais tasks ficaram READY:
   - task-03 (deps: 01, 02) → READY
   - task-04 (deps: 01, 02) → READY
   - task-08 (deps: 04, 07) → BLOCKED (04 ainda nao feita)
3. Distribui task-03 e task-04 para 2 teammates
4. Teammate 3 fica idle (nenhuma task frontend READY)

### Fase 6: Repetir para Waves 3-5

O ciclo se repete:
- **Wave 2** completa → merge → Wave 3 (task-05 + task-08)
- **Wave 3** completa → merge → Wave 4 (task-06 + task-09)
- **Wave 4** completa → merge → Wave 5 (task-10)
- **Wave 5** completa → merge → FIM

---

## Comandos Uteis Durante a POC

### Monitorar PRs

```bash
# Listar PRs abertos
gh pr list --repo thyagoluciano/poc-claude

# Ver detalhes de um PR
gh pr view 1 --repo thyagoluciano/poc-claude

# Merge um PR
gh pr merge 1 --merge --repo thyagoluciano/poc-claude

# Merge todos os PRs abertos (cuidado — só usar quando todos estão aprovados)
gh pr list --repo thyagoluciano/poc-claude --json number -q '.[].number' | \
  xargs -I {} gh pr merge {} --merge --repo thyagoluciano/poc-claude
```

### Monitorar issues e board

```bash
# Listar issues por label
gh issue list --repo thyagoluciano/poc-claude --label "in-progress"
gh issue list --repo thyagoluciano/poc-claude --label "pr-open"
gh issue list --repo thyagoluciano/poc-claude --label "ready"
```

### Atualizar labels das issues (manual)

```bash
# Quando um PR é aberto para uma task
gh issue edit ISSUE_NUMBER --add-label "pr-open" --remove-label "in-progress" --repo thyagoluciano/poc-claude

# Quando um PR é merged
gh issue close ISSUE_NUMBER --repo thyagoluciano/poc-claude
```

### Verificar branches

```bash
# Listar branches remotas
git fetch origin
git branch -r

# Ver o diff de uma branch
git diff main..origin/feat/task-01-models
```

### Pedir review adicional do @claude em um PR

Comentar diretamente no PR no GitHub:

```
@claude analise este PR com foco em segurança e qualidade de código.
Verifique se os testes cobrem os edge cases.
```

---

## Como Lidar com Problemas

### Teammate travou ou parou de responder

```
O teammate trabalhando na task-XX parece travado.
Verifique o status e, se necessário, recrie o teammate para continuar.
```

### Conflito de merge

```
O PR da task-XX tem conflito com main.
Peça ao teammate para fazer rebase da branch dele com main e resolver o conflito.
```

### Teste falhando

```
Os testes da task-XX estão falhando.
Peça ao teammate para ler o output do pytest, diagnosticar o problema e corrigir.
```

### Precisa reiniciar a sessao

Se a sessao do Claude Code for perdida:
1. Verifique quais PRs ja foram merged
2. Verifique quais branches existem
3. Inicie nova sessao e informe o estado atual:

```
Estou retomando a POC. Estado atual:
- Tasks concluídas (merged): task-01, task-02, task-07, task-03, task-04
- PRs abertos: nenhum
- Próxima wave: Wave 3 (task-05 + task-08)

Continue de onde paramos. Crie teammates e distribua as tasks da Wave 3.
```

---

## Timeline Estimada

| Fase | Duracao Estimada | O que acontece |
|------|-----------------|----------------|
| Pre-flight | 2 min | Verificacao e setup |
| Prompt + Criacao teammates | 2 min | Lider cria a squad |
| Wave 1 (3 tasks paralelo) | 8-12 min | Schemas + DB + Next.js |
| Review + Merge W1 | 3 min | Humano revisa e merge |
| Wave 2 (2 tasks paralelo) | 6-8 min | CRUD + Auth |
| Review + Merge W2 | 2 min | Humano revisa e merge |
| Wave 3 (2 tasks paralelo) | 8-10 min | API + Auth UI |
| Review + Merge W3 | 2 min | Humano revisa e merge |
| Wave 4 (2 tasks paralelo) | 8-10 min | E2E Tests + Task UI |
| Review + Merge W4 | 2 min | Humano revisa e merge |
| Wave 5 (1 task) | 5-7 min | Dashboard |
| Review + Merge W5 | 2 min | Merge final |
| **TOTAL** | **~50-70 min** | **10 tasks, 5 waves** |

---

## Checklist de Verificacao

- [ ] Pre-flight checklist completo (repo, board, key, teams, issues)
- [ ] Terminal configurado (tmux ou iTerm2 split)
- [ ] Prompt copiado e pronto para enviar
- [ ] Gravacao de tela iniciada (se for demo gravada)
- [ ] Plano para lidar com problemas comuns

---

## Proximo Passo

Siga para **Etapa 09** — Checklist e dicas para gravacao da demo.
