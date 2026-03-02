---
name: review-pr
description: Executa review paralelo do PR usando 3 subagentes locais. Cada reviewer posta comentario diretamente no PR via gh CLI.
argument-hint: "<PR-number>"
allowed-tools: Read, Glob, Grep, Bash, Agent
---

# Skill: Review de PR Local

Execute review completo de um PR usando 3 subagentes especializados em paralelo.
Cada reviewer posta seu comentario diretamente no PR via `gh pr comment`.

## Argumentos

Numero do PR: $ARGUMENTS
- Se nao fornecido, usar o PR mais recente: `gh pr list --limit 1 --json number -q '.[0].number'`

## Passo 1 — Identificar PR e Arquivos

```bash
PR_NUMBER=$ARGUMENTS

# Ver detalhes do PR
gh pr view $PR_NUMBER

# Listar arquivos modificados
gh pr diff $PR_NUMBER --name-only
```

## Passo 2 — Lancar 3 Reviewers em Paralelo

Lance EXATAMENTE 3 subagentes usando a tool Agent, TODOS EM PARALELO:

### Subagente 1: Security Reviewer
- **agent**: security-reviewer
- **prompt**: Revise o PR #[PR_NUMBER] focando em seguranca OWASP.
  1. Leia o diff com `gh pr diff [PR_NUMBER]`
  2. Leia os arquivos modificados para contexto
  3. Analise vulnerabilidades
  4. Poste seu review com `gh pr comment [PR_NUMBER] --body "..."`
  5. Retorne: aprovado/reprovado + resumo das findings

### Subagente 2: Quality Reviewer
- **agent**: quality-reviewer
- **prompt**: Revise o PR #[PR_NUMBER] focando em qualidade (SOLID, types, clean code).
  1. Leia o diff com `gh pr diff [PR_NUMBER]`
  2. Analise qualidade
  3. Poste seu review com `gh pr comment [PR_NUMBER] --body "..."`
  4. Retorne: aprovado/reprovado + resumo

### Subagente 3: Test Reviewer
- **agent**: test-reviewer
- **prompt**: Revise o PR #[PR_NUMBER] focando em testes (cobertura, edge cases).
  1. Leia o diff com `gh pr diff [PR_NUMBER]`
  2. Analise testes
  3. Poste seu review com `gh pr comment [PR_NUMBER] --body "..."`
  4. Retorne: aprovado/reprovado + resumo

## Passo 3 — Consolidar e Informar

Apos os 3 reviewers terminarem:

1. Consolide os resultados
2. Poste um comentario FINAL consolidado no PR:

```bash
gh pr comment $PR_NUMBER --body "$(cat <<'EOF'
# Review Consolidado

## Seguranca
[resumo do security-reviewer]

## Qualidade
[resumo do quality-reviewer]

## Testes
[resumo do test-reviewer]

## Veredicto Final
- Aprovado / Ressalvas / Precisa de ajustes

### Acoes Sugeridas
1. ...
2. ...
EOF
)"
```

3. Informe o Lead com o veredicto

## Notas
- Tudo roda LOCALMENTE — nao depende de GitHub Actions
- Cada reviewer posta seu proprio comentario no PR
- O Lead posta o consolidado final
- Se houver problemas CRITICOS, o Lead deve notificar o teammate para corrigir ANTES de informar o humano
