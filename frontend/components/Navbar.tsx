"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { motion, AnimatePresence } from "framer-motion";
import { User, LogOut, LayoutGrid, Menu, X } from "lucide-react";

const Navbar = () => {
  const { user, signOut } = useAuth();

  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <motion.nav
      className="fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl z-[100]"
    >
      <div className="backdrop-blur-xl border border-white/10 bg-slate-900/40 rounded-2xl px-6 py-3 flex justify-between items-center shadow-2xl">
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center shadow-[0_0_15px_rgba(37,99,235,0.4)] group-hover:rotate-6 transition-transform">
              <LayoutGrid size={20} className="text-white fill-white/20" />
            </div>
            <span className="text-lg font-bold tracking-tight text-white group-hover:text-blue-400 transition-colors">
              Premium<span className="font-light text-slate-400">Task</span>
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
                  className="text-slate-300 hover:text-white h-9 px-4 text-xs font-bold uppercase tracking-wider"
                >
                  AI Chat
                </Button>
              </Link>
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/5 border border-white/5 text-slate-300">
                <div className="w-5 h-5 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-400 flex items-center justify-center">
                  <User size={10} className="text-white" />
                </div>
                <span className="text-[10px] font-bold uppercase tracking-wider">
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
                  className="text-slate-300 hover:text-white h-9 px-4 text-xs font-bold uppercase tracking-wider"
                >
                  Login
                </Button>
              </Link>
              <Link href="/signup">
                <Button className="bg-blue-600 text-white hover:bg-blue-500 h-9 px-5 rounded-xl text-xs font-bold shadow-lg shadow-blue-600/20 active:scale-95 transition-all">
                  Join Now
                </Button>
              </Link>
            </div>
          )}
        </div>

        {/* Mobile menu button */}
        <div className="md:hidden flex items-center">
          {user ? (
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-slate-300 hover:text-white p-2"
              >
                {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            </div>
          ) : (
            <div className="flex gap-2">
              <Link href="/login">
                <Button
                  variant="ghost"
                  className="text-slate-300 hover:text-white h-9 px-4 text-xs font-bold uppercase tracking-wider"
                >
                  Login
                </Button>
              </Link>
              <Link href="/signup">
                <Button className="bg-blue-600 text-white hover:bg-blue-500 h-9 px-5 rounded-xl text-xs font-bold shadow-lg shadow-blue-600/20 active:scale-95 transition-all">
                  Join Now
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Mobile menu dropdown */}
      <AnimatePresence>
        {isMenuOpen && user && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden mt-2 backdrop-blur-xl border border-white/10 bg-slate-900/80 rounded-2xl px-6 py-4 shadow-2xl"
          >
            <div className="flex flex-col gap-3">
              <Link href="/chat" onClick={() => setIsMenuOpen(false)}>
                <Button
                  variant="ghost"
                  className="w-full justify-start text-slate-300 hover:text-white h-10 text-sm font-bold"
                >
                  AI Chat
                </Button>
              </Link>

              <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white/5 border border-white/5 text-slate-300">
                <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-400 flex items-center justify-center">
                  <User size={12} className="text-white" />
                </div>
                <span className="text-xs font-bold uppercase tracking-wider">
                  {user.email?.split("@")[0]}
                </span>
              </div>

              <Button
                onClick={() => {
                  signOut();
                  setIsMenuOpen(false);
                }}
                variant="ghost"
                className="w-full justify-start text-slate-500 hover:text-red-400 hover:bg-red-400/10 h-10 text-sm font-bold"
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
