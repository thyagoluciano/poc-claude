# Etapa 05 — Configurar Skill de Review de PR

## O que faz

Cria a skill `/review-pr` em `.claude/skills/review-pr/SKILL.md`. Essa skill e invocada com `/review-pr` no Claude Code e lanca 3 subagentes em paralelo — security-reviewer, quality-reviewer e test-reviewer — cada um analisando o PR diff da sua perspectiva. Ao final, consolida os 3 reports em um unico comentario de review.

## Por que

Ao inves de rodar 3 reviews sequenciais, a skill usa subagentes paralelos para otimizar tempo. Cada reviewer tem foco diferente (seguranca, qualidade, testes) e ferramentas limitadas (read-only). A consolidacao gera um report unico e estruturado — como uma revisao de codigo feita por um comite tecnico. Isso demonstra o poder de composicao de agentes no Claude Code.

## Roteiro (para gravacao)

> **Cena 1 — O conceito de Skill (30s)**
> "Skills sao comandos customizados do Claude Code. Quando digito /review-pr, o Claude executa um fluxo pre-definido. Nesse caso, ele lanca 3 subagentes revisores em paralelo."

> **Cena 2 — Os 3 subagentes (1min)**
> "Cada subagente usa um agente diferente: security-reviewer analisa vulnerabilidades, quality-reviewer checa SOLID e clean code, test-reviewer avalia cobertura e edge cases. Eles rodam ao mesmo tempo — paralelo de verdade."

> **Cena 3 — Consolidacao (30s)**
> "Quando os 3 terminam, a skill consolida tudo em um unico report com secoes de seguranca, qualidade e testes. O humano recebe uma analise completa em um so lugar."

> **Cena 4 — Demonstracao (1min)**
> "Vou rodar /review-pr num PR real. Observem os 3 subagentes trabalhando simultaneamente e o report final consolidado."

---

## Conceitos: Skills vs Agents vs Subagents

| Conceito | O que e | Exemplo |
|----------|---------|---------|
| **Agent** | Persona com instrucoes e tools definidos em `.claude/agents/` | `developer.md`, `security-reviewer.md` |
| **Skill** | Comando customizado com fluxo pre-definido em `.claude/skills/` | `/review-pr`, `/implement-task` |
| **Subagent** | Agente lancado dentro de uma skill/agent usando a tool `Task` | Security reviewer rodando dentro de /review-pr |
| **Agent Teams** | Multiplos agentes trabalhando em paralelo na mesma sessao | 3 developers em tasks diferentes |

A skill `/review-pr` usa 3 **agents** como **subagents** dentro de um fluxo orquestrado.

---

## Conteudo Completo da Skill

### `.claude/skills/review-pr/SKILL.md`

```markdown
---
name: review-pr
description: Executa review paralelo do PR atual usando 3 subagentes especializados (segurança, qualidade, testes). Consolida em um único report.
argument-hint: "[branch-name or PR-number (optional)]"
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Skill: Review de PR Paralelo

Execute um review completo do Pull Request atual usando 3 subagentes especializados em paralelo.

## Argumentos

Argumento opcional: $ARGUMENTS
- Se fornecido, usar como referência do PR (branch ou número)
- Se vazio, analisar os arquivos modificados no último commit ou working tree

## Passo 1 — Identificar Arquivos Modificados

Primeiro, identifique os arquivos que precisam ser revisados:

```bash
# Se estiver em uma branch de PR, comparar com main
git diff --name-only main...HEAD

# Ou se quiser o diff completo
git diff main...HEAD
```

Se nenhum argumento foi passado, use o diff do working tree:
```bash
git diff --name-only HEAD
```

## Passo 2 — Lançar 3 Subagentes em Paralelo

Lance EXATAMENTE 3 subagentes usando a tool `Task`, TODOS EM PARALELO (na mesma mensagem):

### Subagente 1: Security Reviewer
- **agent**: security-reviewer
- **prompt**: Analise os seguintes arquivos modificados neste PR focando em segurança (OWASP Top 10, injection, auth, data exposure, access control). Arquivos: [lista dos arquivos]. Leia cada arquivo e produza um report de segurança.

### Subagente 2: Quality Reviewer
- **agent**: quality-reviewer
- **prompt**: Analise os seguintes arquivos modificados neste PR focando em qualidade de código (SOLID, clean code, type hints, arquitetura, DRY). Arquivos: [lista dos arquivos]. Leia cada arquivo e produza um report de qualidade.

### Subagente 3: Test Reviewer
- **agent**: test-reviewer
- **prompt**: Analise os seguintes arquivos de teste neste PR focando em cobertura, edge cases, assertions e boas práticas. Arquivos: [lista dos arquivos de teste]. Leia cada arquivo e produza um report de testes.

**IMPORTANTE**: Lance os 3 subagentes em UMA ÚNICA mensagem com 3 tool calls paralelos.

## Passo 3 — Consolidar Reports

Após os 3 subagentes retornarem, consolide os resultados em um único report com o seguinte formato:

```markdown
# 📋 Review Consolidado do PR

## 🔒 Segurança
[Resumo do report do security-reviewer]
- Vulnerabilidades encontradas (se houver)
- Boas práticas confirmadas

