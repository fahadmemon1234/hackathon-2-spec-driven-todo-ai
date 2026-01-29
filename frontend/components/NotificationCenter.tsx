"use client";

import React, { useState, useEffect } from "react";
import { Bell, Clock, Calendar, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Reminder {
  id: string;
  title: string;
  description?: string;
  due_date: string;
  reminder_time: string;
  task_id: string;
  created_at: string;
}

const NotificationCenter = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data for demonstration - in a real app, this would come from an API
  useEffect(() => {
    // Simulate loading reminders from an API
    const mockReminders: Reminder[] = [
      {
        id: "1",
        title: "Complete project proposal",
        description: "Finish the Q4 project proposal document",
        due_date: "2026-02-01T10:00:00Z",
        reminder_time: "2026-01-31T09:00:00Z",
        task_id: "task-1",
        created_at: "2026-01-29T10:00:00Z",
      },
      {
        id: "2",
        title: "Team meeting",
        description: "Weekly team sync meeting",
        due_date: "2026-01-30T14:00:00Z",
        reminder_time: "2026-01-30T13:30:00Z", // 30 min before
        task_id: "task-2",
        created_at: "2026-01-29T09:00:00Z",
      },
      {
        id: "3",
        title: "Review quarterly reports",
        description: "Review and finalize quarterly financial reports",
        due_date: "2026-02-05T16:00:00Z",
        reminder_time: "2026-02-05T15:00:00Z", // 1 hour before
        task_id: "task-3",
        created_at: "2026-01-29T08:00:00Z",
      },
    ];

    // Simulate API call delay
    const timer = setTimeout(() => {
      setReminders(mockReminders);
      setIsLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  const toggleNotificationCenter = () => {
    setIsOpen(!isOpen);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getRelativeTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = date.getTime() - now.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays > 0) {
      return `${diffDays} day${diffDays !== 1 ? 's' : ''} left`;
    } else if (diffHours > 0) {
      return `${diffHours} hour${diffHours !== 1 ? 's' : ''} left`;
    } else if (diffHours === 0) {
      const diffMinutes = Math.floor(diffMs / (1000 * 60));
      return `${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''} left`;
    } else {
      return "Overdue";
    }
  };

  // Count upcoming reminders (due in the future)
  const upcomingReminders = reminders.filter(
    (reminder) => new Date(reminder.due_date) > new Date()
  );

  return (
    <div className="relative">
      <Button
        variant="ghost"
        size="icon"
        onClick={toggleNotificationCenter}
        className="relative h-10 w-10 rounded-full hover:bg-slate-700/50"
      >
        <Bell className="h-5 w-5 text-slate-300" />
        {upcomingReminders.length > 0 && (
          <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-indigo-500 text-xs text-white">
            {upcomingReminders.length}
          </span>
        )}
      </Button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
            onClick={toggleNotificationCenter}
          />
          <div className="fixed right-4 top-16 z-50 w-80 max-h-96 overflow-hidden rounded-xl border border-slate-700/50 bg-gradient-to-b from-slate-800 to-slate-900 shadow-2xl shadow-slate-900/50">
            <div className="flex items-center justify-between border-b border-slate-700/50 bg-slate-800/50 p-4">
              <h3 className="font-semibold text-slate-200">Upcoming Reminders</h3>
              <Button
                variant="ghost"
                size="icon"
                onClick={toggleNotificationCenter}
                className="h-8 w-8 text-slate-400 hover:text-slate-200"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            <div className="overflow-y-auto max-h-80">
              {isLoading ? (
                <div className="p-4 text-center text-slate-500">Loading reminders...</div>
              ) : reminders.length === 0 ? (
                <div className="p-4 text-center text-slate-500">No reminders scheduled</div>
              ) : (
                <ul>
                  {upcomingReminders.map((reminder) => (
                    <li
                      key={reminder.id}
                      className="border-b border-slate-700/30 p-4 hover:bg-slate-700/20"
                    >
                      <div className="flex items-start gap-3">
                        <div className="mt-0.5 rounded-lg bg-indigo-500/10 p-2 text-indigo-400">
                          <Clock className="h-4 w-4" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-medium text-slate-200 truncate">{reminder.title}</h4>
                          {reminder.description && (
                            <p className="mt-1 text-sm text-slate-400 line-clamp-2">
                              {reminder.description}
                            </p>
                          )}
                          <div className="mt-2 flex items-center gap-4 text-xs text-slate-500">
                            <div className="flex items-center gap-1">
                              <Calendar className="h-3 w-3" />
                              <span>{formatDate(reminder.due_date)}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              <span>{getRelativeTime(reminder.due_date)}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default NotificationCenter;