import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { HeroSection } from './components/HeroSection';
import { SearchBar } from './components/SearchBar';
import { HotelCard } from './components/HotelCard';
import { PriceTrendChart } from './components/PriceTrendChart';
import { BookingModal } from './components/BookingModal';
import { EngineExplanationSection } from './components/EngineExplanationSection';
import { Footer } from './components/Footer';
import { searchRooms } from './api';
import type { RoomSearchResult } from './types';
import { SearchX } from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'search' | 'trend' | 'engine'>('search');

  // Dates defaults: check-in 7 days out, check-out 10 days out
  const today = new Date();
  const defaultCheckIn = new Date(today.getTime() + 7 * 86400000).toISOString().split('T')[0];
  const defaultCheckOut = new Date(today.getTime() + 10 * 86400000).toISOString().split('T')[0];

  const [city, setCity] = useState('');
  const [checkInDate, setCheckInDate] = useState(defaultCheckIn);
  const [checkOutDate, setCheckOutDate] = useState(defaultCheckOut);
  const [guests, setGuests] = useState(1);
  const [sortBy, setSortBy] = useState('recommended');
  const [maxPrice, setMaxPrice] = useState(800);

  const [searchResults, setSearchResults] = useState<RoomSearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedBookingRoom, setSelectedBookingRoom] = useState<RoomSearchResult | null>(null);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const results = await searchRooms({
        city: city || undefined,
        check_in_date: checkInDate,
        check_out_date: checkOutDate,
        guests: guests,
        max_price: maxPrice,
        sort_by: sortBy,
      });
      setSearchResults(results);
    } catch (err) {
      console.error('Failed to search rooms', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    handleSearch();
  }, [city, checkInDate, checkOutDate, guests, sortBy, maxPrice]);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* Sticky Header Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Hero Section */}
      <HeroSection
        onStartSearch={() => {
          setActiveTab('search');
          window.scrollTo({ top: 400, behavior: 'smooth' });
        }}
        onViewTrend={() => {
          setActiveTab('trend');
        }}
      />

      {/* Main View Router */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-10 space-y-12">
        {activeTab === 'search' && (
          <div className="space-y-8">
            {/* Search Filter Bar */}
            <SearchBar
              city={city}
              setCity={setCity}
              checkInDate={checkInDate}
              setCheckInDate={setCheckInDate}
              checkOutDate={checkOutDate}
              setCheckOutDate={setCheckOutDate}
              guests={guests}
              setGuests={setGuests}
              sortBy={sortBy}
              setSortBy={setSortBy}
              maxPrice={maxPrice}
              setMaxPrice={setMaxPrice}
              onSearch={handleSearch}
            />

            {/* Results Title */}
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-black text-slate-900 tracking-tight">Available Rooms & Dynamic Rates</h2>
                <p className="text-xs text-slate-500">
                  Calculated dynamically based on real-time occupancy and date parameters.
                </p>
              </div>

              <span className="text-xs font-bold px-3 py-1 rounded-full bg-slate-200 text-slate-700">
                {searchResults.length} {searchResults.length === 1 ? 'result' : 'results'} found
              </span>
            </div>

            {/* Results Grid / Skeleton Loading */}
            {isLoading ? (
              <div className="space-y-6">
                {[1, 2, 3].map((n) => (
                  <div key={n} className="h-64 rounded-2xl bg-slate-200 animate-pulse" />
                ))}
              </div>
            ) : searchResults.length === 0 ? (
              <div className="py-16 text-center rounded-3xl bg-white border border-slate-200 shadow-sm flex flex-col items-center justify-center space-y-3">
                <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-400">
                  <SearchX className="w-6 h-6" />
                </div>
                <h3 className="font-bold text-lg text-slate-800">No available rooms match your criteria</h3>
                <p className="text-xs text-slate-500 max-w-md">
                  Try adjusting your destination city, increasing your maximum nightly rate, or picking different stay dates.
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                {searchResults.map((room) => (
                  <HotelCard
                    key={`${room.property_id}-${room.room_type_id}`}
                    room={room}
                    onSelectBooking={(r) => setSelectedBookingRoom(r)}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'trend' && (
          <div className="space-y-8">
            <PriceTrendChart />
          </div>
        )}

        {activeTab === 'engine' && (
          <div className="space-y-8">
            <EngineExplanationSection />
          </div>
        )}

        {/* Global Engine Explanation below search for easy reading */}
        {activeTab === 'search' && <EngineExplanationSection />}
      </main>

      {/* Booking Modal */}
      {selectedBookingRoom && (
        <BookingModal
          room={selectedBookingRoom}
          checkInDate={checkInDate}
          checkOutDate={checkOutDate}
          onClose={() => setSelectedBookingRoom(null)}
          onSuccess={() => {
            handleSearch();
          }}
        />
      )}

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default App;