## 📐 Qualidade de Código
[Resumo do report do quality-reviewer]
- Problemas de qualidade (se houver)
- Pontos positivos

## 🧪 Testes
[Resumo do report do test-reviewer]
- Gaps de cobertura (se houver)
- Qualidade das assertions

## Veredicto Final
- ✅ **Aprovado** — Nenhum problema crítico encontrado
- ⚠️ **Aprovado com ressalvas** — Problemas menores a resolver
- ❌ **Precisa de ajustes** — Problemas críticos encontrados

### Ações Sugeridas
1. [Ação mais importante]
2. [Segunda ação]
3. [Terceira ação]
```

## Notas
- Os subagentes são READ-ONLY — eles apenas leem e analisam
- Cada subagente tem acesso apenas a Read, Glob e Grep
- O review foca nos arquivos MODIFICADOS, não no projeto inteiro
- Se não houver arquivos de teste, o test-reviewer analisa se testes deveriam ter sido criados
```

---

## Script / Comandos

### 1. Criar o arquivo da skill

```bash
cd ~/Developer/projetos/poc-claude

# Garantir que o diretório existe
mkdir -p .claude/skills/review-pr

# Criar a skill
cat > .claude/skills/review-pr/SKILL.md << 'SKILL_EOF'
---
name: review-pr
description: Executa review paralelo do PR atual usando 3 subagentes especializados (segurança, qualidade, testes). Consolida em um único report.
argument-hint: "[branch-name or PR-number (optional)]"
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Skill: Review de PR Paralelo

Execute um review completo do Pull Request atual usando 3 subagentes especializados em paralelo.

## Argumentos

Argumento opcional: $ARGUMENTS
- Se fornecido, usar como referência do PR (branch ou número)
- Se vazio, analisar os arquivos modificados no último commit ou working tree

## Passo 1 — Identificar Arquivos Modificados

Identifique os arquivos modificados:

```bash
# Comparar branch atual com main
git diff --name-only main...HEAD 2>/dev/null || git diff --name-only HEAD
```

## Passo 2 — Lançar 3 Subagentes em Paralelo

Lance EXATAMENTE 3 subagentes usando a tool Task, TODOS EM PARALELO:

### Subagente 1: Security Reviewer
- **agent**: security-reviewer
- **prompt**: Analise os arquivos modificados neste PR focando em segurança (OWASP Top 10). Arquivos: [lista]. Produza report de segurança.

### Subagente 2: Quality Reviewer
- **agent**: quality-reviewer
- **prompt**: Analise os arquivos modificados focando em qualidade (SOLID, clean code, types). Arquivos: [lista]. Produza report de qualidade.

### Subagente 3: Test Reviewer
- **agent**: test-reviewer
- **prompt**: Analise os arquivos de teste focando em cobertura, edge cases e assertions. Arquivos: [lista]. Produza report de testes.

**IMPORTANTE**: Lance os 3 em UMA ÚNICA mensagem com 3 tool calls paralelos.

## Passo 3 — Consolidar

Consolide em report único com seções: Segurança, Qualidade, Testes, Veredicto Final e Ações Sugeridas.
SKILL_EOF

echo "✓ Skill review-pr criada"
cat .claude/skills/review-pr/SKILL.md
```

### 2. Commit e push

```bash
cd ~/Developer/projetos/poc-claude

git add .claude/skills/review-pr/SKILL.md
git commit -m "feat: add /review-pr skill with parallel subagent review

- Launches 3 subagents in parallel: security, quality, test
- Each subagent is read-only (analyzes without modifying)
- Consolidates into a single review report"

git push origin main
```

### 3. Testar a skill (apos ter PRs)

```bash
# No Claude Code, dentro do repo poc-claude:
# /review-pr

# Ou com argumento:
# /review-pr feat/task-01-models
```

---

## Como a Skill Funciona (Diagrama)

```
Humano digita: /review-pr
        │
        ▼
┌─────────────────┐
│   SKILL.md      │
│  (orquestrador) │
└────────┬────────┘
         │
         ├──────────────────┬──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Security   │   │  Quality    │   │    Test     │
│  Reviewer   │   │  Reviewer   │   │  Reviewer   │
│ (read-only) │   │ (read-only) │   │ (read-only) │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       │    ┌────────────┘                 │
       │    │    ┌─────────────────────────┘
       ▼    ▼    ▼
┌─────────────────┐
│  Consolidação   │
│  Report Final   │
└─────────────────┘
```

---

## Checklist de Verificacao

- [ ] Arquivo `.claude/skills/review-pr/SKILL.md` criado
- [ ] Skill tem YAML front matter com name, description, allowed-tools
- [ ] allowed-tools inclui `Task` (necessario para subagentes)
- [ ] Instrucoes mencionam lancamento de 3 subagentes em paralelo
- [ ] Cada subagente referencia o agent correto (security-reviewer, quality-reviewer, test-reviewer)
- [ ] Template de consolidacao inclui secoes de seguranca, qualidade e testes
- [ ] Commit feito e push realizado

---

## Proximo Passo

Siga para **Etapa 06** — Habilitar Agent Teams.
