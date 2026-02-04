"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { X, Folder, Calendar, Repeat, Hash, Flag, Target } from "lucide-react";

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
      reminder_type?: string;
      reminder_offset?: number;
      reminder_time?: string;
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
    reminder_type?: string;
    reminder_offset?: number;
    reminder_time?: string;
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
  const [endCondition, setEndCondition] = useState<"none" | "after" | "on">("none");
  const [endAfterCount, setEndAfterCount] = useState<number>(1);
  const [endDate, setEndDate] = useState<string>("");
  const [hasReminder, setHasReminder] = useState(false);
  const [reminderType, setReminderType] = useState<"before_due" | "specific_time">("before_due");
  const [reminderOffset, setReminderOffset] = useState<number>(60); // Default to 60 minutes before due
  const [reminderTime, setReminderTime] = useState<string>("");

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

      // Parse the recurrence rule to extract end conditions if present
      if (initialData.recurrence_rule) {
        const ruleParts = initialData.recurrence_rule.split(';');
        const countPart = ruleParts.find(part => part.startsWith('COUNT='));
        const untilPart = ruleParts.find(part => part.startsWith('UNTIL='));

        if (countPart) {
          const countValue = parseInt(countPart.split('=')[1]);
          setEndCondition("after");
          setEndAfterCount(countValue);
        } else if (untilPart) {
          const untilValue = untilPart.split('=')[1];
          setEndCondition("on");
          // Convert UNTIL format to datetime-local format (YYYY-MM-DDTHH:mm)
          if (untilValue.length >= 8) {
            const year = untilValue.substring(0, 4);
            const month = untilValue.substring(4, 6);
            const day = untilValue.substring(6, 8);
            let timePart = "T00:00";
            if (untilValue.length >= 13) {
              const hour = untilValue.substring(9, 11);
              const minute = untilValue.substring(11, 13);
              timePart = `T${hour}:${minute}`;
            }
            setEndDate(`${year}-${month}-${day}${timePart}`);
          }
        } else {
          setEndCondition("none");
        }
      } else {
        setEndCondition("none");
      }

      // Handle reminder settings if they exist in the initial data
      if (initialData.reminder_type) {
        setHasReminder(true);
        if (initialData.reminder_type === "BEFORE_DUE") {
          setReminderType("before_due");
          setReminderOffset(initialData.reminder_offset || 60);
        } else if (initialData.reminder_time) {
          setReminderType("specific_time");
          setReminderTime(formatForInput(initialData.reminder_time));
        }
      } else {
        setHasReminder(false);
      }
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
      setEndCondition("none");
      setEndAfterCount(1);
      setEndDate("");
      setHasReminder(false);
      setReminderType("before_due");
      setReminderOffset(60);
      setReminderTime("");
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

    // Construct the recurrence rule based on selections
    let finalRecurrenceRule = recurrenceRule;

    if (isRecurring && recurrenceRule) {
      // Add end condition if specified
      if (endCondition === "after" && endAfterCount > 0) {
        finalRecurrenceRule = `${recurrenceRule};COUNT=${endAfterCount}`;
      } else if (endCondition === "on" && endDate) {
        // Convert the date to the required format for UNTIL (YYYYMMDDTHHMMSSZ)
        const dateObj = new Date(endDate);
        const untilDate = dateObj.toISOString().replace(/[-:]/g, '').substring(0, 15) + 'Z';
        finalRecurrenceRule = `${recurrenceRule};UNTIL=${untilDate}`;
      }
    }

    // Prepare reminder data
    let reminderData: {
      reminder_type?: string;
      reminder_offset?: number;
      reminder_time?: string;
    } = {};

    if (hasReminder) {
      if (reminderType === "before_due") {
        reminderData = {
          reminder_type: "BEFORE_DUE",
          reminder_offset: reminderOffset,
        };
      } else if (reminderType === "specific_time" && reminderTime) {
        reminderData = {
          reminder_type: "SPECIFIC_TIME",
          reminder_time: reminderTime,
        };
      }
    }

    onSubmit(
      {
        title,
        description,
        priority,
        category: category || undefined,
        tags: tags.length > 0 ? tags : undefined,
        due_date: dueDate || undefined,
        is_recurring: isRecurring,
        recurrence_rule: isRecurring && finalRecurrenceRule ? finalRecurrenceRule : undefined,
        // Add reminder data
        ...reminderData,
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
            className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm"
            onClick={onClose}
          />

          <motion.div
            className="relative bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
            initial={{ scale: 0.95, y: 20, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.95, y: 20, opacity: 0 }}
          >
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-500" />

            {/* Header */}
            <div className="p-6 md:p-8 flex justify-between items-start border-b border-slate-700/50">
              <div>
                <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight">
                  {initialData ? "Edit Task" : "Create New Task"}
                </h2>
                <p className="text-slate-500 text-xs uppercase tracking-wider font-medium mt-1">
                  {initialData
                    ? "Update your existing task"
                    : "Define a new objective"}
                </p>
              </div>
              <button
                onClick={onClose}
                className="p-2 rounded-lg bg-slate-700/50 text-slate-400 hover:text-white hover:bg-slate-600/50 transition-all"
              >
                <X size={20} />
              </button>
            </div>

            {/* Content */}
            <div className="p-6 md:p-8 overflow-y-auto">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-slate-400 ml-1">
                      Title *
                    </label>
                    <input
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      required
                      className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none transition-all"
                      placeholder="What needs to be done?"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-slate-400 ml-1">
                      Category
                    </label>
                    <div className="relative">
                      <Folder
                        size={14}
                        className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
                      />
                      <input
                        type="text"
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        className="w-full pl-11 pr-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none transition-all"
                        placeholder="e.g. Work, Personal"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-medium text-slate-400 ml-1">
                    Description
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-slate-300 text-sm focus:border-indigo-500/50 outline-none min-h-[80px] resize-none"
                    placeholder="Add details..."
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <label className="text-xs font-medium text-slate-400 ml-1">
                      Priority
                    </label>
                    <div className="flex gap-2 p-1.5 bg-slate-800/50 rounded-lg border border-slate-700/50">
                      {["low", "medium", "high"].map((p) => (
                        <button
                          key={p}
                          type="button"
                          onClick={() => setPriority(p)}
                          className={`flex-1 py-2 text-xs font-medium rounded-md transition-all uppercase ${
                            priority === p
                              ? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-[0_0_10px_rgba(99,102,241,0.3)]"
                              : "text-slate-500 hover:text-slate-300 hover:bg-slate-700/50"
                          }`}
                        >
                          {p}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="space-y-3">
                    <label className="text-xs font-medium text-slate-400 ml-1">
                      Deadline
                    </label>
                    <div className="relative">
                      <Calendar
                        size={14}
                        className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
                      />
                      <input
                        type="datetime-local"
                        value={dueDate}
                        onChange={(e) => setDueDate(e.target.value)}
                        className="w-full pl-11 pr-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none [color-scheme:dark]"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <label className="text-xs font-medium text-slate-400 ml-1">
                    Tags
                  </label>
                  <div className="flex flex-wrap gap-2 mb-2">
                    {tags.map((tag) => (
                      <span
                        key={tag}
                        className="flex items-center gap-1.5 px-3 py-1 bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-medium rounded-full"
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
                    className="w-full px-4 py-2.5 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none"
                    placeholder="Add tag and press Enter..."
                  />
                </div>

                <div className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Repeat size={16} className="text-indigo-400" />
                      <span className="text-sm font-medium text-slate-300">
                        Recurring Task
                      </span>
                    </div>
                    <input
                      type="checkbox"
                      checked={isRecurring}
                      onChange={(e) => setIsRecurring(e.target.checked)}
                      className="w-5 h-5 accent-indigo-600"
                    />
                  </div>

                  {isRecurring && (
                    <div className="mt-4 space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <label className="text-xs font-medium text-slate-400 ml-1">
                            Frequency
                          </label>
                          <select
                            value={recurrenceRule || ''}
                            onChange={(e) => {
                              setRecurrenceRule(e.target.value);
                            }}
                            className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none"
                          >
                            <option value="">Select frequency</option>
                            <option value="FREQ=DAILY">Daily</option>
                            <option value="FREQ=WEEKLY">Weekly</option>
                            <option value="FREQ=MONTHLY">Monthly</option>
                            <option value="FREQ=YEARLY">Yearly</option>
                          </select>
                        </div>

                        <div className="space-y-2">
                          <label className="text-xs font-medium text-slate-400 ml-1">
                            End Condition
                          </label>
                          <select
                            value={endCondition}
                            onChange={(e) => {
                              const value = e.target.value as "none" | "after" | "on";
                              setEndCondition(value);
                            }}
                            className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none"
                          >
                            <option value="none">No end date</option>
                            <option value="after">End after</option>
                            <option value="on">End on</option>
                          </select>

                          {endCondition === "after" && (
                            <div className="mt-2 flex items-center gap-2">
                              <input
                                type="number"
                                min="1"
                                value={endAfterCount}
                                onChange={(e) => setEndAfterCount(parseInt(e.target.value) || 1)}
                                className="w-20 px-3 py-2 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none"
                              />
                              <span className="text-sm text-slate-400">occurrences</span>
                            </div>
                          )}

                          {endCondition === "on" && (
                            <div className="mt-2">
                              <input
                                type="datetime-local"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className="w-full px-3 py-2 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none [color-scheme:dark]"
                              />
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Reminder Section */}
                <div className="p-4 bg-slate-800/30 border border-slate-700/50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-indigo-400">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                      </svg>
                      <span className="text-sm font-medium text-slate-300">
                        Task Reminder
                      </span>
                    </div>
                    <input
                      type="checkbox"
                      checked={hasReminder}
                      onChange={(e) => setHasReminder(e.target.checked)}
                      className="w-5 h-5 accent-indigo-600"
                    />
                  </div>

                  {hasReminder && (
                    <div className="mt-4 space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <label className="text-xs font-medium text-slate-400 ml-1">
                            Reminder Type
                          </label>
                          <select
                            value={reminderType}
                            onChange={(e) => setReminderType(e.target.value as "before_due" | "specific_time")}
                            className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none"
                          >
                            <option value="before_due">Before Due Date</option>
                            <option value="specific_time">Specific Time</option>
                          </select>
                        </div>

                        {reminderType === "before_due" ? (
                          <div className="space-y-2">
                            <label className="text-xs font-medium text-slate-400 ml-1">
                              Reminder Offset (minutes)
                            </label>
                            <input
                              type="number"
                              min="1"
                              value={reminderOffset}
                              onChange={(e) => setReminderOffset(parseInt(e.target.value) || 1)}
                              className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none"
                              placeholder="Minutes before due date"
                            />
                          </div>
                        ) : (
                          <div className="space-y-2">
                            <label className="text-xs font-medium text-slate-400 ml-1">
                              Reminder Time
                            </label>
                            <div className="relative">
                              <Calendar
                                size={14}
                                className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
                              />
                              <input
                                type="datetime-local"
                                value={reminderTime}
                                onChange={(e) => setReminderTime(e.target.value)}
                                className="w-full pl-11 pr-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg text-white text-sm focus:border-indigo-500/50 outline-none [color-scheme:dark]"
                              />
                            </div>
                          </div>
                        )}
                      </div>

                      <div className="text-xs text-slate-500 p-3 bg-slate-800/30 rounded-lg">
                        {reminderType === "before_due"
                          ? `A reminder will be sent ${reminderOffset} minutes before the due date.`
                          : `A reminder will be sent at the specified time.`}
                      </div>
                    </div>
                  )}
                </div>
              </form>
            </div>

            {/* Footer */}
            <div className="p-6 md:p-8 bg-slate-800/30 border-t border-slate-700/50 flex gap-4">
              <Button
                onClick={onClose}
                variant="outline"
                className="flex-1 py-5 bg-slate-700/50 hover:bg-slate-600/50 text-white text-sm font-medium rounded-lg"
              >
                Cancel
              </Button>
              <Button
                onClick={handleSubmit}
                disabled={!title.trim()}
                className="flex-1 py-5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-sm font-medium rounded-lg disabled:opacity-50 shadow-lg shadow-indigo-500/20"
              >
                {initialData ? "Save Changes" : "Create Task"}
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default TaskFormModal;
