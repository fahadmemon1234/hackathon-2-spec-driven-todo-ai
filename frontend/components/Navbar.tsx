"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { motion, AnimatePresence } from "framer-motion";
import { User, LogOut, LayoutGrid, Menu, X, Sparkles, Target } from "lucide-react";
import NotificationBell from "@/components/NotificationBell";
import WebSocketService from "@/utils/websocket";

const Navbar = () => {
  const { user, signOut } = useAuth();

  const [isOpen, setIsOpen] = useState(false);

useEffect(() => {
  const interval = setInterval(() => {
    const opened = localStorage.getItem("openedModel");
    setIsOpen(opened === "true");
  }, 300);

  return () => clearInterval(interval);
}, []);

// Initialize WebSocket connection when user is available
useEffect(() => {
  if (user) {
    // Store user ID in localStorage for WebSocket service
    localStorage.setItem("current_user_id", user.id || user.email?.split("@")[0] || "");
    WebSocketService.connect(user.id || user.email?.split("@")[0]);
  }

  return () => {
    if (user) {
      WebSocketService.disconnect();
    }
  };
}, [user]);


  return (
    <motion.nav
      className={`fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl transition-all duration-500 ${
        isOpen == true
          ? "z-0 opacity-20 blur-sm scale-95"
          : "z-[100] opacity-100"
      }`}
    >
      <div className="backdrop-blur-xl border border-slate-700/50 bg-gradient-to-r from-slate-800/50 to-slate-900/50 rounded-2xl px-6 py-3 flex justify-between items-center shadow-xl">
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center shadow-[0_0_15px_rgba(99,102,241,0.4)] group-hover:rotate-6 transition-transform">
              <Target size={20} className="text-white" />
            </div>
            <span className="text-lg font-bold tracking-tight text-white group-hover:text-indigo-400 transition-colors">
              Task<span className="font-light text-slate-400">Flow</span>
            </span>
          </Link>
        </div>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-4">
          {user ? (
            <>
              <Link href="/chat">
                <Button
                  variant="ghost"
                  className="relative group overflow-hidden bg-slate-800/50 border border-slate-700/50 text-slate-300 hover:text-white h-9 px-4 text-xs font-medium uppercase tracking-wider transition-all duration-300 rounded-lg hover:border-indigo-500/50 hover:shadow-[0_0_15px_rgba(99,102,241,0.2)]"
                >
                  {/* Subtle Background Glow on Hover */}
                  <span className="absolute inset-0 bg-gradient-to-r from-indigo-600/10 to-purple-600/10 opacity-0 group-hover:opacity-100 transition-opacity" />

                  <span className="relative flex items-center gap-2">
                    <Sparkles className="w-3.5 h-3.5 text-indigo-400 group-hover:animate-pulse" />
                    AI Chat
                  </span>
                </Button>
              </Link>

              <NotificationBell />

              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800/50 border border-slate-700/50 text-slate-300">
                <div className="w-5 h-5 rounded-full bg-gradient-to-tr from-indigo-600 to-purple-400 flex items-center justify-center">
                  <User size={10} className="text-white" />
                </div>
                <span className="text-xs font-medium uppercase tracking-wider">
                  {user.email?.split("@")[0]}
                </span>
              </div>
              <Button
                onClick={signOut}
                variant="ghost"
                className="text-slate-500 hover:text-red-400 hover:bg-red-400/10 h-9 px-3 rounded-xl transition-all group"
              >
                <LogOut
                  size={16}
                  className="group-hover:-translate-x-1 transition-transform"
                />
              </Button>
            </>
          ) : (
            <div className="flex gap-2">
              <Link href="/login">
                <Button
                  variant="ghost"
                  className="text-slate-300 hover:text-white h-9 px-4 text-xs font-medium uppercase tracking-wider"
                >
                  Login
                </Button>
              </Link>
              <Link href="/signup">
                <Button className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-500 hover:to-purple-500 h-9 px-5 rounded-xl text-xs font-medium shadow-lg shadow-indigo-500/20 active:scale-95 transition-all">
                  Get Started
                </Button>
              </Link>
            </div>
          )}
        </div>

        {/* Mobile menu button */}
        <div className="md:hidden flex items-center">
          {user ? (
            <div className="flex items-center gap-2">
              <NotificationBell />
              <button
                onClick={() => setIsOpen(!isOpen)}
                className="text-slate-300 hover:text-white p-2"
              >
                {isOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            </div>
          ) : (
            <div className="flex gap-2">
              <Link href="/login">
                <Button
                  variant="ghost"
                  className="text-slate-300 hover:text-white h-9 px-4 text-xs font-medium uppercase tracking-wider"
                >
                  Login
                </Button>
              </Link>
              <Link href="/signup">
                <Button className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-500 hover:to-purple-500 h-9 px-5 rounded-xl text-xs font-medium shadow-lg shadow-indigo-500/20 active:scale-95 transition-all">
                  Get Started
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Mobile menu dropdown */}
      <AnimatePresence>
        {isOpen && user && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden mt-2 backdrop-blur-xl border border-slate-700/50 bg-gradient-to-r from-slate-800/80 to-slate-900/80 rounded-2xl px-6 py-4 shadow-xl"
          >
            <div className="flex flex-col gap-3">
              <Link href="/chat" onClick={() => setIsOpen(false)}>
                <Button
                  variant="ghost"
                  className="w-full justify-start text-slate-300 hover:text-white h-10 text-sm font-medium"
                >
                  AI Chat
                </Button>
              </Link>

              <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-800/50 border border-slate-700/50 text-slate-300">
                <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-indigo-600 to-purple-400 flex items-center justify-center">
                  <User size={12} className="text-white" />
                </div>
                <span className="text-xs font-medium uppercase tracking-wider">
                  {user.email?.split("@")[0]}
                </span>
              </div>

              <Button
                onClick={() => {
                  signOut();
                  setIsOpen(false);
                }}
                variant="ghost"
                className="w-full justify-start text-slate-500 hover:text-red-400 hover:bg-red-400/10 h-10 text-sm font-medium"
              >
                <LogOut size={16} className="mr-2" /> Logout
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

export default Navbar;
