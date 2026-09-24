import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Info, Calendar, Users, Zap, TrendingUp, HelpCircle, X } from 'lucide-react';
import type { PricingBreakdown } from '../types';

interface PricingTooltipProps {
  breakdown: PricingBreakdown[];
  basePrice: number;
  averagePrice: number;
}

export const PricingTooltip: React.FC<PricingTooltipProps> = ({ breakdown, basePrice, averagePrice }) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!breakdown || breakdown.length === 0) return null;

  const firstNight = breakdown[0];
  const priceDiff = averagePrice - basePrice;
  const isSurge = priceDiff > 0;

  return (
    <div className="relative inline-block">
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 hover:bg-indigo-50 text-indigo-700 border border-indigo-200/80 transition-colors shadow-xs"
      >
        <HelpCircle className="w-3.5 h-3.5 text-indigo-600" />
        <span>Why this price?</span>
      </button>

      {/* Popover Modal / Tooltip */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop for mobile closing */}
            <div 
              className="fixed inset-0 z-40 bg-slate-900/20 backdrop-blur-xs md:hidden"
              onClick={() => setIsOpen(false)}
            />

            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              transition={{ duration: 0.2, ease: 'easeOut' }}
              className="absolute left-1/2 -translate-x-1/2 md:left-auto md:right-0 mt-2 z-50 w-[340px] md:w-[380px] p-5 rounded-2xl bg-white border border-slate-200 shadow-2xl text-slate-800"
            >
              {/* Header */}
              <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 rounded-lg bg-indigo-50 text-indigo-600">
                    <TrendingUp className="w-4 h-4" />
                  </div>
                  <h4 className="font-bold text-sm text-slate-900">Dynamic Rate Breakdown</h4>
                </div>
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Price Summary */}
              <div className="p-3 mb-4 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                <div>
                  <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Base Rate</span>
                  <p className="text-sm font-semibold text-slate-700">${basePrice.toFixed(2)}/night</p>
                </div>

                <div className="text-right">
                  <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Dynamic Rate</span>
                  <p className={`text-sm font-bold ${isSurge ? 'text-amber-600' : 'text-emerald-600'}`}>
                    ${averagePrice.toFixed(2)}/night
                  </p>
                </div>
              </div>

              {/* Factors List */}
              <div className="space-y-2.5 mb-4 text-xs">
                {/* Occupancy Factor */}
                <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50/80">
                  <div className="flex items-center gap-2">
                    <Users className="w-3.5 h-3.5 text-indigo-500" />
                    <span className="font-medium text-slate-700">Occupancy Level</span>
                  </div>
                  <span className="font-mono font-semibold px-2 py-0.5 rounded bg-indigo-100 text-indigo-800">
                    {(firstNight.occupancy_rate * 100).toFixed(0)}% ({firstNight.occupancy_multiplier}x)
                  </span>
                </div>

                {/* Lead Time Factor */}
                <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50/80">
                  <div className="flex items-center gap-2">
                    <Calendar className="w-3.5 h-3.5 text-indigo-500" />
                    <span className="font-medium text-slate-700">Lead Time</span>
                  </div>
                  <span className="font-mono font-semibold px-2 py-0.5 rounded bg-indigo-100 text-indigo-800">
                    {firstNight.days_to_checkin}d ahead ({firstNight.lead_time_multiplier}x)
                  </span>
                </div>

                {/* Weekend Premium */}
                {firstNight.is_weekend && (
                  <div className="flex items-center justify-between p-2 rounded-lg bg-amber-50 border border-amber-100">
                    <div className="flex items-center gap-2 text-amber-800">
                      <Zap className="w-3.5 h-3.5 text-amber-600" />
                      <span className="font-medium">Weekend Surge</span>
                    </div>
                    <span className="font-mono font-bold text-amber-700">+{((firstNight.weekend_multiplier - 1) * 100).toFixed(0)}%</span>
                  </div>
                )}

                {/* Event Surge */}
                {firstNight.demand_event_name && (
                  <div className="flex items-center justify-between p-2 rounded-lg bg-emerald-50 border border-emerald-100">
                    <div className="flex items-center gap-2 text-emerald-800">
                      <Zap className="w-3.5 h-3.5 text-emerald-600" />
                      <span className="font-medium truncate max-w-[170px]">{firstNight.demand_event_name}</span>
                    </div>
                    <span className="font-mono font-bold text-emerald-700">+{((firstNight.demand_event_multiplier - 1) * 100).toFixed(0)}%</span>
                  </div>
                )}
              </div>

              {/* Plain Language Explanation */}
              <div className="p-2.5 rounded-lg bg-indigo-50/60 border border-indigo-100 text-[11px] text-indigo-900 leading-relaxed flex gap-2">
                <Info className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
                <p>{firstNight.explanation}</p>
              </div>

            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};
