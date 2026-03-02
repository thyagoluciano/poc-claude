'use client';

import {useEffect, useState} from 'react';
import {
  Boxed,
  ButtonPrimary,
  Callout,
  EmailField,
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

export default function RegisterPage() {
  const router = useRouter();
  const {register, isAuthenticated, loading} = useAuth();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/');
    }
  }, [loading, isAuthenticated, router]);

  const handleSubmit = async (values: Record<string, unknown>) => {
    setError(null);
    try {
      await register(
        values['email'] as string,
        values['username'] as string,
        values['password'] as string
      );
      router.push('/login');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar conta');
    }
  };

  if (loading) {
    return null;
  }

  return (
    <ResponsiveLayout>
      <Stack space={24}>
        <Title1>Criar Conta</Title1>
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
                <EmailField name="email" label="Email" />
                <TextField name="username" label="Username" />
                <PasswordField name="password" label="Senha" />
                <ButtonPrimary submit>Registrar</ButtonPrimary>
              </Stack>
            </Form>
            <TextLink onPress={() => router.push('/login')}>
              Ja tem conta? Faca login
            </TextLink>
          </Stack>
        </Boxed>
      </Stack>
    </ResponsiveLayout>
  );
}
