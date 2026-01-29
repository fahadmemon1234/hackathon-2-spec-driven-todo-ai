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
  LayoutGrid,
  TrendingUp,
  Target,
  Calendar as CalendarIcon
} from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";

const Dashboard = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState<
    "all" | "pending" | "completed"
  >("all");
  const [sortBy, setSortBy] = useState<"created" | "title">("created");
  const [searchQuery, setSearchQuery] = useState("");
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

  // Fetch tasks when component mounts or when filters change
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const tasksData = await api.getTasks(
          activeFilter === "all" ? undefined : activeFilter,
          undefined, // priority filter
          undefined, // category filter
          sortBy,
          searchQuery // search query
        );
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
  }, [showLoader, activeFilter, sortBy, searchQuery]);

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
      // Clear search query to show the new task
      setSearchQuery("");
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

      // Determine action type for notification
      if (taskData.completed !== undefined) {
        if (taskData.completed) {
          toast.success("Task completed!");
        } else {
          toast.info("Task marked as pending");
        }
      } else {
        toast.success("Task updated successfully");
      }

      // Clear search query to show the updated task
      setSearchQuery("");
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
  };

  // Handle closing the task form modal
  const handleCloseTaskModal = () => {
    setIsTaskModalOpen(false);
    setEditingTask(null);
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

      // Clear search query to show the updated task
      setSearchQuery("");
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
        // Clear search query to show the remaining tasks
        setSearchQuery("");
      }
    } catch (error) {
      console.error("Error deleting task:", error);
      toast.error("Failed to delete task");
    }
  };

  // Calculate dashboard statistics based on all tasks (not filtered)
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

  // Calculate tagged task statistics
  const taggedTasks = sortedTasks.filter(task =>
    task.tags && Array.isArray(task.tags) && task.tags.length > 0
  );
  const totalTagged = taggedTasks.length;
  const inProgressTagged = taggedTasks.filter(t => !t.completed).length;
  const completedTagged = taggedTasks.filter(t => t.completed).length;

  if (showLoader) {
    return <PremiumLoader onComplete={() => setShowLoader(false)} />;
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900/10 to-indigo-900/10 text-slate-200 relative overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-600/5 blur-[120px] rounded-full" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-indigo-600/5 blur-[120px] rounded-full" />
        </div>

        <Navbar />

        <div className="container relative z-10 mx-auto px-4 sm:px-6 pt-32 pb-20 max-w-7xl">
          <div className="flex flex-col lg:flex-row justify-between items-start lg:items-end gap-6 mb-10">
            <div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-3 mb-3"
              >
                <div className="p-2 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg">
                  <Target className="text-white w-5 h-5" />
                </div>
                <span className="text-xs font-bold uppercase tracking-widest text-indigo-400">
                  Productivity Dashboard
                </span>
              </motion.div>
              <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight">
                My <span className="text-indigo-400">Tasks</span>
              </h1>
            </div>

            <div className="flex flex-wrap items-center gap-3 w-full lg:w-auto">
              <div className="relative group flex-1 lg:flex-none">
                <select
                  value={activeFilter}
                  onChange={(e) => setActiveFilter(e.target.value as any)}
                  className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-2.5 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 appearance-none pr-10 hover:bg-slate-700/50 transition-all cursor-pointer"
                >
                  <option value="all">All Tasks</option>
                  <option value="pending">Pending</option>
                  <option value="completed">Completed</option>
                </select>
                <Filter className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4 pointer-events-none group-hover:text-indigo-400 transition-colors" />
              </div>

              <div className="relative group flex-1 lg:flex-none">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-2.5 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 appearance-none pr-10 hover:bg-slate-700/50 transition-all cursor-pointer"
                >
                  <option value="created">Sort by Date</option>
                  <option value="title">Sort by Title</option>
                </select>
                <LayoutGrid className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4 pointer-events-none group-hover:text-indigo-400 transition-colors" />
              </div>

              <div className="relative group flex-1 lg:flex-none">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search tasks..."
                  className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-2.5 pl-10 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 appearance-none hover:bg-slate-700/50 transition-all"
                />
                <svg
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4 pointer-events-none"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  ></path>
                </svg>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
            {[
              {
                icon: Target,
                label: "Total Tasks",
                val: totalTasks,
                color: "text-indigo-400",
              },
              {
                icon: Clock,
                label: "In Progress",
                val: inProgressTasks,
                color: "text-amber-400",
              },
              {
                icon: CheckCircle,
                label: "Completed",
                val: completedTasks,
                color: "text-emerald-400",
              },
              {
                icon: TrendingUp,
                label: "Completion",
                val: totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) + "%" : "0%",
                color: "text-blue-400",
              },
            ].map((stat, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-lg border border-slate-700/50 rounded-2xl p-5 transition-all duration-500 hover:border-slate-600/70"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`p-3 rounded-xl bg-slate-700/50 ${stat.color} transition-transform duration-300 hover:scale-110`}
                  >
                    <stat.icon size={20} strokeWidth={2.5} />
                  </div>
                  <div>
                    <p className="text-slate-500 text-xs uppercase tracking-wider font-medium">
                      {stat.label}
                    </p>
                    <div className="flex items-baseline gap-1">
                      <p className="text-2xl font-bold text-white mt-1 leading-none">
                        {stat.val}
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          <main className="relative z-10">
            <div className="mb-8">
              <TaskInput onAddTask={handleAddTask} />
            </div>

            {loading ? (
              <div className="grid gap-4 mt-8">
                {[...Array(3)].map((_, i) => (
                  <div
                    key={i}
                    className="h-20 bg-slate-800/30 border border-slate-700/50 rounded-xl animate-pulse"
                  />
                ))}
              </div>
            ) : sortedTasks.length === 0 ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center justify-center py-20 text-center border border-dashed border-slate-700/50 rounded-2xl bg-slate-800/20 backdrop-blur-sm"
              >
                <div className="relative mb-6">
                  <div className="absolute inset-0 bg-indigo-500/20 blur-xl rounded-full" />
                  <div className="relative w-16 h-16 bg-slate-800 border border-slate-700/50 rounded-xl flex items-center justify-center text-slate-500">
                    <LayoutGrid size={24} />
                  </div>
                </div>
                <h3 className="text-xl font-bold text-white mb-2 tracking-tight">
                  {searchQuery ? "No matching tasks found" : "No tasks yet"}
                </h3>
                <p className="text-slate-500 max-w-xs mb-6 text-sm">
                  {searchQuery
                    ? "Try adjusting your search terms to find what you're looking for."
                    : "Get started by creating your first task."
                  }
                </p>
                <Button
                  onClick={() => {
                    if (searchQuery) {
                      setSearchQuery(""); // Clear search when clicking "Clear Search"
                    } else {
                      document.getElementById("task-input-title")?.focus(); // Focus on input when adding task
                    }
                  }}
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl px-6 h-11 font-medium shadow-lg shadow-indigo-500/20 active:scale-95 transition-all"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  {searchQuery ? "Clear Search" : "Add Task"}
                </Button>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-6 space-y-4"
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