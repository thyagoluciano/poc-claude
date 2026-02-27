# Slide 06 — Demo & Resultados Esperados

## Metadata

| Campo     | Valor                        |
|-----------|------------------------------|
| Slide ID  | `slide-poc-demo`             |
| Title     | Demo & Resultados Esperados  |
| Badge     | POC Zup — Demo               |
| Position  | Após `slide-poc-lifecycle`, antes de `slide-roadmap` |

---

## HTML

Adicionar este bloco após `</div><!-- fim slide-poc-lifecycle -->` e antes de `<!-- Roadmap -->`:

```html
<!-- POC Demo -->
<div class="slide" id="slide-poc-demo">
  <div class="slide-content">
    <span class="badge">POC Zup — Demo</span>
    <h2>Demo & Resultados Esperados</h2>
    <div class="divider"></div>

    <div class="two-cols">
      <!-- Left column: Checklist -->
      <div>
        <h3 style="color: var(--gold-light); font-size: 1.1rem; margin-bottom: 16px;">O que será demonstrado</h3>
        <ul class="bullet-list">
          <li><span class="accent">✅</span> GitHub Project Board com 10 tasks</li>
          <li><span class="accent">✅</span> Agent Teams construindo em paralelo (3 agentes Wave 1)</li>
          <li><span class="accent">✅</span> PRs com review automático multi-perspectiva</li>
          <li><span class="accent">✅</span> Human merge como gate de qualidade</li>
          <li><span class="accent">✅</span> Retomada automática após merge</li>
          <li><span class="accent">✅</span> Backend API + Frontend UI funcionando</li>
        </ul>
      </div>

      <!-- Right column: Stats -->
      <div>
        <h3 style="color: var(--gold-light); font-size: 1.1rem; margin-bottom: 16px;">Métricas Esperadas</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div class="stat">
            <div class="stat-value">10</div>
            <div class="stat-label">Tasks completadas</div>
          </div>
          <div class="stat">
            <div class="stat-value">5</div>
            <div class="stat-label">Waves paralelas</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="font-size: 1.8rem;">~30-45min</div>
            <div class="stat-label">Tempo total</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="font-size: 1.8rem;">$5-15</div>
            <div class="stat-label">Custo API</div>
          </div>
          <div class="stat">
            <div class="stat-value">30</div>
            <div class="stat-label">Reviews automáticos</div>
          </div>
          <div class="stat">
            <div class="stat-value">100%</div>
            <div class="stat-label">Autonomia até merge</div>
          </div>
        </div>
      </div>
    </div>

    <div style="margin-top: 24px; background: linear-gradient(135deg, rgba(78, 205, 196, 0.1), rgba(212, 168, 67, 0.1)); border: 1px solid rgba(212, 168, 67, 0.3); border-radius: 16px; padding: 16px 24px; text-align: center;">
      <p style="font-size: 1.05rem; color: var(--white); font-weight: 500;">
        TaskFlow API rodando em localhost — Backend <span class="accent">/docs</span> + Frontend <span class="highlight">/</span>
      </p>
    </div>
  </div>
</div>
```

---

## slideNotes

Adicionar ao objeto `slideNotes` no JavaScript:

```javascript
'slide-poc-demo': {
  duration: '2 min',
  roteiro: 'Este slide prepara a audiência para a demo ao vivo (ou gravada). Apresente o que será demonstrado — cada item do checklist. Depois mostre as métricas esperadas: 10 tasks em 5 waves, estimativa de 30-45 minutos, custo entre $5-15 em API, 30 reviews automáticos (3 por PR vezes 10 PRs), e 100% de autonomia até o ponto de merge. O resultado final é uma aplicação rodando em localhost com o backend servindo a API em /docs (Swagger) e o frontend em /.',
  dicas: [
    { icon: '🎬', text: '<strong>Demo prep:</strong> "Vou mostrar tudo isso ao vivo. O board no GitHub, os agentes trabalhando, os PRs sendo criados e revisados, e o merge manual."' },
    { icon: '⏱️', text: '<strong>Tempo:</strong> "O tempo total estimado é 30-45 minutos para as 10 tasks. Na demo, vamos acelerar mostrando os momentos-chave."' },
    { icon: '💰', text: '<strong>Custo:</strong> "O custo em API é entre $5-15 para construir uma aplicação completa. Compare com horas de desenvolvimento humano."' },
    { icon: '📊', text: '<strong>Reviews:</strong> "30 reviews automáticos — 3 perspectivas diferentes para cada PR. Segurança, qualidade e testes. Em um time humano, quantas vezes conseguimos 3 reviews por PR?"' },
    { icon: '🖥️', text: '<strong>Resultado:</strong> "No final, teremos uma TaskFlow API funcionando. Backend com Swagger em /docs, frontend com Next.js na raiz. Tudo construído por agentes."' }
  ]
},
```

---

## Referências

Nenhuma referência adicional para este slide.
