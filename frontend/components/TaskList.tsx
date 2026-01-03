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
    <div className="relative mt-8">
      <div className="space-y-4">
        <AnimatePresence mode="popLayout">
          {tasks.map((task, index) => (
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
                createdAt={task.created_at}
                onToggle={onToggleComplete}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {tasks.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 py-6 border-t border-white/5 flex justify-center"
        >
          <div className="px-4 py-1.5 rounded-full bg-slate-900/50 border border-white/5 text-[10px] text-slate-500 uppercase tracking-[0.3em] font-bold">
            End of Workspace
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default TaskList;
