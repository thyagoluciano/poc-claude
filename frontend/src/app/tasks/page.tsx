'use client';

import {useCallback, useEffect, useState} from 'react';
import {
  ButtonPrimary,
  Callout,
  EmptyState,
  IconClipboardRegular,
  ResponsiveLayout,
  SkeletonRectangle,
  Stack,
  Tabs,
  Title1,
} from '@telefonica/mistica';
import {useRouter} from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import TaskCard from '@/components/TaskCard';
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

const TAB_FILTERS: ReadonlyArray<{text: string; status: TaskStatus | 'all'}> = [
  {text: 'Todas', status: 'all'},
  {text: 'Pendentes', status: 'pending'},
  {text: 'Em Progresso', status: 'in_progress'},
  {text: 'Concluidas', status: 'done'},
] as const;

export default function TasksPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState(0);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get<Task[]>('/tasks');
      setTasks(data);
    } catch {
      setError('Erro ao carregar tasks. Tente novamente.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const activeFilter = TAB_FILTERS[selectedTab].status;
  const filteredTasks =
    activeFilter === 'all' ? tasks : tasks.filter((t) => t.status === activeFilter);

  return (
    <ProtectedRoute>
      <ResponsiveLayout>
        <Stack space={24}>
          <Stack space={16}>
            <Title1>Tasks</Title1>
            <ButtonPrimary small onPress={() => router.push('/tasks/new')}>
              Nova Task
            </ButtonPrimary>
          </Stack>

          <Tabs
            selectedIndex={selectedTab}
            onChange={setSelectedTab}
            tabs={TAB_FILTERS.map((tab) => ({text: tab.text}))}
          />

          {error && (
            <Callout
              title="Erro"
              description={error}
              onClose={() => setError(null)}
            />
          )}

          {loading ? (
            <Stack space={16}>
              {Array.from({length: 3}, (_, i) => (
                <SkeletonRectangle key={i} height={120} />
              ))}
            </Stack>
          ) : filteredTasks.length === 0 ? (
            <EmptyState
              title="Nenhuma task encontrada"
              description={
                activeFilter === 'all'
                  ? 'Crie sua primeira task clicando no botao acima.'
                  : 'Nenhuma task com este status.'
              }
              asset={<IconClipboardRegular size={48} />}
              button={
                <ButtonPrimary small onPress={() => router.push('/tasks/new')}>
                  Criar Task
                </ButtonPrimary>
              }
            />
          ) : (
            <Stack space={16}>
              {filteredTasks.map((task) => (
                <TaskCard key={task.id} task={task} />
              ))}
            </Stack>
          )}
        </Stack>
      </ResponsiveLayout>
    </ProtectedRoute>
  );
}
