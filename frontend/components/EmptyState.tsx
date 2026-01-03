import React from 'react';
import { Card, CardContent } from '@/components/ui/card';

const EmptyState = () => {
  return (
    <Card className="bg-luxury-card border border-luxury-primary/30 rounded-lg p-8 text-center">
      <CardContent>
        <div className="flex flex-col items-center justify-center">
          <div className="bg-luxury-background rounded-full p-4 mb-4">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-12 w-12 text-luxury-secondary" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" 
              />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-luxury-text-primary mb-2">No tasks yet</h3>
          <p className="text-luxury-text-secondary mb-4">Add your first task to get started</p>
          <p className="text-sm text-luxury-text-secondary/70 italic">
            Your tasks will appear here when you create them
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default EmptyState;