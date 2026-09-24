import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ShieldCheck, TrendingUp, Search } from 'lucide-react';

interface HeroSectionProps {
  onStartSearch: () => void;
  onViewTrend: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ onStartSearch, onViewTrend }) => {
  return (
    <div className="relative overflow-hidden pt-12 pb-16 px-4 bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 text-white border-b border-slate-800">
      {/* Glow Effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 w-[400px] h-[250px] bg-amber-500/10 rounded-full blur-[100px] pointer-events-none" />

      <div className="relative max-w-7xl mx-auto flex flex-col items-center text-center">
        
        {/* Top Pill Badge */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-xs font-semibold mb-6 backdrop-blur-md shadow-lg"
        >
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          Real-Time Demand Rate Optimization Engine
        </motion.div>

        {/* Main Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-4xl sm:text-5xl md:text-6xl font-black tracking-tight max-w-4xl leading-[1.1] mb-6"
        >
          Next-Generation Dynamic Hotel{' '}
          <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-amber-300 bg-clip-text text-transparent">
            Pricing & Booking Engine
          </span>
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-base sm:text-lg text-slate-300 max-w-2xl font-normal leading-relaxed mb-8"
        >
          Simulating real-time occupancy surges, lead time discounts, weekend premiums, and local event multipliers with concurrency-safe availability locks.
        </motion.p>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex flex-col sm:flex-row items-center gap-4 mb-12"
        >
          <button
            type="button"
            onClick={onStartSearch}
            className="w-full sm:w-auto px-8 py-4 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-base shadow-xl shadow-indigo-600/30 transition-all flex items-center justify-center gap-2 group"
          >
            <Search className="w-5 h-5 group-hover:scale-110 transition-transform" />
            Explore Available Rooms
          </button>

          <button
            type="button"
            onClick={onViewTrend}
            className="w-full sm:w-auto px-8 py-4 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white font-bold text-base border border-slate-700 transition-all flex items-center justify-center gap-2"
          >
            <TrendingUp className="w-5 h-5 text-indigo-400" />
            View 30-Day Forecast
          </button>
        </motion.div>

        {/* Key Feature Stats Bar */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="w-full max-w-4xl grid grid-cols-2 md:grid-cols-4 gap-4 p-4 rounded-2xl bg-slate-800/40 border border-slate-800 backdrop-blur-md text-left"
        >
          <div className="p-3 border-r border-slate-800/80 last:border-r-0">
            <span className="text-xs text-slate-400 font-medium">Concurrency Lock</span>
            <p className="text-base font-bold text-emerald-400 flex items-center gap-1 mt-0.5">
              <ShieldCheck className="w-4 h-4" /> Zero Overbooking
            </p>
          </div>

          <div className="p-3 border-r border-slate-800/80 last:border-r-0">
            <span className="text-xs text-slate-400 font-medium">Pricing Factors</span>
            <p className="text-base font-bold text-indigo-300 mt-0.5">4 Tunable Vectors</p>
          </div>

          <div className="p-3 border-r border-slate-800/80 last:border-r-0">
            <span className="text-xs text-slate-400 font-medium">Cache Layer</span>
            <p className="text-base font-bold text-amber-300 mt-0.5">Redis / In-Memory</p>
          </div>

          <div className="p-3">
            <span className="text-xs text-slate-400 font-medium">API Response</span>
            <p className="text-base font-bold text-white mt-0.5">&lt; 15ms Latency</p>
          </div>
        </motion.div>

      </div>
    </div>
  );
};
