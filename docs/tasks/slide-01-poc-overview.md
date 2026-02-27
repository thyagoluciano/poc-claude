# Slide 01 — POC Overview

## Metadata

| Campo     | Valor                        |
|-----------|------------------------------|
| Slide ID  | `slide-poc-overview`         |
| Title     | POC: Squad Híbrida Autônoma  |
| Badge     | POC Zup                      |
| Position  | Após `slide-novas-pocs`, antes de `slide-roadmap` |

---

## HTML

Adicionar este bloco após `</div><!-- fim slide-novas-pocs -->` e antes de `<!-- Roadmap -->`:

```html
<!-- POC Overview -->
<div class="slide" id="slide-poc-overview">
  <div class="slide-content">
    <span class="badge">POC Zup</span>
    <h2>POC: Squad Híbrida Autônoma</h2>
    <div class="divider"></div>

    <div class="cards" style="grid-template-columns: repeat(2, 1fr);">
      <div class="card">
        <div class="card-icon">🚀</div>
        <h3>Produto</h3>
        <p>TaskFlow API — Backend FastAPI + Frontend Next.js, autenticação JWT, CRUD de tasks</p>
      </div>
      <div class="card">
        <div class="card-icon">🤖</div>
        <h3>Squad</h3>
        <p>2 Agent Devs (Backend + Frontend) + 3 Agent Reviewers + 1 Humano (merge gate)</p>
      </div>
      <div class="card">
        <div class="card-icon">🔗</div>
        <h3>Orquestração</h3>
        <p>Agent Teams — sessões independentes com comunicação peer-to-peer e task list compartilhada</p>
      </div>
      <div class="card">
        <div class="card-icon">📋</div>
        <h3>Board</h3>
        <p>GitHub Projects + GitHub Actions — <span class="accent">@claude</span> para review automático nos PRs</p>
      </div>
    </div>

    <div class="stats">
      <div class="stat">
        <div class="stat-value">10</div>
        <div class="stat-label">Tasks</div>
      </div>
      <div class="stat">
        <div class="stat-value">5</div>
        <div class="stat-label">Waves</div>
      </div>
      <div class="stat">
        <div class="stat-value">3</div>
        <div class="stat-label">Reviews por PR</div>
      </div>
      <div class="stat">
        <div class="stat-value">1</div>
        <div class="stat-label">Human Gate</div>
      </div>
    </div>
  </div>
</div>
```

---

## slideNotes

Adicionar ao objeto `slideNotes` no JavaScript:

```javascript
'slide-poc-overview': {
  duration: '2 min',
  roteiro: 'Apresente a POC como o próximo passo prático da apresentação. Explique que vamos construir um produto real — a TaskFlow API — usando uma squad 100% híbrida. O objetivo é demonstrar que agentes podem desenvolver software de ponta a ponta com supervisão mínima. A TaskFlow API foi escolhida porque é complexa o suficiente para ter dependências reais entre tasks, mas simples o bastante para ser construída em uma sessão.',
  dicas: [
    { icon: '🚀', text: '<strong>Produto:</strong> "Vamos construir uma API REST completa com frontend. Não é um hello world — tem autenticação, CRUD, testes e UI."' },
    { icon: '🤖', text: '<strong>Squad:</strong> "5 agentes especializados + 1 humano. Os agentes fazem tudo, o humano só aprova o merge."' },
    { icon: '🔗', text: '<strong>Orquestração:</strong> "Agent Teams do Claude Code — cada agente roda em sua própria sessão, comunicam entre si via task list."' },
    { icon: '📋', text: '<strong>Board:</strong> "GitHub Projects como source of truth. GitHub Actions dispara review automático com @claude em cada PR."' }
  ]
},
```

---

## Referências

Nenhuma referência adicional para este slide.
