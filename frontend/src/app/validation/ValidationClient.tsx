"use client";

import { useState, useEffect } from "react";
import { Activity, Play, AlertTriangle, CheckCircle, ArrowLeft } from "lucide-react";
import { useRouter } from "next/navigation";
import MethodologyPanel from "@/components/validation/MethodologyPanel";
import PredictiveMetrics from "@/components/validation/PredictiveMetrics";
import TradingPerformance from "@/components/validation/TradingPerformance";
import BaselineComparison from "@/components/validation/BaselineComparison";
import EquityCurveChart from "@/components/validation/EquityCurveChart";
import DrawdownChart from "@/components/validation/DrawdownChart";
import CalibrationChart from "@/components/validation/CalibrationChart";
import FoldStability from "@/components/validation/FoldStability";
import FeatureImportance from "@/components/validation/FeatureImportance";
import ModelVerdict from "@/components/validation/ModelVerdict";

export default function ValidationClient() {
  const router = useRouter();
  const [symbol, setSymbol] = useState("AAPL");
  const [model, setModel] = useState("LIGHTGBM");
  
  const timeOptions = [
    { label: "1 MONTH", value: "21" },
    { label: "3 MONTHS", value: "63" },
    { label: "1 YEAR", value: "252" },
    { label: "3 YEAR", value: "756" },
    { label: "5 YEAR", value: "1260" },
    { label: "10 YEAR", value: "2520" },
  ];
  const [time, setTime] = useState("252"); // Default 1 YEAR
  
  const [status, setStatus] = useState<"IDLE" | "QUEUED" | "RUNNING" | "COMPLETED" | "FAILED">("IDLE");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  const availableModels = ["MOMENTUM", "MEAN REVERSION", "LINEAR REGRESSION", "ARIMA", "LIGHTGBM", "XGBOOST", "RANDOM FOREST"];

  const handleRun = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("QUEUED");
    setError(null);
    setResult(null);

    try {
      const runRes = await fetch("http://127.0.0.1:8000/api/validation/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol, model, horizon: parseInt(time) })
      });
      const runData = await runRes.json();
      if (!runRes.ok) throw new Error(runData.detail || "Failed to start validation job");

      const jobId = runData.job_id;
      pollJob(jobId);
    } catch (err: any) {
      setError(err.message);
      setStatus("FAILED");
    }
  };

  const pollJob = async (jobId: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/validation/jobs/${jobId}`);
      const data = await res.json();
      
      if (!res.ok) throw new Error(data.detail || "Failed to fetch job status");
      
      if (data.status === "FAILED") {
        throw new Error(data.error || "Validation job failed internally.");
      }

      setStatus(data.status); // RUNNING, QUEUED, COMPLETED

      if (data.status === "COMPLETED") {
        fetchResults(jobId);
      } else {
        setTimeout(() => pollJob(jobId), 2000); // Poll every 2 seconds
      }
    } catch (err: any) {
      setError(err.message);
      setStatus("FAILED");
    }
  };

  const fetchResults = async (jobId: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/validation/jobs/${jobId}/results`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to fetch results");
      setResult(data);
    } catch (err: any) {
      setError(err.message);
      setStatus("FAILED");
    }
  };

  return (
    <div className="flex-1 flex flex-col min-h-0 gap-6">
      <div className="flex items-center">
        <button type="button" onClick={() => router.back()} className="text-quant-text-muted hover:text-white transition-colors flex items-center gap-1.5 text-[10px] tracking-widest uppercase font-bold">
          <ArrowLeft className="w-3.5 h-3.5" /> Back
        </button>
      </div>

      <form onSubmit={handleRun} className="matte-panel p-4 shrink-0 flex flex-col gap-6">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
          <div className="col-span-1 md:col-span-3">
            <label className="block text-[10px] tracking-widest uppercase text-quant-text-muted mb-1.5">Asset</label>
            <input 
              type="text" 
              value={symbol} 
              onChange={e => setSymbol(e.target.value.toUpperCase())}
              className="w-full bg-quant-bg border border-quant-border rounded-sm p-2 text-sm font-mono tabular-nums text-quant-text-primary focus:outline-none focus:border-quant-text-muted transition-colors"
              placeholder="e.g. AAPL"
              required
            />
          </div>
          
          <div className="col-span-1 md:col-span-4">
            <label className="block text-[10px] tracking-widest uppercase text-quant-text-muted mb-1.5">Time (Horizon)</label>
            <select 
              value={time}
              onChange={e => setTime(e.target.value)}
              className="w-full bg-quant-bg border border-quant-border rounded-sm p-2 text-sm font-mono text-quant-text-primary focus:outline-none focus:border-quant-text-muted transition-colors appearance-none"
            >
              {timeOptions.map(t => <option key={t.label} value={t.value}>{t.label}</option>)}
            </select>
          </div>

          <div className="col-span-1 md:col-span-5 flex items-end h-[58px]">
            <button 
              type="submit" 
              disabled={status === "QUEUED" || status === "RUNNING"}
              className="w-full bg-quant-border text-quant-text-primary text-[10px] tracking-widest font-bold rounded-sm p-2 border border-transparent hover:border-quant-text-muted transition-colors disabled:opacity-50 flex items-center justify-center gap-2 h-[38px] uppercase"
            >
              {status === "QUEUED" || status === "RUNNING" ? (
                <><img src="/logo.png" alt="Loading" className="w-3.5 h-3.5 animate-[spin_4s_linear_infinite]" /> {status}</>
              ) : (
                <><Play className="w-3.5 h-3.5" /> RUN OOS VALIDATION</>
              )}
            </button>
          </div>
        </div>

        <div className="col-span-1 md:col-span-12">
          <label className="block text-[10px] tracking-widest uppercase text-quant-text-muted mb-3">Model Topology</label>
          <div className="flex flex-wrap gap-2">
            {availableModels.map(m => (
              <button
                key={m}
                type="button"
                onClick={() => setModel(m)}
                className={`px-4 py-2 text-xs font-bold tracking-widest uppercase rounded-sm border transition-colors ${
                  model === m 
                    ? 'bg-[#10B981] text-black border-[#10B981]' 
                    : 'bg-quant-bg text-quant-text-primary border-quant-border hover:border-quant-text-muted'
                }`}
              >
                {m}
              </button>
            ))}
          </div>
        </div>
      </form>

      {error && (
        <div className="bg-quant-down/10 border border-quant-down/30 text-quant-down-text p-4 rounded-sm flex items-center gap-3 text-xs">
          <AlertTriangle className="w-4 h-4" />
          <p>{error}</p>
        </div>
      )}

      {status === "COMPLETED" && result && (
        <div className="flex-1 overflow-y-auto space-y-6 pb-10">
          
          {result.verdict && (
            <ModelVerdict data={result.verdict} />
          )}

          <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
            <div className="md:col-span-3">
              <MethodologyPanel data={result.methodology} />
            </div>
            <div className="md:col-span-4">
              <PredictiveMetrics data={result.predictive_metrics} />
            </div>
            <div className="md:col-span-5">
              <TradingPerformance data={result.trading_performance} />
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <EquityCurveChart data={result.equity_curve} />
            <div className="flex flex-col gap-6">
              <DrawdownChart data={result.drawdown} />
              <CalibrationChart data={result.calibration} />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <FoldStability data={result.fold_stability} />
            </div>
            <div className="lg:col-span-1">
              <FeatureImportance data={result.feature_importance} />
            </div>
            <div className="lg:col-span-1">
              <BaselineComparison data={result.baseline_comparison} />
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
