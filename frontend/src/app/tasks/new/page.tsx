'use client';

import {useState} from 'react';
import {
  Boxed,
  ButtonPrimary,
  ButtonSecondary,
  Callout,
  Form,
  ResponsiveLayout,
  Select,
  Stack,
  TextField,
  Title1,
} from '@telefonica/mistica';
import {useRouter} from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import {api} from '@/lib/api';

interface CreateTaskPayload {
  title: string;
  description?: string;
  status: string;
  priority: string;
}

const STATUS_OPTIONS = [
  {value: 'pending', text: 'Pendente'},
  {value: 'in_progress', text: 'Em Progresso'},
  {value: 'done', text: 'Concluida'},
] as const;

const PRIORITY_OPTIONS = [
  {value: 'low', text: 'Baixa'},
  {value: 'medium', text: 'Media'},
  {value: 'high', text: 'Alta'},
] as const;

export default function NewTaskPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (values: Record<string, unknown>) => {
    setError(null);
    setSubmitting(true);
    try {
      const payload: CreateTaskPayload = {
        title: values['title'] as string,
        description: (values['description'] as string) || undefined,
        status: (values['status'] as string) || 'pending',
        priority: (values['priority'] as string) || 'medium',
      };
      await api.post('/tasks', payload);
      router.push('/tasks');
    } catch {
      setError('Erro ao criar task. Verifique os dados e tente novamente.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <ProtectedRoute>
      <ResponsiveLayout>
        <Stack space={24}>
          <Title1>Nova Task</Title1>
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
                  <TextField
                    name="title"
                    label="Titulo"
                    validate={(value) => (value ? undefined : 'Titulo obrigatorio')}
                  />
                  <TextField
                    name="description"
                    label="Descricao"
                    multiline
                    optional
                  />
                  <Select
                    name="status"
                    label="Status"
                    options={[...STATUS_OPTIONS]}
                    value="pending"
                  />
                  <Select
                    name="priority"
                    label="Prioridade"
                    options={[...PRIORITY_OPTIONS]}
                    value="medium"
                  />
                  <Stack space={12}>
                    <ButtonPrimary submit disabled={submitting}>
                      {submitting ? 'Criando...' : 'Criar Task'}
                    </ButtonPrimary>
                    <ButtonSecondary onPress={() => router.push('/tasks')}>
                      Cancelar
                    </ButtonSecondary>
                  </Stack>
                </Stack>
              </Form>
            </Stack>
          </Boxed>
        </Stack>
      </ResponsiveLayout>
    </ProtectedRoute>
  );
}
