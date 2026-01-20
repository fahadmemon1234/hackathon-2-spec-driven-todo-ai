"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { api } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import Navbar from "@/components/Navbar";
import TaskInput from "@/components/TaskInput";
import TaskList from "@/components/TaskList";
import TaskFormModal from "@/components/TaskFormModal";
import ProtectedRoute from "@/components/ProtectedRoute";
import PremiumLoader from "@/components/PremiumLoader";
import {
  CheckCircle,
  Circle,
  Clock,
  Plus,
  Filter,
  Sparkles,
} from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { LayoutGrid } from "lucide-react";

const Dashboard = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState<
    "all" | "pending" | "completed"
  >("all");
  const [sortBy, setSortBy] = useState<"created" | "title">("created");
  const [showLoader, setShowLoader] = useState(true);
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<any>(null);

  // Simulate loading completion for the premium loader
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowLoader(false);
    }, 2500); // Show loader for 2.5 seconds

    return () => clearTimeout(timer);
  }, []);

  // Fetch tasks when component mounts
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const tasksData = await api.getTasks();
        setTasks(tasksData);
      } catch (error) {
        console.error("Error fetching tasks:", error);
        toast.error("Failed to load tasks");
      } finally {
        setLoading(false);
      }
    };

    if (!showLoader) {
      fetchTasks();
    }
  }, [showLoader]);

  const handleAddTask = async (taskData: {
    title: string;
    description?: string;
    priority?: string;
    category?: string;
    tags?: string[];
    due_date?: string;
    is_recurring?: boolean;
    recurrence_rule?: string;
  }) => {
    try {
      const newTask = await api.createTask(taskData);
      setTasks([newTask, ...tasks]);
      toast.success("Task created successfully");
    } catch (error) {
      console.error("Error adding task:", error);
      toast.error("Failed to create task");
    }
  };

  const handleUpdateTask = async (taskData: {
    id: string;
    title?: string;
    description?: string;
    completed?: boolean;
    priority?: string;
    category?: string;
    tags?: string[];
    due_date?: string;
    is_recurring?: boolean;
    recurrence_rule?: string;
    next_occurrence?: string;
  }) => {
    try {
      const updatedTask = await api.updateTask(taskData);
      setTasks(
        tasks.map((task) => (task.id === taskData.id ? updatedTask : task))
      );
      if (taskData.completed !== undefined) {
        if (taskData.completed) {
          toast.success("Task completed!");
        } else {
          toast.info("Task marked as pending");
        }
      } else {
        toast.success("Task updated successfully");
      }
    } catch (error) {
      console.error("Error updating task:", error);
      toast.error("Failed to update task");
    }
  };

  // Handle opening the edit form with pre-filled data
  const handleEditTask = (task: any) => {
    setEditingTask({
      id: task.id,
      title: task.title,
      description: task.description,
      priority: task.priority,
      category: task.category,
      tags: task.tags,
      due_date: task.due_date,
      is_recurring: task.is_recurring,
      recurrence_rule: task.recurrence_rule
    });
    setIsTaskModalOpen(true);
    localStorage.setItem("openedModel", "true");
    // if (typeof window !== "undefined") {
    //   localStorage.setItem("openedModel", "true");
    // }
  };

  // Handle closing the task form modal
  const handleCloseTaskModal = () => {
    setIsTaskModalOpen(false);
    setEditingTask(null);
    localStorage.removeItem("openedModel");
    // if (typeof window !== "undefined") {
    //   localStorage.removeItem("openedModel");
    // }
  };

  // Handle submitting the task form (both create and update)
  const handleSubmitTask = async (
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
    id?: string
  ) => {
    if (id) {
      // This is an update operation
      await handleUpdateTask({ id, ...taskData });
    } else {
      // This is a create operation
      await handleAddTask(taskData);
    }
    handleCloseTaskModal();
  };

  const handleToggleComplete = async (id: string) => {
    try {
      const updatedTask = await api.toggleComplete(id);
      setTasks(tasks.map((task) => (task.id === id ? updatedTask : task)));

      const task = tasks.find((t) => t.id === id);
      if (task) {
        if (task.completed) {
          toast.info("Task marked as pending");
        } else {
          toast.success("Task completed!");
        }
      }
    } catch (error) {
      console.error("Error toggling task completion:", error);
      toast.error("Failed to update task status");
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      const success = await api.deleteTask(id);
      if (success) {
        setTasks(tasks.filter((task) => task.id !== id));
        toast.success("Task deleted successfully");
      }
    } catch (error) {
      console.error("Error deleting task:", error);
      toast.error("Failed to delete task");
    }
  };

  // Calculate dashboard statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((task) => task.completed).length;
  const inProgressTasks = totalTasks - completedTasks;

  // Filter tasks based on active filter
  const filteredTasks = tasks.filter((task) => {
    if (activeFilter === "pending") return !task.completed;
    if (activeFilter === "completed") return task.completed;
    return true; // 'all'
  });

  // Sort tasks based on sort option
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    if (sortBy === "title") {
      return a.title.localeCompare(b.title);
    } else {
      // 'created'
      return (
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      ); // Newest first
    }
  });

  if (showLoader) {
    return <PremiumLoader onComplete={() => setShowLoader(false)} />;
  }

  // 1. Pehle tagged tasks ko filter karein
