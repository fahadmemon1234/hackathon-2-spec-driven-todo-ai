"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Plus, Calendar, X, Hash, Folder, AlertCircle, Sparkles } from "lucide-react";

interface TaskInputProps {
  onAddTask: (taskData: {
    title: string;
    description: string;
    priority: "high" | "medium" | "low";
    category: string;
    tags: string[];
    due_date?: string;
  }) => void;
}

const TaskInput: React.FC<TaskInputProps> = ({ onAddTask }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<"high" | "medium" | "low">("medium");
  const [category, setCategory] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isShaking, setIsShaking] = useState(false);

  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const priorityMap = {
    high: "bg-red-500 text-white shadow-[0_0_10px_rgba(239,68,68,0.3)]",
    medium: "bg-amber-500 text-white shadow-[0_0_10px_rgba(245,158,11,0.3)]",
    low: "bg-emerald-500 text-white shadow-[0_0_10px_rgba(16,185,129,0.3)]",
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [description]);

  // Simplified validation - only title is required
  const validate = () => {
    const newErrors: { [key: string]: string } = {};

    if (!title.trim()) {
      newErrors.title = "Task title is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleAddTag = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      const val = tagInput.trim().replace(",", "");
      if (val && !tags.includes(val) && tags.length < 5) { // Limit to 5 tags
        setTags([...tags, val]);
        setTagInput("");
        setErrors((prev) => ({ ...prev, tags: "" }));
      }
    }
  };

  const removeTag = (tagToRemove: string) => {
    setTags(tags.filter((t) => t !== tagToRemove));
  };

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();

    const isValid = validate();

    if (!isValid) {
      setIsShaking(true);
      setTimeout(() => setIsShaking(false), 500);
      return;
    }

    if (isSubmitting) return;

    setIsSubmitting(true);

    onAddTask({
      title: title.trim(),
      description: description.trim(),
      priority,
      category: category.trim() || "General", // Default to "General" if empty
      due_date: dueDate || undefined,
      tags: tags,
    });

    // Reset Form
    setTitle("");
    setDescription("");
    setCategory("");
    setDueDate("");
    setTags([]);
    setPriority("medium");
    setErrors({});

    setTimeout(() => setIsSubmitting(false), 500);
  };

  return (
    <motion.form
      animate={isShaking ? { x: [-10, 10, -10, 10, 0] } : { opacity: 1, y: 0 }}
      className={`relative bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-xl rounded-2xl mb-10 overflow-hidden border transition-all duration-500 ${
        Object.keys(errors).length > 0
          ? "border-red-500/50"
          : isFocused
            ? "border-indigo-500/40"
            : "border-slate-700/50"
      } shadow-xl`}
      onSubmit={handleSubmit}
    >
      <div className="p-6">
        <div className="flex gap-4 items-start">
          <div className="flex-1 space-y-4">
            {/* Title Section */}
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-3">
                <div
                  className={`w-3 h-3 rounded-full ${errors.title ? "bg-red-500" : "bg-indigo-500"}`}
                />
                <input
                  id="task-input-title"
                  type="text"
                  value={title}
                  onChange={(e) => {
                    setTitle(e.target.value);
                    if (errors.title) setErrors((p) => ({ ...p, title: "" }));
                  }}
                  onFocus={() => setIsFocused(true)}
                  onBlur={() => setIsFocused(false)}
                  placeholder="What needs to be done?"
                  className="w-full bg-transparent border-none focus:outline-none text-white text-xl font-semibold placeholder-slate-500"
                />
              </div>
              {errors.title && (
                <span className="text-red-400 text-xs ml-5 flex items-center gap-1">
                  <AlertCircle size={12} />
                  {errors.title}
                </span>
              )}
            </div>

            {/* Description Section */}
            <div className="flex flex-col gap-1">
              <textarea
                ref={textareaRef}
                value={description}
                onChange={(e) => {
                  setDescription(e.target.value);
                  if (errors.description)
                    setErrors((p) => ({ ...p, description: "" }));
                }}
                placeholder="Add details (optional)"
                className={`w-full bg-slate-800/30 border rounded-xl px-4 py-3 text-slate-300 placeholder-slate-600 focus:outline-none transition-all text-sm resize-none ${errors.description ? "border-red-500/30" : "border-slate-700/50"}`}
              />
            </div>
          </div>

          <Button
            type="submit"
            disabled={isSubmitting}
            className={`h-12 w-12 rounded-xl transition-all ${
              !title
                ? "bg-slate-800 text-slate-600"
                : "bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50"
            }`}
          >
            <Plus
              size={20}
              strokeWidth={3}
              className={isSubmitting ? "animate-spin" : ""}
            />
          </Button>
        </div>

        <div className="mt-4 space-y-4 pt-4 border-t border-slate-800/50">
          {/* Tags Display */}
          <div className="flex flex-wrap gap-2">
            {tags.map((tag) => (
              <span
                key={tag}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-medium rounded-full"
              >
                <Hash size={10} /> {tag}
                <button
                  type="button"
                  onClick={() => removeTag(tag)}
                  className="hover:text-white"
                >
                  <X size={12} />
                </button>
              </span>
            ))}

            {tags.length === 0 && (
              <span className="text-slate-600 text-xs italic">Add tags to categorize your task</span>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            {/* Priority */}
            <div className="flex flex-col gap-1">
              <span className="text-xs font-medium text-slate-500 ml-1">
                Priority
              </span>
              <div className="flex gap-1 p-1 bg-slate-800/50 rounded-lg border border-slate-700/50">
                {(["low", "medium", "high"] as const).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPriority(p)}
                    className={`flex-1 py-1.5 text-[10px] font-bold rounded-md transition-all uppercase ${
                      priority === p
                        ? priorityMap[p]
                        : "text-slate-500 hover:bg-slate-700/50"
                    }`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            {/* Category */}
            <div className="flex flex-col gap-1">
              <span className="text-xs font-medium text-slate-500 ml-1">
                Category
              </span>
              <div className="relative">
                <Folder
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600"
                  size={14}
                />
                <input
                  type="text"
                  value={category}
                  onChange={(e) => {
                    setCategory(e.target.value);
                    if (errors.category)
                      setErrors((p) => ({ ...p, category: "" }));
                  }}
                  placeholder="Work, Personal..."
                  className={`w-full bg-slate-800/30 border rounded-lg pl-9 pr-3 py-2 text-sm text-slate-300 focus:outline-none transition-all ${errors.category ? "border-red-500/30" : "border-slate-700/50"}`}
                />
              </div>
            </div>

            {/* Tag Input */}
            <div className="flex flex-col gap-1">
              <span className="text-xs font-medium text-slate-500 ml-1">
                Add Tags
              </span>
              <div className="relative">
                <Hash
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600"
                  size={14}
                />
                <input
                  type="text"
                  value={tagInput}
                  onKeyDown={handleAddTag}
                  onChange={(e) => setTagInput(e.target.value)}
                  placeholder="Press Enter to add..."
                  className="w-full bg-slate-800/30 border border-slate-700/50 rounded-lg pl-9 pr-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-indigo-500/30 transition-all"
                />
              </div>
            </div>

            {/* Due Date */}
            <div className="flex flex-col gap-1">
              <span className="text-xs font-medium text-slate-500 ml-1">
                Due Date
              </span>
              <div className="relative group">
                <Calendar
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600 pointer-events-none"
                  size={14}
                />
                <input
                  type="datetime-local"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="w-full bg-slate-800/30 border border-slate-700/50 rounded-lg pl-9 pr-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-indigo-500/30 transition-all [color-scheme:dark] cursor-pointer"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.form>
  );
};

export default TaskInput;
