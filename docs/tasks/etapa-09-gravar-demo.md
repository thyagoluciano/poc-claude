# Etapa 09 — Gravar a Demo

## O que faz

Guia completo para gravar a demonstracao da POC. Inclui checklist pre-gravacao, configuracao de tela, roteiro de narracao cena a cena, metricas a capturar, troubleshooting de problemas comuns e dicas de pos-producao.

## Por que

A gravacao e o produto final da POC. Uma demo bem gravada vale mais que mil slides. O objetivo e mostrar, em tempo real, uma squad hibrida (humano + agentes IA) construindo uma aplicacao full-stack do zero. A narrativa deve ser clara, os resultados visiveis e as metricas concretas.

## Roteiro (para gravacao)

Este documento E o roteiro. Siga as cenas abaixo na ordem.

---

## Pre-requisitos (tudo de etapa-01 a etapa-08)

### Checklist Completo

```
REPO E CONFIGURACAO
[ ] Repo poc-claude existe no GitHub
[ ] CLAUDE.md na raiz do repo
[ ] product_backlog.yaml com 10 tasks
[ ] 5 agents em .claude/agents/
[ ] Skill review-pr em .claude/skills/review-pr/SKILL.md
[ ] Workflow claude-review.yml em .github/workflows/
[ ] Secret ANTHROPIC_API_KEY configurado

GITHUB PROJECT
[ ] Project board criado
[ ] 10 issues criadas com body completo
[ ] Labels criadas (ai-agent, backend, frontend, ready, blocked, in-progress, pr-open)
[ ] Issues 01, 02, 07 com label "ready"
[ ] Todas as issues adicionadas ao project

AMBIENTE LOCAL
[ ] Agent Teams habilitado (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)
[ ] Claude Code instalado e funcionando
[ ] Git configurado (user.name, user.email)
[ ] gh CLI autenticado
[ ] Node.js instalado (para task-07)
[ ] Python 3.12+ instalado (para tasks backend)

GRAVACAO
[ ] Software de gravação de tela instalado (OBS, QuickTime, Loom)
[ ] Microfone testado (se for narrar ao vivo)
[ ] Terminal com fonte grande (16-18pt)
[ ] Tema escuro no terminal
[ ] Notificações do sistema desabilitadas
[ ] Resolução de tela: 1920x1080 ou 2560x1440
```

---

## Configuracao de Tela para Gravacao

### Layout Recomendado (Split Screen)

```
┌─────────────────────────────────────┬──────────────────────┐
│                                     │                      │
│         TERMINAL PRINCIPAL          │    GITHUB (Browser)  │
│         (Claude Code)               │                      │
│                                     │    - PR list         │
│         70% da tela                 │    - Project board   │
│                                     │    - Issue details   │
│                                     │                      │
│                                     │    30% da tela       │
│                                     │                      │
└─────────────────────────────────────┴──────────────────────┘
```

### Alternativa com tmux (tudo no terminal)

```
┌──────────────────────────────┬──────────────────────┐
│                              │                      │
│     CLAUDE CODE              │   gh pr list         │
│     (sessao principal)       │   (watch mode)       │
│                              │                      │
│     65% largura              ├──────────────────────┤
│                              │                      │
│                              │   git log --oneline  │
│                              │   (watch mode)       │
│                              │                      │
└──────────────────────────────┴──────────────────────┘
```

### Configuracoes Visuais

```bash
# Terminal - fonte grande e limpa
# iTerm2: Preferences > Profiles > Text > Font: Menlo 16pt ou JetBrains Mono 16pt

# Desabilitar notificações (macOS)
# System Settings > Focus > Do Not Disturb > ON

# Limpar desktop (esconder ícones)
defaults write com.apple.finder CreateDesktop false && killall Finder
# Para restaurar depois:
# defaults write com.apple.finder CreateDesktop true && killall Finder

# Limpar terminal
clear
```

---

## Roteiro de Narracao — Cena a Cena

### Abertura (1 minuto)

**Mostrar**: Terminal limpo com o repo poc-claude aberto.

**Narrar**:
> "Vou demonstrar como uma squad hibrida — um humano e agentes IA — constroi uma aplicacao full-stack do zero. O projeto e a TaskFlow API: um backend FastAPI e um frontend Next.js. O backlog tem 10 tasks organizadas em 5 waves com dependencias entre elas."

