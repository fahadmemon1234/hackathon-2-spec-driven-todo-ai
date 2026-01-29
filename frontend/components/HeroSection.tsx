"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArrowRight, BarChart3, ShieldCheck, Zap, Layers, CheckCircle, Star, Users } from "lucide-react";

const HeroSection = () => {
  return (
    <section
      className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900/20 to-indigo-900/20 text-slate-200 overflow-hidden font-sans"
      style={{ paddingTop: "5%" }}
    >
      {/* Animated background elements */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="container relative z-10 mx-auto px-6 py-20">
        <div className="max-w-5xl mx-auto">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-center mb-8"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-blue-500/30 bg-blue-500/10 backdrop-blur-sm shadow-lg">
              <Star className="w-4 h-4 text-yellow-400 fill-current" />
              <span className="text-sm font-medium tracking-tight text-blue-300">
                #1 Productivity Platform
              </span>
              <ArrowRight size={16} className="text-blue-300" />
            </div>
          </motion.div>

          {/* Headings */}
          <div className="text-center mb-12">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight text-white mb-6 leading-tight"
            >
              Transform Your <br />
              <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent">
                Productivity
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed font-light"
            >
              The ultimate task management solution designed for teams who demand excellence.
              Streamline workflows, boost efficiency, and achieve more with our intuitive platform.
            </motion.p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20">
            <motion.div
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
              className="w-full sm:w-auto"
            >
              <Link href="/signup">
                <Button className="w-full h-14 px-10 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-500 hover:to-indigo-500 font-bold text-base transition-all shadow-lg shadow-blue-500/30">
                  Start Free Trial
                </Button>
              </Link>
            </motion.div>
            <motion.div
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
              className="w-full sm:w-auto"
            >
              <Link href="/login">
                <Button
                  variant="outline"
                  className="w-full h-14 px-10 rounded-xl border-2 border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white transition-all font-bold text-base"
                >
                  Sign In
                </Button>
              </Link>
            </motion.div>
          </div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20"
          >
            {[
              { value: "99.9%", label: "Uptime" },
              { value: "10k+", label: "Active Users" },
              { value: "50%", label: "Productivity Boost" },
            ].map((stat, i) => (
              <div
                key={i}
                className="p-6 rounded-2xl bg-slate-800/40 backdrop-blur-lg border border-slate-700/50 text-center"
              >
                <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-slate-400 text-sm">{stat.label}</div>
              </div>
            ))}
          </motion.div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                icon: ShieldCheck,
                title: "Bank-Level Security",
                desc: "Military-grade encryption keeps your data safe.",
              },
              {
                icon: Zap,
                title: "Lightning Fast",
                desc: "Optimized for speed and seamless performance.",
              },
              {
                icon: Users,
                title: "Team Collaboration",
                desc: "Work together in real-time with your team.",
              },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * i + 0.4 }}
                whileHover={{ y: -8, borderColor: "rgba(99, 102, 241, 0.5)" }}
                className="p-8 rounded-2xl border border-slate-800 bg-slate-900/30 backdrop-blur-xl transition-all duration-500 group cursor-default shadow-lg hover:shadow-xl hover:shadow-indigo-500/10"
              >
                <div className="w-14 h-14 rounded-xl bg-indigo-500/10 flex items-center justify-center mb-6 text-indigo-400 group-hover:bg-indigo-500 group-hover:text-white transition-colors">
                  <feature.icon size={24} />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-slate-400 leading-relaxed font-light group-hover:text-slate-300 transition-colors">
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </div>

          {/* Testimonial */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="mt-16 max-w-2xl mx-auto text-center p-6 rounded-2xl bg-slate-800/30 backdrop-blur-lg border border-slate-700/50"
          >
            <div className="flex justify-center mb-4">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
              ))}
            </div>
            <p className="text-slate-300 italic text-lg mb-4">
              "This platform transformed how our team manages projects. We've seen a 40% increase in productivity since switching."
            </p>
            <div className="text-slate-500 font-medium">Sarah Johnson, Product Manager</div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
