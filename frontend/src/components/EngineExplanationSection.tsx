import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Cpu, Users, Calendar, Zap, Sparkles, Sliders } from 'lucide-react';

export const EngineExplanationSection: React.FC = () => {
  // Interactive Simulator State
  const [basePrice, setBasePrice] = useState(200);
  const [occupancyPct, setOccupancyPct] = useState(75);
  const [leadDays, setLeadDays] = useState(3);
  const [isWeekend, setIsWeekend] = useState(true);
  const [eventMultiplier, setEventMultiplier] = useState(1.3);

  // Compute multipliers live
  const getOccupancyMult = (occ: number) => {
    if (occ < 30) return 0.85;
    if (occ < 60) return 1.0;
    if (occ < 80) return 1.2;
    if (occ < 95) return 1.4;
    return 1.65;
  };

  const getLeadMult = (days: number) => {
    if (days <= 2) return 1.25;
    if (days <= 7) return 1.10;
    if (days <= 30) return 1.0;
    if (days <= 60) return 0.92;
    return 0.85;
  };

  const occMult = getOccupancyMult(occupancyPct);
  const leadMult = getLeadMult(leadDays);
  const weekendMult = isWeekend ? 1.2 : 1.0;
  const totalMult = occMult * leadMult * weekendMult * eventMultiplier;

  // Clamped between 0.5x and 3.0x
  const rawPrice = basePrice * totalMult;
  const finalPrice = Math.min(Math.max(rawPrice, basePrice * 0.5), basePrice * 3.0);

  return (
    <div className="py-12 px-4 max-w-7xl mx-auto space-y-12">
      {/* Overview Header */}
      <div className="text-center max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-indigo-100 text-indigo-700 border border-indigo-200 mb-3">
          <Cpu className="w-3.5 h-3.5 text-indigo-600" /> Technical Architecture & Mechanics
        </div>
        <h2 className="text-3xl md:text-4xl font-black tracking-tight text-slate-900 mb-4">
          How the Zenith Pricing Engine Works
        </h2>
        <p className="text-slate-600 leading-relaxed text-base">
          Our rate engine optimizes revenue per available room (RevPAR) dynamically. Rates adjust every second based on real-time inventory commitments, booking window horizons, calendar premiums, and regional events.
        </p>
      </div>

      {/* 4 Pillars Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Pillar 1 */}
        <motion.div
          whileHover={{ y: -4 }}
          className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-md space-y-3"
        >
          <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-black">
            <Users className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-lg text-slate-900">1. Occupancy Rate</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Measures booked rooms vs total capacity. Under 30% occupancy offers incentive discounts (0.85x), scaling up to last-unit surges (1.65x) above 95%.
          </p>
        </motion.div>

        {/* Pillar 2 */}
        <motion.div
          whileHover={{ y: -4 }}
          className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-md space-y-3"
        >
          <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-black">
            <Calendar className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-lg text-slate-900">2. Lead Time Horizon</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Distinguishes last-minute urgent bookings (&le;2 days: 1.25x premium) from advance early-bird planners (&gt;60 days: 0.85x discount).
          </p>
        </motion.div>

        {/* Pillar 3 */}
        <motion.div
          whileHover={{ y: -4 }}
          className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-md space-y-3"
        >
          <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-black">
            <Zap className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-lg text-slate-900">3. Weekend Premium</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Friday and Saturday stay nights command a standard +20% (1.20x) weekend surge multiplier due to leisure demand spikes.
          </p>
        </motion.div>

        {/* Pillar 4 */}
        <motion.div
          whileHover={{ y: -4 }}
          className="p-6 rounded-2xl bg-white border border-slate-200/80 shadow-md space-y-3"
        >
          <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-black">
            <Sparkles className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-lg text-slate-900">4. Local Demand Events</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Matches active conventions, festivals, or holidays in the city (e.g. Art Basel 1.45x, Fashion Week 1.60x) to capture peak willingness to pay.
          </p>
        </motion.div>
      </div>

      {/* Interactive Live Rule Simulator */}
      <div className="p-8 rounded-3xl bg-slate-950 text-white border border-slate-800 shadow-2xl">
        <div className="flex items-center justify-between mb-8 pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Sliders className="w-5 h-5 text-indigo-400" />
            <h3 className="font-extrabold text-xl">Interactive Dynamic Rate Simulator</h3>
          </div>
          <span className="text-xs font-mono text-indigo-400 bg-indigo-500/20 px-3 py-1 rounded-full border border-indigo-500/30">
            Live Math Engine
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Sliders Control Panel */}
          <div className="space-y-5 text-sm">
            {/* Base Price */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-400">Base Room Rate</span>
                <span className="text-amber-400 font-mono">${basePrice}</span>
              </div>
              <input
                type="range"
                min="100"
                max="500"
                step="10"
                value={basePrice}
                onChange={(e) => setBasePrice(Number(e.target.value))}
                className="w-full accent-indigo-500 bg-slate-800"
              />
            </div>

            {/* Occupancy Slider */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-400">Target Date Occupancy</span>
                <span className="text-indigo-400 font-mono">{occupancyPct}% ({occMult}x)</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                step="5"
                value={occupancyPct}
                onChange={(e) => setOccupancyPct(Number(e.target.value))}
                className="w-full accent-indigo-500 bg-slate-800"
              />
            </div>

            {/* Lead Days */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-400">Days Until Check-In</span>
                <span className="text-indigo-400 font-mono">{leadDays} days ({leadMult}x)</span>
              </div>
              <input
                type="range"
                min="0"
                max="90"
                step="1"
                value={leadDays}
                onChange={(e) => setLeadDays(Number(e.target.value))}
                className="w-full accent-indigo-500 bg-slate-800"
              />
            </div>

            {/* Toggles */}
            <div className="flex items-center justify-between pt-2">
              <label className="flex items-center gap-2 cursor-pointer text-xs font-medium">
                <input
                  type="checkbox"
                  checked={isWeekend}
                  onChange={(e) => setIsWeekend(e.target.checked)}
                  className="rounded accent-indigo-500 w-4 h-4"
                />
                Weekend Stay (Fri/Sat 1.20x)
              </label>

              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-400">Event Surge:</span>
                <select
                  value={eventMultiplier}
                  onChange={(e) => setEventMultiplier(Number(e.target.value))}
                  className="bg-slate-800 text-xs px-2.5 py-1 rounded border border-slate-700 text-white font-mono"
                >
                  <option value={1.0}>None (1.0x)</option>
                  <option value={1.3}>Tech Conference (1.30x)</option>
                  <option value={1.5}>Festival (1.50x)</option>
                  <option value={1.75}>Major Grand Prix (1.75x)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Computed Result Output Card */}
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col justify-between space-y-4">
            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Formula Equation</span>
              <div className="p-3 mt-2 rounded-xl bg-slate-950 font-mono text-xs text-indigo-300 space-y-1 border border-slate-800">
                <p>${basePrice} &times; {occMult} (Occ) &times; {leadMult} (Lead) &times; {weekendMult} (Wkend) &times; {eventMultiplier} (Evt)</p>
                <p className="text-slate-500 text-[11px]">= Raw Multiplier: {totalMult.toFixed(3)}x</p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-between">
              <div>
                <span className="text-xs font-medium text-slate-300">Computed Nightly Price</span>
                <p className="text-3xl font-black text-white">${finalPrice.toFixed(2)}</p>
              </div>

              <div className="text-right">
                <span className="text-xs text-slate-400">Rate Difference</span>
                <p className={`text-sm font-bold ${finalPrice > basePrice ? 'text-amber-400' : 'text-emerald-400'}`}>
                  {finalPrice >= basePrice ? `+$${(finalPrice - basePrice).toFixed(2)}` : `-$${(basePrice - finalPrice).toFixed(2)}`}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