**Acao**: Mostrar rapidamente o `product_backlog.yaml` e o board do GitHub Projects.

```bash
# Mostrar o backlog
cat product_backlog.yaml | head -20

# Mostrar o board (alternar para browser)
# GitHub Projects URL
```

---

### Cena 1 — O Setup (1 minuto)

**Mostrar**: Estrutura do repo e arquivos de configuracao.

**Narrar**:
> "O repo ja esta configurado. Temos o CLAUDE.md com as regras do projeto, 5 agentes especializados, uma skill de review e um workflow do GitHub Actions. O backlog YAML e a fonte de verdade — os agentes leem dele para saber o que fazer."

**Acao**:
```bash
tree -a -I '.git|node_modules|__pycache__|.venv' --dirsfirst -L 2
cat CLAUDE.md | head -30
ls .claude/agents/
```

---

### Cena 2 — Iniciando os Agentes (2 minutos)

**Mostrar**: Claude Code recebendo o prompt.

**Narrar**:
> "Agora envio UM unico prompt. Ele define o papel do lider, as regras da squad e pede para comecar com as 3 tasks da Wave 1 — que nao tem dependencias e podem rodar em paralelo."

**Acao**: Copiar e colar o prompt da Etapa 08. Esperar o Claude Code processar.

**Narrar** (enquanto processa):
> "Observem: o Claude Code esta lendo o backlog, identificando as tasks sem dependencias e criando 3 teammates. Cada teammate vai receber uma task e trabalhar em sua propria branch."

---

### Cena 3 — Wave 1 em Paralelo (5-8 minutos)

**Mostrar**: Os 3 teammates trabalhando simultaneamente.

**Narrar**:
> "Agora temos 3 agentes trabalhando em paralelo:
> - O Teammate 1 esta criando os schemas Pydantic — os modelos de dados da API
> - O Teammate 2 esta configurando o SQLAlchemy com SQLite — o banco de dados
> - O Teammate 3 esta criando o projeto Next.js — o frontend
>
> Cada um esta em sua propria branch. Nao ha conflito porque as tasks da mesma wave tocam em arquivos diferentes."

**Acao**: Alternar entre os paineis mostrando o progresso de cada teammate.

**Pontos de destaque durante a Wave 1**:
- Quando um teammate cria um arquivo: "Olha, o teammate 1 acabou de criar o schemas.py com todas as validacoes Pydantic"
- Quando um teammate roda testes: "O teammate 2 esta rodando pytest... todos os testes passaram"
- Quando um teammate faz commit: "Commit feito com mensagem seguindo Conventional Commits — isso esta definido no CLAUDE.md"

---

### Cena 4 — PRs e Review Automatico (2 minutos)

**Mostrar**: GitHub com os 3 PRs abertos.

**Narrar**:
> "Os 3 teammates criaram seus PRs. E vejam — o GitHub Action ja rodou o review automatico via @claude. Cada PR tem uma analise de seguranca, qualidade e cobertura de testes. O humano nao precisa fazer nada — o review chega automaticamente."

**Acao**: Abrir um dos PRs no browser e mostrar o comentario do @claude.

---

### Cena 5 — Merge Humano (1 minuto)

**Mostrar**: Fazendo merge dos PRs.

**Narrar**:
> "Agora e o meu turno. Reviso os PRs, leio o feedback do @claude e faco merge. Esse e o checkpoint humano — o ponto de controle onde valido o trabalho dos agentes antes de seguir."

**Acao**:
```bash
gh pr merge 1 --merge --repo thyagoluciano/poc-claude
gh pr merge 2 --merge --repo thyagoluciano/poc-claude
gh pr merge 3 --merge --repo thyagoluciano/poc-claude
```

---

### Cena 6 — Proximas Waves (resumo rapido, 2-3 minutos)

**Mostrar**: Claude Code recebendo a confirmacao de merge e distribuindo novas tasks.

**Narrar**:
> "Informo ao Claude Code que os merges foram feitos. Ele recalcula as dependencias e distribui a Wave 2: task-03 (CRUD) e task-04 (Auth JWT). O ciclo se repete: implementar, testar, PR, review, merge."

**Acao**: Enviar mensagem ao Claude Code e mostrar os teammates recebendo novas tasks.

