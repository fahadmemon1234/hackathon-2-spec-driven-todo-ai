import React from 'react';

const TaskSkeleton = () => {
  return (
    <div className="bg-luxury-card border border-luxury-primary/30 rounded-lg shadow-lg p-4 animate-pulse">
      <div className="flex items-start gap-3">
        <div className="h-5 w-5 rounded bg-luxury-background mt-1"></div>
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-luxury-background rounded w-3/4"></div>
          <div className="h-3 bg-luxury-background rounded w-full"></div>
          <div className="h-3 bg-luxury-background rounded w-2/3"></div>
        </div>
      </div>
      <div className="flex justify-between mt-4 pt-3 border-t border-luxury-primary/20">
        <div className="h-3 bg-luxury-background rounded w-16"></div>
        <div className="flex gap-2">
          <div className="h-8 w-16 bg-luxury-background rounded"></div>
          <div className="h-8 w-16 bg-luxury-background rounded"></div>
        </div>
      </div>
    </div>
  );
};

export default TaskSkeleton;