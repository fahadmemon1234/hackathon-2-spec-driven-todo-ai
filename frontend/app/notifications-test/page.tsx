"use client";

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import WebSocketService from '@/utils/websocket';

const NotificationsTestPage = () => {
  const [notification, setNotification] = useState({
    title: 'Test Notification',
    message: 'This is a test notification from the frontend',
    type: 'info'
  });

  const sendTestNotification = () => {
    const payload = {
      type: 'notification',
      payload: {
        title: notification.title,
        message: notification.message,
        type: notification.type,
        user_id: localStorage.getItem('current_user_id') // Send to specific user
      }
    };

    WebSocketService.send(payload);
  };

  const sendBroadcastNotification = () => {
    const payload = {
      type: 'notification',
      payload: {
        title: 'Broadcast Notification',
        message: 'This is a broadcast notification to all users',
        type: 'info'
      }
    };

    WebSocketService.send(payload);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setNotification(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 flex items-center justify-center p-4">
      <Card className="w-full max-w-md bg-slate-900/40 border border-white/10 rounded-2xl backdrop-blur-xl shadow-2xl">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-white">Notification Test</CardTitle>
          <CardDescription className="text-slate-400">
            Test sending notifications via WebSocket
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-slate-300 mb-1">
              Title
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={notification.title}
              onChange={handleChange}
              className="w-full bg-slate-800/50 border border-white/10 rounded-lg px-4 py-2 text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600/50"
            />
          </div>
          <div>
            <label htmlFor="message" className="block text-sm font-medium text-slate-300 mb-1">
              Message
            </label>
            <input
              type="text"
              id="message"
              name="message"
              value={notification.message}
              onChange={handleChange}
              className="w-full bg-slate-800/50 border border-white/10 rounded-lg px-4 py-2 text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600/50"
            />
          </div>
          <div>
            <label htmlFor="type" className="block text-sm font-medium text-slate-300 mb-1">
              Type
            </label>
            <select
              id="type"
              name="type"
              value={notification.type}
              onChange={handleChange}
              className="w-full bg-slate-800/50 border border-white/10 rounded-lg px-4 py-2 text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600/50"
            >
              <option value="info">Info</option>
              <option value="success">Success</option>
              <option value="warning">Warning</option>
              <option value="error">Error</option>
            </select>
          </div>
        </CardContent>
        <CardFooter className="flex flex-col gap-2">
          <Button
            onClick={sendTestNotification}
            className="w-full bg-blue-600 hover:bg-blue-500 text-white py-2 rounded-lg font-medium"
          >
            Send Test Notification
          </Button>
          <Button
            onClick={sendBroadcastNotification}
            variant="outline"
            className="w-full border border-slate-700 text-slate-300 hover:bg-slate-800/50 py-2 rounded-lg font-medium"
          >
            Send Broadcast Notification
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default NotificationsTestPage;