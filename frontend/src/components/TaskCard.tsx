'use client';

import {DataCard, Tag} from '@telefonica/mistica';
import {useRouter} from 'next/navigation';
import StatusBadge from './StatusBadge';

type TaskStatus = 'pending' | 'in_progress' | 'done';
type TaskPriority = 'low' | 'medium' | 'high';

interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: TaskPriority;
}

interface TaskCardProps {
  task: Task;
}

const priorityConfig: Record<TaskPriority, {label: string; type: 'info' | 'warning' | 'error'}> = {
  low: {label: 'Baixa', type: 'info'},
  medium: {label: 'Media', type: 'warning'},
  high: {label: 'Alta', type: 'error'},
};

export default function TaskCard({task}: TaskCardProps) {
  const router = useRouter();
  const priority = priorityConfig[task.priority];

  return (
    <DataCard
      headline={<Tag type={priority.type}>{priority.label}</Tag>}
      title={task.title}
      description={task.description ?? ''}
      onPress={() => router.push(`/tasks/${task.id}/edit`)}
      slot={<StatusBadge status={task.status} />}
    />
  );
}
