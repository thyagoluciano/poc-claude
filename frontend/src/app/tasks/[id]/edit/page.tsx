'use client';

import {useCallback, useEffect, useState} from 'react';
import {
  Boxed,
  ButtonDanger,
  ButtonPrimary,
  ButtonSecondary,
  Callout,
  ErrorFeedbackScreen,
  Form,
  ResponsiveLayout,
  Select,
  SkeletonRectangle,
  Stack,
  TextField,
  Title1,
  useDialog,
  useSnackbar,
} from '@telefonica/mistica';
import {useParams, useRouter} from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import {api} from '@/lib/api';

type TaskStatus = 'pending' | 'in_progress' | 'done';
type TaskPriority = 'low' | 'medium' | 'high';

interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  created_at: string;
  updated_at: string;
  owner_id: number;
}

interface UpdateTaskPayload {
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

function EditFormSkeleton() {
  return (
    <Boxed>
      <Stack space={16}>
        <SkeletonRectangle height={56} />
        <SkeletonRectangle height={96} />
        <SkeletonRectangle height={56} />
        <SkeletonRectangle height={56} />
        <SkeletonRectangle height={48} width={160} />
      </Stack>
    </Boxed>
  );
}

export default function EditTaskPage() {
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;
  const {confirm} = useDialog();
  const {openSnackbar} = useSnackbar();

  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const fetchTask = useCallback(async () => {
    setLoading(true);
    setLoadError(false);
    try {
      const data = await api.get<Task>(`/tasks/${taskId}`);
      setTask(data);
    } catch {
      setLoadError(true);
    } finally {
      setLoading(false);
    }
  }, [taskId]);

  useEffect(() => {
    fetchTask();
  }, [fetchTask]);

  const handleSubmit = async (values: Record<string, unknown>) => {
    setError(null);
    setSubmitting(true);
    try {
      const payload: UpdateTaskPayload = {
        title: values['title'] as string,
        description: (values['description'] as string) || undefined,
        status: values['status'] as string,
        priority: values['priority'] as string,
      };
      await api.put(`/tasks/${taskId}`, payload);
      openSnackbar({message: 'Task atualizada com sucesso!'});
      router.push('/tasks');
    } catch {
      openSnackbar({message: 'Erro ao atualizar task.', type: 'CRITICAL'});
      setError('Erro ao atualizar task. Verifique os dados e tente novamente.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = () => {
    confirm({
      title: 'Excluir Task',
      message: `Tem certeza que deseja excluir "${task?.title}"? Esta acao nao pode ser desfeita.`,
      acceptText: 'Excluir',
      cancelText: 'Cancelar',
      destructive: true,
      onAccept: async () => {
        try {
          await api.delete(`/tasks/${taskId}`);
          openSnackbar({message: 'Task excluida com sucesso!'});
          router.push('/tasks');
        } catch {
          openSnackbar({message: 'Erro ao excluir task.', type: 'CRITICAL'});
          setError('Erro ao excluir task.');
        }
      },
    });
  };

  if (!loading && loadError) {
    return (
      <ProtectedRoute>
        <ErrorFeedbackScreen
          title="Erro ao carregar task"
          description="Nao foi possivel carregar os dados da task. Verifique sua conexao e tente novamente."
          primaryButton={
            <ButtonPrimary onPress={() => fetchTask()}>
              Tentar novamente
            </ButtonPrimary>
          }
          secondaryButton={
            <ButtonSecondary onPress={() => router.push('/tasks')}>
              Voltar para Tasks
            </ButtonSecondary>
          }
        />
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <ResponsiveLayout>
        <Stack space={24}>
          <Title1>Editar Task</Title1>

          {error && (
            <Callout
              title="Erro"
              description={error}
              onClose={() => setError(null)}
            />
          )}

          {loading ? (
            <EditFormSkeleton />
          ) : task ? (
            <Boxed>
              <Stack space={16}>
                <Form onSubmit={handleSubmit}>
                  <Stack space={16}>
                    <TextField
                      name="title"
                      label="Titulo"
                      defaultValue={task.title}
                      validate={(value) => (value ? undefined : 'Titulo obrigatorio')}
                    />
                    <TextField
                      name="description"
                      label="Descricao"
                      multiline
                      optional
                      defaultValue={task.description ?? ''}
                    />
                    <Select
                      name="status"
                      label="Status"
                      options={[...STATUS_OPTIONS]}
                      value={task.status}
                    />
                    <Select
                      name="priority"
                      label="Prioridade"
                      options={[...PRIORITY_OPTIONS]}
                      value={task.priority}
                    />
                    <Stack space={12}>
                      <ButtonPrimary submit disabled={submitting}>
                        {submitting ? 'Salvando...' : 'Salvar'}
                      </ButtonPrimary>
                      <ButtonDanger onPress={handleDelete}>
                        Excluir Task
                      </ButtonDanger>
                      <ButtonSecondary onPress={() => router.push('/tasks')}>
                        Cancelar
                      </ButtonSecondary>
                    </Stack>
                  </Stack>
                </Form>
              </Stack>
            </Boxed>
          ) : (
            <Callout
              title="Task nao encontrada"
              description="A task solicitada nao foi encontrada."
            />
          )}
        </Stack>
      </ResponsiveLayout>
    </ProtectedRoute>
  );
}
