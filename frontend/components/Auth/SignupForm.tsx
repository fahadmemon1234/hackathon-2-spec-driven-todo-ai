"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

export const SignupForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    debugger;

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      debugger;
      const res = await fetch("/api/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await res.json();

      if (!res.ok || data?.error) {
        setError(data?.error || "Signup failed");
        return;
      }

      // signup successful
      router.push("/tasks");
    } catch (err: any) {
      setError(err.message || "An error occurred during signup");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm flex items-center gap-3"
        >
          <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
          {error}
        </motion.div>
      )}

    
      <div className="space-y-2">
        <label
          htmlFor="email"
          className="block text-xs font-bold uppercase tracking-widest text-slate-500 ml-1"
        >
          Business Email
        </label>
        <div className="relative group">
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-600/50 focus:border-blue-600 transition-all duration-300 group-hover:bg-white/[0.08]"
            placeholder="name@company.com"
          />
        </div>
      </div>

      
      <div className="space-y-2">
        <label
          htmlFor="password"
          className="block text-xs font-bold uppercase tracking-widest text-slate-500 ml-1"
        >
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full px-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-600/50 focus:border-blue-600 transition-all duration-300 group-hover:bg-white/[0.08]"
          placeholder="••••••••"
        />
      </div>

     
      <div className="space-y-2">
        <label
          htmlFor="confirmPassword"
          className="block text-xs font-bold uppercase tracking-widest text-slate-500 ml-1"
        >
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          className="w-full px-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-600/50 focus:border-blue-600 transition-all duration-300 group-hover:bg-white/[0.08]"
          placeholder="••••••••"
        />
      </div>

      
      <div className="pt-2">
        <Button
          type="submit"
          className="w-full h-14 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold text-sm uppercase tracking-widest shadow-lg shadow-blue-600/20 transition-all active:scale-[0.98] group"
        >
          <span className="flex items-center justify-center gap-2">
            Create Workspace
            <ArrowRight
              size={16}
              className="group-hover:translate-x-1 transition-transform"
            />
          </span>
        </Button>
      </div>

      <p className="text-[10px] text-center text-slate-600 mt-4 leading-relaxed px-6 uppercase tracking-tighter">
        By clicking create account, you agree to our
        <span className="text-slate-400"> Terms of Service </span>
        and <span className="text-slate-400"> Privacy Policy</span>.
      </p>
    </form>
  );
};
