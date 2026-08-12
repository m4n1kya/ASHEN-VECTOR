"use client";

import { useState } from "react";
import { Activity, Play, AlertTriangle, HeartPulse, Info, BarChart2, Shield, TrendingUp, Layers, Wind, Activity as ActivityIcon, Loader2 } from "lucide-react";
import Link from "next/link";

export default function ModelsClient() {
  const [symbol, setSymbol] = useState("TSLA");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  const handleRun = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/live/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol, models: ["ALL"], horizons: [21] })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to fetch live data");
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSignalColor = (signal: string) => {
    if (!signal) return "text-gray-300";
    const s = signal.toUpperCase();
    if (s.includes("BUY") || s.includes("BULL") || s.includes("STRONG") || s.includes("HIGH EVID")) return "text-[#10B981]";
    if (s.includes("SELL") || s.includes("BEAR") || s.includes("WEAK") || s.includes("RISK")) return "text-[#EF4444]";
    return "text-[#F59E0B]"; // HOLD/MODERATE
  };

  return (
    <div className="flex-1 flex flex-col min-h-0 gap-6 bg-black text-gray-300 font-sans h-full">
      <form onSubmit={handleRun} className="bg-[#0A0A0A] matte-panel p-4 shrink-0 rounded-sm border border-gray-800">
        <div className="flex items-end gap-4">
          <div className="flex-1">
            <label className="block text-[10px] tracking-widest uppercase text-gray-500 mb-1.5">Target Symbol</label>
            <input 
              type="text" 
              value={symbol} 
              onChange={e => setSymbol(e.target.value.toUpperCase())}
              className="w-full bg-black border border-gray-800 rounded-sm p-2 text-sm font-mono tabular-nums text-gray-200 focus:outline-none focus:border-gray-500 transition-colors uppercase"
              placeholder="e.g. TSLA"
              required
            />
          </div>
          <button 
            type="submit" 
            disabled={loading}
            className="bg-gray-800 text-gray-200 text-xs tracking-widest font-bold rounded-sm px-6 py-2 border border-transparent hover:border-gray-500 transition-colors disabled:opacity-50 flex items-center justify-center gap-2 h-[38px]"
          >
            {loading ? (
              <><Loader2 className="w-3.5 h-3.5 animate-spin text-gray-400" /> ANALYZING...</>
            ) : (
              <><Play className="w-3.5 h-3.5" /> INFER</>
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-[#1A0505] border border-[#FF0000]/30 text-[#FF0000] p-4 rounded-sm flex items-center gap-3 text-xs font-mono">
          <AlertTriangle className="w-4 h-4" />
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="flex-1 overflow-y-auto font-mono text-sm space-y-6 pb-6">
          {/* Header Block with ARS Score */}
          <div className="flex flex-col lg:flex-row justify-between gap-6">
            <div className="flex flex-col">
              <h1 className="text-4xl font-bold tracking-tight text-white mb-1">{result.symbol}</h1>
              <div className="flex items-baseline gap-4">
                <span className="text-gray-400">{result.name}</span>
                <span className="text-white text-lg">${result.latest_price?.toFixed(2)}</span>
              </div>
              
              {/* Context Navbar */}
              <div className="mt-4 flex gap-4 border border-gray-800 bg-[#0A0A0A] p-2 rounded-sm shadow-inner">
                <Link href="/validation" className="text-[10px] tracking-widest uppercase font-bold text-gray-400 hover:text-white hover:bg-[#1A1A1A] border border-transparent hover:border-gray-800 px-4 py-2 rounded-sm transition-all flex items-center gap-2">
                  <ActivityIcon className="w-3.5 h-3.5" /> Detailed Model Analysis
                </Link>
                <a href={`https://www.bloomberg.com/search?query=${result.name || result.symbol}`} target="_blank" rel="noopener noreferrer" className="text-[10px] tracking-widest uppercase font-bold text-gray-400 hover:text-white hover:bg-[#1A1A1A] border border-transparent hover:border-gray-800 px-4 py-2 rounded-sm transition-all flex items-center gap-2">
                  <Play className="w-3.5 h-3.5" /> News (Bloomberg)
                </a>
              </div>
            </div>

            {/* ASHEN RELIABILITY SCORE CARD */}
            <div className="bg-[#0A0A0A] matte-panel border border-gray-800 p-4 rounded-sm lg:w-[400px] shrink-0">
              <div className="text-center border-b border-gray-800 pb-3 mb-3">
                <div className="text-[10px] tracking-widest text-gray-500 mb-1 flex items-center justify-center gap-1" title="Calculated from out-of-sample edge, regime coverage, stability, and Sharpe.">
                  ASHEN RELIABILITY <Info className="w-3 h-3 text-gray-600" />
                </div>
                <div className="flex justify-center items-baseline gap-2">
                  <span className="text-4xl font-bold text-white">{result.reliability_score}</span>
                  <span className="text-gray-500">/ 100</span>
                </div>
                <div className={`text-xs font-bold tracking-widest mt-1 ${getSignalColor(result.evidence_level)}`}>
                  {result.evidence_level}
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-[10px] uppercase tracking-widest">
                <div className="flex justify-between text-gray-400"><span>OOS Perf</span><span className="text-white">{result.ars_components["OOS PERFORMANCE"]}</span></div>
                <div className="flex justify-between text-gray-400"><span>Regime</span><span className="text-white">{result.ars_components["REGIME ROBUSTNESS"]}</span></div>
                <div className="flex justify-between text-gray-400"><span>Calibr</span><span className="text-white">{result.ars_components["CALIBRATION"]}</span></div>
                <div className="flex justify-between text-gray-400"><span>Risk Adj</span><span className="text-white">{result.ars_components["RISK ADJUSTMENT"]}</span></div>
                <div className="flex justify-between text-gray-400"><span>Fold Stab</span><span className="text-white">{result.ars_components["FOLD STABILITY"]}</span></div>
                <div className="flex justify-between text-gray-400"><span>Recency</span><span className="text-white">{result.ars_components["RECENCY"]}</span></div>
              </div>
              <div className="mt-3 flex justify-between border-t border-gray-800 pt-2 text-[10px] tracking-widest">
                <span className="text-gray-500">PREDICTION PROB</span>
                <span className="text-white font-bold">{(result.probability_up * 100).toFixed(1)}%</span>
              </div>
            </div>
          </div>

          {/* MATHEMATICAL STACK GRID */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            
            {/* Momentum */}
            <div className="bg-[#0A0A0A] border border-gray-800 rounded-sm p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-gray-500 border-b border-gray-800 pb-2 mb-3 flex items-center gap-2"><TrendingUp className="w-3 h-3" /> Momentum Z-Scores</h3>
              {result.math_details?.momentum ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="5D Momentum" val={result.math_details.momentum["5D"]} isPct tooltip="Short-term 1-week momentum. >0 is positive." />
                  <MathRow label="21D Momentum" val={result.math_details.momentum["21D"]} isPct tooltip="1-month momentum. >0 indicates upward trend." />
                  <MathRow label="63D Momentum" val={result.math_details.momentum["63D"]} isPct tooltip="1-quarter momentum. Institutional focus." />
                  <MathRow label="126D Momentum" val={result.math_details.momentum["126D"]} isPct tooltip="Half-year momentum." />
                  <MathRow label="252D Momentum" val={result.math_details.momentum["252D"]} isPct tooltip="1-year momentum. >0 means positive 1Y return." />
                  <div className="border-t border-gray-800 pt-2 mt-2">
                    <MathRow label="Composite Score" val={result.math_details.momentum["Composite"]} isPct highlight tooltip="Average across all timeframes. High positive means strong systemic momentum." />
                  </div>
                </div>
              ) : <span className="text-xs text-gray-600">No Momentum data</span>}
            </div>

            {/* Ornstein-Uhlenbeck (Mean Reversion) */}
            <div className="bg-[#0A0A0A] border border-gray-800 rounded-sm p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-gray-500 border-b border-gray-800 pb-2 mb-3 flex items-center gap-2"><Wind className="w-3 h-3" /> Ornstein-Uhlenbeck</h3>
              {result.math_details?.mean_reversion ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="Long-Term Mean (μ)" val={result.math_details.mean_reversion.long_term_mean} tooltip="The theoretical equilibrium price it reverts to." />
                  <MathRow label="Current Price" val={result.math_details.mean_reversion.current_price} tooltip="Latest close price." />
                  <MathRow label="Deviation" val={result.math_details.mean_reversion.deviation} isPct tooltip="How far off the mean it is. High positive means overvalued." />
                  <MathRow label="Reversion Speed (θ)" val={result.math_details.mean_reversion.theta} tooltip="Higher means it snaps back faster. <0 means non-reverting." />
                  <MathRow label="Half-Life (Days)" val={result.math_details.mean_reversion.half_life} tooltip="Days it takes to revert half the distance to the mean. Lower is faster mean-reversion." />
                  <div className="border-t border-gray-800 pt-2 mt-2 flex justify-between group relative cursor-help">
                    <span className="text-gray-400 flex items-center gap-1.5">Reversion Pressure <Info className="w-3 h-3 text-gray-600 group-hover:text-gray-300 transition-colors" /></span>
                    <span className={result.math_details.mean_reversion.pressure === 'HIGH' ? 'text-[#F59E0B] font-bold' : 'text-gray-300'}>{result.math_details.mean_reversion.pressure}</span>
                    <div className="pointer-events-none absolute bottom-full left-0 mb-1 w-48 opacity-0 group-hover:opacity-100 transition-opacity z-50">
                      <div className="bg-[#1A1A1A] text-gray-300 text-[10px] p-2 rounded-sm border border-gray-800 shadow-lg leading-relaxed">
                        HIGH means extreme deviation. A snap-back is mathematically likely.
                      </div>
                    </div>
                  </div>
                </div>
              ) : <span className="text-xs text-gray-600">No OU data (Needs 252D)</span>}
            </div>

            {/* Fama-French Factor Fingerprint */}
            <div className="bg-[#0A0A0A] border border-gray-800 rounded-sm p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-gray-500 border-b border-gray-800 pb-2 mb-3 flex items-center gap-2"><Layers className="w-3 h-3" /> Fama-French Factors</h3>
              {result.math_details?.fama_french ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="Market (Beta)" val={result.math_details.fama_french.market} tooltip="CAPM Beta. 1.0 means it moves exactly with the market. >1 is volatile." />
                  <MathRow label="Size (SMB)" val={result.math_details.fama_french.size} tooltip="Small Minus Big. >0 means it behaves like a small-cap stock." />
                  <MathRow label="Value (HML)" val={result.math_details.fama_french.value} tooltip="High Minus Low. >0 means it behaves like a value stock." />
                  <MathRow label="Profitability (RMW)" val={result.math_details.fama_french.profitability} tooltip="Robust Minus Weak. >0 means it has strong operating profitability." />
                  <MathRow label="Investment (CMA)" val={result.math_details.fama_french.investment} tooltip="Conservative Minus Aggressive. >0 means it invests conservatively." />
                  <div className="border-t border-gray-800 pt-2 mt-2">
                    <MathRow label="Annualized Alpha" val={result.math_details.fama_french.alpha} isPct highlight tooltip="Excess return unexplained by the 5 factors. >0 is purely idiosyncratic outperformance." />
                  </div>
                </div>
              ) : <span className="text-xs text-gray-600">No Factor data available</span>}
            </div>

            {/* GARCH Volatility */}
            <div className="bg-[#0A0A0A] border border-gray-800 rounded-sm p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-gray-500 border-b border-gray-800 pb-2 mb-3 flex items-center gap-2"><ActivityIcon className="w-3 h-3" /> GARCH Volatility</h3>
              {result.math_details?.garch ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="1D Expected Vol" val={result.math_details.garch["1D"]} isPct tooltip="Predicted volatility tomorrow." />
                  <MathRow label="5D Expected Vol" val={result.math_details.garch["5D"]} isPct tooltip="Predicted volatility over the next week." />
                  <MathRow label="21D Expected Vol" val={result.math_details.garch["21D"]} isPct tooltip="Predicted volatility over the next month." />
                  <div className="border-t border-gray-800 pt-2 mt-2 flex justify-between group relative cursor-help">
                    <span className="text-gray-400 flex items-center gap-1.5">Volatility Regime <Info className="w-3 h-3 text-gray-600 group-hover:text-gray-300 transition-colors" /></span>
                    <span className={result.math_details.garch.regime === 'HIGH' ? 'text-[#EF4444] font-bold' : 'text-gray-300'}>{result.math_details.garch.regime}</span>
                    <div className="pointer-events-none absolute bottom-full left-0 mb-1 w-48 opacity-0 group-hover:opacity-100 transition-opacity z-50">
                      <div className="bg-[#1A1A1A] text-gray-300 text-[10px] p-2 rounded-sm border border-gray-800 shadow-lg leading-relaxed">
                        HIGH means GARCH predicts &gt;8% volatility over the next 21 days (unsafe).
                      </div>
                    </div>
                  </div>
                </div>
              ) : <span className="text-xs text-gray-600">No GARCH data</span>}
            </div>

            {/* HMM Regimes */}
            <div className="bg-[#0A0A0A] border border-gray-800 rounded-sm p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-gray-500 border-b border-gray-800 pb-2 mb-3 flex items-center gap-2"><BarChart2 className="w-3 h-3" /> HMM Regime Probabilities</h3>
              {result.math_details?.hmm ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="Bull Regime" val={result.math_details.hmm["BULL"]} isPct tooltip="Probability the market stays in a strong uptrend." />
                  <MathRow label="Bear Regime" val={result.math_details.hmm["BEAR"]} isPct tooltip="Probability the market stays in a downtrend." />
                  <MathRow label="High Volatility" val={result.math_details.hmm["HIGH VOL"]} isPct tooltip="Probability of entering choppy, high-risk sideways action." />
                  <MathRow label="Low Volatility" val={result.math_details.hmm["LOW VOL"]} isPct tooltip="Probability of entering calm, flat action." />
                  <div className="border-t border-gray-800 pt-2 mt-2 flex justify-between group relative cursor-help">
                    <span className="text-gray-400 flex items-center gap-1.5">Current State <Info className="w-3 h-3 text-gray-600 group-hover:text-gray-300 transition-colors" /></span>
                    <span className={`font-bold ${getSignalColor(result.math_details.hmm_regime)}`}>{result.math_details.hmm_regime}</span>
                    <div className="pointer-events-none absolute bottom-full left-0 mb-1 w-48 opacity-0 group-hover:opacity-100 transition-opacity z-50">
                      <div className="bg-[#1A1A1A] text-gray-300 text-[10px] p-2 rounded-sm border border-gray-800 shadow-lg leading-relaxed">
                        The dominant hidden state right now according to the Markov model.
                      </div>
                    </div>
                  </div>
                </div>
              ) : <span className="text-xs text-gray-600">No HMM data</span>}
            </div>

            {/* Monte Carlo */}
            <div className="bg-[#0A0A0A] border border-gray-800 rounded-sm p-4">
              <h3 className="text-[10px] tracking-widest uppercase text-gray-500 border-b border-gray-800 pb-2 mb-3 flex items-center gap-2"><Shield className="w-3 h-3" /> Monte Carlo (10,000 Paths)</h3>
              {result.math_details?.monte_carlo ? (
                <div className="space-y-2 text-xs">
                  <MathRow label="Prob > +10%" val={result.math_details.monte_carlo.prob_gt_10} isPct tooltip="Probability of extreme upside." />
                  <MathRow label="Prob Positive" val={result.math_details.monte_carlo.prob_positive} isPct tooltip="Probability you make money. >55% is good." />
                  <MathRow label="Prob < -10%" val={result.math_details.monte_carlo.prob_lt_m10} isPct tooltip="Probability of extreme downside (Tail risk)." />
                  <div className="border-t border-gray-800 pt-2 mt-2">
                    <MathRow label="Median Simulated Return" val={result.math_details.monte_carlo.median_ret} isPct highlight tooltip="The exact middle outcome out of 10,000 parallel universe simulations." />
                  </div>
                </div>
              ) : <span className="text-xs text-gray-600">No Monte Carlo data</span>}
            </div>

          </div>

          {/* Model Consensus Bars */}
          <div className="bg-[#0A0A0A] matte-panel border border-gray-800 p-4 rounded-sm">
            <div className="flex justify-between items-center border-b border-gray-800 pb-2 mb-4">
              <h2 className="text-[10px] font-bold tracking-widest text-gray-500">ENSEMBLE ENGINE CONSENSUS</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
              {result.consensus.breakdown.map((m: any, i: number) => {
                const strengthColor = (m.signal.includes('BUY') || m.signal.includes('BULL')) ? 'bg-[#10B981]' : ((m.signal.includes('SELL') || m.signal.includes('BEAR') || m.signal.includes('RISK') || m.signal.includes('HIGH')) ? 'bg-[#EF4444]' : 'bg-[#F59E0B]');
                return (
                  <div key={i} className="flex flex-col gap-1.5">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-300 w-1/3 truncate">{m.name}</span>
                      <span className={`text-[10px] font-bold tracking-widest w-1/4 text-right ${getSignalColor(m.signal)}`}>
                        {m.signal}
                      </span>
                    </div>
                    <div className="w-full bg-black h-1.5 rounded-full overflow-hidden border border-gray-800">
                      <div 
                        className={`h-full ${strengthColor}`} 
                        style={{ width: `${Math.min(100, Math.max(0, m.strength * 100))}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="text-[9px] text-gray-600 tracking-wider text-center border-t border-gray-800 pt-4 pb-4">
            ⚠ RELIABILITY IS NOT A GUARANTEE OF FUTURE PERFORMANCE. THIS IS AN INTERNALLY COMPUTED EVIDENCE SCORE BASED ON HISTORICAL OUT-OF-SAMPLE TESTING.
          </div>
        </div>
      )}
    </div>
  );
}

function MathRow({ label, val, isPct = false, highlight = false, tooltip }: { label: string, val: number, isPct?: boolean, highlight?: boolean, tooltip?: string }) {
  const isPos = val > 0;
  const isNeg = val < 0;
  let color = 'text-gray-300';
  if (highlight) {
    if (isPos) color = 'text-[#10B981] font-bold';
    else if (isNeg) color = 'text-[#EF4444] font-bold';
    else color = 'text-white font-bold';
  }
  
  let disp = '';
  if (isPct) {
    disp = (val * 100).toFixed(2) + '%';
  } else {
    disp = val.toFixed(3);
  }

  return (
    <div className="flex justify-between items-center group relative cursor-help">
      <span className="text-gray-400 flex items-center gap-1.5">
        {label}
        {tooltip && <Info className="w-3 h-3 text-gray-600 group-hover:text-gray-300 transition-colors" />}
      </span>
      <span className={`font-mono tabular-nums ${color}`}>{val > 0 && highlight ? '+' : ''}{disp}</span>
      
      {tooltip && (
        <div className="pointer-events-none absolute bottom-full left-0 mb-1 w-48 opacity-0 group-hover:opacity-100 transition-opacity z-50">
          <div className="bg-[#1A1A1A] text-gray-300 text-[10px] p-2 rounded-sm border border-gray-800 shadow-lg leading-relaxed">
            {tooltip}
          </div>
        </div>
      )}
    </div>
  );
}
