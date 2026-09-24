import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, User, Mail, ShieldCheck, CheckCircle, AlertTriangle, Loader2, Sparkles } from 'lucide-react';
import { createReservation } from '../api';
import type { RoomSearchResult, Reservation } from '../types';

interface BookingModalProps {
  room: RoomSearchResult | null;
  onClose: () => void;
  onSuccess: () => void;
}

export const BookingModal: React.FC<BookingModalProps> = ({ room, onClose, onSuccess }) => {
  const [guestName, setGuestName] = useState('');
  const [guestEmail, setGuestEmail] = useState('');
  const [guestCount, setGuestCount] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [confirmedReservation, setConfirmedReservation] = useState<Reservation | null>(null);

  if (!room) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setIsLoading(true);

    try {
      const res = await createReservation({
        room_type_id: room.room_type_id,
        guest_name: guestName,
        guest_email: guestEmail,
        check_in_date: room.nightly_breakdown[0]?.date || new Date().toISOString().split('T')[0],
        check_out_date:
          room.nightly_breakdown[room.nightly_breakdown.length - 1]?.date ||
          new Date(Date.now() + 86400000).toISOString().split('T')[0],
        guest_count: guestCount,
      });

      setConfirmedReservation(res);
      onSuccess();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Booking failed. Please try another room or date.';
      setErrorMsg(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-md">
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          className="relative w-full max-w-lg bg-white rounded-3xl border border-slate-200 shadow-2xl overflow-hidden"
        >
          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 z-10 p-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>

          {confirmedReservation ? (
            /* Confirmation Screen */
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-8 text-center"
            >
              <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-emerald-500 text-white flex items-center justify-center shadow-lg shadow-emerald-500/30">
                <CheckCircle className="w-10 h-10" />
              </div>

              <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200 inline-flex items-center gap-1 mb-2">
                <Sparkles className="w-3 h-3 text-emerald-600" /> Booking Confirmed!
              </span>

              <h2 className="text-2xl font-black text-slate-900 mb-1">Reservation Complete</h2>
              <p className="text-sm text-slate-500 mb-6">Your room has been locked in the inventory engine.</p>

              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 text-left space-y-3 mb-6">
                <div className="flex justify-between items-center pb-2 border-b border-slate-200">
                  <span className="text-xs text-slate-500 font-medium">Reservation Code</span>
                  <span className="font-mono font-bold text-indigo-600 text-sm">{confirmedReservation.reservation_code}</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-500">Property</span>
                  <span className="font-semibold text-slate-800">{room.property_name}</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-500">Room</span>
                  <span className="font-semibold text-slate-800">{room.room_name}</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-500">Total Price</span>
                  <span className="font-extrabold text-slate-900">${confirmedReservation.total_price.toFixed(2)}</span>
                </div>
              </div>

              <button
                type="button"
                onClick={onClose}
                className="w-full py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-md transition-all"
              >
                Done
              </button>
            </motion.div>
          ) : (
            /* Booking Form */
            <form onSubmit={handleSubmit} className="p-6 md:p-8">
              <div className="mb-6">
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">{room.property_name}</span>
                <h2 className="text-2xl font-black text-slate-900">{room.room_name}</h2>
                <p className="text-xs text-slate-500 mt-1">
                  ${room.average_nightly_price.toFixed(2)} / night avg • {room.nightly_breakdown.length} nights
                </p>
              </div>

              {errorMsg && (
                <div className="p-3 mb-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                  <p>{errorMsg}</p>
                </div>
              )}

              <div className="space-y-4 mb-6">
                {/* Guest Name */}
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Guest Full Name</label>
                  <div className="relative">
                    <User className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      required
                      placeholder="e.g. Sarah Jenkins"
                      value={guestName}
                      onChange={(e) => setGuestName(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-sm font-medium focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Email Address */}
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
                  <div className="relative">
                    <Mail className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                    <input
                      type="email"
                      required
                      placeholder="sarah@example.com"
                      value={guestEmail}
                      onChange={(e) => setGuestEmail(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-sm font-medium focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Guests Count */}
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Guests</label>
                  <select
                    value={guestCount}
                    onChange={(e) => setGuestCount(Number(e.target.value))}
                    className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-medium focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                  >
                    {Array.from({ length: room.max_occupancy }, (_, i) => i + 1).map((n) => (
                      <option key={n} value={n}>
                        {n} {n === 1 ? 'Guest' : 'Guests'}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Price Breakdown Footer */}
              <div className="p-4 mb-6 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                <div>
                  <span className="text-xs text-slate-500 font-medium">Total Stay Amount</span>
                  <p className="text-xl font-black text-slate-900">${room.total_price.toFixed(2)}</p>
                </div>
                <div className="flex items-center gap-1 text-xs text-emerald-600 font-bold bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
                  <ShieldCheck className="w-4 h-4" /> Concurrency-Protected Lock
                </div>
              </div>

              {/* Confirm CTA */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-lg shadow-indigo-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" /> Confirming Reservation...
                  </>
                ) : (
                  'Confirm & Reserve Room'
                )}
              </button>
            </form>
          )}
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
