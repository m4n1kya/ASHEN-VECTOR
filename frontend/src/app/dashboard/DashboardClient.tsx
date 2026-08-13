"use client";

import { useState } from "react";
import { Play, Loader2 } from "lucide-react";
import StockDetailClient from "../stocks/[symbol]/StockDetailClient";

export default function DashboardClient() {
  const [inputSymbol, setInputSymbol] = useState("TSLA");
  const [activeSymbol, setActiveSymbol] = useState("TSLA");
  const [loading, setLoading] = useState(false);

  const handleRun = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputSymbol.trim()) return;
    setLoading(true);
    setActiveSymbol(inputSymbol.trim().toUpperCase());
    // Simulate slight loading delay for the button state, actual loading is in StockDetailClient
    setTimeout(() => setLoading(false), 500); 
  };

  return (
    <div className="flex-1 flex flex-col h-full gap-6 max-w-[1600px] mx-auto w-full pb-8">
      
      {/* SEARCH FORM (Like old ModelsClient) */}
      <form onSubmit={handleRun} className="bg-[#0A0A0A] matte-panel p-4 shrink-0 rounded-sm border border-quant-border mt-6">
        <div className="flex items-end gap-4">
          <div className="flex-1">
            <label className="block text-[10px] tracking-widest uppercase text-quant-text-secondary mb-1.5">Target Symbol</label>
            <input 
              type="text" 
              value={inputSymbol} 
              onChange={e => setInputSymbol(e.target.value.toUpperCase())}
              className="w-full bg-black border border-quant-border rounded-sm p-2 text-sm font-mono tabular-nums text-quant-text-primary focus:outline-none focus:border-quant-text-secondary transition-colors uppercase"
              placeholder="e.g. TSLA"
              required
            />
          </div>
          <button 
            type="submit" 
            disabled={loading}
            className="bg-quant-elevated text-quant-text-primary text-xs tracking-widest font-bold rounded-sm px-6 py-2 border border-transparent hover:border-quant-text-secondary transition-colors disabled:opacity-50 flex items-center justify-center gap-2 h-[38px]"
          >
            {loading ? (
              <><Loader2 className="w-3.5 h-3.5 animate-spin text-quant-text-secondary" /> ANALYZING...</>
            ) : (
              <><Play className="w-3.5 h-3.5" /> INFER</>
            )}
          </button>
        </div>
      </form>

      {/* RENDER THE DEEP RESEARCH GRID */}
      <StockDetailClient symbol={activeSymbol} />
      
    </div>
  );
}
