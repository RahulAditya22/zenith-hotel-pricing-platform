import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, ReferenceLine } from 'recharts';
import { TrendingUp, Zap, RefreshCw } from 'lucide-react';
import { fetchPriceTrend, fetchProperties, fetchPropertyRooms } from '../api';
import type { Property, RoomType, PriceTrendResponse } from '../types';

export const PriceTrendChart: React.FC = () => {
  const [properties, setProperties] = useState<Property[]>([]);
  const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
  const [selectedPropId, setSelectedPropId] = useState<number | null>(null);
  const [selectedRoomId, setSelectedRoomId] = useState<number | null>(null);
  const [trendData, setTrendData] = useState<PriceTrendResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initial load properties
  useEffect(() => {
    const loadProps = async () => {
      try {
        const props = await fetchProperties();
        setProperties(props);
        if (props.length > 0) {
          setSelectedPropId(props[0].id);
        }
      } catch (err) {
        console.error('Failed to load properties for chart', err);
      }
    };
    loadProps();
  }, []);

  // Load room types when property changes
  useEffect(() => {
    if (!selectedPropId) return;
    const loadRooms = async () => {
      try {
        const rooms = await fetchPropertyRooms(selectedPropId);
        setRoomTypes(rooms);
        if (rooms.length > 0) {
          setSelectedRoomId(rooms[0].id);
        }
      } catch (err) {
        console.error('Failed to load room types', err);
      }
    };
    loadRooms();
  }, [selectedPropId]);

  // Fetch 30-day price trend when room changes
  useEffect(() => {
    if (!selectedRoomId) return;
    const loadTrend = async () => {
      setIsLoading(true);
      try {
        const data = await fetchPriceTrend({ room_type_id: selectedRoomId, days: 30 });
        setTrendData(data);
      } catch (err) {
        console.error('Failed to load price trend', err);
      } finally {
        setIsLoading(false);
      }
    };
    loadTrend();
  }, [selectedRoomId]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="p-6 md:p-8 rounded-3xl bg-slate-900 border border-slate-800 text-white shadow-2xl"
    >
      {/* Chart Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-8 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 flex items-center gap-1.5">
              <TrendingUp className="w-3.5 h-3.5" /> Dynamic Rate Projection
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight">30-Day Rate Forecast</h2>
          <p className="text-sm text-slate-400 mt-1">
            Simulating occupancy surges, weekend premiums, and event multipliers across future dates.
          </p>
        </div>

        {/* Dropdown Selectors */}
        <div className="flex flex-col sm:flex-row items-center gap-3">
          {/* Property Select */}
          <div className="w-full sm:w-auto relative">
            <select
              value={selectedPropId || ''}
              onChange={(e) => setSelectedPropId(Number(e.target.value))}
              className="w-full sm:w-auto bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              {properties.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.city})
                </option>
              ))}
            </select>
          </div>

          {/* Room Type Select */}
          <div className="w-full sm:w-auto relative">
            <select
              value={selectedRoomId || ''}
              onChange={(e) => setSelectedRoomId(Number(e.target.value))}
              className="w-full sm:w-auto bg-indigo-600 border border-indigo-500 text-white rounded-xl px-4 py-2.5 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-amber-400 shadow-md shadow-indigo-600/30"
            >
              {roomTypes.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.name} (${r.base_price}/base)
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Chart Canvas */}
      {isLoading ? (
        <div className="h-80 flex flex-col items-center justify-center text-slate-400">
          <RefreshCw className="w-8 h-8 animate-spin text-indigo-500 mb-3" />
          <p className="text-sm font-medium">Calculating 30-day dynamic pricing vectors...</p>
        </div>
      ) : trendData ? (
        <div>
          {/* Key Stats Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
            <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <span className="text-[11px] font-medium text-slate-400 uppercase">Base Rate</span>
              <p className="text-lg font-bold text-slate-200">${trendData.base_price.toFixed(2)}</p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <span className="text-[11px] font-medium text-slate-400 uppercase">Peak Forecast</span>
              <p className="text-lg font-bold text-amber-400">
                ${Math.max(...trendData.points.map((p) => p.price)).toFixed(2)}
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <span className="text-[11px] font-medium text-slate-400 uppercase">Lowest Rate</span>
              <p className="text-lg font-bold text-emerald-400">
                ${Math.min(...trendData.points.map((p) => p.price)).toFixed(2)}
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60">
              <span className="text-[11px] font-medium text-slate-400 uppercase">Average Rate</span>
              <p className="text-lg font-bold text-indigo-300">
                ${(
                  trendData.points.reduce((acc, curr) => acc + curr.price, 0) /
                  trendData.points.length
                ).toFixed(2)}
              </p>
            </div>
          </div>

          {/* Recharts Component */}
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData.points} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.6} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
                  </linearGradient>
                </defs>

                <XAxis
                  dataKey="date"
                  tickFormatter={(val: string) => val.slice(8)} // show DD
                  stroke="#64748b"
                  fontSize={12}
                  tickLine={false}
                />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} />

                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const pt = payload[0].payload;
                      return (
                        <div className="p-3 rounded-xl bg-slate-900 border border-slate-700 shadow-xl text-xs space-y-1.5">
                          <div className="font-bold text-slate-200 border-b border-slate-800 pb-1 flex justify-between gap-4">
                            <span>{pt.date} ({pt.day_name})</span>
                            {pt.is_weekend && <span className="text-amber-400">Weekend</span>}
                          </div>
                          <div className="flex justify-between gap-4 text-indigo-400 font-bold text-sm">
                            <span>Nightly Rate:</span>
                            <span>${pt.price.toFixed(2)}</span>
                          </div>
                          <div className="text-slate-400">
                            Occupancy: {(pt.occupancy_rate * 100).toFixed(0)}% ({pt.occupancy_multiplier}x)
                          </div>
                          {pt.event_name && (
                            <div className="text-emerald-400 font-semibold flex items-center gap-1">
                              <Zap className="w-3 h-3" /> Event: {pt.event_name} (+{((pt.event_multiplier - 1) * 100).toFixed(0)}%)
                            </div>
                          )}
                        </div>
                      );
                    }
                    return null;
                  }}
                />

                <ReferenceLine
                  y={trendData.base_price}
                  stroke="#f59e0b"
                  strokeDasharray="4 4"
                  label={{ value: 'Base Rate', fill: '#f59e0b', fontSize: 11, position: 'insideTopLeft' }}
                />

                <Area
                  type="monotone"
                  dataKey="price"
                  stroke="#818cf8"
                  strokeWidth={3}
                  fillOpacity={1}
                  fill="url(#priceGradient)"
                  animationDuration={1200}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      ) : null}
    </motion.div>
  );
};
