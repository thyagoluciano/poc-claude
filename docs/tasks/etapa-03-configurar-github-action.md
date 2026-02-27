# Etapa 03 — Configurar GitHub Action para Review com `@claude`

## O que faz

Cria o workflow do GitHub Actions que permite invocar o Claude Code diretamente nos Pull Requests. Quando alguem menciona `@claude` em um comentario de PR (ou quando um PR e aberto/sincronizado), o workflow executa o Claude Code Action que analisa o codigo, responde perguntas e pode ate sugerir correcoes.

## Por que

Esse e o ponto de conexao entre os agentes que escrevem codigo e o humano que revisa. Na squad hibrida, os agentes criam PRs e o humano usa `@claude` para pedir analises de seguranca, qualidade, testes — sem precisar rodar nada local. Isso demonstra o conceito de "review automatizado por IA" que e um dos pilares da POC.

## Roteiro (para gravacao)

> **Cena 1 — Contexto (30s)**
> "Agora vamos configurar a ponte entre os agentes e o fluxo de review. O GitHub Actions vai escutar por mencoes a @claude nos PRs e acionar o Claude Code automaticamente."

> **Cena 2 — O workflow YAML (1min)**
> "Esse workflow tem dois triggers: quando um PR e aberto ou sincronizado, e quando alguem comenta `@claude` em um PR. O primeiro trigger pode rodar uma analise automatica. O segundo permite interacao direta — como pedir uma analise de seguranca ou correcao de testes."

> **Cena 3 — Configurando o secret (30s)**
> "Precisamos configurar a API key da Anthropic como secret do repositorio. Isso permite que a Action autentique com a API do Claude."

> **Cena 4 — Testando (1min)**
> "Vou criar um PR de teste e comentar @claude com um pedido de review. Vejam como o Claude analisa o diff e responde diretamente no PR."

---

## Workflow YAML Completo

Criar o arquivo `.github/workflows/claude-review.yml`:

```yaml
name: Claude Code Review

on:
  # Trigger automático quando PR é aberto ou atualizado
  pull_request:
    types: [opened, synchronize]

  # Trigger manual via comentário @claude no PR
  issue_comment:
    types: [created]

  # Trigger por review comment (comentário inline no diff)
  pull_request_review_comment:
    types: [created]

jobs:
  claude-review:
    # Só roda se:
    # 1. É um evento de PR (opened/synchronize), OU
    # 2. É um comentário que menciona @claude em uma issue que é PR
    if: |
      github.event_name == 'pull_request' ||
      (github.event_name == 'issue_comment' &&
       github.event.issue.pull_request &&
       contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' &&
       contains(github.event.comment.body, '@claude'))

    runs-on: ubuntu-latest

    permissions:
      contents: read
      pull-requests: write
      issues: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Claude Code Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

          # Prompt padrão para PRs abertos/sincronizados (review automático)
          direct_prompt: |
            Analise este Pull Request de forma concisa:

            1. **Resumo**: O que este PR faz (1-2 frases)
            2. **Problemas**: Bugs, vulnerabilidades ou erros de lógica
            3. **Sugestões**: Melhorias de código (max 3)
            4. **Veredicto**: ✅ Aprovado | ⚠️ Precisa de ajustes | ❌ Precisa retrabalho

            Seja direto e objetivo. Foque em problemas reais, não em estilo.

          # Modelo a usar
          model: "claude-sonnet-4-20250514"

          # Timeout em segundos
          timeout_minutes: 10
```

---

## Script / Comandos

### 1. Criar o arquivo de workflow

```bash
cd ~/Developer/projetos/poc-claude

# Garantir que o diretório existe
mkdir -p .github/workflows

# Criar o workflow
cat > .github/workflows/claude-review.yml << 'WORKFLOW_EOF'
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

  issue_comment:
    types: [created]

  pull_request_review_comment:
    types: [created]

jobs:
  claude-review:
    if: |
      github.event_name == 'pull_request' ||
      (github.event_name == 'issue_comment' &&
       github.event.issue.pull_request &&
       contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' &&
       contains(github.event.comment.body, '@claude'))

    runs-on: ubuntu-latest

    permissions:
      contents: read
      pull-requests: write
      issues: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Claude Code Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          direct_prompt: |
            Analise este Pull Request de forma concisa:

            1. **Resumo**: O que este PR faz (1-2 frases)
            2. **Problemas**: Bugs, vulnerabilidades ou erros de lógica
            3. **Sugestões**: Melhorias de código (max 3)
            4. **Veredicto**: ✅ Aprovado | ⚠️ Precisa de ajustes | ❌ Precisa retrabalho

            Seja direto e objetivo. Foque em problemas reais, não em estilo.
          model: "claude-sonnet-4-20250514"
          timeout_minutes: 10
WORKFLOW_EOF
```

