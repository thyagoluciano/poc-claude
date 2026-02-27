# Slide 03 — Arquitetura da Squad

## Metadata

| Campo     | Valor                        |
|-----------|------------------------------|
| Slide ID  | `slide-poc-architecture`     |
| Title     | Arquitetura da Squad         |
| Badge     | POC Zup — Arquitetura        |
| Position  | Após `slide-poc-dag`, antes de `slide-roadmap` |

---

## HTML

Adicionar este bloco após `</div><!-- fim slide-poc-dag -->` e antes de `<!-- Roadmap -->`:

```html
<!-- POC Architecture -->
<div class="slide" id="slide-poc-architecture">
  <div class="slide-content">
    <span class="badge">POC Zup — Arquitetura</span>
    <h2>Arquitetura da Squad</h2>
    <div class="divider"></div>

    <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.08); text-align: center;">
      <pre class="mermaid">
graph TB
  subgraph "📋 GitHub Projects"
    Board["Task Board<br/>10 Tasks"]
  end
  subgraph "🤖 Agent Teams"
    TL["Team Leader<br/>Orquestrador"]
    A1["Agent Dev 1<br/>Backend Python"]
    A2["Agent Dev 2<br/>Frontend Next.js"]
  end
  subgraph "🔍 GitHub Actions"
    SR["Security<br/>Reviewer"]
    QR["Quality<br/>Reviewer"]
    TR["Test<br/>Reviewer"]
  end
  Human["👤 Human<br/>Merge Gate"]

  Board -->|"tasks READY"| TL
  TL -->|"distribui"| A1
  TL -->|"distribui"| A2
  A1 -->|"cria PR"| SR
  A1 -->|"cria PR"| QR
  A1 -->|"cria PR"| TR
  A2 -->|"cria PR"| SR
  A2 -->|"cria PR"| QR
  A2 -->|"cria PR"| TR
  SR -->|"✅"| Human
  QR -->|"✅"| Human
  TR -->|"✅"| Human
  Human -->|"merge"| Board
      </pre>
    </div>
  </div>
</div>
```

---

## slideNotes

Adicionar ao objeto `slideNotes` no JavaScript:

```javascript
'slide-poc-architecture': {
  duration: '3 min',
  roteiro: 'Caminhe pela arquitetura de cima para baixo. O GitHub Projects é o source of truth — contém as 10 tasks com status e dependências. O Agent Teams (Team Leader) consulta o board, identifica tasks READY e distribui para os agentes devs especializados. Cada dev trabalha em sua sessão isolada, cria branch, implementa, testa e abre PR. O PR dispara GitHub Actions que invoca 3 reviewers (@claude) em paralelo: segurança, qualidade e testes. Quando os 3 aprovam, o humano faz o merge. O merge atualiza o board e libera novas tasks.',
  dicas: [
    { icon: '📋', text: '<strong>GitHub Projects:</strong> "O board é o source of truth. Tasks com status: TODO, READY, IN_PROGRESS, REVIEW, DONE."' },
    { icon: '🤖', text: '<strong>Agent Teams:</strong> "O Team Leader é o orquestrador. Ele não codifica — só distribui tasks. Os devs são especializados por stack."' },
    { icon: '🔍', text: '<strong>GitHub Actions:</strong> "Quando um PR é aberto, o workflow dispara 3 reviews em paralelo com @claude. Cada reviewer tem um system prompt diferente."' },
    { icon: '👤', text: '<strong>Human Gate:</strong> "O humano só aparece aqui — no merge. Ele valida o PR, vê os reviews, e decide: merge ou request changes."' },
    { icon: '🔄', text: '<strong>Ciclo:</strong> "O merge fecha o ciclo. Atualiza o board, recalcula dependências, e novas tasks ficam READY. O loop continua."' }
  ]
},
```

---

## Referências

Nenhuma referência adicional para este slide.
