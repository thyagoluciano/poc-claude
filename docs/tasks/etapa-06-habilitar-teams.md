# Etapa 06 — Habilitar Agent Teams

## O que faz

Habilita a feature experimental **Agent Teams** no Claude Code. Com essa feature ativa, uma sessao do Claude Code pode coordenar multiplos agentes (teammates) trabalhando em paralelo no mesmo repositorio — cada um em sua propria branch, implementando tasks diferentes simultaneamente.

## Por que

Agent Teams e o recurso central da POC. Sem ele, o Claude Code trabalha com apenas um agente por vez (ou subagentes efemeros). Com Teams, podemos ter 3 desenvolvedores trabalhando em paralelo: um nos schemas, outro no banco de dados, outro no frontend — exatamente como uma squad real. Isso e o que diferencia a demo de um simples "Claude escrevendo codigo".

## Roteiro (para gravacao)

> **Cena 1 — O que e Agent Teams (30s)**
> "Agent Teams e uma feature experimental do Claude Code que permite coordenar multiplos agentes em paralelo. Cada agente — chamado de teammate — trabalha em sua propria branch, focado em uma task especifica."

> **Cena 2 — Teams vs Subagents (1min)**
> "Qual a diferenca de subagentes? Subagentes sao efemeros — eles executam uma tarefa e desaparecem. Teammates sao persistentes durante a sessao. O lider da equipe distribui tasks, acompanha progresso e coordena dependencias. Cada teammate tem seu proprio contexto e pode usar ferramentas diferentes."

> **Cena 3 — Habilitando (30s)**
> "Para habilitar, basta configurar uma variavel de ambiente. Vou usar o comando `claude config set`. Pronto — a partir de agora, posso criar equipes de agentes."

> **Cena 4 — Limitacoes (30s)**
> "Importante notar: Teams e experimental. Nao ha resumption de sessao — se fechar o terminal, a sessao se perde. So pode ter uma equipe por sessao. E o recomendado e comecar com 3 a 5 teammates para manter controle."

---

## Agent Teams vs Subagents — Comparacao Detalhada

| Aspecto | Subagents | Agent Teams |
|---------|-----------|-------------|
| **Duracao** | Efemeros (executam e terminam) | Persistentes durante a sessao |
| **Coordenacao** | Lancados manualmente via tool `Task` | Lider coordena automaticamente |
| **Paralelismo** | Sim (multiplos Task calls) | Sim (teammates em branches separadas) |
| **Contexto** | Isolado por execucao | Mantido durante toda a sessao |
| **Branching** | Nao gerencia branches | Cada teammate em sua branch |
| **Commits/PRs** | Manual | Teammates fazem commit e criam PRs |
| **Caso de uso** | Reviews paralelos, analises | Desenvolvimento paralelo de features |
| **Exemplo** | `/review-pr` (3 reviewers) | Squad com 3 devs em tasks diferentes |

### Quando usar cada um

- **Subagents**: para tarefas curtas, analises, reviews — quando voce quer multiplas perspectivas sobre o mesmo codigo
- **Agent Teams**: para desenvolvimento paralelo — quando voce quer multiplos agentes implementando features diferentes ao mesmo tempo

---

## Script / Comandos

### 1. Habilitar Agent Teams via CLI

```bash
# Opção 1: Configurar globalmente via claude config
claude config set -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1

# Verificar que foi configurado
claude config get -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
```

### 2. Habilitar via settings.json (alternativa)

```bash
# O arquivo de configuração global fica em:
# macOS/Linux: ~/.claude/settings.json

# Verificar se o arquivo existe
cat ~/.claude/settings.json 2>/dev/null || echo "{}"

# Editar manualmente (ou criar se não existe)
# Adicionar/atualizar a chave "env":
```

O `settings.json` deve conter:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

> **Nota:** Se o arquivo ja tem outras configuracoes, adicione apenas a chave dentro de `"env"`. Nao sobrescreva o conteudo existente.

### 3. Habilitar via variavel de ambiente (alternativa por sessao)

```bash
# Exportar antes de rodar o Claude Code (válido apenas na sessão atual)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

### 4. Verificar que esta habilitado

```bash
# Dentro do Claude Code, o líder deve conseguir criar teammates
# Teste: inicie o Claude Code e peça para criar uma equipe
claude

# Prompt de teste:
# "Crie um teammate chamado 'test-agent' para verificar se Agent Teams está habilitado"
```

---

## Limitacoes Conhecidas

### 1. Sem Resumption de Sessao
Se voce fechar o terminal ou a sessao do Claude Code, a equipe se perde. Nao ha como retomar uma sessao de team. Isso significa que a POC deve rodar do inicio ao fim em uma unica sessao.

**Mitigacao**: Planeje a gravacao para que a sessao nao seja interrompida. Se precisar parar, os PRs criados ja estarao no GitHub — o progresso nao se perde, apenas a coordenacao.

### 2. Uma Equipe por Sessao
Nao e possivel ter multiplas equipes rodando em sessoes paralelas do Claude Code no mesmo repositorio. Apenas uma instancia com Teams ativa por vez.

**Mitigacao**: Se precisar reiniciar, verifique o estado dos PRs e branches antes de iniciar uma nova sessao.

### 3. Controle de Concorrencia
Teammates trabalham em branches separadas, mas conflitos de merge podem ocorrer se dois teammates editarem o mesmo arquivo. O lider deve distribuir tasks que tocam em arquivos diferentes.

**Mitigacao**: O backlog da POC foi desenhado para minimizar conflitos — tasks da mesma wave tocam em arquivos diferentes.

### 4. Custo de API
Cada teammate consome tokens independentemente. Com 3 teammates, o custo de API e aproximadamente 3x o de uma sessao normal.

**Mitigacao**: Monitore o custo na dashboard da Anthropic. Para a POC, use Sonnet quando possivel (mais barato que Opus).

---

## Dicas para Usar Agent Teams

### Comece pequeno
Comece com 2-3 teammates. Mais que 5 pode ficar dificil de coordenar e o custo sobe rapidamente.

### Separe por arquivos
Distribua tasks que tocam em arquivos diferentes para evitar conflitos. Na POC:
- Wave 1: task-01 (schemas), task-02 (database), task-07 (frontend) — ZERO conflito
- Wave 2: task-03 (repositories), task-04 (auth) — ZERO conflito

### Use o lider como orquestrador
O lider (a sessao principal) nao deve implementar codigo — ele deve distribuir tasks, monitorar progresso e coordenar merges. Pense nele como o Tech Lead da squad.

### Monitore os PRs
Cada teammate cria PRs. Acompanhe no GitHub Projects e faca merge na ordem correta (respeitar dependencias).

---

## Checklist de Verificacao

- [ ] Feature habilitada via `claude config set -g env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1`
- [ ] Verificado que a configuracao esta ativa
- [ ] Entendidas as limitacoes (sem resumption, 1 team/sessao, custo 3x)
- [ ] Terminal/sessao pronta para rodar sem interrupcao

---

## Proximo Passo

Siga para **Etapa 07** — Atualizar o Backlog com as tasks de frontend.
