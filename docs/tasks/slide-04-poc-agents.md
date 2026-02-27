# Slide 04 — Agentes Especializados

## Metadata

| Campo     | Valor                        |
|-----------|------------------------------|
| Slide ID  | `slide-poc-agents`           |
| Title     | Agentes Especializados       |
| Badge     | POC Zup — Agentes            |
| Position  | Após `slide-poc-architecture`, antes de `slide-roadmap` |

---

## HTML

Adicionar este bloco após `</div><!-- fim slide-poc-architecture -->` e antes de `<!-- Roadmap -->`:

```html
<!-- POC Agents -->
<div class="slide" id="slide-poc-agents">
  <div class="slide-content">
    <span class="badge">POC Zup — Agentes</span>
    <h2>Agentes Especializados</h2>
    <div class="divider"></div>

    <!-- Row 1: Developers -->
    <div class="cards" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 16px;">
      <div class="card" style="border-top: 3px solid var(--cyan);">
        <div class="card-icon">🐍</div>
        <h3>Backend Developer</h3>
        <p><span class="accent">Python, FastAPI, SQLAlchemy, Pydantic, pytest</span></p>
        <p style="margin-top: 8px; font-size: 0.85rem;">Tools: Read, Write, Edit, Bash</p>
        <p style="margin-top: 6px; font-style: italic; color: var(--gold-light); font-size: 0.9rem;">"Implementa, testa e faz commit autonomamente"</p>
      </div>
      <div class="card" style="border-top: 3px solid var(--cyan);">
        <div class="card-icon">⚛️</div>
        <h3>Frontend Developer</h3>
        <p><span class="accent">Next.js, React, TypeScript, Tailwind</span></p>
        <p style="margin-top: 8px; font-size: 0.85rem;">Tools: Read, Write, Edit, Bash</p>
        <p style="margin-top: 6px; font-style: italic; color: var(--gold-light); font-size: 0.9rem;">"Cria UI, integra com API e valida build"</p>
      </div>
    </div>

    <!-- Row 2: Reviewers -->
    <div class="cards" style="grid-template-columns: repeat(3, 1fr);">
      <div class="card" style="border-top: 3px solid var(--gold);">
        <div class="card-icon">🔒</div>
        <h3>Security Reviewer</h3>
        <p style="font-size: 0.85rem;">OWASP Top 10, SQL Injection, Auth bypass, Secrets, XSS</p>
        <p style="margin-top: 8px; font-size: 0.8rem; color: var(--white-soft);">Tools: <span class="highlight">Read-only</span></p>
        <p style="margin-top: 6px; font-style: italic; color: var(--gold-light); font-size: 0.85rem;">"Analisa vulnerabilidades no diff do PR"</p>
      </div>
      <div class="card" style="border-top: 3px solid var(--gold);">
        <div class="card-icon">✨</div>
        <h3>Quality Reviewer</h3>
        <p style="font-size: 0.85rem;">SOLID, DRY, Type hints, Clean Code, Naming</p>
        <p style="margin-top: 8px; font-size: 0.8rem; color: var(--white-soft);">Tools: <span class="highlight">Read-only</span></p>
        <p style="margin-top: 6px; font-style: italic; color: var(--gold-light); font-size: 0.85rem;">"Avalia qualidade e padrões de código"</p>
      </div>
      <div class="card" style="border-top: 3px solid var(--gold);">
        <div class="card-icon">🧪</div>
        <h3>Test Reviewer</h3>
        <p style="font-size: 0.85rem;">Cobertura, Edge cases, Fixtures, Assertions</p>
        <p style="margin-top: 8px; font-size: 0.8rem; color: var(--white-soft);">Tools: <span class="highlight">Read-only</span></p>
        <p style="margin-top: 6px; font-style: italic; color: var(--gold-light); font-size: 0.85rem;">"Verifica completude e qualidade dos testes"</p>
      </div>
    </div>

    <div class="quote" style="margin-top: 20px; font-size: 1rem;">
      Reviewers são <strong>read-only</strong> — analisam mas não modificam o código
    </div>
  </div>
</div>
```

---

## slideNotes

Adicionar ao objeto `slideNotes` no JavaScript:

```javascript
'slide-poc-agents': {
  duration: '2 min',
  roteiro: 'Apresente os 5 agentes da squad. Comece pelos 2 desenvolvedores — são agentes com acesso total (Read, Write, Edit, Bash). O Backend Dev é especialista em Python/FastAPI, o Frontend Dev em Next.js/React. Depois apresente os 3 reviewers — são agentes read-only que só analisam diffs de PR. Cada um tem uma perspectiva diferente: segurança, qualidade e testes. Enfatize que os reviewers não podem modificar código — isso garante separação de responsabilidades.',
  dicas: [
    { icon: '🐍', text: '<strong>Backend Dev:</strong> "Tem acesso total ao sistema. Cria arquivos, roda pytest, faz commit e push. É autônomo do início ao fim da task."' },
    { icon: '⚛️', text: '<strong>Frontend Dev:</strong> "Mesmo nível de autonomia, mas especializado em Next.js. Cria componentes, integra com API, valida o build."' },
    { icon: '🔒', text: '<strong>Security Reviewer:</strong> "Olha o diff do PR procurando vulnerabilidades: SQL injection, auth bypass, secrets hardcoded, XSS."' },
    { icon: '✨', text: '<strong>Quality Reviewer:</strong> "Avalia padrões de código: SOLID, DRY, naming, type hints. Garante que o código é maintainable."' },
    { icon: '🧪', text: '<strong>Test Reviewer:</strong> "Verifica se os testes são completos: edge cases, fixtures, assertions, cobertura."' },
    { icon: '🔑', text: '<strong>Read-only:</strong> "Reviewers são read-only por design. Não podem modificar código, só comentar. Isso evita conflitos e garante auditoria."' }
  ]
},
```

---

## Referências

Nenhuma referência adicional para este slide.
