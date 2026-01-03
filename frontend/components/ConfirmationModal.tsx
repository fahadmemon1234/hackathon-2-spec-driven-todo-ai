'use client';

import React from 'react';
import { Button } from "@/components/ui/button";

interface ConfirmationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
}

const ConfirmationModal: React.FC<ConfirmationModalProps> = ({ 
  isOpen, 
  onClose, 
  onConfirm, 
  title, 
  message 
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-luxury-card rounded-lg shadow-xl w-full max-w-md border border-luxury-primary/30">
        <div className="p-6">
          <h2 className="text-xl font-bold text-luxury-text-primary mb-2">
            {title}
          </h2>
          <p className="text-luxury-text-secondary mb-6">
            {message}
          </p>
          
          <div className="flex justify-end gap-3">
            <Button 
              type="button" 
              variant="outline"
              onClick={onClose}
              className="border-luxury-secondary text-luxury-secondary hover:bg-luxury-secondary hover:text-luxury-background"
            >
              Cancel
            </Button>
            <Button 
              type="button" 
              onClick={() => {
                onConfirm();
                onClose();
              }}
              className="bg-luxury-primary text-luxury-text-primary hover:bg-luxury-primary/90"
            >
              Confirm
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationModal;