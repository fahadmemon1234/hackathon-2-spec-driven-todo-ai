"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArrowRight, BarChart3, ShieldCheck, Zap, Layers } from "lucide-react";

const HeroSection = () => {
  return (
    <section
      className="relative min-h-screen flex items-center justify-center bg-[#020617] text-slate-200 overflow-hidden font-sans"
      style={{ paddingTop: "5%" }}
    >
      <div className="absolute inset-0 z-0">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-blue-600/10 blur-[120px] rounded-full" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-20" />
      </div>

      <div className="container relative z-10 mx-auto px-6 py-20">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-center mb-8"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-slate-700 bg-slate-900/50 backdrop-blur-sm shadow-inner">
              <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
              <span className="text-xs font-medium tracking-tight text-slate-300">
                New: Enterprise-grade analytics is here
              </span>
              <ArrowRight size={12} className="text-slate-500" />
            </div>
          </motion.div>

          <div className="text-center mb-12">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-5xl md:text-7xl font-bold tracking-tight text-white mb-6"
            >
              Organize your work <br />
              <span className="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent italic">
                with total precision.
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed font-normal"
            >
              A high-performance task engine built for modern teams. Secure,
              lightning-fast, and designed for deep focus.
            </motion.p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-24">
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Link href="/signup">
                <Button className="h-12 px-8 rounded-lg bg-blue-600 text-white hover:bg-blue-500 font-semibold transition-all shadow-[0_0_20px_rgba(37,99,235,0.3)]">
                  Get Started for Free
                </Button>
              </Link>
            </motion.div>
            <Link href="/login">
              <Button
                variant="ghost"
                className="h-12 px-8 rounded-lg border border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white transition-all"
              >
                Sign In
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                icon: ShieldCheck,
                title: "Enterprise Security",
                desc: "Military-grade encryption for all your sensitive data.",
              },
              {
                icon: BarChart3,
                title: "Advanced Metrics",
                desc: "Track productivity with deep visual analytics.",
              },
              {
                icon: Layers,
                title: "Unified Workflow",
                desc: "Integrate with all your existing professional tools.",
              },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * i + 0.4 }}
                whileHover={{ y: -5, borderColor: "rgba(59, 130, 246, 0.5)" }}
                className="p-8 rounded-2xl border border-slate-800 bg-slate-900/30 backdrop-blur-xl transition-all duration-300 group cursor-default"
              >
                <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center mb-6 text-blue-400 group-hover:bg-blue-500 group-hover:text-white transition-colors">
                  <feature.icon size={20} />
                </div>
                <h3 className="text-lg font-bold text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-slate-500 leading-relaxed font-light group-hover:text-slate-400 transition-colors">
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
