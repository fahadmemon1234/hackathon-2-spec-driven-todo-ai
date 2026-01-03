"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

interface PremiumLoaderProps {
  onComplete: () => void;
}

const PremiumLoader: React.FC<PremiumLoaderProps> = ({ onComplete }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // Simulate loading completion after 2 seconds
    const timer = setTimeout(() => {
      setIsVisible(false);
      // Give time for fade-out animation before calling onComplete
      setTimeout(onComplete, 300);
    }, 2000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  if (!isVisible) {
    return null; // Don't render anything when hidden
  }

  return (
    <div className="fixed inset-0 bg-[#020617] flex items-center justify-center z-[100]">
      
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-blue-600/10 blur-[100px] rounded-full" />

      <motion.div
        className="text-center relative z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.5 }}
      >
        
        <div className="relative w-20 h-20 mx-auto mb-10">
          
          <motion.div
            className="absolute inset-0 border-[3px] border-blue-600/20 border-t-blue-600 rounded-full"
            animate={{ rotate: 360 }}
            transition={{ duration: 1.2, repeat: Infinity, ease: "linear" }}
          />

          
          <motion.div
            className="absolute inset-4 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-[0_0_20px_rgba(37,99,235,0.4)] flex items-center justify-center"
            animate={{
              scale: [1, 0.9, 1],
              rotate: [0, 90, 180, 270, 360],
              borderRadius: ["20%", "50%", "20%"],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          >
            <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
          </motion.div>

          
          <motion.div
            className="absolute inset-[-10px] border border-blue-400/10 rounded-full"
            animate={{ scale: [1, 1.3, 1], opacity: [0, 0.5, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </div>

        
        <div className="space-y-3">
          <motion.h2
            className="text-white text-sm font-bold uppercase tracking-[0.4em] ml-[0.4em]"
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            Initializing
          </motion.h2>
          <div className="flex items-center justify-center gap-1.5">
            <span className="text-[10px] text-slate-500 font-medium uppercase tracking-widest">
              Secure Workspace
            </span>
            <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" />
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default PremiumLoader;
