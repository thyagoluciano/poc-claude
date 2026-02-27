interface StatusBadgeProps {
  type: "status" | "priority";
  value: string;
}

const STATUS_STYLES: Record<string, string> = {
  todo: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300",
  in_progress:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
  done: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
};

const PRIORITY_STYLES: Record<string, string> = {
  low: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
  medium:
    "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
  high: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
};

const STATUS_LABELS: Record<string, string> = {
  todo: "To Do",
  in_progress: "In Progress",
  done: "Done",
};

const PRIORITY_LABELS: Record<string, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
};

export default function StatusBadge({ type, value }: StatusBadgeProps) {
  const styles =
    type === "status" ? STATUS_STYLES[value] : PRIORITY_STYLES[value];
  const label =
    type === "status" ? STATUS_LABELS[value] : PRIORITY_LABELS[value];

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${styles ?? "bg-gray-100 text-gray-700"}`}
    >
      {label ?? value}
    </span>
  );
}
