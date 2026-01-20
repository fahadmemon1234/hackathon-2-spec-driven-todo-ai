"use client";

import React from "react";
import { motion } from "framer-motion";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Calendar,
  Hash,
  LayoutGrid,
  RotateCw,
  Edit3,
  Trash2,
} from "lucide-react";

interface TaskCardProps {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: string;
  category?: string;
  tags?: string[];
  due_date?: string;
  is_recurring?: boolean;
  recurrence_rule?: string;
  createdAt: string;
  onToggle: (id: string) => void;
  onEdit: (task: any) => void;
  onDelete: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  id,
  title,
  description,
  completed,
  priority,
  category,
  tags = [],
  due_date,
  is_recurring,
  recurrence_rule,
  createdAt,
  onToggle,
  onEdit,
  onDelete,
}) => {
  const formatDate = (dateString?: string) => {
    if (!dateString) return "";

    // Agar date string mein timezone (+00 ya Z) hai,
    // toh use replace kar denge taaki browser use local hi treat kare
    const cleanDateString = dateString.replace("Z", "").split("+")[0];
    const date = new Date(cleanDateString);

    const datePart = date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });

    const timePart = date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });

    return `${datePart}, ${timePart}`;
  };

  // Priority Style Mapping (Matches Input Form)
  const priorityStyles: Record<string, string> = {
    high: "text-red-400 bg-red-500/10 border-red-500/20 shadow-[0_0_10px_rgba(239,68,68,0.1)]",
    medium:
      "text-amber-400 bg-amber-500/10 border-amber-500/20 shadow-[0_0_10px_rgba(245,158,11,0.1)]",
    low: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20 shadow-[0_0_10px_rgba(16,185,129,0.1)]",
  };

  const prioritySidebar: Record<string, string> = {
    high: "bg-red-500 shadow-[2px_0_15px_rgba(239,68,68,0.5)]",
    medium: "bg-amber-500 shadow-[2px_0_15px_rgba(245,158,11,0.4)]",
    low: "bg-emerald-500 shadow-[2px_0_15px_rgba(16,185,129,0.3)]",
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="relative group mb-4"
    >
      {/* Dynamic Priority Sidebar */}
      <div
        className={`absolute left-0 top-3 bottom-3 w-[4px] rounded-r-full z-10 transition-all duration-500 ${prioritySidebar[priority] || "bg-slate-700"}`}
      />

      <Card
        className={`relative overflow-hidden pl-4 bg-slate-900/40 backdrop-blur-2xl border border-white/5 rounded-[24px] transition-all duration-500 group-hover:border-white/10 group-hover:bg-slate-800/40 ${completed ? "opacity-60" : ""}`}
      >
        <div className="p-5">
          <div className="flex gap-4">
            {/* Custom Checkbox Area */}
            <div className="pt-1">
              <Checkbox
                checked={completed}
                onCheckedChange={() => onToggle(id)}
                className={`w-6 h-6 rounded-full border-2 transition-all duration-500 ${
                  completed
                    ? "bg-blue-600 border-blue-600 shadow-[0_0_15px_rgba(37,99,235,0.4)]"
                    : "border-slate-700 hover:border-blue-500"
                }`}
              />
            </div>

            <div className="flex-1 min-w-0">
              {/* Badges Row */}
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <span
                  className={`text-[9px] font-black uppercase tracking-widest px-2.5 py-1 rounded-lg border ${priorityStyles[priority]}`}
                >
                  {priority}
                </span>

                {category && (
                  <span className="flex items-center gap-1 text-[9px] font-bold uppercase tracking-wider bg-white/5 text-slate-400 px-2.5 py-1 rounded-lg border border-white/5">
                    <LayoutGrid size={10} />
                    {category}
                  </span>
                )}

                {is_recurring && (
                  <span className="flex items-center gap-1 text-[9px] font-bold bg-indigo-500/10 text-indigo-400 px-2.5 py-1 rounded-lg border border-indigo-500/20 uppercase tracking-widest">
                    <RotateCw size={10} className="animate-spin-slow" />
                    Recurring
                  </span>
                )}
              </div>

              {/* Title & Description */}
              <h3
                className={`text-lg font-bold tracking-tight transition-all duration-300 ${completed ? "line-through text-slate-600" : "text-white"}`}
              >
                {title}
              </h3>

              {description && (
                <p
                  className={`mt-1.5 text-sm leading-relaxed line-clamp-2 ${completed ? "text-slate-700" : "text-slate-400"}`}
                >
                  {description}
                </p>
              )}

              {/* Tags Section - Render only if exists */}
              {tags && tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-4">
                  {tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="flex items-center gap-1 text-[10px] font-medium px-2.5 py-1 rounded-full bg-blue-500/5 text-blue-400/80 border border-blue-500/10 hover:border-blue-500/30 transition-colors"
                    >
                      <Hash size={10} className="text-blue-500/50" />
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer Info & Actions */}
        <div className="flex items-center justify-between px-6 py-3 bg-black/20 border-t border-white/5">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 text-[10px] font-bold text-slate-600 uppercase tracking-wider">
              <Calendar size={12} className="opacity-50" />
              <span>Created: {formatDate(createdAt)}</span>
            </div>

            {due_date && (
              <div
                className={`flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider ${completed ? "text-slate-700" : "text-amber-500/80"}`}
              >
                <div className="w-1 h-1 rounded-full bg-current" />
                Due: {formatDate(due_date)}
              </div>
            )}
          </div>

          <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <Button
              variant="ghost"
              size="icon"
              onClick={() =>
                onEdit({
                  id,
                  title,
                  description,
                  priority,
                  category,
                  tags,
                  due_date,
                  is_recurring,
                  recurrence_rule,
                })
              }
              className="h-8 w-8 text-slate-500 hover:text-white hover:bg-white/5 rounded-full"
            >
              <Edit3 size={14} />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onDelete(id)}
              className="h-8 w-8 text-slate-500 hover:text-red-400 hover:bg-red-400/5 rounded-full"
            >
              <Trash2 size={14} />
            </Button>
          </div>
        </div>
      </Card>
    </motion.div>
  );
};

export default TaskCard;
