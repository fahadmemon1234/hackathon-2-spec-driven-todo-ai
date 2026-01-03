"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { X, Tag } from "lucide-react";
import { text } from "stream/consumers";

interface TaskFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (
    taskData: {
      title: string;
      description: string;
      priority: string;
      category?: string;
    },
    id?: string
  ) => void;
  initialData?: {
    id: string;
    title: string;
    description: string;
    priority: string;
    category?: string;
  };
}

const TaskFormModal: React.FC<TaskFormModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
}) => {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(
    initialData?.description || ""
  );
  const [priority, setPriority] = useState(initialData?.priority || "medium");
  const [category, setCategory] = useState(initialData?.category || "");

  // Reset form when modal opens with new initialData
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title);
      setDescription(initialData.description);
      setPriority(initialData.priority || "medium");
      setCategory(initialData.category || "");
    } else {
      setTitle("");
      setDescription("");
      setPriority("medium");
      setCategory("");
    }
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (initialData) {
      // This is an update operation
      onSubmit(
        {
          title,
          description,
          priority,
          category: category || undefined,
        },
        initialData.id
      );
    } else {
      // This is a create operation
      onSubmit({
        title,
        description,
        priority,
        category: category || undefined,
      });
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-[9999] flex items-start justify-center p-4 overflow-y-auto pt-12 pb-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="fixed inset-0 bg-[#020617]/90 backdrop-blur-xl"
            onClick={onClose}
          />

          <motion.div
            className="relative bg-slate-900/50 border border-white/10 w-full max-w-lg rounded-[32px] shadow-2xl backdrop-blur-2xl"
            initial={{ scale: 0.9, y: 20, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.9, y: 20, opacity: 0 }}
            transition={{ type: "spring", damping: 25, stiffness: 400 }}
          >
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50 rounded-t-[32px]" />

            <div className="p-8">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-white tracking-tight italic">
                    {initialData ? "Refine Task" : "New Objective"}
                  </h2>
                  <p className="text-slate-500 text-[10px] uppercase tracking-[0.2em] font-black mt-1">
                    {initialData ? "Modify milestone" : "Establish a target"}
                  </p>
                </div>
                <button
                  onClick={onClose}
                  className="p-2 rounded-full bg-white/5 text-slate-400 hover:text-white transition-all"
                >
                  <X size={18} />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="grid grid-cols-2 gap-4">
                  <div className="group space-y-2">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1 group-focus-within:text-blue-400 transition-colors">
                      Title *
                    </label>
                    <input
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      required
                      className="w-full px-4 py-3 bg-slate-950/40 border border-white/5 rounded-2xl text-white text-sm focus:border-blue-500/50 outline-none transition-all placeholder:text-slate-600 shadow-inner"
                      placeholder="Task Name"
                    />
                  </div>

                  <div className="group space-y-2">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1 group-focus-within:text-blue-400 transition-colors">
                      Category
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        className="w-full px-4 py-3 bg-slate-950/40 border border-white/5 rounded-2xl text-white text-sm focus:border-blue-500/50 outline-none transition-all placeholder:text-slate-600 shadow-inner pl-10"
                        placeholder="e.g. Work"
                      />
                      <Tag
                        size={14}
                        className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-500 transition-colors"
                      />
                    </div>
                  </div>
                </div>

                <div className="group space-y-2">
                  <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1 group-focus-within:text-blue-400 transition-colors">
                    Description
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full px-5 py-3.5 bg-slate-950/40 border border-white/5 rounded-2xl text-slate-300 text-sm focus:border-blue-500/50 outline-none transition-all min-h-[80px] max-h-[120px] resize-none placeholder:text-slate-600 shadow-inner"
                    placeholder="Briefly describe the task..."
                  />
                </div>

                <div className="space-y-3">
                  <label className="text-[10px] font-bold uppercase tracking-widest text-slate-500 ml-1">
                    Priority Level
                  </label>
                  <div className="flex gap-2 p-1.5 bg-slate-950/60 rounded-2xl border border-white/5">
                    {[
                      { id: "low", label: "Low", color: "bg-slate-500" },
                      { id: "medium", label: "Medium", color: "bg-amber-500" },
                      { id: "high", label: "High", color: "bg-blue-600" },
                    ].map((p) => (
                      <button
                        key={p.id}
                        type="button"
                        onClick={() => setPriority(p.id)}
                        className={`flex-1 py-2 text-[10px] font-black rounded-xl transition-all duration-300 uppercase ${
                          priority === p.id
                            ? `${p.color} text-white shadow-lg`
                            : "text-slate-500 hover:text-slate-300"
                        }`}
                      >
                        {p.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex gap-3 pt-2">
                  <Button
                    type="button"
                    onClick={onClose}
                    className="flex-[2] py-4 bg-white/5 hover:bg-white/10 text-white text-[11px] font-black rounded-2xl shadow-xl transition-all active:scale-95 uppercase tracking-widest"
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    className="flex-[2] py-4 bg-blue-600 hover:bg-blue-500 text-white text-[11px] font-black rounded-2xl shadow-xl transition-all active:scale-95 uppercase tracking-widest"
                  >
                    {initialData ? "Update" : "Initialize Task"}
                  </Button>
                </div>
              </form>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default TaskFormModal;
