// components/Toast.tsx
'use client';

import { Toaster } from 'sonner';

export const Toast = () => {
  return (
    <Toaster 
      position="top-right"
      toastOptions={{
        style: {
          background: '#1e1e1e', // luxury-card color
          color: '#ffffff',      // luxury-text-primary color
          border: '1px solid #d904294d', // luxury-primary with opacity
        },
        className: 'luxury-toast',
      }}
    />
  );
};