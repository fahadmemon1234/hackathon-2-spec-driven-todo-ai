"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import TaskCard from "@/components/TaskCard";

interface TaskListProps {
  tasks: any[];
  onToggleComplete: (id: string) => void;
  onEdit: (task: any) => void;
  onDelete: (id: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggleComplete,
  onEdit,
  onDelete,
}) => {
  // FILTER LOGIC: Sirf wahi tasks rakho jinme tags array khali nahi hai
  // Yaani task.tags.length > 0 hona chahiye
  const filteredTasks = tasks.filter(task => 
    task.tags && Array.isArray(task.tags) && task.tags.length > 0
  );

  return (
    <div className="relative mt-8 min-h-[200px]">
      <div className="space-y-4">
        <AnimatePresence mode="popLayout" initial={false}>
          {filteredTasks.length === 0 ? (
            /* Agar koi task aisa nahi hai jisme tags hon */
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col items-center justify-center py-20 text-slate-500"
            >
              <p className="text-[10px] uppercase tracking-[0.2em] font-bold opacity-40">
                No tagged milestones found
              </p>
            </motion.div>
          ) : (
            filteredTasks.map((task, index) => (
              <motion.div
                key={task.id}
                layout
                initial={{ opacity: 0, x: -20, filter: "blur(10px)" }}
                animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
                exit={{
                  opacity: 0,
                  scale: 0.9,
                  x: 20,
                  filter: "blur(10px)",
                  transition: { duration: 0.2 },
                }}
                transition={{
                  type: "spring",
                  stiffness: 260,
                  damping: 20,
                  delay: index * 0.04,
                }}
              >
                <TaskCard
                  id={task.id}
                  title={task.title}
                  description={task.description}
                  completed={task.completed}
                  priority={task.priority}
                  category={task.category}
                  tags={task.tags} // Ab yahan humein pata hai tags ["a", "b"] format mein hain
                  due_date={task.due_date}
                  is_recurring={task.is_recurring}
                  recurrence_rule={task.recurrence_rule}
                  createdAt={task.created_at}
                  onToggle={onToggleComplete}
                  onEdit={onEdit}
                  onDelete={onDelete}
                />
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>

      {filteredTasks.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 py-6 border-t border-white/5 flex justify-center"
        >
          <div className="px-4 py-1.5 rounded-full bg-slate-900/50 border border-white/5 text-[10px] text-slate-500 uppercase tracking-[0.3em] font-bold">
            End of Tagged Tasks
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default TaskList;