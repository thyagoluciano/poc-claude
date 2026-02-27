# Frontend Rules — TaskFlow UI

## Stack
- Next.js 14+, TypeScript strict, Tailwind CSS, App Router
- Estado: React Context API
- HTTP: Fetch API com wrapper em lib/api.ts

## Convenções
- TypeScript strict mode — nunca usar `any`
- Componentes funcionais com interfaces explícitas
- `'use client'` apenas quando necessário (interatividade)
- Tailwind puro — sem libs de UI externas (shadcn, MUI, etc)
- Cliente API centralizado em lib/api.ts
- Tratar loading states, error states e empty states

## Estrutura
```
frontend/
  src/
    app/
      layout.tsx          # Layout base com navbar
      page.tsx            # Home page
      login/page.tsx      # Login
      register/page.tsx   # Registro
      dashboard/page.tsx  # Dashboard com stats
      tasks/
        page.tsx          # Lista de tasks
        new/page.tsx      # Criar task
        [id]/edit/page.tsx # Editar task
    components/
      ProtectedRoute.tsx  # Wrapper de auth
      TaskCard.tsx        # Card de task
      StatusBadge.tsx     # Badge de status/prioridade
    lib/
      api.ts              # Cliente HTTP para a API
      auth.ts             # AuthContext e helpers
```
