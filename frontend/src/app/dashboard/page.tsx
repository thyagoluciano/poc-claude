'use client';

import {useCallback, useEffect, useState} from 'react';
import {
  Boxed,
  ButtonPrimary,
  Callout,
  DataCard,
  EmptyState,
  IconAlertRegular,
  IconCheckRegular,
  IconClipboardRegular,
  IconTimeRegular,
  ProgressBar,
  ResponsiveLayout,
  Row,
  RowList,
  SkeletonRectangle,
  Stack,
  Text2,
  Title1,
  Title2,
} from '@telefonica/mistica';
import {useRouter} from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import StatusBadge from '@/components/StatusBadge';
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

interface TaskStats {
  total: number;
  pending: number;
  inProgress: number;
  done: number;
  completionPercent: number;
}

function computeStats(tasks: Task[]): TaskStats {
  const total = tasks.length;
  const pending = tasks.filter((t) => t.status === 'pending').length;
  const inProgress = tasks.filter((t) => t.status === 'in_progress').length;
  const done = tasks.filter((t) => t.status === 'done').length;
  const completionPercent = total > 0 ? Math.round((done / total) * 100) : 0;
  return {total, pending, inProgress, done, completionPercent};
}

function getRecentTasks(tasks: Task[], limit: number): Task[] {
  return [...tasks]
    .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
    .slice(0, limit);
}

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get<Task[]>('/tasks');
      setTasks(data);
    } catch {
      setError('Erro ao carregar dados do dashboard.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  if (loading) {
    return (
      <ProtectedRoute>
        <ResponsiveLayout>
          <Stack space={32}>
            <Title1>Dashboard</Title1>
            <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16}}>
              {Array.from({length: 4}, (_, i) => (
                <SkeletonRectangle key={i} height={120} />
              ))}
            </div>
            <SkeletonRectangle height={80} />
            <Stack space={16}>
              {Array.from({length: 3}, (_, i) => (
                <SkeletonRectangle key={i} height={64} />
              ))}
            </Stack>
          </Stack>
        </ResponsiveLayout>
      </ProtectedRoute>
    );
  }

  const stats = computeStats(tasks);
  const recentTasks = getRecentTasks(tasks, 5);

  return (
    <ProtectedRoute>
      <ResponsiveLayout>
        <Stack space={32}>
          <Title1>Dashboard</Title1>

          {error && (
            <Callout
              title="Erro"
              description={error}
              onClose={() => setError(null)}
            />
          )}

          {/* Stats Cards */}
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16}}>
            <DataCard
              title={String(stats.total)}
              subtitle="Total de Tasks"
              asset={<IconClipboardRegular size={40} />}
            />
            <DataCard
              title={String(stats.pending)}
              subtitle="Pendentes"
              asset={<IconAlertRegular size={40} />}
            />
            <DataCard
              title={String(stats.inProgress)}
              subtitle="Em Progresso"
              asset={<IconTimeRegular size={40} />}
            />
            <DataCard
              title={String(stats.done)}
              subtitle="Concluidas"
              asset={<IconCheckRegular size={40} />}
            />
          </div>

          {/* Progress Bar */}
          <Boxed>
            <Stack space={12}>
              <Title2>Progresso de Conclusao</Title2>
              <ProgressBar progressPercent={stats.completionPercent} aria-label="Progresso de conclusao" />
              <Text2 regular>{stats.completionPercent}% concluido ({stats.done} de {stats.total} tasks)</Text2>
            </Stack>
          </Boxed>

          {/* Callout Tip */}
          <Callout
            title="Dica"
            description="Mantenha suas tasks atualizadas para acompanhar o progresso do projeto. Tasks concluidas aparecem na barra de progresso acima."
          />

          {/* Recent Tasks */}
          <Stack space={16}>
            <Title2>Tasks Recentes</Title2>
            {recentTasks.length === 0 ? (
              <EmptyState
                title="Nenhuma task encontrada"
                description="Crie sua primeira task para comecar."
                asset={<IconClipboardRegular size={48} />}
                button={
                  <ButtonPrimary small onPress={() => router.push('/tasks/new')}>
                    Criar Task
                  </ButtonPrimary>
                }
              />
            ) : (
              <RowList>
                {recentTasks.map((task) => (
                  <Row
                    key={task.id}
                    title={task.title}
                    description={task.description}
                    onPress={() => router.push(`/tasks/${task.id}/edit`)}
                    right={<StatusBadge status={task.status} />}
                  />
                ))}
              </RowList>
            )}
          </Stack>
        </Stack>
      </ResponsiveLayout>
    </ProtectedRoute>
  );
}