const taggedTasks = tasks.filter(task => 
  task.tags && Array.isArray(task.tags) && task.tags.length > 0
);

// 2. Ab stats sirf filtered tasks se calculate karein
const totalTagged = taggedTasks.length;
const inProgressTagged = taggedTasks.filter(t => !t.completed).length;
const completedTagged = taggedTasks.filter(t => t.completed).length;

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#020617] text-slate-200 relative overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-600/5 blur-[120px] rounded-full" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-indigo-600/5 blur-[120px] rounded-full" />
        </div>

        <Navbar />

        <div className="container relative z-10 mx-auto px-6 pt-32 pb-20 max-w-6xl">
          <div className="flex flex-col lg:flex-row justify-between items-start lg:items-end gap-6 mb-12">
            <div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-3 mb-3"
              >
                <div className="p-2 bg-blue-600/10 rounded-lg">
                  <Sparkles className="text-blue-500 w-5 h-5" />
                </div>
                <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-blue-500/80">
                  Personal Workspace
                </span>
              </motion.div>
              <h1 className="text-4xl md:text-5xl font-bold text-white tracking-tight">
                Task{" "}
                <span className="text-slate-500 font-light text-3xl md:text-4xl">
                  Dashboard
                </span>
              </h1>
            </div>

            <div className="flex flex-wrap items-center gap-3 w-full lg:w-auto">
              <div className="relative group flex-1 lg:flex-none">
                <select
                  value={activeFilter}
                  onChange={(e) => setActiveFilter(e.target.value as any)}
                  className="w-full bg-slate-900/40 border border-white/10 rounded-xl px-5 py-2.5 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600/50 appearance-none pr-10 hover:bg-slate-800/60 transition-all cursor-pointer"
                >
                  <option value="all">All Tasks</option>
                  <option value="pending">Pending</option>
                  <option value="completed">Completed</option>
                </select>
                <Filter className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4 pointer-events-none group-hover:text-blue-400 transition-colors" />
              </div>

              <div className="relative group flex-1 lg:flex-none">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="w-full bg-slate-900/40 border border-white/10 rounded-xl px-5 py-2.5 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600/50 appearance-none pr-10 hover:bg-slate-800/60 transition-all cursor-pointer"
                >
                  <option value="created">Sort by Date</option>
                  <option value="title">Sort by Title</option>
                </select>
                <LayoutGrid className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4 pointer-events-none group-hover:text-blue-400 transition-colors" />
              </div>
            </div>
          </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-12">
    {[
      {
        icon: Clock,
        label: "Tagged Tasks", // Label update kiya
        val: totalTagged,
        color: "text-blue-500",
        glow: "group-hover:shadow-[0_0_20px_rgba(59,130,246,0.15)]",
      },
      {
        icon: Circle,
        label: "Active Tags",
        val: inProgressTagged,
        color: "text-amber-500",
        glow: "group-hover:shadow-[0_0_20px_rgba(245,158,11,0.15)]",
      },
      {
        icon: CheckCircle,
        label: "Tagged Done",
        val: completedTagged,
        color: "text-emerald-500",
        glow: "group-hover:shadow-[0_0_20px_rgba(16,185,129,0.15)]",
      },
    ].map((stat, i) => (
      <motion.div
        key={i}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: i * 0.1 }}
        className={`group bg-slate-900/40 border border-white/5 rounded-[24px] p-6 backdrop-blur-xl transition-all duration-500 hover:border-white/10 ${stat.glow}`}
      >
        <div className="flex items-center gap-4">
          <div
            className={`p-4 rounded-2xl bg-slate-800/40 ${stat.color} group-hover:scale-110 transition-transform duration-500 shadow-inner`}
          >
            <stat.icon size={22} strokeWidth={2.5} />
          </div>
          <div>
            <p className="text-slate-500 text-[10px] uppercase tracking-[0.25em] font-black">
              {stat.label}
            </p>
            <div className="flex items-baseline gap-1">
              <p className="text-3xl font-black text-white mt-1 leading-none tracking-tight">
                {stat.val}
              </p>
              <div className={`w-1 h-1 rounded-full ${stat.color.replace('text', 'bg')} animate-pulse`} />
            </div>
          </div>
        </div>
      </motion.div>
    ))}
  </div>

          <main className="relative z-10">
            <div className="mb-10">
              <TaskInput onAddTask={handleAddTask} />
            </div>

            {loading ? (
              <div className="grid gap-4 mt-8">
                {[...Array(3)].map((_, i) => (
                  <div
                    key={i}
                    className="h-24 bg-white/5 border border-white/5 rounded-2xl animate-pulse"
                  />
                ))}
              </div>
            ) : sortedTasks.length === 0 ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center justify-center py-24 text-center border border-dashed border-white/10 rounded-[32px] bg-white/[0.01]"
              >
                <div className="relative mb-6">
                  <div className="absolute inset-0 bg-blue-500/20 blur-2xl rounded-full" />
                  <div className="relative w-20 h-20 bg-slate-900 border border-white/10 rounded-2xl flex items-center justify-center text-slate-500">
                    <LayoutGrid size={32} />
                  </div>
                </div>
                <h3 className="text-xl font-bold text-white mb-2 tracking-tight">
                  Focus on what matters
                </h3>
                <p className="text-slate-500 max-w-xs mb-8 text-sm font-light">
                  Your task sanctuary is empty. Create your first milestone to
                  begin your journey.
                </p>
                <Button
                  onClick={() =>
                    document.getElementById("task-input-title")?.focus()
                  }
                  className="bg-blue-600 hover:bg-blue-500 text-white rounded-xl px-8 h-12 font-bold shadow-lg shadow-blue-600/20 active:scale-95 transition-all"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add First Task
                </Button>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-8 space-y-4"
              >
                <AnimatePresence mode="popLayout">
                  <TaskList
                    tasks={sortedTasks}
                    onToggleComplete={handleToggleComplete}
                    onEdit={handleEditTask}
                    onDelete={handleDeleteTask}
                  />
                </AnimatePresence>
              </motion.div>
            )}
          </main>

          <TaskFormModal
            isOpen={isTaskModalOpen}
            onClose={handleCloseTaskModal}
            onSubmit={handleSubmitTask}
            initialData={editingTask}
          />
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default Dashboard;
