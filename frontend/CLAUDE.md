# Frontend Rules — TaskFlow UI com Mistica

## Stack
- Next.js 14+, TypeScript strict, App Router
- UI: @telefonica/mistica (Mistica Design System da Telefonica)
- Estado: React Context API
- HTTP: Fetch API com wrapper em lib/api.ts

## Mistica Design System
- SEMPRE use componentes Mistica em vez de HTML puro ou Tailwind
- ThemeContextProvider obrigatorio no root layout com skin configurada
- Componentes principais:
  - Layout: ResponsiveLayout, Stack, Box, Boxed
  - Botoes: ButtonPrimary, ButtonSecondary, ButtonDanger, ButtonLink
  - Forms: Form, TextField, EmailField, PasswordField, Select
  - Cards: DataCard, SnapCard
  - Navegacao: NavigationBar, MainNavigationBar, Tabs
  - Feedback: Snackbar, FeedbackScreen, Tag, Badge
  - Tabelas: Table, RowList, Row
  - Tipografia: Text1-Text10, Title1-Title4
  - Progress: ProgressBar, Stepper
  - Outros: Divider, Spinner, Chip, Avatar, Callout, EmptyState

## Configuracao do Mistica

### lib/theme.ts — Configuracao centralizada do tema
```tsx
import {getMovistarSkin} from '@telefonica/mistica';
// Trocar por getVivoSkin() se for para Vivo

export const misticaTheme = {
  skin: getMovistarSkin(),
  i18n: {locale: 'pt-BR', phoneNumberFormattingRegionCode: 'BR'},
};
```

### layout.tsx — Importa o tema
```tsx
import {ThemeContextProvider} from '@telefonica/mistica';
import {misticaTheme} from '@/lib/theme';

// Envolver app com <ThemeContextProvider theme={misticaTheme}>
```

## next.config.ts
```ts
const nextConfig = {
  experimental: {
    optimizePackageImports: ['@telefonica/mistica'],
  },
};
```

## Convencoes
- TypeScript strict mode — nunca usar `any`
- Componentes funcionais com interfaces explicitas
- `'use client'` apenas quando necessario (interatividade)
- NAO usar Tailwind CSS — usar apenas componentes Mistica e CSS inline quando necessario
- Cliente API centralizado em lib/api.ts
- Tratar loading states, error states e empty states com componentes Mistica
- Para icones, usar os icones exportados pelo Mistica (Icon*)

## Estrutura
frontend/
  src/
    app/
      layout.tsx          # ThemeContextProvider + NavigationBar
      page.tsx            # Home page
      login/page.tsx      # Login com Mistica Form
      register/page.tsx   # Registro com Mistica Form
      dashboard/page.tsx  # Dashboard com DataCards e ProgressBar
      tasks/
        page.tsx          # Lista com RowList e filtros
        new/page.tsx      # Criar task com Mistica Form
        [id]/edit/page.tsx # Editar task
    components/
      ProtectedRoute.tsx  # Wrapper de auth
      TaskCard.tsx        # DataCard do Mistica
      StatusBadge.tsx     # Tag do Mistica
    lib/
      api.ts              # Cliente HTTP para a API
      auth.tsx            # AuthContext e helpers
      theme.ts            # Mistica theme config (skin + i18n)
