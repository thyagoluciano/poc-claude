'use client';

import {useEffect, useState} from 'react';
import {
  Boxed,
  ButtonPrimary,
  Callout,
  Form,
  PasswordField,
  ResponsiveLayout,
  Stack,
  TextField,
  TextLink,
  Title1,
} from '@telefonica/mistica';
import {useRouter} from 'next/navigation';
import {useAuth} from '@/lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const {login, isAuthenticated, loading} = useAuth();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/');
    }
  }, [loading, isAuthenticated, router]);

  const handleSubmit = async (values: Record<string, unknown>) => {
    setError(null);
    try {
      await login(values['username'] as string, values['password'] as string);
      router.push('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao fazer login');
    }
  };

  if (loading) {
    return null;
  }

  return (
    <ResponsiveLayout>
      <Stack space={24}>
        <Title1>Login</Title1>
        <Boxed>
          <Stack space={16}>
            {error && (
              <Callout
                title="Erro"
                description={error}
                onClose={() => setError(null)}
              />
            )}
            <Form onSubmit={handleSubmit}>
              <Stack space={16}>
                <TextField name="username" label="Username" />
                <PasswordField name="password" label="Senha" />
                <ButtonPrimary submit>Entrar</ButtonPrimary>
              </Stack>
            </Form>
            <TextLink onPress={() => router.push('/register')}>
              Nao tem conta? Registre-se
            </TextLink>
          </Stack>
        </Boxed>
      </Stack>
    </ResponsiveLayout>
  );
}
