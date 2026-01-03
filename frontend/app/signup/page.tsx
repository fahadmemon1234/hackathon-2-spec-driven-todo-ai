'use client';

import React from 'react';
import Link from 'next/link';
import { SignupForm } from "@/components/Auth/SignupForm";
import { motion } from 'framer-motion';
import { LayoutGrid, ArrowLeft, Sparkles } from 'lucide-react';

const SignupPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#020617] text-slate-200 relative overflow-hidden p-4">
      
      <div className="absolute inset-0 z-0">
        <div className="absolute top-1/3 right-1/4 w-[600px] h-[600px] bg-blue-600/5 blur-[120px] rounded-full opacity-40" />
        <div className="absolute bottom-1/4 left-1/4 w-[400px] h-[400px] bg-indigo-600/5 blur-[100px] rounded-full opacity-30" />
        <div className="absolute inset-0 bg-[radial-gradient(#ffffff03_1px,transparent_1px)] [background-size:24px_24px]" />
      </div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-[480px] relative z-10"
      >
        <Link 
          href="/" 
          className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-white transition-colors mb-6 group"
        >
          <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" />
          Back to website
        </Link>

        <div className="bg-slate-900/40 backdrop-blur-3xl rounded-[32px] p-8 md:p-12 shadow-2xl border border-white/10 relative overflow-hidden">
          
          <div className="absolute top-0 left-0 right-0 h-1.5 bg-white/5">
             <div className="h-full w-1/3 bg-blue-600 rounded-r-full shadow-[0_0_10px_rgba(37,99,235,0.5)]" />
          </div>

          <div className="mb-10 text-left">
            <div className="flex items-center gap-2 text-blue-400 font-bold mb-4 uppercase tracking-[0.2em] text-[10px]">
              <Sparkles size={12} />
              Start your journey
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-white mb-3">Create Account</h1>
            <p className="text-slate-400 font-light leading-relaxed">
              Join the elite circle of high-performers today.
            </p>
          </div>
          
          <SignupForm />
          
          <div className="mt-10 pt-8 border-t border-white/5">
            <p className="text-center text-sm text-slate-500 font-light">
              Already have an account?{' '}
              <Link 
                href="/login" 
                className="text-white hover:text-blue-400 font-semibold underline-offset-4 hover:underline transition-all"
              >
                Sign in instead
              </Link>
            </p>
          </div>
        </div>

        
        <div className="mt-8 flex justify-center items-center gap-6 opacity-40 grayscale hover:grayscale-0 transition-all duration-500">
             <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest">
                <LayoutGrid size={14} /> Encrypted
             </div>
             <div className="w-1 h-1 bg-slate-600 rounded-full" />
             <div className="text-[10px] font-bold uppercase tracking-widest">
                ISO Certified
             </div>
             <div className="w-1 h-1 bg-slate-600 rounded-full" />
             <div className="text-[10px] font-bold uppercase tracking-widest">
                24/7 Support
             </div>
        </div>
      </motion.div>
    </div>
  );
};

export default SignupPage;