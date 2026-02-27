# Slide 02 — Grafo de Dependências (DAG)

## Metadata

| Campo     | Valor                        |
|-----------|------------------------------|
| Slide ID  | `slide-poc-dag`              |
| Title     | Grafo de Dependências        |
| Badge     | POC Zup — Tasks              |
| Position  | Após `slide-poc-overview`, antes de `slide-roadmap` |

---

## HTML

Adicionar este bloco após `</div><!-- fim slide-poc-overview -->` e antes de `<!-- Roadmap -->`:

```html
<!-- POC DAG -->
<div class="slide" id="slide-poc-dag">
  <div class="slide-content">
    <span class="badge">POC Zup — Tasks</span>
    <h2>Grafo de Dependências</h2>
    <div class="divider"></div>

    <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.08); text-align: center;">
      <pre class="mermaid">
graph LR
  T1["<b>Task 01</b><br/>Schemas"] --> T3["<b>Task 03</b><br/>CRUD"]
  T2["<b>Task 02</b><br/>Database"] --> T3
  T1 --> T4["<b>Task 04</b><br/>Auth JWT"]
  T2 --> T4
  T3 --> T5["<b>Task 05</b><br/>API Endpoints"]
  T4 --> T5
  T5 --> T6["<b>Task 06</b><br/>Testes E2E"]
  T7["<b>Task 07</b><br/>Next.js Setup"] --> T8["<b>Task 08</b><br/>Auth UI"]
  T4 --> T8
  T7 --> T9["<b>Task 09</b><br/>Task UI"]
  T5 --> T9
  T8 --> T10["<b>Task 10</b><br/>Dashboard"]
  T9 --> T10

  style T1 fill:#4ECDC4,color:#000
  style T2 fill:#4ECDC4,color:#000
  style T7 fill:#4ECDC4,color:#000
  style T3 fill:#D4A843,color:#000
  style T4 fill:#D4A843,color:#000
  style T5 fill:#E8914F,color:#000
  style T8 fill:#E8914F,color:#000
  style T6 fill:#E8707A,color:#000
  style T9 fill:#E8707A,color:#000
  style T10 fill:#6B1D2A,color:#fff
      </pre>
    </div>

    <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 20px; justify-content: center;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: #4ECDC4;"></span>
        <span style="color: var(--white-soft); font-size: 0.9rem;"><strong style="color: var(--cyan);">Wave 1:</strong> T01 + T02 + T07 (3 em paralelo)</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: #D4A843;"></span>
        <span style="color: var(--white-soft); font-size: 0.9rem;"><strong style="color: var(--gold);">Wave 2:</strong> T03 + T04 (após merge Wave 1)</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: #E8914F;"></span>
        <span style="color: var(--white-soft); font-size: 0.9rem;"><strong style="color: var(--orange);">Wave 3:</strong> T05 + T08 (API + Auth UI)</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: #E8707A;"></span>
        <span style="color: var(--white-soft); font-size: 0.9rem;"><strong style="color: var(--red-light);">Wave 4:</strong> T06 + T09 (Testes + Task UI)</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: #6B1D2A; border: 1px solid rgba(255,255,255,0.3);"></span>
        <span style="color: var(--white-soft); font-size: 0.9rem;"><strong style="color: var(--white);">Wave 5:</strong> T10 (Integração Final)</span>
      </div>
    </div>
  </div>
</div>
```

---

## slideNotes

Adicionar ao objeto `slideNotes` no JavaScript:

```javascript
'slide-poc-dag': {
  duration: '2 min',
  roteiro: 'Mostre o grafo de dependências das 10 tasks. Explique que o grafo define a ordem de execução — tasks sem dependência rodam em paralelo. Destaque as 5 waves: a Wave 1 dispara 3 tasks simultâneas (2 backend + 1 frontend), e cada wave subsequente só começa quando suas dependências são mergeadas. Enfatize que o backend e o frontend avançam em paralelo quando possível.',
  dicas: [
    { icon: '🟢', text: '<strong>Wave 1:</strong> "3 tasks em paralelo — Schemas, Database e Next.js Setup. Sem dependências, os 3 agentes trabalham ao mesmo tempo."' },
    { icon: '🟡', text: '<strong>Wave 2:</strong> "CRUD e Auth JWT dependem de Schemas e Database. Só começam após o merge da Wave 1."' },
    { icon: '🟠', text: '<strong>Wave 3:</strong> "API Endpoints e Auth UI. O frontend já integra com o backend a partir daqui."' },
    { icon: '🔴', text: '<strong>Wave 4-5:</strong> "Testes E2E, Task UI e Dashboard. A integração final só roda quando tudo mais está pronto."' },
    { icon: '📊', text: '<strong>Paralelismo:</strong> "10 tasks, mas apenas 5 waves. Isso é ~50% de redução no tempo total comparado com execução sequencial."' }
  ]
},
```

---

## Referências

Nenhuma referência adicional para este slide.