### 2. Configurar o Secret da API Key

```bash
# Opção 1: Definir via CLI (interativo — pede o valor)
gh secret set ANTHROPIC_API_KEY --repo thyagoluciano/poc-claude

# Opção 2: Definir via variável de ambiente
echo "$ANTHROPIC_API_KEY" | gh secret set ANTHROPIC_API_KEY --repo thyagoluciano/poc-claude

# Opção 3: Definir via arquivo
gh secret set ANTHROPIC_API_KEY --repo thyagoluciano/poc-claude < ~/.anthropic-key
```

### 3. Commit e push

```bash
cd ~/Developer/projetos/poc-claude

git add .github/workflows/claude-review.yml
git commit -m "ci: add GitHub Action for Claude Code PR review

- Triggers: PR open/sync + @claude mentions in comments
- Uses anthropics/claude-code-action@v1
- Automated review on PR open
- Interactive review via @claude comments"

git push origin main
```

### 4. Verificar que o workflow foi registrado

```bash
# Listar workflows do repositório
gh workflow list --repo thyagoluciano/poc-claude

# Ver detalhes do workflow
gh workflow view "Claude Code Review" --repo thyagoluciano/poc-claude
```

---

## Como Funciona na Pratica

### Trigger Automatico (PR aberto)

Quando um agente cria um PR, o workflow roda automaticamente e posta um comentario com a analise. O humano le o review e decide se faz merge.

### Trigger Manual (`@claude` no comentario)

O humano pode interagir diretamente com o Claude nos PRs. Exemplos de comentarios:

```
@claude analise este PR focando em segurança. Verifique:
- SQL injection
- Validação de input
- Exposição de dados sensíveis
```

```
@claude o teste test_auth.py está falhando. Analise o erro e sugira uma correção.
```

```
@claude resuma as mudanças deste PR para um desenvolvedor junior.
```

```
@claude verifique se este código segue os padrões definidos no CLAUDE.md.
```

```
@claude fix the failing test in test_repositories.py
```

### Trigger por Review Comment (comentario inline no diff)

O humano pode selecionar uma linha especifica do diff e comentar:

```
@claude esse trecho parece vulnerável a race condition. O que você acha?
```

---

## Permissoes Necessarias

O workflow precisa das seguintes permissoes (ja configuradas no YAML):

| Permissao | Motivo |
|-----------|--------|
| `contents: read` | Ler o codigo-fonte do repo |
| `pull-requests: write` | Postar comentarios no PR |
| `issues: write` | Responder a issue_comments |

Se o repositorio for privado, pode ser necessario configurar um `GITHUB_TOKEN` com permissoes adicionais.

---

## Troubleshooting

### Workflow nao aparece

- Verifique que o arquivo esta em `.github/workflows/` (com o ponto)
- Verifique que o YAML e valido: `python -c "import yaml; yaml.safe_load(open('.github/workflows/claude-review.yml'))"`
- O workflow so aparece apos ser pushado para a branch default (main)

### `@claude` nao responde

- Verifique que o secret `ANTHROPIC_API_KEY` esta configurado: `gh secret list --repo thyagoluciano/poc-claude`
- Verifique que o comentario esta em um PR (nao em issue comum)
- Verifique os logs do workflow: `gh run list --repo thyagoluciano/poc-claude`

### Erro de permissao

- Em repos novos, pode ser necessario habilitar "Allow GitHub Actions to create and approve pull requests" em Settings > Actions > General

---

## Checklist de Verificacao

- [ ] Arquivo `.github/workflows/claude-review.yml` criado e commitado
- [ ] Secret `ANTHROPIC_API_KEY` configurado no repo
- [ ] Workflow aparece em `gh workflow list`
- [ ] Testar: criar um PR de teste e verificar se o review automatico roda
- [ ] Testar: comentar `@claude` em um PR e verificar resposta

---

## Proximo Passo

Siga para **Etapa 04** — Configurar os Agents especializados.
