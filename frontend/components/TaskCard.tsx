"use client";

import React from "react";
import { motion } from "framer-motion";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Calendar,
  Hash,
  Folder,
  RotateCw,
  Edit3,
  Trash2,
  Clock,
  Flag,
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
    high: "bg-gradient-to-b from-red-500 to-red-600 shadow-[2px_0_15px_rgba(239,68,68,0.5)]",
    medium: "bg-gradient-to-b from-amber-500 to-amber-600 shadow-[2px_0_15px_rgba(245,158,11,0.4)]",
    low: "bg-gradient-to-b from-emerald-500 to-emerald-600 shadow-[2px_0_15px_rgba(16,185,129,0.3)]",
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="relative mb-4"
    >
      {/* Dynamic Priority Sidebar */}
      <div
        className={`absolute left-0 top-4 bottom-4 w-1 rounded-r-full z-10 transition-all duration-500 ${prioritySidebar[priority] || "bg-slate-700"}`}
      />

      <Card
        className={`relative overflow-hidden pl-5 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl transition-all duration-500 hover:border-slate-600/70 hover:shadow-lg hover:shadow-indigo-500/5 group ${completed ? "opacity-70" : ""}`}
      >
        <div className="p-5">
          <div className="flex gap-4">
            {/* Custom Checkbox Area */}
            <div className="pt-1">
              <Checkbox
                checked={completed}
                onCheckedChange={() => onToggle(id)}
                className={`w-5 h-5 rounded-md border-2 transition-all duration-300 ${
                  completed
                    ? "bg-gradient-to-r from-indigo-600 to-purple-600 border-indigo-600 shadow-[0_0_10px_rgba(99,102,241,0.4)]"
                    : "border-slate-600 hover:border-indigo-500 bg-slate-800/50"
                }`}
              />
            </div>

            <div className="flex-1 min-w-0">
              {/* Badges Row */}
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <span
                  className={`text-[9px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md border flex items-center gap-1 ${priorityStyles[priority]}`}
                >
                  <Flag size={10} className="text-current" /> {priority}
                </span>

                {category && (
                  <span className="flex items-center gap-1 text-[9px] font-bold uppercase tracking-wider bg-slate-800/50 text-slate-400 px-2.5 py-1 rounded-md border border-slate-700/50">
                    <Folder size={10} />
                    {category}
                  </span>
                )}

                {is_recurring && (
                  <span className="flex items-center gap-1 text-[9px] font-bold bg-indigo-500/10 text-indigo-400 px-2.5 py-1 rounded-md border border-indigo-500/20 uppercase tracking-widest">
                    <RotateCw size={10} className="animate-spin-slow" />
                    Recurring
                  </span>
                )}
              </div>

              {/* Title & Description */}
              <h3
                className={`text-lg font-bold tracking-tight transition-all duration-300 ${completed ? "line-through text-slate-500" : "text-white"}`}
              >
                {title}
              </h3>

              {description && (
                <p
                  className={`mt-2 text-sm leading-relaxed ${completed ? "text-slate-600" : "text-slate-400"}`}
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
                      className="flex items-center gap-1 text-[10px] font-medium px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20"
                    >
                      <Hash size={10} className="text-indigo-400" />
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer Info & Actions */}
        <div className="flex items-center justify-between px-5 py-3 bg-slate-800/30 border-t border-slate-700/50">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 text-[10px] font-medium text-slate-500">
              <Clock size={12} className="text-slate-600" />
              <span>Created: {formatDate(createdAt)}</span>
            </div>

            {due_date && (
              <div
                className={`flex items-center gap-1.5 text-[10px] font-medium ${completed ? "text-slate-600" : "text-amber-500"}`}
              >
                <Calendar size={12} className="text-current" />
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
              className="h-8 w-8 text-slate-500 hover:text-indigo-400 hover:bg-indigo-500/10 rounded-md transition-colors"
            >
              <Edit3 size={14} />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onDelete(id)}
              className="h-8 w-8 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded-md transition-colors"
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
