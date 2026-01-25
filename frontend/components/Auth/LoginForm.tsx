"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import Link from "next/link";

export const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();
  const { signIn } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
debugger;
    try {
      // Call the login API route
      const response = await fetch(`/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Invalid email or password. Please try again.");
      } else {
        // Successful login, update auth context and redirect
        await signIn(email, password);
        router.push("/tasks");
      }
    } catch (err: any) {
      setError(
        err.message || "An error occurred during login. Please try again."
      );
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm flex items-center gap-3"
        >
          <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
          {error}
        </motion.div>
      )}

      <div className="space-y-2">
        <label
          htmlFor="email"
          className="block text-xs font-bold uppercase tracking-[0.2em] text-slate-500 ml-1"
        >
          Email Address
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-4 py-4 bg-white/[0.03] border border-white/10 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-600/50 focus:border-blue-600 transition-all duration-300 hover:bg-white/[0.06]"
          placeholder="your@email.com"
        />
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center ml-1">
          <label
            htmlFor="password"
            className="block text-xs font-bold uppercase tracking-[0.2em] text-slate-500"
          >
            Password
          </label>
        </div>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full px-4 py-4 bg-white/[0.03] border border-white/10 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-600/50 focus:border-blue-600 transition-all duration-300 hover:bg-white/[0.06]"
          placeholder="••••••••"
        />
      </div>

      <div className="pt-2">
        <Button
          type="submit"
          className="w-full h-14 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold text-sm uppercase tracking-[0.2em] shadow-lg shadow-blue-600/20 transition-all active:scale-[0.98] group"
        >
          <span className="flex items-center justify-center gap-2">
            Sign In to Portal
            <ArrowRight
              size={16}
              className="group-hover:translate-x-1 transition-transform"
            />
          </span>
        </Button>
      </div>

      <div className="flex items-center justify-center gap-2 mt-6 py-3 px-4 rounded-lg bg-white/[0.02] border border-white/[0.05]">
        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
        <span className="text-[10px] text-slate-500 uppercase tracking-widest font-medium">
          Secure end-to-end encrypted session
        </span>
      </div>
    </form>
  );
};
