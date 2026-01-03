"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Calendar } from "lucide-react";

interface TaskCardProps {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: string;
  category?: string;
  createdAt: string;
  onToggle: (id: string) => void;
  onEdit: (task: any) => void; // Changed to pass the full task object
  onDelete: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  id,
  title,
  description,
  completed,
  priority,
  category,
  createdAt,
  onToggle,
  onEdit,
  onDelete,
}) => {
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  // Determine priority text for display
  const priorityText =
    priority === "high" ? "HIGH" : priority === "medium" ? "MEDIUM" : "LOW";

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95, height: 0 }}
      transition={{ duration: 0.3 }}
      className="relative group"
    >
      <div
        className={`
    absolute left-0 top-4 bottom-4 w-[3px] rounded-r-full z-20 transition-all duration-500
    ${
      priority === "high"
        ? "bg-red-500 shadow-[4px_0_15px_rgba(239,68,68,0.4)]"
        : ""
    }
    ${
      priority === "medium"
        ? "bg-amber-400 shadow-[4px_0_15px_rgba(251,191,36,0.3)]"
        : ""
    }
    ${
      priority === "low"
        ? "bg-slate-500 shadow-[4px_0_15px_rgba(100,116,139,0.2)]"
        : ""
    }
  `}
      />

      <Card
        className={`
      relative overflow-hidden pl-5 bg-slate-900/40 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl transition-all duration-300
      group-hover:border-blue-500/30 group-hover:bg-slate-800/50
      ${completed ? "opacity-50" : ""}
    `}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />

        <div className="p-5">
          <div className="flex items-start gap-4">
            <div className="mt-1">
              <Checkbox
                checked={completed}
                onCheckedChange={() => onToggle(id)}
                className={`w-5 h-5 rounded-lg border-2 transition-all duration-300 cursor-pointer 
              ${
                completed
                  ? "bg-emerald-500 border-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]"
                  : "border-slate-700 hover:border-blue-500"
              }`}
              />
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-2">
                <span
                  className={`text-[9px] font-black uppercase tracking-[0.2em] px-2 py-0.5 rounded border
              ${
                priority === "high"
                  ? "text-red-400 border-red-500/20 bg-red-500/5"
                  : ""
              }
              ${
                priority === "medium"
                  ? "text-amber-400 border-amber-500/20 bg-amber-500/5"
                  : ""
              }
              ${
                priority === "low"
                  ? "text-slate-500 border-slate-700 bg-slate-800/50"
                  : ""
              }
            `}
                >
                  {priority}
                </span>

                {category && (
                  <span className="text-[9px] font-bold uppercase tracking-[0.1em] text-blue-400/60 group-hover:text-blue-400 transition-colors">
                    # {category}
                  </span>
                )}
              </div>

              <h3
                className={`text-lg font-bold tracking-tight transition-all duration-300 ${
                  completed
                    ? "line-through text-slate-600"
                    : "text-white group-hover:text-blue-500"
                }`}
              >
                {title}
              </h3>

              {description && (
                <p
                  className={`mt-2 text-sm leading-relaxed line-clamp-2 transition-all ${
                    completed ? "text-slate-700" : "text-slate-400"
                  }`}
                >
                  {description}
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="flex justify-between items-center px-5 py-3 bg-white/[0.02] border-t border-white/5">
          <div className="flex items-center gap-2 text-[10px] font-medium text-slate-600 uppercase tracking-widest">
            <Calendar size={12} className="opacity-50" />
            {formatDate(createdAt)}
          </div>

          <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0">
            <Button
              variant="ghost"
              size="sm"
              onClick={() =>
                onEdit({ id, title, description, priority, category })
              }
              className="h-8 px-3 text-[10px] font-bold uppercase tracking-widest text-slate-400 hover:text-white hover:bg-white/10 rounded-lg transition-all"
            >
              Edit
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(id)}
              className="h-8 px-3 text-[10px] font-bold uppercase tracking-widest text-slate-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all"
            >
              Delete
            </Button>
          </div>
        </div>
      </Card>
    </motion.div>
  );
};

export default TaskCard;
