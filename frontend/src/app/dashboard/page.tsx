"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import StatusBadge from "@/components/StatusBadge";
import { apiGet } from "@/lib/api";

interface Task {
  id: number;
  title: string;
  description: string | null;
  priority: string;
  status: string;
  created_at: string;
  updated_at: string | null;
  owner_id: number;
}

interface TaskStats {
  total: number;
  todo: number;
  inProgress: number;
  done: number;
  low: number;
  medium: number;
  high: number;
}

function computeStats(tasks: Task[]): TaskStats {
  return {
    total: tasks.length,
    todo: tasks.filter((t) => t.status === "todo").length,
    inProgress: tasks.filter((t) => t.status === "in_progress").length,
    done: tasks.filter((t) => t.status === "done").length,
    low: tasks.filter((t) => t.priority === "low").length,
    medium: tasks.filter((t) => t.priority === "medium").length,
    high: tasks.filter((t) => t.priority === "high").length,
  };
}

function BarChart({ stats }: { stats: TaskStats }) {
  const maxCount = Math.max(stats.todo, stats.inProgress, stats.done, 1);

  const bars = [
    { label: "To Do", count: stats.todo, color: "bg-gray-400" },
    { label: "In Progress", count: stats.inProgress, color: "bg-yellow-400" },
    { label: "Done", count: stats.done, color: "bg-green-500" },
  ];

  return (
    <div className="space-y-3">
      {bars.map((bar) => (
        <div key={bar.label} className="flex items-center gap-3">
          <span className="w-24 text-right text-sm text-gray-600 dark:text-gray-400">
            {bar.label}
          </span>
          <div className="flex-1">
            <div className="h-8 w-full rounded-full bg-gray-100 dark:bg-gray-800">
              <div
                className={`flex h-8 items-center rounded-full ${bar.color} transition-all duration-500`}
                style={{
                  width: `${Math.max((bar.count / maxCount) * 100, bar.count > 0 ? 8 : 0)}%`,
                }}
              >
                {bar.count > 0 && (
                  <span className="px-3 text-sm font-semibold text-white">
                    {bar.count}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchTasks() {
      try {
        const data = await apiGet<Task[]>("/tasks/");
        setTasks(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load tasks");
      } finally {
        setIsLoading(false);
      }
    }
    fetchTasks();
  }, []);

  const stats = computeStats(tasks);
  const recentTasks = [...tasks]
    .sort(
      (a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
    .slice(0, 5);

  return (
    <ProtectedRoute>
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <Link
            href="/tasks/new"
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700"
          >
            New Task
          </Link>
        </div>

        {isLoading && (
          <div className="flex justify-center py-12">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-blue-600" />
          </div>
        )}

        {error && (
          <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-800 dark:bg-red-950 dark:text-red-400">
            {error}
          </div>
        )}

        {!isLoading && !error && (
          <>
            {/* Stats Cards */}
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-900">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Total Tasks
                </p>
                <p className="mt-1 text-3xl font-bold text-gray-900 dark:text-white">
                  {stats.total}
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-900">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  To Do
                </p>
                <p className="mt-1 text-3xl font-bold text-gray-600 dark:text-gray-300">
                  {stats.todo}
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-900">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  In Progress
                </p>
                <p className="mt-1 text-3xl font-bold text-yellow-600 dark:text-yellow-400">
                  {stats.inProgress}
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-900">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Done
                </p>
                <p className="mt-1 text-3xl font-bold text-green-600 dark:text-green-400">
                  {stats.done}
                </p>
              </div>
            </div>

            {/* Priority breakdown */}
            <div className="mt-6 grid gap-6 lg:grid-cols-2">
              {/* Bar Chart */}
              <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-900">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Tasks by Status
                </h2>
                <div className="mt-4">
                  {stats.total === 0 ? (
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      No tasks yet.
                    </p>
                  ) : (
                    <BarChart stats={stats} />
                  )}
                </div>
              </div>

              {/* Priority Cards */}
              <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-900">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Tasks by Priority
                </h2>
                <div className="mt-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <StatusBadge type="priority" value="high" />
                    <span className="text-lg font-semibold text-gray-900 dark:text-white">
                      {stats.high}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <StatusBadge type="priority" value="medium" />
                    <span className="text-lg font-semibold text-gray-900 dark:text-white">
                      {stats.medium}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <StatusBadge type="priority" value="low" />
                    <span className="text-lg font-semibold text-gray-900 dark:text-white">
                      {stats.low}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Tasks */}
            <div className="mt-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-900">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Recent Tasks
                </h2>
                <Link
                  href="/tasks"
                  className="text-sm font-medium text-blue-600 hover:text-blue-500"
                >
                  View all
                </Link>
              </div>
              <div className="mt-4">
                {recentTasks.length === 0 ? (
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    No tasks yet.{" "}
                    <Link
                      href="/tasks/new"
                      className="text-blue-600 hover:text-blue-500"
                    >
                      Create your first task
                    </Link>
                  </p>
                ) : (
                  <div className="divide-y divide-gray-100 dark:divide-gray-800">
                    {recentTasks.map((task) => (
                      <div
                        key={task.id}
                        className="flex items-center justify-between py-3"
                      >
                        <div className="min-w-0 flex-1">
                          <Link
                            href={`/tasks/${task.id}/edit`}
                            className="truncate text-sm font-medium text-gray-900 hover:text-blue-600 dark:text-white dark:hover:text-blue-400"
                          >
                            {task.title}
                          </Link>
                          <p className="text-xs text-gray-500 dark:text-gray-400">
                            {new Date(task.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <div className="ml-4 flex items-center gap-2">
                          <StatusBadge type="status" value={task.status} />
                          <StatusBadge type="priority" value={task.priority} />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
