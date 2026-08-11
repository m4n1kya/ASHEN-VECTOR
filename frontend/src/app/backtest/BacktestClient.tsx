"use client";

import { useState, useEffect } from "react";
import { runBacktest, checkBacktestStatus, getBacktestResult } from "@/lib/api";
import { Activity, Play, AlertTriangle } from "lucide-react";
import ResultsDisplay from "./ResultsDisplay";

export default function BacktestClient({ defaultSymbol }: { defaultSymbol: string }) {
  const [symbol, setSymbol] = useState(defaultSymbol);
  const [startDate, setStartDate] = useState("2020-01-01");
  const [endDate, setEndDate] = useState("2021-01-01");
  const [horizon, setHorizon] = useState(5);
  
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setJobId(null);
    setStatus("SUBMITTING");
    setError(null);
    setResult(null);

    try {
      const job = await runBacktest({
        symbol,
        start_date: startDate,
        end_date: endDate,
        horizon,
        initial_capital: 100000,
        strategy: "ashen_vector",
        commission_bps: 5,
        slippage_bps: 5
      });
      setJobId(job.job_id);
      setStatus(job.status);
    } catch (err: any) {
      setError(err.message);
      setStatus(null);
    }
  };

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (jobId && (status === "QUEUED" || status === "RUNNING")) {
      interval = setInterval(async () => {
        try {
          const job = await checkBacktestStatus(jobId);
          setStatus(job.status);
          
          if (job.status === "COMPLETED") {
            const res = await getBacktestResult(jobId);
            setResult(res);
          } else if (job.status === "FAILED") {
            setError(job.error || "Job failed");
          }
        } catch (err: any) {
          setError(err.message);
        }
      }, 2000);
    }
    
    return () => clearInterval(interval);
  }, [jobId, status]);

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="matte-panel p-4 grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
        <div>
          <label className="block text-[10px] tracking-widest uppercase text-quant-text-muted mb-1.5">Symbol</label>
          <input 
            type="text" 
            value={symbol} 
            onChange={e => setSymbol(e.target.value.toUpperCase())}
            className="w-full bg-quant-bg border border-quant-border rounded-sm p-1.5 text-xs font-mono tabular-nums text-quant-text-primary focus:outline-none focus:border-quant-text-muted transition-colors"
            required
          />
        </div>
        <div>
          <label className="block text-[10px] tracking-widest uppercase text-quant-text-muted mb-1.5">Start Date</label>
          <input 
            type="date" 
            value={startDate} 
            onChange={e => setStartDate(e.target.value)}
            className="w-full bg-quant-bg border border-quant-border rounded-sm p-1.5 text-xs font-mono tabular-nums text-quant-text-primary focus:outline-none focus:border-quant-text-muted transition-colors"
            required
          />
        </div>
        <div>
          <label className="block text-[10px] tracking-widest uppercase text-quant-text-muted mb-1.5">End Date</label>
          <input 
            type="date" 
            value={endDate} 
            onChange={e => setEndDate(e.target.value)}
            className="w-full bg-quant-bg border border-quant-border rounded-sm p-1.5 text-xs font-mono tabular-nums text-quant-text-primary focus:outline-none focus:border-quant-text-muted transition-colors"
            required
          />
        </div>
        <div>
          <label className="block text-[10px] tracking-widest uppercase text-quant-text-muted mb-1.5">Horizon (Days)</label>
          <input 
            type="number" 
            value={horizon} 
            onChange={e => setHorizon(parseInt(e.target.value))}
            className="w-full bg-quant-bg border border-quant-border rounded-sm p-1.5 text-xs font-mono tabular-nums text-quant-text-primary focus:outline-none focus:border-quant-text-muted transition-colors"
            min={1}
            required
          />
        </div>
        <div>
          <button 
            type="submit" 
            disabled={status === "RUNNING" || status === "QUEUED"}
            className="w-full bg-quant-border text-quant-text-primary text-xs tracking-widest font-bold rounded-sm p-1.5 border border-transparent hover:border-quant-text-muted transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {status === "RUNNING" || status === "QUEUED" ? (
              <><Activity className="w-3.5 h-3.5 animate-spin" /> {status}</>
            ) : (
              <><Play className="w-3.5 h-3.5" /> EXECUTE</>
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-quant-down/10 border border-quant-down/30 text-quant-down-text p-3 rounded-sm flex items-center gap-3 text-xs">
          <AlertTriangle className="w-4 h-4" />
          <p>{error}</p>
        </div>
      )}

      {result && <ResultsDisplay result={result} />}
    </div>
  );
}
