# 07 — Troubleshooting

Problemas comuns e como resolver durante a execucao da PoC.

---

## 7.1 Teammate travou ou parou de responder

**Sintoma:** Um teammate nao envia mensagens ha mais de 5 minutos.

**Solucao:** Envie uma mensagem direta ao teammate:
```
Qual o status da task que voce esta trabalhando?
Se esta travado, descreva o problema.
```

Se nao responder, o Lead pode:
1. Verificar se o teammate ainda esta ativo
2. Criar um novo teammate para continuar a task
3. A branch e o PR parcial continuam existindo no GitHub

---

## 7.2 Conflito de merge entre branches

**Sintoma:** Um PR mostra conflitos com a branch main.

**Solucao:** O Lead pede ao teammate:
```
O PR da task-XX tem conflitos com main. Faca:
1. git fetch origin
2. git rebase origin/main
3. Resolva os conflitos mantendo ambas as mudancas
4. git push --force-with-lease
```

**Prevencao:** As tasks foram projetadas para tocar em arquivos diferentes.
Conflitos devem ser raros na Wave 1-3. Waves 4-5 podem ter conflitos em
`app.py` (registrar novos routers) ou `layout.tsx` (adicionar providers).

---

## 7.3 Testes falhando

**Sintoma:** pytest ou npm run build falha.

**Solucao para backend:**
```
Os testes estao falhando na task-XX. Rode:
cd backend && python -m pytest tests/ -v --tb=long
Leia o output, identifique o problema e corrija.
```

**Solucao para frontend:**
```
O build esta falhando. Rode:
cd frontend && npm run build
Leia os erros TypeScript e corrija. Lembre: strict mode, sem any.
```

---

## 7.4 Mistica nao encontra componente

**Sintoma:** `Module not found: Can't resolve '@telefonica/mistica'`

**Solucao:**
```bash
cd frontend
npm install @telefonica/mistica
```

**Se o erro for de um componente especifico:**
Verifique se o import esta correto. Todos os componentes sao exportados do index:
```tsx
import {ButtonPrimary, Stack, TextField} from '@telefonica/mistica';
```

NAO fazer:
```tsx
import {ButtonPrimary} from '@telefonica/mistica/dist/ButtonPrimary'; // ERRADO
```

---

## 7.5 Mistica ThemeContextProvider faltando

**Sintoma:** Erro "ThemeContext not found" ou "useTheme must be used within ThemeContextProvider"

**Solucao:** Garantir que o root layout.tsx tem:
```tsx
import {ThemeContextProvider, getMovistarSkin} from '@telefonica/mistica';

const theme = {
  skin: getMovistarSkin(),
  i18n: {locale: 'pt-BR', phoneNumberFormattingRegionCode: 'BR'},
};

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="pt-BR">
      <body>
        <ThemeContextProvider theme={theme}>
          {children}
        </ThemeContextProvider>
      </body>
    </html>
  );
}
```

---

## 7.6 Sessao do Claude Code perdida

**Sintoma:** Terminal fechou, conexao caiu, ou precisa reiniciar.

**Impacto:** A equipe de teammates se perde. MAS:
- Commits ja feitos continuam nas branches
- PRs ja criados continuam abertos
- Issues e board mantem o estado

**Solucao:**
1. Verifique o estado atual:
```bash
gh pr list                        # PRs abertos
gh issue list --label "in-progress"  # Tasks em andamento
git branch -r                     # Branches remotas
```

2. Retome com o prompt de retomada (veja 04-prompt-lead.md secao 4.6)

---

## 7.7 Rate limiting da API Anthropic

**Sintoma:** Erros 429 ou "rate limited" durante a execucao.

**Solucao:**
- Reduzir para 2 teammates em vez de 3
- Usar modelo Sonnet para teammates (mais barato e rapido)
- Aguardar alguns minutos e retomar

---

## 7.8 Frontend nao conecta com backend

**Sintoma:** Erros CORS ou "Failed to fetch" no frontend.

**Solucao:**
1. Verificar que o backend esta rodando:
```bash
cd backend && uvicorn src.taskflow.app:app --reload
```

2. Verificar CORS no app.py:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Verificar NEXT_PUBLIC_API_URL no frontend:
```bash
# Se nao definido, default e http://localhost:8000
echo $NEXT_PUBLIC_API_URL
```

---

## 7.9 Teammate cria branch com nome errado

**Sintoma:** Branch nao segue o padrao `feat/task-{id}`.

**Solucao:** O Lead instrui o teammate:
```
A branch deveria ser feat/task-04. Renomeie:
git branch -m feat/task-04
git push -u origin feat/task-04
```

---

## 7.10 Review local nao detectou a vulnerabilidade da task-11

**Sintoma:** O security-reviewer postou "Aprovado" no PR da task-11.

**Solucao:** O Lead pode:
1. Lancar o security-reviewer novamente com prompt mais especifico:
```
Lance o security-reviewer com este prompt:
"Revise o PR #<N> com foco EXCLUSIVO em seguranca OWASP.
Verifique ESPECIFICAMENTE:
- O endpoint /search/tasks requer autenticacao?
- Dados sensiveis (email) sao retornados?
- Qualquer usuario pode ver tasks de outros usuarios?
Poste seu review via gh pr comment <N>."
```

2. Ou pedir ao Snyk (se configurado):
```
Rode snyk_code_scan no backend/src/taskflow/search_router.py
```

3. Em ultimo caso, o humano recusa o merge e comenta no PR:
```bash
gh pr comment <N> --body "REJEITADO: O endpoint /search/tasks expoe email sem autenticacao. Corrija antes do merge."
```

---

## 7.11 Custo de API alto

**Estimativa de custo por wave:**

| Item | Tokens aprox. | Custo (Sonnet) |
|------|--------------|----------------|
| Lead (orquestrador) | ~50k por wave | ~$0.50 |
| Teammate backend | ~100k por task | ~$1.00 |
| Teammate frontend | ~150k por task | ~$1.50 |
| Review (3 agents) | ~50k por PR | ~$0.50 |
| **Total por wave** | **~350-500k** | **~$3-5** |
| **Total 5 waves** | **~2M tokens** | **~$15-25** |

**Dicas para reduzir custo:**
- Usar Sonnet (4x mais barato que Opus)
- Reduzir para 2 teammates
- Nao rodar review em tasks triviais (Wave 1)

---

## 7.12 Checklist de Problemas Rapidos

| Problema | Comando |
|----------|---------|
| Ver PRs | `gh pr list` |
| Ver issues | `gh issue list` |
| Ver branches | `git fetch && git branch -r` |
| Merge PR | `gh pr merge <N> --merge` |
| Fechar issue | `gh issue close <N>` |
| Ver logs do PR | `gh pr view <N> --comments` |
| Status do board | `gh project item-list <N> --owner <USER>` |

---

Voltar ao [Indice](./00-INDICE.md)
