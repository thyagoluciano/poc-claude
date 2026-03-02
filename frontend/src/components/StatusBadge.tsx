'use client';

import {Tag} from '@telefonica/mistica';
import type {TagType} from '@telefonica/mistica';

type TaskStatus = 'pending' | 'in_progress' | 'done';

interface StatusBadgeProps {
  status: TaskStatus;
}

const statusConfig: Record<TaskStatus, {label: string; type: TagType}> = {
  pending: {label: 'Pendente', type: 'warning'},
  in_progress: {label: 'Em Progresso', type: 'info'},
  done: {label: 'Concluida', type: 'success'},
};

export default function StatusBadge({status}: StatusBadgeProps) {
  const config = statusConfig[status];
  return <Tag type={config.type}>{config.label}</Tag>;
}
