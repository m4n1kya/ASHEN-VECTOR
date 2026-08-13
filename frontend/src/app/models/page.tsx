"use client";

import { useState } from "react";
import { Cpu, Search, AlertTriangle } from "lucide-react";
import Link from "next/link";

export default function ModelsPage() {
  const [symbol, setSymbol] = useState("AAPL");
  const [models, setModels] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchModels = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/stocks/${symbol.toUpperCase()}/models`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to fetch models");
      setModels(data.models || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full gap-8 py-8 animate-in fade-in duration-500">
      
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-quant-border">
        <div>
          <h1 className="text-3xl font-normal tracking-wider text-quant-text-primary mb-2 flex items-center gap-3">
            <Cpu className="w-8 h-8 text-quant-text-muted" />
            MODEL REGISTRY
          </h1>
          <p className="text-xs tracking-widest text-quant-text-secondary uppercase">Instrument-Specific Trained Models</p>
        </div>
      </div>

      <form onSubmit={fetchModels} className="matte-panel p-4 flex gap-4 w-full md:w-1/2">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="ENTER SYMBOL (E.G. AAPL)"
          className="flex-1 bg-quant-bg border border-quant-border p-2 text-xs font-mono uppercase text-quant-text-primary focus:outline-none focus:border-quant-text-muted"
        />
        <button 
          type="submit" 
          disabled={loading}
          className="bg-quant-border hover:bg-quant-text-muted transition-colors text-quant-text-primary px-6 text-[10px] font-bold tracking-widest uppercase rounded-sm disabled:opacity-50 flex items-center gap-2"
        >
          {loading ? "SEARCHING..." : <><Search className="w-3.5 h-3.5" /> SEARCH</>}
        </button>
      </form>

      {error && (
        <div className="bg-quant-down/10 border border-quant-down/30 text-quant-down-text p-4 rounded-sm flex items-center gap-3 text-xs font-mono">
          <AlertTriangle className="w-4 h-4" />
          <p>{error}</p>
        </div>
      )}

      {models && models.length === 0 && !error && (
        <div className="matte-panel p-12 flex flex-col items-center justify-center text-center">
          <div className="text-sm font-mono tracking-widest text-quant-text-secondary mb-2 uppercase">NO MODELS FOUND FOR {symbol}</div>
          <p className="text-xs text-quant-text-muted">The backend model registry returned 0 active models for this instrument.</p>
        </div>
      )}

      {models && models.length > 0 && (
        <div className="flex flex-col gap-4">
          <div className="grid grid-cols-7 gap-4 px-4 pb-2 border-b border-quant-border text-[10px] font-bold tracking-widest text-quant-text-muted uppercase">
            <div className="col-span-2">Model Name / ID</div>
            <div>Type</div>
            <div>Target</div>
            <div>Horizon</div>
            <div>Validation</div>
            <div>Calibration</div>
          </div>
          
          {models.map((m: any, i: number) => (
            <div key={i} className="matte-panel p-4 grid grid-cols-7 gap-4 items-center">
              <div className="col-span-2 flex flex-col">
                <span className="text-xs font-mono text-quant-text-primary truncate" title={m.model_id}>{m.model_id}</span>
                <span className="text-[10px] tracking-widest text-quant-text-secondary">v{m.version || '1.0'}</span>
              </div>
              <div className="text-[10px] font-bold tracking-widest uppercase text-quant-text-primary">{m.type || 'N/A'}</div>
              <div className="text-[10px] font-mono tracking-widest text-quant-text-secondary">{m.target || 'N/A'}</div>
              <div className="text-[10px] font-mono tracking-widest text-quant-text-secondary">{m.horizon ? `${m.horizon}D` : 'N/A'}</div>
              <div className="text-[10px] font-bold tracking-widest uppercase text-quant-text-primary">{m.validation?.method || 'N/A'}</div>
              <div className="text-[10px] font-bold tracking-widest uppercase text-quant-text-primary">{m.calibration?.method || 'N/A'}</div>
            </div>
          ))}
        </div>
      )}
      
      {!models && !loading && !error && (
        <div className="text-[10px] text-quant-text-muted uppercase tracking-widest text-center py-12 border border-dashed border-quant-border rounded-sm">
          Select an instrument to view its trained models.
        </div>
      )}

    </div>
  );
}
