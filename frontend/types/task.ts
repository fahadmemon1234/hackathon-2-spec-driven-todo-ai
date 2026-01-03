// frontend/types/task.ts
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  priority: string;  // 'high' | 'medium' | 'low'
  category?: string;
}