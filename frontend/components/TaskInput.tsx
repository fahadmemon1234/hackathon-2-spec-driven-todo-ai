"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

interface TaskInputProps {
  onAddTask: (taskData: {
    title: string;
    description?: string;
    priority?: string;
    category?: string;
  }) => void;
}

const TaskInput: React.FC<TaskInputProps> = ({ onAddTask }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<"high" | "medium" | "low">("medium");
  const [category, setCategory] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    onAddTask({
      title: title.trim(),
      description: description.trim() || undefined,
      priority,
      category: category.trim() || undefined,
    });
    setTitle("");
    setDescription("");
    setCategory("");
    setPriority("medium");
  };

  return (
    <motion.form
      className={`relative bg-slate-900/40 backdrop-blur-2xl rounded-[24px] mb-10 overflow-hidden transition-all duration-500 border ${
        isFocused
          ? "border-blue-500/50 shadow-[0_0_40px_rgba(37,99,235,0.15)] ring-1 ring-blue-500/20"
          : "border-white/10 shadow-2xl"
      }`}
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
    >
      {isFocused && (
        <motion.div
          layoutId="activeGlow"
          className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-blue-500 to-transparent z-20"
        />
      )}

      <div className="p-6">
        <div className="flex gap-4 items-start">
          <div className="flex-1 space-y-4">
            <div className="flex items-center gap-3">
              <div
                className={`w-2 h-2 rounded-full transition-colors duration-500 ${
                  isFocused ? "bg-blue-500 animate-pulse" : "bg-slate-600"
                }`}
              />
              <input
                id="task-input-title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="What's the next milestone?"
                className="w-full bg-transparent border-none focus:outline-none focus:ring-0 text-white text-xl font-semibold placeholder-slate-600"
                onFocus={() => setIsFocused(true)}
              />
            </div>

            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add further context or notes..."
              className="w-full bg-white/[0.03] border border-white/5 rounded-xl px-4 py-3 text-slate-300 placeholder-slate-600 focus:outline-none focus:border-blue-500/30 focus:bg-white/[0.05] transition-all min-h-[60px] text-sm resize-none"
              rows={1}
              onFocus={() => setIsFocused(true)}
            />
          </div>

          <Button
            type="submit"
            disabled={!title.trim()}
            className={`mt-1 h-12 w-12 rounded-xl transition-all duration-300 ${
              title.trim()
                ? "bg-blue-600 text-white shadow-lg shadow-blue-600/30 hover:scale-105 active:scale-95"
                : "bg-slate-800 text-slate-500 opacity-50"
            }`}
          >
            <Plus size={24} strokeWidth={3} />
          </Button>
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-6 pt-6 border-t border-white/5">
          <div className="flex flex-col gap-2">
            <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500 ml-1">
              Priority Level
            </span>
            <div className="flex gap-2 p-1 bg-black/20 rounded-xl border border-white/5">
              {[
                {
                  id: "high",
                  label: "High",
                  color: "bg-red-500",
                  text: "text-red-500",
                },
                {
                  id: "medium",
                  label: "Med",
                  color: "bg-amber-500",
                  text: "text-amber-500",
                },
                {
                  id: "low",
                  label: "Low",
                  color: "bg-slate-500",
                  text: "text-slate-400",
                },
              ].map((p) => (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setPriority(p.id as any)}
                  className={`px-4 py-1.5 text-[10px] font-bold rounded-lg transition-all flex items-center gap-2 ${
                    priority === p.id
                      ? `${p.color} text-white shadow-lg`
                      : `text-slate-500 hover:bg-white/5`
                  }`}
                >
                  <div
                    className={`w-1.5 h-1.5 rounded-full ${
                      priority === p.id ? "bg-white" : p.color
                    }`}
                  />
                  {p.label.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          <div className="flex-1 flex flex-col gap-2 min-w-[200px]">
            <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500 ml-1">
              Classification
            </span>
            <div className="relative group">
              <input
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="e.g. Engineering, Strategy..."
                className="w-full bg-black/20 border border-white/5 rounded-xl px-4 py-2 text-sm text-slate-300 placeholder-slate-700 focus:outline-none focus:border-blue-500/30 focus:bg-black/40 transition-all"
                onFocus={() => setIsFocused(true)}
              />
              <div className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-slate-700 font-bold tracking-widest uppercase pointer-events-none group-focus-within:text-blue-500/50 transition-colors">
                Tag
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.form>
  );
};

export default TaskInput;
