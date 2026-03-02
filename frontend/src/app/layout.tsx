'use client';

import {ThemeContextProvider, MainNavigationBar, ResponsiveLayout} from '@telefonica/mistica';
import {misticaTheme} from '@/lib/theme';
import {useRouter, usePathname} from 'next/navigation';

const sections = [
  {title: 'Home', href: '/'},
  {title: 'Tasks', href: '/tasks'},
  {title: 'Dashboard', href: '/dashboard'},
];

function getSelectedIndex(pathname: string): number {
  if (pathname === '/') return 0;
  if (pathname.startsWith('/tasks')) return 1;
  if (pathname.startsWith('/dashboard')) return 2;
  return -1;
}

function AppLayout({children}: {children: React.ReactNode}) {
  const router = useRouter();
  const pathname = usePathname();

  return (
    <html lang="pt-BR">
      <body style={{margin: 0}}>
        <ThemeContextProvider theme={misticaTheme}>
          <MainNavigationBar
            sections={sections.map((section) => ({
              title: section.title,
              onPress: () => router.push(section.href),
            }))}
            selectedIndex={getSelectedIndex(pathname)}
          />
          <ResponsiveLayout>
            <main style={{paddingTop: 24, paddingBottom: 48}}>
              {children}
            </main>
          </ResponsiveLayout>
        </ThemeContextProvider>
      </body>
    </html>
  );
}

export default AppLayout;