> Para a gravacao, nao e necessario mostrar todas as 5 waves completas. Voce pode:
> - Mostrar Wave 1 completa (demonstra o fluxo)
> - Acelerar Waves 2-4 (time-lapse ou corte)
> - Mostrar Wave 5 (conclusao com dashboard)

---

### Cena 7 — Resultado Final (2 minutos)

**Mostrar**: A aplicacao rodando.

**Narrar**:
> "A aplicacao esta completa. Vou mostrar: o backend rodando com FastAPI e a documentacao OpenAPI, e o frontend Next.js com login, dashboard e gerenciamento de tasks. Tudo isso foi construido por agentes IA coordenados por um humano."

**Acao**:
```bash
# Rodar o backend
cd ~/Developer/projetos/poc-claude/backend
uvicorn src.taskflow.app:app --reload &

# Abrir docs
open http://localhost:8000/docs

# Rodar o frontend
cd ~/Developer/projetos/poc-claude/frontend
npm run dev &
open http://localhost:3000
```

---

### Fechamento (1 minuto)

**Mostrar**: Board do GitHub Projects com todas as issues closed.

**Narrar**:
> "10 tasks, 5 waves, tudo construido por uma squad hibrida. O humano definiu o backlog, revisou os PRs e fez os merges. Os agentes implementaram, testaram e criaram PRs. Cada parte fez o que faz melhor. Isso e o futuro do desenvolvimento de software."

**Acao**: Mostrar metricas (tempo total, custo, numero de PRs).

---

## Metricas a Capturar

Anote estes dados durante a execucao para apresentar no fechamento:

| Metrica | Como medir | Exemplo |
|---------|-----------|---------|
| **Tempo total** | Cronometro do inicio ao fim | ~60 min |
| **Tempo por wave** | Anotar inicio/fim de cada wave | W1: 12min, W2: 8min, ... |
| **PRs criados** | `gh pr list --state all --repo ...` | 10 PRs (5 waves * ~2 PRs) |
| **Commits totais** | `git log --oneline \| wc -l` | ~20-30 commits |
| **Linhas de codigo** | `cloc backend/src/ frontend/src/ backend/tests/` | ~2000-3000 LOC |
| **Testes** | `cd backend && pytest --tb=short \| tail -5` | 25+ testes passando |
| **Custo API** | Dashboard Anthropic | ~$5-15 (estimativa) |
| **Reviews automaticos** | Contar comentarios @claude nos PRs | 10+ reviews |

### Como capturar no final

```bash
cd ~/Developer/projetos/poc-claude

# Total de PRs
echo "PRs criados: $(gh pr list --state all --repo thyagoluciano/poc-claude --json number -q '. | length')"

# Total de commits
echo "Commits: $(git log --oneline | wc -l)"

# Linhas de código
cloc backend/src/ frontend/src/ backend/tests/ 2>/dev/null || find backend/src/ frontend/src/ backend/tests/ -name "*.py" -o -name "*.ts" -o -name "*.tsx" | xargs wc -l | tail -1

# Testes
cd ~/Developer/projetos/poc-claude/backend && pytest --tb=short 2>/dev/null | tail -5
```

---

## Troubleshooting — Problemas Comuns

### 1. Agente travado (nao responde por mais de 2 minutos)

**Sintoma**: Um teammate para de produzir output.
**Solucao**: Diga ao Claude Code:
```
O teammate trabalhando na task-XX parece travado. Por favor, verifique o status dele
e, se necessário, cancele e recrie para continuar a task.
```

### 2. Conflito de merge no PR

**Sintoma**: PR nao pode ser merged automaticamente.
**Solucao**:
```bash
# Resolver manualmente
git checkout feat/task-XX
git rebase main
# Resolver conflitos
git add .
git rebase --continue
git push --force-with-lease origin feat/task-XX
```
Ou diga ao Claude Code:
```
O PR da task-XX tem conflito com main. Peça ao teammate para fazer rebase com main.
```

### 3. Teste falhando

**Sintoma**: pytest falha e o teammate nao consegue resolver.
**Solucao**: Diga ao Claude Code:
```
O teste test_XX está falhando com o erro: [colar o erro].
Peça ao teammate para diagnosticar e corrigir.
```

