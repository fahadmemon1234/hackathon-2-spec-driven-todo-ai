'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Trash2, Edit3 } from 'lucide-react';

interface TaskItemProps {
  task: any;
  onToggleComplete: (id: string) => void;
  onEdit: (id: string, taskData: { title: string; description?: string }) => void;
  onDelete: (id: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ 
  task, 
  onToggleComplete, 
  onEdit, 
  onDelete 
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const handleSaveEdit = () => {
    onEdit(task.id, { title: editTitle, description: editDescription || undefined });
    setIsEditing(false);
  };

  return (
    <motion.div 
      className={`corporate-card mb-3 rounded-md border ${
        task.completed 
          ? 'border-corporate-status-completed/30' 
          : 'border-corporate-border'
      } ${isHovered ? 'border-corporate-text-primary' : ''}`}
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ scale: 1.01 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {isEditing ? (
        <div className="p-4 space-y-3">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full bg-transparent border-b border-corporate-border focus:outline-none focus:ring-0 text-corporate-text-primary mb-2"
            autoFocus
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full bg-transparent border-b border-corporate-border focus:outline-none focus:ring-0 text-corporate-text-secondary text-sm"
            rows={2}
          />
          <div className="flex justify-end gap-2 mt-2">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => setIsEditing(false)}
              className="border-corporate-text-primary text-corporate-text-primary hover:bg-corporate-background"
            >
              Cancel
            </Button>
            <Button 
              size="sm" 
              onClick={handleSaveEdit}
              className="bg-corporate-accent-crimson text-white hover:bg-[#b80322]"
            >
              Save
            </Button>
          </div>
        </div>
      ) : (
        <div className="p-4 flex items-start gap-3">
          <div className="mt-1">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggleComplete(task.id)}
              className="custom-checkbox"
            />
          </div>
          
          <div className={`flex-1 min-w-0 ${task.completed ? 'opacity-75' : ''}`}>
            <div className="flex justify-between items-start">
              <div className={`${task.completed ? 'line-through text-corporate-text-secondary' : 'text-corporate-text-primary'}`}>
                <h3 className="text-base font-medium">{task.title}</h3>
                
                {task.description && (
                  <AnimatePresence>
                    <motion.p 
                      className={`mt-2 text-sm ${
                        task.completed ? 'line-through' : ''
                      } text-corporate-text-secondary`}
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                    >
                      {task.description}
                    </motion.p>
                  </AnimatePresence>
                )}
              </div>
              
              <div className="flex gap-1 ml-2">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setIsEditing(true)}
                  className="text-corporate-text-primary hover:text-corporate-accent-crimson"
                >
                  <Edit3 size={16} />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onDelete(task.id)}
                  className="text-corporate-text-primary hover:text-corporate-accent-crimson"
                >
                  <Trash2 size={16} />
                </Button>
              </div>
            </div>
            
            <div className="mt-3 flex justify-between items-center">
              <span className="text-xs text-corporate-text-secondary">
                Created: {formatDate(task.created_at)}
              </span>
              <div className="flex items-center">
                <span className={`status-dot ${task.completed ? 'status-completed' : 'status-pending'}`}></span>
                <span className="text-xs text-corporate-text-secondary ml-1">
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default TaskItem;