import React from 'react';
import { motion } from 'framer-motion';
import { Star, MapPin, Users, CheckCircle2, ArrowRight } from 'lucide-react';
import type { RoomSearchResult } from '../types';
import { PricingTooltip } from './PricingTooltip';

interface HotelCardProps {
  room: RoomSearchResult;
  onSelectBooking: (room: RoomSearchResult) => void;
}

export const HotelCard: React.FC<HotelCardProps> = ({ room, onSelectBooking }) => {
  const isSurge = room.average_nightly_price > room.base_nightly_price;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.3 }}
      className="group rounded-2xl bg-white border border-slate-200/80 shadow-md hover:shadow-xl hover:border-slate-300 transition-all overflow-hidden flex flex-col md:flex-row"
    >
      {/* Image Thumbnail with Badges */}
      <div className="relative md:w-2/5 h-64 md:h-auto overflow-hidden shrink-0">
        <img
          src={room.room_image_url || room.property_image_url}
          alt={room.room_name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 via-transparent to-transparent" />

        {/* City & Rating overlay badges */}
        <div className="absolute top-3 left-3 flex flex-wrap gap-2">
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-900/80 backdrop-blur-md text-white border border-white/20 flex items-center gap-1">
            <MapPin className="w-3 h-3 text-indigo-400" /> {room.property_city}
          </span>
          {room.value_score > 4.5 && (
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-500 text-slate-950 shadow-md">
              High Value Score ({room.value_score})
            </span>
          )}
        </div>

        {/* Availability Badge */}
        <div className="absolute bottom-3 left-3">
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/90 text-white backdrop-blur-xs flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> {room.available_rooms} {room.available_rooms === 1 ? 'room' : 'rooms'} available
          </span>
        </div>
      </div>

      {/* Content Section */}
      <div className="p-6 md:w-3/5 flex flex-col justify-between">
        <div>
          {/* Header & Rating */}
          <div className="flex items-start justify-between gap-2 mb-2">
            <div>
              <p className="text-xs font-bold text-indigo-600 uppercase tracking-wider">{room.property_name}</p>
              <h3 className="text-xl font-extrabold text-slate-900 group-hover:text-indigo-600 transition-colors">
                {room.room_name}
              </h3>
            </div>
            
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 text-white shrink-0">
              <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
              <span className="font-bold text-xs">{room.review_score}</span>
              <span className="text-[10px] text-slate-400">({room.review_count})</span>
            </div>
          </div>

          {/* Max occupancy & amenities */}
          <div className="flex items-center gap-3 text-xs text-slate-500 mb-4">
            <span className="flex items-center gap-1 font-medium text-slate-700">
              <Users className="w-3.5 h-3.5 text-slate-400" /> Max {room.max_occupancy} guests
            </span>
            <span>•</span>
            <div className="flex flex-wrap gap-1.5">
              {room.property_amenities.slice(0, 3).map((amenity, idx) => (
                <span key={idx} className="px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium">
                  {amenity}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Pricing Footer */}
        <div className="pt-4 border-t border-slate-100 flex items-end justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <PricingTooltip
                breakdown={room.nightly_breakdown}
                basePrice={room.base_nightly_price}
                averagePrice={room.average_nightly_price}
              />
            </div>

            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-black text-slate-900">${room.average_nightly_price.toFixed(2)}</span>
              <span className="text-xs text-slate-500 font-medium">/ night</span>

              {isSurge && (
                <span className="text-xs font-semibold text-slate-400 line-through">
                  ${room.base_nightly_price.toFixed(2)}
                </span>
              )}
            </div>
          </div>

          <button
            type="button"
            onClick={() => onSelectBooking(room)}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-600/20 hover:shadow-indigo-600/40 transition-all group/btn"
          >
            Book Room
            <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>
    </motion.div>
  );
};
