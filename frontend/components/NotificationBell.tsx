"use client";

import React, { useState, useEffect } from 'react';
import { Bell, X, CheckCircle, AlertCircle, Info, XCircle } from 'lucide-react';
import WebSocketService from '@/utils/websocket';

interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  timestamp: Date;
  read: boolean;
}

const NotificationBell = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isVisible, setIsVisible] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    // Subscribe to WebSocket notifications
    const handleMessage = (data: any) => {
      if (data.type === 'notification' || data.event === 'notification') {
        const newNotification: Notification = {
          id: Math.random().toString(36).substring(7),
          title: data.title || 'New Notification',
          message: data.message || data.text || 'You have a new notification',
          type: data.type || data.level || 'info',
          timestamp: new Date(),
          read: false
        };
        
        setNotifications(prev => [newNotification, ...prev]);
      } else if (data.type === 'task-update' || data.event === 'task-update') {
        const newNotification: Notification = {
          id: Math.random().toString(36).substring(7),
          title: 'Task Updated',
          message: data.message || `Task "${data.task?.title || 'Unknown'}" was updated`,
          type: 'info',
          timestamp: new Date(),
          read: false
        };
        
        setNotifications(prev => [newNotification, ...prev]);
      }
    };

    WebSocketService.subscribe('message', handleMessage);
    WebSocketService.subscribe('notification', handleMessage);
    WebSocketService.subscribe('task-update', handleMessage);

    return () => {
      WebSocketService.unsubscribe('message', handleMessage);
      WebSocketService.unsubscribe('notification', handleMessage);
      WebSocketService.unsubscribe('task-update', handleMessage);
    };
  }, []);

  useEffect(() => {
    const unread = notifications.filter(n => !n.read).length;
    setUnreadCount(unread);
  }, [notifications]);

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(notification =>
        notification.id === id ? { ...notification, read: true } : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev =>
      prev.map(notification => ({ ...notification, read: true }))
    );
  };

  const clearNotification = (id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  };

  const clearAllNotifications = () => {
    setNotifications([]);
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'warning':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Info className="w-5 h-5 text-blue-500" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'success':
        return 'border-green-500/30 bg-green-500/5';
      case 'warning':
        return 'border-yellow-500/30 bg-yellow-500/5';
      case 'error':
        return 'border-red-500/30 bg-red-500/5';
      default:
        return 'border-blue-500/30 bg-blue-500/5';
    }
  };

  return (
    <div className="relative">
      <button
        onClick={toggleVisibility}
        className="relative p-2 rounded-lg hover:bg-slate-800/50 transition-colors"
        aria-label="Notifications"
      >
        <Bell className="w-5 h-5 text-slate-300" />
        {unreadCount > 0 && (
          <span className="absolute top-0 right-0 flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full transform translate-x-1 -translate-y-1">
            {unreadCount}
          </span>
        )}
      </button>

      {isVisible && (
        <div className="absolute right-0 mt-2 w-80 bg-slate-800/90 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl z-50 overflow-hidden">
          <div className="p-4 border-b border-white/10 flex justify-between items-center">
            <h3 className="font-bold text-white">Notifications</h3>
            <div className="flex gap-2">
              {notifications.some(n => !n.read) && (
                <button
                  onClick={markAllAsRead}
                  className="text-xs text-slate-400 hover:text-white px-2 py-1 rounded hover:bg-slate-700/50"
                >
                  Mark all as read
                </button>
              )}
              <button
                onClick={clearAllNotifications}
                className="text-xs text-slate-400 hover:text-red-400 px-2 py-1 rounded hover:bg-slate-700/50"
              >
                Clear all
              </button>
              <button
                onClick={toggleVisibility}
                className="text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="p-6 text-center text-slate-500">
                <Bell className="w-10 h-10 mx-auto mb-3 opacity-50" />
                <p>No notifications yet</p>
              </div>
            ) : (
              <div className="divide-y divide-white/5">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-4 ${getTypeColor(notification.type)} ${!notification.read ? 'bg-blue-500/10' : ''}`}
                  >
                    <div className="flex justify-between">
                      <div className="flex items-start gap-3">
                        {getIcon(notification.type)}
                        <div className="flex-1 min-w-0">
                          <h4 className="font-medium text-white text-sm">
                            {notification.title}
                          </h4>
                          <p className="text-slate-400 text-sm mt-1">
                            {notification.message}
                          </p>
                          <p className="text-xs text-slate-500 mt-2">
                            {notification.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </p>
                        </div>
                      </div>
                      <button
                        onClick={() => clearNotification(notification.id)}
                        className="text-slate-500 hover:text-white ml-2"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                    {!notification.read && (
                      <button
                        onClick={() => markAsRead(notification.id)}
                        className="mt-2 text-xs text-blue-400 hover:text-blue-300"
                      >
                        Mark as read
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Overlay to close notifications when clicking outside */}
      {isVisible && (
        <div
          className="fixed inset-0 z-40"
          onClick={toggleVisibility}
        />
      )}
    </div>
  );
};

export default NotificationBell;