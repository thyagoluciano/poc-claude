'use client';

import {
  Stack,
  Title1,
  Text2,
  ButtonPrimary,
  ButtonSecondary,
  ResponsiveLayout,
} from '@telefonica/mistica';
import {useRouter} from 'next/navigation';

export default function HomePage() {
  const router = useRouter();

  return (
    <ResponsiveLayout>
      <Stack space={24}>
        <Stack space={16}>
          <Title1>TaskFlow</Title1>
          <Text2 regular>
            Gerencie suas tarefas de forma simples e eficiente. Organize, priorize e acompanhe
            o progresso de tudo que precisa ser feito.
          </Text2>
        </Stack>
        <Stack space={16}>
          <ButtonPrimary onPress={() => router.push('/tasks')}>
            Ver Tasks
          </ButtonPrimary>
          <ButtonSecondary onPress={() => router.push('/dashboard')}>
            Dashboard
          </ButtonSecondary>
        </Stack>
      </Stack>
    </ResponsiveLayout>
  );
}
