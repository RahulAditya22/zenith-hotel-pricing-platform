import React from 'react';
import { Building2, ExternalLink } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-950 text-slate-400 py-12 px-4 border-t border-slate-800">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-black">
            <Building2 className="w-4 h-4" />
          </div>
          <div>
            <p className="text-sm font-bold text-white tracking-wide">ZENITH HOTEL PRICING ENGINE</p>
            <p className="text-xs text-slate-500">Portfolio Project • Built with FastAPI, React, Tailwind & Render</p>
          </div>
        </div>

        {/* Tech Badges */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">FastAPI</span>
          <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">SQLAlchemy 2.0</span>
          <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">React + Vite</span>
          <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">Framer Motion</span>
          <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">Recharts</span>
        </div>

        {/* Links */}
        <div className="flex items-center space-x-4 text-xs font-semibold">
          <a
            href={`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-white flex items-center gap-1 transition-colors"
          >
            Swagger /docs <ExternalLink className="w-3 h-3" />
          </a>
        </div>

      </div>
    </footer>
  );
};
