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
  return (
    <div className="relative mt-8 min-h-[200px]">
      <div className="space-y-4">
        <AnimatePresence mode="popLayout" initial={false}>
          {tasks.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="flex flex-col items-center justify-center py-20 text-slate-500"
            >
              <p className="text-xs uppercase tracking-wide font-medium opacity-60">
                No tasks found
              </p>
            </motion.div>
          ) : (
            tasks.map((task, index) => (
              <motion.div
                key={task.id}
                layout
                initial={{ opacity: 0, y: 20, filter: "blur(10px)" }}
                animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                exit={{
                  opacity: 0,
                  scale: 0.95,
                  y: -10,
                  filter: "blur(10px)",
                  transition: { duration: 0.2 },
                }}
                transition={{
                  type: "spring",
                  stiffness: 200,
                  damping: 25,
                  mass: 0.8,
                  delay: index * 0.03,
                }}
                whileHover={{ y: -2 }}
              >
                <TaskCard
                  id={task.id}
                  title={task.title}
                  description={task.description}
                  completed={task.completed}
                  priority={task.priority}
                  category={task.category}
                  tags={task.tags}
                  due_date={task.due_date}
                  is_recurring={task.is_recurring}
                  recurrence_rule={task.recurrence_rule}
                  reminder_type={task.reminder_type}
                  reminder_offset={task.reminder_offset}
                  reminder_time={task.reminder_time}
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

      {tasks.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-12 py-6 border-t border-slate-700/50 flex justify-center"
        >
          <div className="px-4 py-1.5 rounded-full bg-slate-800/50 border border-slate-700/50 text-xs text-slate-500 uppercase tracking-wider font-medium">
            End of Tasks
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default TaskList;