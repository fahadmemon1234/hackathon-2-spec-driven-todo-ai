// components/ProtectedRoute.tsx
'use client';

import React from 'react';
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { motion } from 'framer-motion';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="fixed inset-0 bg-[#020617] flex items-center justify-center z-[100]">
  <div className="flex flex-col items-center">
    
    
    <div className="relative w-20 h-20 flex items-center justify-center mb-8">
     
      <motion.div 
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ 
          opacity: [0.1, 0.3, 0], 
          scale: [1, 1.8, 2.2],
        }}
        transition={{ 
          duration: 2, 
          repeat: Infinity, 
          ease: "easeOut" 
        }}
        className="absolute inset-0 bg-blue-500 rounded-full"
      />
      
      
      <motion.div
        initial={{ y: 0 }}
        animate={{ y: [-4, 4, -4] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        className="relative z-10 w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center shadow-[0_0_30px_rgba(37,99,235,0.4)]"
      >
        <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
      </motion.div>
    </div>

    
    <div className="flex flex-col items-center gap-4">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-white text-[10px] font-bold uppercase tracking-[0.5em] ml-[0.5em] opacity-80"
      >
        Authenticating
      </motion.div>

      
      <div className="w-48 h-[2px] bg-white/5 rounded-full overflow-hidden relative">
        <motion.div 
          className="absolute inset-0 bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.8)]"
          initial={{ left: "-100%" }}
          animate={{ left: "100%" }}
          transition={{ 
            duration: 1.5, 
            repeat: Infinity, 
            ease: "easeInOut" 
          }}
        />
      </div>

      <div className="text-slate-500 text-[10px] italic font-light">
        Please wait a moment...
      </div>
    </div>
  </div>
</div>
    );
  }

  if (!user) {
    return null; // The redirect happens in the effect above
  }

  return <>{children}</>;
};

export default ProtectedRoute;