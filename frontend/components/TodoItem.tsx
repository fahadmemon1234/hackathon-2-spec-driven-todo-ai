'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Trash2, Edit3, Calendar } from 'lucide-react';

interface TodoItemProps {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  onToggleComplete: (id: string) => void;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({
  id,
  title,
  description,
  completed,
  createdAt,
  onToggleComplete,
  onEdit,
  onDelete
}) => {
  const [isHovered, setIsHovered] = useState(false);

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

  return (
    <motion.div
      className={`glass rounded-2xl p-4 border border-luxury-border mb-4 flex items-start gap-4 group ${
        completed ? 'opacity-70' : ''
      }`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.8 }}
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="mt-1">
        <Checkbox
          checked={completed}
          onCheckedChange={() => onToggleComplete(id)}
          className={`w-6 h-6 rounded-md border-2 ${
            completed
              ? 'bg-luxury-accent-gold border-luxury-accent-gold'
              : 'border-luxury-text-secondary hover:border-luxury-accent-gold'
          }`}
        />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex justify-between items-start">
          <h3 className={`text-lg font-medium ${
            completed
              ? 'line-through text-luxury-text-secondary'
              : 'text-luxury-text-primary'
          }`}>
            {title}
          </h3>
          <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onEdit(id)}
              className="text-luxury-accent-gold hover:bg-luxury-accent-gold/10"
            >
              <Edit3 size={18} />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onDelete(id)}
              className="text-luxury-accent-purple hover:bg-luxury-accent-purple/10"
            >
              <Trash2 size={18} />
            </Button>
          </div>
        </div>

        {description && (
          <AnimatePresence>
            <motion.p
              className={`mt-2 text-luxury-text-secondary ${
                completed ? 'line-through' : ''
              }`}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              {description}
            </motion.p>
          </AnimatePresence>
        )}

        <div className="mt-3 flex items-center text-sm text-luxury-text-secondary">
          <Calendar size={14} className="mr-1" />
          {formatDate(createdAt)}
        </div>
      </div>
    </motion.div>
  );
};

export default TodoItem;