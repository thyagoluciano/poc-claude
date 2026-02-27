---
name: review-pr
description: Executa review multi-perspectiva de um PR. Lança 3 agentes em paralelo (security, quality, tests) que analisam o diff do PR de suas respectivas perspectivas.
argument-hint: "[PR number or 'current']"
allowed-tools: Read, Grep, Glob, Bash, Task
---

# Review Multi-Perspectiva de PR

Execute um review completo do PR atual ou especificado, lançando 3 agentes especializados em paralelo.

## Argumentos
$ARGUMENTS

## Instruções

1. Identifique o PR a ser revisado:
   - Se argumento é um número: use `gh pr view $1 --json files,body,title`
   - Se argumento é 'current' ou vazio: use `gh pr view --json files,body,title`

2. Obtenha o diff do PR:
   ```bash
   gh pr diff $PR_NUMBER
   ```

3. Lance 3 subagentes em PARALELO (Task tool com subagent_type "general-purpose"), cada um recebendo o diff e analisando de sua perspectiva:

   **Subagente 1 — Security Review**:
   Analise o diff focando em: SQL injection, auth bypass, secrets exposure, XSS, CORS, JWT security, input validation, error handling.
   Output: comentário com findings categorizados (🔴 Crítico, 🟡 Atenção, 🟢 OK) + score /10.

   **Subagente 2 — Quality Review**:
   Analise o diff focando em: SOLID, DRY, KISS, type hints, naming, docstrings, FastAPI/React patterns, error handling.
   Output: comentário com findings categorizados + score /10.

   **Subagente 3 — Test Review**:
   Analise o diff focando em: cobertura, happy path, edge cases, error cases, fixtures, assertions, naming, isolation.
   Output: comentário com findings categorizados + cobertura estimada + score /10.

4. Consolide os 3 reviews em um único comentário:
   ```bash
   gh pr comment $PR_NUMBER --body "CONSOLIDATED_REVIEW"
   ```

## Formato do Comentário Final

```markdown
# 🔍 Review Automático — Squad Híbrida

## 🔒 Security Review (Score: X/10)
[Resumo do security review]

## ✨ Quality Review (Score: X/10)
[Resumo do quality review]

## 🧪 Test Review (Score: X/10 | Cobertura: Y%)
[Resumo do test review]

---
**Score Geral: X/10**
*Review realizado por 3 agentes especializados em paralelo*
```