### 4. GitHub Action nao dispara

**Sintoma**: @claude nao responde no PR.
**Solucao**:
```bash
# Verificar se o workflow existe
gh workflow list --repo thyagoluciano/poc-claude

# Verificar runs recentes
gh run list --repo thyagoluciano/poc-claude --limit 5

# Verificar secret
gh secret list --repo thyagoluciano/poc-claude
```

### 5. Sessao do Claude Code perdida

**Sintoma**: Terminal fechou, sessao perdida.
**Solucao**: Ver instruções de retomada na Etapa 08 (secao "Precisa reiniciar a sessao").

### 6. Teammate cria arquivos no lugar errado

**Sintoma**: Arquivos criados fora da estrutura esperada.
**Solucao**:
```
O teammate criou arquivos na estrutura errada. A estrutura correta é:
- Backend: backend/src/taskflow/
- Frontend: frontend/src/
- Testes backend: backend/tests/
Por favor, corrija a estrutura.
```

### 7. Custo de API alto demais

**Sintoma**: Consumo de tokens acima do esperado.
**Solucao**:
- Reduza para 2 teammates ao inves de 3
- Use Sonnet ao inves de Opus para os teammates
- Faca as waves mais simples primeiro para calibrar

---

## Pos-Gravacao

### Edicao do Video

1. **Cortar tempos mortos**: Quando os agentes estao processando sem output visivel, acelere (2x-4x) ou corte
2. **Adicionar captions**: Nos momentos-chave, adicione textos explicativos
3. **Destacar metricas**: No fechamento, use overlay com as metricas capturadas
4. **Adicionar musica de fundo** (opcional): Lo-fi ou ambient suave durante o time-lapse

### Pontos de Corte Recomendados

| Momento | Acao de edicao |
|---------|---------------|
| Agente processando (sem output) | Acelerar 4x |
| npm install / pip install | Cortar ou acelerar 8x |
| Testes rodando | Manter velocidade normal (e rapido e importante) |
| PR sendo criado | Manter velocidade normal |
| Merge humano | Manter velocidade normal |
| Transicao entre waves | Adicionar card de transicao ("Wave 2 - CRUD + Auth") |

### Estrutura Sugerida do Video Final

```
0:00 - 1:00   Intro (o que vamos fazer)
1:00 - 2:00   Setup (repo, board, agents)
2:00 - 4:00   Prompt e criação dos teammates
4:00 - 8:00   Wave 1 (3 tasks paralelo) — com narração
8:00 - 9:00   PRs e @claude review
9:00 - 10:00  Merge humano
10:00 - 12:00 Wave 2 (time-lapse)
12:00 - 14:00 Waves 3-4 (montage/summary)
14:00 - 16:00 Wave 5 + App rodando
16:00 - 18:00 Métricas e fechamento
```

### Duracao ideal

- **Demo completa**: 15-20 minutos (para apresentacao tecnica)
- **Highlight reel**: 5-7 minutos (para social media / quick demo)
- **Full recording**: 50-70 minutos (para referencia interna)

---

## Metricas de Sucesso da POC

A POC e considerada um sucesso se:

1. **Funcional**: A aplicacao TaskFlow roda end-to-end (registro, login, CRUD de tasks, dashboard)
2. **Autonomo**: Os agentes implementaram 80%+ do codigo sem intervencao humana no codigo
3. **Paralelo**: Pelo menos 2 teammates trabalharam em paralelo em pelo menos 3 waves
4. **Qualidade**: Todos os testes passam (pytest), zero erros de TypeScript (npm run build)
5. **Fluxo**: O fluxo PR → @claude review → merge humano funcionou em pelo menos 5 PRs
6. **Tempo**: Menos de 90 minutos do prompt inicial ate a aplicacao rodando
7. **Custo**: Menos de $20 em API calls

---

## Checklist Final

- [ ] Todos os pre-requisitos verificados
- [ ] Tela configurada (split, fonte grande, tema escuro)
- [ ] Software de gravacao configurado e testado
- [ ] Roteiro de narracao revisado
- [ ] Cronometro pronto para medir tempo por wave
- [ ] Planilha de metricas pronta para preencher
- [ ] Plano B para problemas comuns (troubleshooting lido)
- [ ] Gravacao iniciada
- [ ] GO!
