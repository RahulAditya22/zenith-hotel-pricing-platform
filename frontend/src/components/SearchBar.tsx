import React from 'react';
import { Search, MapPin, Calendar, Users, SlidersHorizontal } from 'lucide-react';

interface SearchBarProps {
  city: string;
  setCity: (city: string) => void;
  checkInDate: string;
  setCheckInDate: (date: string) => void;
  checkOutDate: string;
  setCheckOutDate: (date: string) => void;
  guests: number;
  setGuests: (n: number) => void;
  sortBy: string;
  setSortBy: (sort: string) => void;
  maxPrice: number;
  setMaxPrice: (price: number) => void;
  onSearch: () => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  city,
  setCity,
  checkInDate,
  setCheckInDate,
  checkOutDate,
  setCheckOutDate,
  guests,
  setGuests,
  sortBy,
  setSortBy,
  maxPrice,
  setMaxPrice,
  onSearch,
}) => {
  const cities = ['All Cities', 'Miami', 'New York', 'Tokyo', 'Paris', 'Aspen'];

  return (
    <div className="w-full p-4 md:p-6 rounded-3xl bg-white border border-slate-200/90 shadow-xl space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* City Filter */}
        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5 text-indigo-600" /> Destination City
          </label>
          <select
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-800 bg-slate-50/50 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          >
            {cities.map((c) => (
              <option key={c} value={c === 'All Cities' ? '' : c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        {/* Check-In Date */}
        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center gap-1">
            <Calendar className="w-3.5 h-3.5 text-indigo-600" /> Check-In
          </label>
          <input
            type="date"
            value={checkInDate}
            onChange={(e) => setCheckInDate(e.target.value)}
            className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-800 bg-slate-50/50 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        {/* Check-Out Date */}
        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center gap-1">
            <Calendar className="w-3.5 h-3.5 text-indigo-600" /> Check-Out
          </label>
          <input
            type="date"
            value={checkOutDate}
            onChange={(e) => setCheckOutDate(e.target.value)}
            className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-800 bg-slate-50/50 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        {/* Guests */}
        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center gap-1">
            <Users className="w-3.5 h-3.5 text-indigo-600" /> Guests
          </label>
          <select
            value={guests}
            onChange={(e) => setGuests(Number(e.target.value))}
            className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-800 bg-slate-50/50 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          >
            {[1, 2, 3, 4, 5, 6].map((n) => (
              <option key={n} value={n}>
                {n} {n === 1 ? 'Guest' : 'Guests'}
              </option>
            ))}
          </select>
        </div>

      </div>

      {/* Secondary Controls: Sorting & Price Filter */}
      <div className="pt-3 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-4 w-full sm:w-auto">
          {/* Sort By */}
          <div className="flex items-center gap-2 text-xs">
            <SlidersHorizontal className="w-4 h-4 text-slate-400" />
            <span className="font-bold text-slate-700">Sort By:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-1.5 rounded-lg border border-slate-300 text-xs font-semibold text-slate-800 bg-white"
            >
              <option value="recommended">Recommended (Value Score)</option>
              <option value="price_low">Price: Low to High</option>
              <option value="price_high">Price: High to Low</option>
              <option value="rating">Review Rating</option>
            </select>
          </div>

          {/* Max Price Slider */}
          <div className="flex items-center gap-2 text-xs">
            <span className="font-bold text-slate-700">Max Rate:</span>
            <input
              type="range"
              min="100"
              max="1000"
              step="50"
              value={maxPrice}
              onChange={(e) => setMaxPrice(Number(e.target.value))}
              className="accent-indigo-600 w-24 sm:w-32"
            />
            <span className="font-mono font-bold text-indigo-700">${maxPrice}</span>
          </div>
        </div>

        {/* Search CTA */}
        <button
          type="button"
          onClick={onSearch}
          className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-600/20 transition-all flex items-center justify-center gap-2"
        >
          <Search className="w-4 h-4" /> Search Availability
        </button>
      </div>
    </div>
  );
};
