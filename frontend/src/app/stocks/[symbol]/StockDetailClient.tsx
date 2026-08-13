"use client";

import { useState, useEffect } from "react";
import { Activity, Play, AlertTriangle, Info, BarChart2, Shield, TrendingUp, Layers, Wind, Activity as ActivityIcon, Loader2, Triangle } from "lucide-react";
import Link from "next/link";
import PriceChart from "./PriceChart"; // Ensure we copy this from instruments/[symbol]/PriceChart.tsx

export default function StockDetailClient({ symbol }: { symbol: string }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [overview, setOverview] = useState<any>(null);
  const [liveMath, setLiveMath] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [overviewRes, liveRes] = await Promise.all([
          fetch(`http://127.0.0.1:8000/api/stocks/${symbol}/overview`),
          fetch(`http://127.0.0.1:8000/api/live/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol, models: ["ALL"], horizons: [21] })
          })
        ]);

        if (!liveRes.ok) {
          const errData = await liveRes.json().catch(() => ({}));
          throw new Error(errData.detail || "Failed to fetch quantitative analysis");
        }

        const liveData = await liveRes.json();
        let overviewData = null;
        if (overviewRes.ok) {
          overviewData = await overviewRes.json();
        }

        setOverview(overviewData);
        setLiveMath(liveData);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [symbol]);

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center h-full gap-4 text-quant-text-secondary animate-in fade-in duration-500">
        <Loader2 className="w-8 h-8 animate-spin" />
        <div className="text-[10px] tracking-widest uppercase font-mono">Loading Quantitative Model...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 flex flex-col items-center justify-center h-full">
        <AlertTriangle className="w-8 h-8 text-quant-down-text mb-4" />
        <h1 className="text-xl font-bold tracking-widest text-quant-down-text mb-4">FAILED TO LOAD {symbol}</h1>
        <p className="text-xs text-quant-text-muted font-mono">{error}</p>
      </div>
    );
  }

  const getSignalColor = (signal: string) => {
    if (!signal) return "text-quant-text-secondary";
    const s = signal.toUpperCase();
    if (s.includes("BUY") || s.includes("BULL") || s.includes("STRONG") || s.includes("HIGH EVID")) return "text-quant-up-text";
    if (s.includes("SELL") || s.includes("BEAR") || s.includes("WEAK") || s.includes("RISK")) return "text-quant-down-text";
    return "text-quant-warn-text"; // HOLD/MODERATE
  };

  const market = overview?.market || {};
  const perf = overview?.performance || {};
  const risk = overview?.risk || {};
  
  // Real Price (fallback to liveData latest_price)
  const price = market.close || liveMath?.latest_price || 0;
  const ret = perf.return_1d || 0;

  return (
    <div className="flex flex-col h-full space-y-6 animate-in fade-in duration-500 pb-8">
      
      {/* HEADER */}
      <div className="flex items-center justify-between pb-6 border-b border-quant-border">
        <div className="flex items-center gap-4">
          <h1 className="text-5xl font-light tracking-wide text-quant-text-primary">{symbol}</h1>
          <div className="flex flex-col">
            <span className="text-sm text-quant-text-secondary">{overview?.instrument?.name || liveMath?.name || 'Unknown Name'}</span>
            <span className="text-xs text-quant-text-muted">{overview?.instrument?.exchange || 'EXCHANGE'}</span>
          </div>
          
          {/* Context Navbar */}
          <div className="ml-8 flex gap-4 bg-quant-elevated p-2 rounded-sm border border-quant-border">
            <Link href="/validation" className="text-[10px] tracking-widest uppercase font-bold text-quant-text-secondary hover:text-quant-text-primary hover:bg-quant-border px-4 py-2 rounded-sm transition-all flex items-center gap-2">
              <ActivityIcon className="w-3.5 h-3.5" /> Detailed Model Analysis
            </Link>
            <a href={`https://www.bloomberg.com/search?query=${overview?.instrument?.name || liveMath?.name || symbol}`} target="_blank" rel="noopener noreferrer" className="text-[10px] tracking-widest uppercase font-bold text-quant-text-secondary hover:text-quant-text-primary hover:bg-quant-border px-4 py-2 rounded-sm transition-all flex items-center gap-2">
              <Play className="w-3.5 h-3.5" /> News (Bloomberg)
            </a>
          </div>
        </div>
        
        <div className="flex items-center gap-12">
          <div className="flex flex-col items-end">
            <span className="text-[10px] tracking-widest uppercase text-quant-text-muted mb-1">PRICE</span>
            <span className="text-3xl font-mono tabular-nums text-quant-text-primary">${price.toFixed(2)}</span>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-[10px] tracking-widest uppercase text-quant-text-muted mb-1">DAILY</span>
            <span className={`text-2xl font-mono tabular-nums flex items-center gap-1 ${ret >= 0 ? 'text-quant-up-text' : 'text-quant-down-text'}`}>
              <Triangle className={`w-3.5 h-3.5 ${ret < 0 && 'rotate-180'} fill-current`} />
              {ret >= 0 ? '+' : ''}{(ret * 100).toFixed(2)}%
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
        
        {/* LEFT COLUMN: Main Chart & Math Grid */}
        <div className="xl:col-span-3 flex flex-col gap-6">
          
          {/* CHART */}
          <div className="matte-panel p-2 h-[450px]">
            <PriceChart symbol={symbol} />
          </div>

          {/* MATHEMATICAL STACK GRID (From ModelsClient) */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Momentum */}
            <div className="matte-panel p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-quant-text-muted border-b border-quant-border pb-2 mb-3 flex items-center gap-2"><TrendingUp className="w-3 h-3" /> Momentum Z-Scores</h3>
              {liveMath?.math_details?.momentum ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="5D Momentum" val={liveMath.math_details.momentum["5D"]} isPct tooltip="Short-term 1-week momentum." />
                  <MathRow label="21D Momentum" val={liveMath.math_details.momentum["21D"]} isPct tooltip="1-month momentum." />
                  <MathRow label="63D Momentum" val={liveMath.math_details.momentum["63D"]} isPct tooltip="1-quarter momentum." />
                  <MathRow label="126D Momentum" val={liveMath.math_details.momentum["126D"]} isPct tooltip="Half-year momentum." />
                  <MathRow label="252D Momentum" val={liveMath.math_details.momentum["252D"]} isPct tooltip="1-year momentum." />
                  <div className="border-t border-quant-border pt-2 mt-2">
                    <MathRow label="Composite Score" val={liveMath.math_details.momentum["Composite"]} isPct highlight tooltip="Average across all timeframes." />
                  </div>
                </div>
              ) : <span className="text-[10px] text-quant-text-muted uppercase">No Data</span>}
            </div>

            {/* Ornstein-Uhlenbeck */}
            <div className="matte-panel p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-quant-text-muted border-b border-quant-border pb-2 mb-3 flex items-center gap-2"><Wind className="w-3 h-3" /> Ornstein-Uhlenbeck</h3>
              {liveMath?.math_details?.mean_reversion ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="Long-Term Mean (μ)" val={liveMath.math_details.mean_reversion.long_term_mean} tooltip="Theoretical equilibrium price." />
                  <MathRow label="Current Price" val={liveMath.math_details.mean_reversion.current_price} />
                  <MathRow label="Deviation" val={liveMath.math_details.mean_reversion.deviation} isPct />
                  <MathRow label="Reversion Speed (θ)" val={liveMath.math_details.mean_reversion.theta} />
                  <MathRow label="Half-Life (Days)" val={liveMath.math_details.mean_reversion.half_life} />
                  <div className="border-t border-quant-border pt-2 mt-2 flex justify-between group relative cursor-help">
                    <span className="text-quant-text-secondary flex items-center gap-1.5">Reversion Pressure <Info className="w-3 h-3 text-quant-text-muted group-hover:text-quant-text-primary transition-colors" /></span>
                    <span className={liveMath.math_details.mean_reversion.pressure === 'HIGH' ? 'text-quant-warn-text font-bold' : 'text-quant-text-primary'}>{liveMath.math_details.mean_reversion.pressure}</span>
                  </div>
                </div>
              ) : <span className="text-[10px] text-quant-text-muted uppercase">No Data</span>}
            </div>

            {/* Fama-French */}
            <div className="matte-panel p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-quant-text-muted border-b border-quant-border pb-2 mb-3 flex items-center gap-2"><Layers className="w-3 h-3" /> Fama-French</h3>
              {liveMath?.math_details?.fama_french ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="Market (Beta)" val={liveMath.math_details.fama_french.market} />
                  <MathRow label="Size (SMB)" val={liveMath.math_details.fama_french.size} />
                  <MathRow label="Value (HML)" val={liveMath.math_details.fama_french.value} />
                  <MathRow label="Profitability (RMW)" val={liveMath.math_details.fama_french.profitability} />
                  <MathRow label="Investment (CMA)" val={liveMath.math_details.fama_french.investment} />
                  <div className="border-t border-quant-border pt-2 mt-2">
                    <MathRow label="Annualized Alpha" val={liveMath.math_details.fama_french.alpha} isPct highlight />
                  </div>
                </div>
              ) : <span className="text-[10px] text-quant-text-muted uppercase">No Data</span>}
            </div>
            
            {/* GARCH */}
            <div className="matte-panel p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-quant-text-muted border-b border-quant-border pb-2 mb-3 flex items-center gap-2"><ActivityIcon className="w-3 h-3" /> GARCH Volatility</h3>
              {liveMath?.math_details?.garch ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="1D Expected Vol" val={liveMath.math_details.garch["1D"]} isPct />
                  <MathRow label="5D Expected Vol" val={liveMath.math_details.garch["5D"]} isPct />
                  <MathRow label="21D Expected Vol" val={liveMath.math_details.garch["21D"]} isPct />
                  <div className="border-t border-quant-border pt-2 mt-2 flex justify-between group relative cursor-help">
                    <span className="text-quant-text-secondary flex items-center gap-1.5">Volatility Regime <Info className="w-3 h-3 text-quant-text-muted group-hover:text-quant-text-primary transition-colors" /></span>
                    <span className={liveMath.math_details.garch.regime === 'HIGH' ? 'text-quant-down-text font-bold' : 'text-quant-text-primary'}>{liveMath.math_details.garch.regime}</span>
                  </div>
                </div>
              ) : <span className="text-[10px] text-quant-text-muted uppercase">No Data</span>}
            </div>

            {/* HMM Regimes */}
            <div className="matte-panel p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-quant-text-muted border-b border-quant-border pb-2 mb-3 flex items-center gap-2"><BarChart2 className="w-3 h-3" /> HMM Regime</h3>
              {liveMath?.math_details?.hmm ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="Bull Regime" val={liveMath.math_details.hmm["BULL"]} isPct />
                  <MathRow label="Bear Regime" val={liveMath.math_details.hmm["BEAR"]} isPct />
                  <MathRow label="High Volatility" val={liveMath.math_details.hmm["HIGH VOL"]} isPct />
                  <MathRow label="Low Volatility" val={liveMath.math_details.hmm["LOW VOL"]} isPct />
                  <div className="border-t border-quant-border pt-2 mt-2 flex justify-between group relative cursor-help">
                    <span className="text-quant-text-secondary flex items-center gap-1.5">Current State <Info className="w-3 h-3 text-quant-text-muted group-hover:text-quant-text-primary transition-colors" /></span>
                    <span className={`font-bold ${getSignalColor(liveMath.math_details.hmm_regime)}`}>{liveMath.math_details.hmm_regime}</span>
                  </div>
                </div>
              ) : <span className="text-[10px] text-quant-text-muted uppercase">No Data</span>}
            </div>

            {/* Monte Carlo */}
            <div className="matte-panel p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-quant-text-muted border-b border-quant-border pb-2 mb-3 flex items-center gap-2"><Shield className="w-3 h-3" /> Monte Carlo</h3>
              {liveMath?.math_details?.monte_carlo ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="Prob > +10%" val={liveMath.math_details.monte_carlo.prob_gt_10} isPct />
                  <MathRow label="Prob Positive" val={liveMath.math_details.monte_carlo.prob_positive} isPct />
                  <MathRow label="Prob < -10%" val={liveMath.math_details.monte_carlo.prob_lt_m10} isPct />
                  <div className="border-t border-quant-border pt-2 mt-2">
                    <MathRow label="Median Return" val={liveMath.math_details.monte_carlo.median_ret} isPct highlight />
                  </div>
                </div>
              ) : <span className="text-[10px] text-quant-text-muted uppercase">No Data</span>}
            </div>

          </div>

        </div>

        {/* RIGHT COLUMN: Signals & Consensus */}
        <div className="xl:col-span-1 flex flex-col gap-6">
          
          {/* ASHEN RELIABILITY SCORE CARD */}
          <div className="matte-panel p-6 shrink-0 border-t-2 border-t-quant-text-primary">
            <div className="text-center border-b border-quant-border pb-4 mb-4">
              <div className="text-[10px] tracking-widest text-quant-text-muted mb-2 flex items-center justify-center gap-1">
                MODEL RELIABILITY SCORE <Info className="w-3 h-3 text-quant-text-secondary" />
              </div>
              <div className="flex justify-center items-baseline gap-2 mb-1">
                <span className="text-5xl font-light text-quant-text-primary">{liveMath?.reliability_score || 'N/A'}</span>
                <span className="text-quant-text-secondary text-sm">/ 100</span>
              </div>
              <div className={`text-xs font-bold tracking-widest uppercase ${getSignalColor(liveMath?.evidence_level)}`}>
                {liveMath?.evidence_level || 'UNAVAILABLE'}
              </div>
            </div>
            
            <div className="grid grid-cols-1 gap-y-3 text-[10px] uppercase tracking-widest">
              <div className="flex justify-between border-b border-quant-border pb-2"><span className="text-quant-text-secondary">OOS Performance</span><span className="text-quant-text-primary">{liveMath?.ars_components?.["OOS PERFORMANCE"] || 'N/A'}</span></div>
              <div className="flex justify-between border-b border-quant-border pb-2"><span className="text-quant-text-secondary">Regime Robustness</span><span className="text-quant-text-primary">{liveMath?.ars_components?.["REGIME ROBUSTNESS"] || 'N/A'}</span></div>
              <div className="flex justify-between border-b border-quant-border pb-2"><span className="text-quant-text-secondary">Calibration</span><span className="text-quant-text-primary">{liveMath?.ars_components?.["CALIBRATION"] || 'N/A'}</span></div>
              <div className="flex justify-between border-b border-quant-border pb-2"><span className="text-quant-text-secondary">Risk Adjustment</span><span className="text-quant-text-primary">{liveMath?.ars_components?.["RISK ADJUSTMENT"] || 'N/A'}</span></div>
              <div className="flex justify-between"><span className="text-quant-text-secondary">Fold Stability</span><span className="text-quant-text-primary">{liveMath?.ars_components?.["FOLD STABILITY"] || 'N/A'}</span></div>
            </div>
            
            <Link href="/validation" className="mt-6 w-full text-center block text-[10px] tracking-widest font-bold uppercase text-quant-text-primary bg-quant-elevated py-3 rounded-sm hover:bg-quant-border transition-colors">
              VIEW VALIDATION METHODOLOGY →
            </Link>
          </div>

          {/* SYSTEM SIGNAL */}
          <div className="matte-panel p-6 shrink-0">
            <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-6 border-b border-quant-border pb-4">SYSTEM SIGNAL</h2>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-[10px] uppercase tracking-widest text-quant-text-muted">Global Signal</span>
                <span className={`text-sm font-bold tracking-widest uppercase ${getSignalColor(liveMath?.global_signal)}`}>{liveMath?.global_signal || 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-[10px] uppercase tracking-widest text-quant-text-muted">Probability (UP)</span>
                <span className="text-sm font-mono text-quant-text-primary">{liveMath?.probability_up ? (liveMath.probability_up * 100).toFixed(1) + '%' : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-[10px] uppercase tracking-widest text-quant-text-muted">Expected Return</span>
                <span className="text-sm font-mono text-quant-text-primary">{liveMath?.expected_return ? (liveMath.expected_return * 100).toFixed(2) + '%' : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-[10px] uppercase tracking-widest text-quant-text-muted">Current Regime</span>
                <span className="text-[11px] font-bold tracking-widest uppercase text-quant-text-primary">{liveMath?.current_regime || 'N/A'}</span>
              </div>
            </div>
          </div>

          {/* MODEL CONSENSUS */}
          <div className="matte-panel p-6 shrink-0">
            <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-6 border-b border-quant-border pb-4">MODEL CONSENSUS</h2>
            
            <div className="flex flex-col gap-5">
              {liveMath?.consensus?.breakdown?.map((m: any, i: number) => {
                const isBull = m.signal.includes('BUY') || m.signal.includes('BULL');
                const isBear = m.signal.includes('SELL') || m.signal.includes('BEAR') || m.signal.includes('RISK') || m.signal.includes('HIGH');
                const strengthColor = isBull ? 'bg-quant-up-text' : isBear ? 'bg-quant-down-text' : 'bg-quant-warn-text';
                
                return (
                  <div key={i} className="flex flex-col gap-2">
                    <div className="flex justify-between items-center">
                      <span className="text-[11px] font-mono tracking-wider text-quant-text-primary truncate">{m.name}</span>
                      <span className={`text-[10px] font-bold tracking-widest uppercase ${getSignalColor(m.signal)}`}>
                        {m.signal}
                      </span>
                    </div>
                    <div className="w-full bg-black h-1 rounded-full overflow-hidden border border-quant-border">
                      <div className={`h-full ${strengthColor}`} style={{ width: `${Math.min(100, Math.max(0, m.strength * 100))}%` }} />
                    </div>
                  </div>
                );
              })}
              
              {!liveMath?.consensus?.breakdown && (
                <div className="text-xs text-quant-text-muted italic">No consensus models available.</div>
              )}
            </div>
            
            <Link href="/research/consensus" className="mt-6 w-full text-center block text-[10px] tracking-widest uppercase text-quant-text-muted hover:text-quant-text-primary transition-colors">
              VIEW DETAILED CONSENSUS →
            </Link>
          </div>

        </div>
      </div>
    </div>
  );
}

function MathRow({ label, val, isPct = false, highlight = false, tooltip }: { label: string, val: number, isPct?: boolean, highlight?: boolean, tooltip?: string }) {
  const isPos = val > 0;
  const isNeg = val < 0;
  let color = 'text-quant-text-primary';
  if (highlight) {
    if (isPos) color = 'text-quant-up-text font-bold';
    else if (isNeg) color = 'text-quant-down-text font-bold';
    else color = 'text-quant-text-primary font-bold';
  }
  
  let disp = '';
  if (isPct) {
    disp = (val * 100).toFixed(2) + '%';
  } else {
    disp = val.toFixed(3);
  }

  return (
    <div className="flex justify-between items-center group relative cursor-help">
      <span className="text-quant-text-secondary flex items-center gap-1.5">
        {label}
      </span>
      <span className={`font-mono tabular-nums ${color}`}>{val > 0 && highlight ? '+' : ''}{disp}</span>
      
      {tooltip && (
        <div className="pointer-events-none absolute bottom-full left-0 mb-1 w-48 opacity-0 group-hover:opacity-100 transition-opacity z-50">
          <div className="bg-quant-elevated text-quant-text-primary text-[10px] p-2 rounded-sm border border-quant-border shadow-lg leading-relaxed">
            {tooltip}
          </div>
        </div>
      )}
    </div>
  );
}
