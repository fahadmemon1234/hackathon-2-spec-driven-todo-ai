'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

interface AddTodoInputProps {
  onAddTask: (taskData: { title: string; description?: string }) => void;
}

const AddTodoInput: React.FC<AddTodoInputProps> = ({ onAddTask }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    onAddTask({ title: title.trim(), description: description.trim() || undefined });
    setTitle('');
    setDescription('');
    if (isExpanded) {
      setIsExpanded(false);
    }
  };

  return (
    <motion.form 
      className="glass rounded-2xl p-4 border border-luxury-border mb-6"
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <div className="flex gap-3">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Add a new task..."
          className="flex-1 bg-transparent border-none focus:outline-none focus:ring-0 text-luxury-text-primary placeholder-luxury-text-secondary"
          onFocus={() => setIsExpanded(true)}
        />
        <Button 
          type="submit"
          className={`bg-luxury-accent-gold text-luxury-background hover:bg-luxury-accent-gold/90 ${
            title.trim() ? 'shadow-gold/20' : ''
          }`}
          disabled={!title.trim()}
        >
          <Plus size={18} />
        </Button>
      </div>
      
      {isExpanded && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: 'auto', opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="mt-4 pt-4 border-t border-luxury-border"
        >
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add details (optional)"
            className="w-full bg-transparent border-none focus:outline-none focus:ring-0 text-luxury-text-secondary placeholder-luxury-text-secondary min-h-[60px]"
            rows={2}
          />
        </motion.div>
      )}
    </motion.form>
  );
};

export default AddTodoInput;