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

Consolide os resultados em um único report:

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
