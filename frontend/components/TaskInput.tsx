"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Plus, Calendar, X, Hash, LayoutGrid, AlertCircle } from "lucide-react";

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

  // --- STRICT VALIDATION (AB SAB KUCH REQUIRED HAI) ---
  const validate = () => {
    const newErrors: { [key: string]: string } = {};

    if (!title.trim()) {
      newErrors.title = "Title is required";
    } else if (!description.trim()) {
      newErrors.description = "Description is required";
    } else if (!category.trim()) {
      newErrors.category = "Category is required";
    } else if (tags.length === 0) {
      newErrors.tags = "At least one tag is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleAddTag = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      const val = tagInput.trim().replace(",", "");
      if (val && !tags.includes(val)) {
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

    // Pehle validate karein
    const isValid = validate();

    if (!isValid) {
      // Agar koi bhi ek error milti hai, toh form shake karega aur logic ruk jayega
      setIsShaking(true);
      setTimeout(() => setIsShaking(false), 500);
      return;
    }

    if (isSubmitting) return;

    setIsSubmitting(true);

    // API ya Parent function call
    onAddTask({
      title: title.trim(),
      description: description.trim(),
      priority,
      category: category.trim(),
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
      className={`relative bg-slate-900/60 backdrop-blur-2xl rounded-[28px] mb-10 overflow-hidden border transition-all duration-500 ${
        Object.keys(errors).length > 0
          ? "border-red-500/50"
          : isFocused
            ? "border-blue-500/40"
            : "border-white/5"
      }`}
      onSubmit={handleSubmit}
    >
      <div className="p-6">
        <div className="flex gap-4 items-start">
          <div className="flex-1 space-y-4">
            {/* Title Section */}
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-3">
                <div
                  className={`w-2 h-2 rounded-full ${errors.title ? "bg-red-500" : "bg-blue-500"}`}
                />
                <input
                  type="text"
                  value={title}
                  onChange={(e) => {
                    setTitle(e.target.value);
                    if (errors.title) setErrors((p) => ({ ...p, title: "" }));
                  }}
                  placeholder="Task Title (Required)"
                  className="w-full bg-transparent border-none focus:outline-none text-white text-xl font-bold placeholder-slate-700"
                />
              </div>
              {errors.title && (
                <span className="text-red-400 text-[10px] ml-5 uppercase font-bold tracking-widest flex items-center gap-1">
                  <AlertCircle size={10} />
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
                placeholder="Detailed Description (Required)"
                className={`w-full bg-white/[0.02] border rounded-2xl px-4 py-3 text-slate-300 placeholder-slate-700 focus:outline-none transition-all text-sm resize-none ${errors.description ? "border-red-500/30" : "border-white/5"}`}
              />
              {errors.description && (
                <span className="text-red-400 text-[10px] uppercase font-bold tracking-widest pl-1">
                  {errors.description}
                </span>
              )}
            </div>
          </div>

          <Button
            type="submit"
            disabled={isSubmitting}
            className={`h-14 w-14 rounded-2xl transition-all ${
              !title || !description || !category || tags.length === 0
                ? "bg-slate-800 text-slate-600"
                : "bg-blue-600 text-white shadow-lg shadow-blue-600/20"
            }`}
          >
            <Plus
              size={28}
              strokeWidth={3}
              className={isSubmitting ? "animate-spin" : ""}
            />
          </Button>
        </div>

        <div className="mt-6 space-y-6 pt-6 border-t border-white/5">
          {/* Tags Display */}
          <div className="flex flex-col gap-2">
            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="flex items-center gap-1.5 px-3 py-1 bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-medium rounded-full"
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
            </div>
            {errors.tags && (
              <span className="text-red-400 text-[10px] uppercase font-bold tracking-widest">
                {errors.tags}
              </span>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-end">
            {/* Priority */}
            <div className="flex flex-col gap-2">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500 ml-1">
                Urgency
              </span>
              <div className="flex gap-1 p-1 bg-black/40 rounded-xl border border-white/5">
                {(["low", "medium", "high"] as const).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPriority(p)}
                    className={`flex-1 py-1.5 text-[10px] font-black rounded-lg transition-all uppercase ${priority === p ? priorityMap[p] : "text-slate-500 hover:bg-white/5"}`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            {/* Category */}
            <div className="flex flex-col gap-2">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500 ml-1">
                Category (Required)
              </span>
              <div className="relative">
                <LayoutGrid
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
                  placeholder="Work, Life..."
                  className={`w-full bg-black/40 border rounded-xl pl-9 pr-3 py-2 text-sm text-slate-300 focus:outline-none transition-all ${errors.category ? "border-red-500/30" : "border-white/5"}`}
                />
              </div>
              {errors.category && (
                <span className="text-red-400 text-[9px] uppercase font-bold tracking-widest mt-1">
                  {errors.category}
                </span>
              )}
            </div>

            {/* Tag Input */}
            <div className="flex flex-col gap-2">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500 ml-1">
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
                  placeholder="Enter to add..."
                  className="w-full bg-black/40 border border-white/5 rounded-xl pl-9 pr-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-blue-500/30 transition-all"
                />
              </div>
            </div>

            {/* Due Date */}
            <div className="flex flex-col gap-2">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500 ml-1">
                Deadline
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
                  className="w-full bg-black/40 border border-white/5 rounded-xl pl-9 pr-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-blue-500/30 transition-all [color-scheme:dark] cursor-pointer"
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
