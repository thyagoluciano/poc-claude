# Slide 05 — Ciclo de Vida Autônomo

## Metadata

| Campo     | Valor                        |
|-----------|------------------------------|
| Slide ID  | `slide-poc-lifecycle`        |
| Title     | Ciclo de Vida Autônomo       |
| Badge     | POC Zup — Ciclo              |
| Position  | Após `slide-poc-agents`, antes de `slide-roadmap` |

---

## HTML

Adicionar este bloco após `</div><!-- fim slide-poc-agents -->` e antes de `<!-- Roadmap -->`:

```html
<!-- POC Lifecycle -->
<div class="slide" id="slide-poc-lifecycle">
  <div class="slide-content">
    <span class="badge">POC Zup — Ciclo</span>
    <h2>Ciclo de Vida Autônomo</h2>
    <div class="divider"></div>

    <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.08); text-align: center;">
      <pre class="mermaid">
stateDiagram-v2
  [*] --> READY: Dependências satisfeitas
  READY --> IN_PROGRESS: Agent pega task
  IN_PROGRESS --> PR_OPEN: Commit + Push + PR
  PR_OPEN --> REVIEW: GitHub Action dispara
  REVIEW --> APPROVED: 3 Reviews passam
  APPROVED --> MERGED: 👤 Human merge
  MERGED --> COMPLETED: Branch merged
  COMPLETED --> [*]: Recalcula deps → novas tasks READY
      </pre>
    </div>

    <div class="two-cols" style="margin-top: 24px;">
      <div style="background: rgba(78, 205, 196, 0.08); border: 2px solid var(--cyan); border-radius: 16px; padding: 20px;">
        <h3 style="color: var(--cyan); font-size: 1.1rem; margin-bottom: 8px;">🤖 Autônomo</h3>
        <p style="font-size: 0.9rem; color: var(--white-soft); margin-bottom: 8px;">READY → IN_PROGRESS → PR_OPEN → REVIEW → APPROVED</p>
        <p style="font-size: 0.95rem; color: var(--cyan-light); font-weight: 500;">100% automático, sem intervenção humana</p>
      </div>
      <div style="background: rgba(212, 168, 67, 0.08); border: 2px solid var(--gold); border-radius: 16px; padding: 20px;">
        <h3 style="color: var(--gold); font-size: 1.1rem; margin-bottom: 8px;">👤 Human Gate</h3>
        <p style="font-size: 0.9rem; color: var(--white-soft); margin-bottom: 8px;">APPROVED → MERGED</p>
        <p style="font-size: 0.95rem; color: var(--gold-light); font-weight: 500;">Único ponto de decisão humana</p>
      </div>
    </div>

    <div class="quote" style="margin-top: 20px; font-size: 1rem; text-align: center; border-left: none; border-top: 2px solid var(--gold); border-radius: 12px; padding: 16px;">
      O agente só para quando <strong>NÃO há tasks READY</strong> — todas bloqueadas por dependências aguardando merge
    </div>
  </div>
</div>
```

---

## slideNotes

Adicionar ao objeto `slideNotes` no JavaScript:

```javascript
'slide-poc-lifecycle': {
  duration: '2 min',
  roteiro: 'Caminhe pelo diagrama de estados, estado por estado. Uma task nasce como TODO no backlog. Quando suas dependências são satisfeitas (mergeadas), ela vira READY. O Agent Teams detecta tasks READY e atribui ao agente dev apropriado — a task vira IN_PROGRESS. O agente implementa, testa, commita, faz push e abre PR — vira PR_OPEN. O GitHub Actions dispara os 3 reviewers automaticamente — vira REVIEW. Quando os 3 aprovam, a task fica APPROVED. O humano revisa e faz merge — vira MERGED. O merge recalcula dependências e novas tasks podem ficar READY. O ciclo continua até todas serem COMPLETED.',
  dicas: [
    { icon: '🤖', text: '<strong>Autônomo:</strong> "De READY a APPROVED é 100% automático. Nenhuma intervenção humana. O agente pega a task, implementa, testa, abre PR e recebe 3 reviews."' },
    { icon: '👤', text: '<strong>Human Gate:</strong> "O humano só aparece em um ponto: APPROVED → MERGED. Ele vê o código, vê os 3 reviews, e decide: merge ou pede mudanças."' },
    { icon: '🔄', text: '<strong>Cascata:</strong> "O merge de uma task pode liberar outras. Ex: merge de Task 01 (Schemas) libera Task 03 (CRUD) e Task 04 (Auth)."' },
    { icon: '⏸️', text: '<strong>Quando para:</strong> "O agente não fica ocioso esperando. Se não há task READY, ele para. O humano faz merge, novas tasks ficam READY, e o agente retoma."' },
    { icon: '📝', text: '<strong>Observação:</strong> "Se um reviewer rejeita, o dev agent recebe o feedback e corrige automaticamente. O ciclo de review pode iterar."' }
  ]
},
```

---

## Referências

Nenhuma referência adicional para este slide.
