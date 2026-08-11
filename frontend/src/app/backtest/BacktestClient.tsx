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
      <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-xl grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
        <div>
          <label className="block text-xs uppercase text-ashen-ash-light mb-1">Symbol</label>
          <input 
            type="text" 
            value={symbol} 
            onChange={e => setSymbol(e.target.value.toUpperCase())}
            className="w-full bg-ashen-charcoal-light border border-ashen-ash rounded p-2 text-ashen-bone focus:outline-none focus:border-ashen-up"
            required
          />
        </div>
        <div>
          <label className="block text-xs uppercase text-ashen-ash-light mb-1">Start Date</label>
          <input 
            type="date" 
            value={startDate} 
            onChange={e => setStartDate(e.target.value)}
            className="w-full bg-ashen-charcoal-light border border-ashen-ash rounded p-2 text-ashen-bone focus:outline-none focus:border-ashen-up"
            required
          />
        </div>
        <div>
          <label className="block text-xs uppercase text-ashen-ash-light mb-1">End Date</label>
          <input 
            type="date" 
            value={endDate} 
            onChange={e => setEndDate(e.target.value)}
            className="w-full bg-ashen-charcoal-light border border-ashen-ash rounded p-2 text-ashen-bone focus:outline-none focus:border-ashen-up"
            required
          />
        </div>
        <div>
          <label className="block text-xs uppercase text-ashen-ash-light mb-1">Horizon (Days)</label>
          <input 
            type="number" 
            value={horizon} 
            onChange={e => setHorizon(parseInt(e.target.value))}
            className="w-full bg-ashen-charcoal-light border border-ashen-ash rounded p-2 text-ashen-bone focus:outline-none focus:border-ashen-up"
            min={1}
            required
          />
        </div>
        <div>
          <button 
            type="submit" 
            disabled={status === "RUNNING" || status === "QUEUED"}
            className="w-full bg-ashen-bone text-ashen-black font-bold rounded p-2 hover:bg-white transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {status === "RUNNING" || status === "QUEUED" ? (
              <><Activity className="w-4 h-4 animate-spin" /> {status}</>
            ) : (
              <><Play className="w-4 h-4" /> Run Backtest</>
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-ashen-down/10 border border-ashen-down text-ashen-down p-4 rounded flex items-center gap-3">
          <AlertTriangle className="w-5 h-5" />
          <p>{error}</p>
        </div>
      )}

      {result && <ResultsDisplay result={result} />}
    </div>
  );
}
