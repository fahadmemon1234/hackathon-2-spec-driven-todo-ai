"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { X, Tag, Calendar, Repeat, Hash } from "lucide-react";

interface TaskFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (
    taskData: {
      title: string;
      description?: string;
      priority?: string;
      category?: string;
      tags?: string[];
      due_date?: string;
      is_recurring?: boolean;
      recurrence_rule?: string;
    },
    id?: string,
  ) => void;
  initialData?: {
    id: string;
    title: string;
    description: string;
    priority: string;
    category?: string;
    tags?: string[];
    due_date?: string;
    is_recurring?: boolean;
    recurrence_rule?: string;
  };
}

const TaskFormModal: React.FC<TaskFormModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
}) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");
  const [category, setCategory] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [currentTag, setCurrentTag] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurrenceRule, setRecurrenceRule] = useState("");

  // Function to convert database date string to "YYYY-MM-DDTHH:mm"
  const formatForInput = (dateStr?: string) => {
    if (!dateStr) return "";
    try {
      // Agar date string mein 'Z' ya '+00' hai, toh use remove kar dein
      // taaki browser use UTC na samjhe aur extra hours add na kare
      const cleanDateStr = dateStr.replace("Z", "").split("+")[0];
      const date = new Date(cleanDateStr);

      if (isNaN(date.getTime())) return "";

      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");

      return `${year}-${month}-${day}T${hours}:${minutes}`;
    } catch (e) {
      return "";
    }
  };

  useEffect(() => {
    if (initialData && isOpen) {
      setTitle(initialData.title || "");
      setDescription(initialData.description || "");
      setPriority(initialData.priority || "medium");
      setCategory(initialData.category || "");
      setTags(initialData.tags || []);
      setDueDate(formatForInput(initialData.due_date)); // Proper Formatting
      setIsRecurring(initialData.is_recurring || false);
      setRecurrenceRule(initialData.recurrence_rule || "");
    } else if (!isOpen) {
      // Reset form on close
      setTitle("");
      setDescription("");
      setPriority("medium");
      setCategory("");
      setTags([]);
      setCurrentTag("");
      setDueDate("");
      setIsRecurring(false);
      setRecurrenceRule("");
    }
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleAddTag = () => {
    if (currentTag.trim() && !tags.includes(currentTag.trim())) {
      setTags([...tags, currentTag.trim()]);
      setCurrentTag("");
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter((tag) => tag !== tagToRemove));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(
      {
        title,
        description,
        priority,
        category: category || undefined,
        tags: tags.length > 0 ? tags : undefined,
        due_date: dueDate || undefined,
        is_recurring: isRecurring,
        recurrence_rule:
          isRecurring && recurrenceRule ? recurrenceRule : undefined,
      },
      initialData?.id,
    );
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-[9999] flex items-center justify-center p-4 md:p-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="fixed inset-0 bg-slate-950/90 backdrop-blur-md"
            onClick={onClose}
          />

          <motion.div
            className="relative bg-slate-900 border border-white/10 w-full max-w-2xl rounded-[32px] shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
            initial={{ scale: 0.95, y: 20, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.95, y: 20, opacity: 0 }}
          >
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50" />

            {/* Header */}
            <div className="p-6 md:p-8 flex justify-between items-start border-b border-white/5">
              <div>
                <h2 className="text-2xl font-bold text-white tracking-tight italic">
                  {initialData ? "Refine Task" : "New Objective"}
                </h2>
                <p className="text-slate-500 text-[10px] uppercase tracking-[0.2em] font-black mt-1">
                  {initialData
                    ? "Modify existing milestone"
                    : "Establish a new target"}
                </p>
              </div>
              <button
                onClick={onClose}
                className="p-2 rounded-full bg-white/5 text-slate-400 hover:text-white transition-all"
              >
                <X size={20} />
              </button>
            </div>

            {/* Content */}
            <div className="p-6 md:p-8 overflow-y-auto custom-scrollbar">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1">
                      Title *
                    </label>
                    <input
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      required
                      className="w-full px-4 py-3 bg-black/20 border border-white/5 rounded-2xl text-white text-sm focus:border-blue-500/50 outline-none transition-all"
                      placeholder="What needs to be done?"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1">
                      Category
                    </label>
                    <div className="relative">
                      <Tag
                        size={14}
                        className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600"
                      />
                      <input
                        type="text"
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        className="w-full pl-11 pr-4 py-3 bg-black/20 border border-white/5 rounded-2xl text-white text-sm focus:border-blue-500/50 outline-none transition-all"
                        placeholder="e.g. Work, Health"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1">
                    Description
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full px-4 py-3 bg-black/20 border border-white/5 rounded-2xl text-slate-300 text-sm focus:border-blue-500/50 outline-none min-h-[80px] resize-none"
                    placeholder="Add details..."
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1">
                      Urgency
                    </label>
                    <div className="flex gap-2 p-1.5 bg-black/30 rounded-2xl border border-white/5">
                      {["low", "medium", "high"].map((p) => (
                        <button
                          key={p}
                          type="button"
                          onClick={() => setPriority(p)}
                          className={`flex-1 py-2 text-[10px] font-black rounded-xl transition-all uppercase ${
                            priority === p
                              ? "bg-blue-600 text-white"
                              : "text-slate-500 hover:text-slate-300"
                          }`}
                        >
                          {p}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="space-y-3">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1">
                      Deadline
                    </label>
                    <div className="relative">
                      <Calendar
                        size={14}
                        className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600"
                      />
                      <input
                        type="datetime-local"
                        value={dueDate}
                        onChange={(e) => setDueDate(e.target.value)}
                        className="w-full pl-11 pr-4 py-3 bg-black/20 border border-white/5 rounded-2xl text-white text-sm focus:border-blue-500/50 outline-none [color-scheme:dark]"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1">
                    Tags
                  </label>
                  <div className="flex flex-wrap gap-2 mb-2">
                    {tags.map((tag) => (
                      <span
                        key={tag}
                        className="flex items-center gap-1.5 px-3 py-1 bg-blue-500/10 border border-blue-500/20 text-blue-400 text-[10px] font-bold rounded-full uppercase"
                      >
                        <Hash size={10} /> {tag}
                        <button
                          type="button"
                          onClick={() => handleRemoveTag(tag)}
                          className="hover:text-white"
                        >
                          <X size={12} />
                        </button>
                      </span>
                    ))}
                  </div>
                  <input
                    type="text"
                    value={currentTag}
                    onChange={(e) => setCurrentTag(e.target.value)}
                    onKeyDown={(e) =>
                      e.key === "Enter" && (e.preventDefault(), handleAddTag())
                    }
                    className="w-full px-4 py-2.5 bg-black/20 border border-white/5 rounded-xl text-white text-sm focus:border-blue-500/50 outline-none"
                    placeholder="Add tag..."
                  />
                </div>

                <div className="p-4 bg-white/[0.02] border border-white/5 rounded-2xl">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Repeat size={16} className="text-blue-500" />
                      <span className="text-sm font-medium text-slate-300">
                        Recurring Task
                      </span>
                    </div>
                    <input
                      type="checkbox"
                      checked={isRecurring}
                      onChange={(e) => setIsRecurring(e.target.checked)}
                      className="w-5 h-5 accent-blue-600"
                    />
                  </div>
                  {isRecurring && (
                    <input
                      type="text"
                      value={recurrenceRule}
                      onChange={(e) => setRecurrenceRule(e.target.value)}
                      className="w-full mt-3 px-4 py-3 bg-black/20 border border-white/5 rounded-xl text-white text-sm"
                      placeholder="e.g. FREQ=DAILY"
                    />
                  )}
                </div>
              </form>
            </div>

            {/* Footer */}
            <div className="p-6 md:p-8 bg-black/20 border-t border-white/5 flex gap-4">
              <Button
                onClick={onClose}
                className="flex-1 py-6 bg-white/5 hover:bg-white/10 text-white text-xs font-bold rounded-2xl uppercase tracking-widest"
              >
                Cancel
              </Button>
              <Button
                onClick={handleSubmit}
                disabled={!title.trim()}
                className="flex-1 py-6 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-2xl uppercase tracking-widest disabled:opacity-50"
              >
                {initialData ? "Save Changes" : "Initialize Task"}
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default TaskFormModal;
