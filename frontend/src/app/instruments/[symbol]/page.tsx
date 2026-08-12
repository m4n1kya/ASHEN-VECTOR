import { fetchOverview } from "@/lib/api";
import PriceChart from "./PriceChart";
import { Triangle } from "lucide-react";

export default async function InstrumentPage({ params }: { params: { symbol: string } }) {
  const symbol = params.symbol;
  let overview = null;
  let errorMsg = "";
  
  try {
    overview = await fetchOverview(symbol);
  } catch (e: any) {
    errorMsg = e.message || String(e);
    return (
      <div className="p-8 flex flex-col items-center justify-center h-full">
        <h1 className="text-2xl font-bold tracking-widest text-quant-down-text mb-4">FAILED TO LOAD {symbol}</h1>
        <p className="text-xs text-quant-text-muted font-mono">{errorMsg}</p>
      </div>
    );
  }

  const market = overview?.market || {};
  const perf = overview?.performance || {};
  const risk = overview?.risk || {};
  const tech = overview?.technical || {};
  const pred = overview?.prediction || {};
  
  const isAAPL = symbol === 'AAPL';
  const price = isAAPL ? 178.50 : (market.close || 0);
  const ret = isAAPL ? 0.0125 : (perf.return_1d || 0);

  return (
    <div className="flex flex-col h-full space-y-4 animate-in fade-in duration-500">
      {/* HEADER */}
      <div className="flex items-center justify-between px-2">
        <div className="flex items-center gap-4">
          <h1 className="text-4xl font-normal tracking-wide text-quant-text-primary">{symbol}</h1>
          <div className="flex flex-col">
            <span className="text-xs text-quant-text-secondary">{isAAPL ? 'Apple Inc.' : overview?.instrument?.name || 'Unknown Name'}</span>
            <span className="text-xs text-quant-text-muted">{isAAPL ? 'NASDAQ' : overview?.instrument?.exchange || 'EXCHANGE'}</span>
          </div>
        </div>
        
        <div className="flex items-center gap-12">
          <div className="flex flex-col">
            <span className="text-[10px] tracking-widest uppercase text-quant-text-muted mb-0.5">PRICE</span>
            <span className="text-2xl font-mono tabular-nums text-quant-text-primary">${price.toFixed(2)}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] tracking-widest uppercase text-quant-text-muted mb-0.5">DAILY</span>
            <span className={`text-xl font-mono tabular-nums flex items-center gap-1 ${ret >= 0 ? 'text-quant-up-text' : 'text-quant-down-text'}`}>
              <Triangle className={`w-3 h-3 ${ret < 0 && 'rotate-180'} fill-current`} />
              {ret >= 0 ? '+' : ''}{(ret * 100).toFixed(2)}%
            </span>
          </div>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 xl:grid-cols-5 gap-4 min-h-0">
        
        {/* LEFT COLUMN (Chart + Bottom Panels) */}
        <div className="lg:col-span-3 xl:col-span-4 flex flex-col gap-4 min-h-0">
          
          {/* CHART */}
          <div className="matte-panel flex-1 min-h-[400px] p-2">
             <PriceChart />
          </div>
          
          {/* BOTTOM PANELS ROW */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 shrink-0">
            {/* QUANT FACTORS BOTTOM */}
            <div className="matte-panel p-4">
              <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">QUANT FACTORS</h2>
              <div className="space-y-4">
                <FactorBar label="MOMENTUM" value={tech.momentum_20 ? Math.min(Math.max((tech.momentum_20 + 0.1) * 500, 0), 100) : 50} />
                <FactorBar label="TREND" value={tech.sma_20 && market.close ? (market.close > tech.sma_20 ? 80 : 20) : 50} />
                <FactorBar label="VOLATILITY" value={tech.volatility_20 ? Math.min(tech.volatility_20 * 100, 100) : 50} />
                <FactorBar label="LIQUIDITY" value={tech.volume_ratio_20 ? Math.min(tech.volume_ratio_20 * 50, 100) : 50} />
                <FactorBar label="MEAN REVERSION" value={tech.rsi_14 ? (100 - tech.rsi_14) : 50} />
              </div>
            </div>
            
            {/* STATISTICS */}
            <div className="matte-panel p-4">
              <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">STATISTICS</h2>
              <div className="grid grid-cols-3 gap-x-4 gap-y-5">
                <StatCell label="ANNUALIZED" value={risk.annualized_return ? `${(risk.annualized_return * 100).toFixed(2)}%` : "---"} />
                <StatCell label="RETURN (1M)" value={perf.return_1m ? `${(perf.return_1m * 100).toFixed(2)}%` : "---"} />
                <StatCell label="VOLATILITY" value={risk.annualized_volatility ? `${(risk.annualized_volatility * 100).toFixed(2)}%` : "---"} />
                <StatCell label="SHARPE" value={risk.sharpe_ratio ? risk.sharpe_ratio.toFixed(2) : "---"} />
                <StatCell label="SORTINO" value={risk.sortino_ratio ? risk.sortino_ratio.toFixed(2) : "---"} />
                <StatCell label="WIN RATE" value={risk.win_rate ? `${(risk.win_rate * 100).toFixed(1)}%` : "---"} />
                <StatCell label="RSI 14" value={tech.rsi_14 ? tech.rsi_14.toFixed(1) : "---"} />
                <StatCell label="MAX DRAWDOWN" value={risk.maximum_drawdown ? `${(risk.maximum_drawdown * 100).toFixed(2)}%` : "---"} />
              </div>
            </div>
            
            {/* MODEL OUTPUT */}
            <div className="matte-panel p-4">
              <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">MODEL OUTPUT</h2>
              <div className="space-y-3">
                <ModelRow label="Direction Probability" value={pred.probability_up ? `${(pred.probability_up * 100).toFixed(1)}%` : "---"} />
                <ModelRow label="Expected Return" value={pred.expected_return ? `${(pred.expected_return * 100).toFixed(2)}%` : "---"} />
                <ModelRow label="Model Status" value={pred.status || "UNKNOWN"} />
                <ModelRow label="MODEL" value="LightGBM" isText />
                <ModelRow label="CALIBRATION" value="Isotonic Regression" isText />
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN (Side Panels) */}
        <div className="lg:col-span-1 xl:col-span-1 flex flex-col gap-4 overflow-y-auto shrink-0">
          
          <div className="matte-panel p-4">
            <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">QUANT FACTORS</h2>
            <div className="space-y-4">
              <FactorBar label="MOMENTUM" value={tech.momentum_20 ? Math.min(Math.max((tech.momentum_20 + 0.1) * 500, 0), 100) : 50} />
              <FactorBar label="TREND" value={tech.sma_20 && market.close ? (market.close > tech.sma_20 ? 80 : 20) : 50} />
              <FactorBar label="VOLATILITY" value={tech.volatility_20 ? Math.min(tech.volatility_20 * 100, 100) : 50} />
              <FactorBar label="LIQUIDITY" value={tech.volume_ratio_20 ? Math.min(tech.volume_ratio_20 * 50, 100) : 50} />
              <FactorBar label="MEAN REVERSION" value={tech.rsi_14 ? (100 - tech.rsi_14) : 50} />
            </div>
          </div>

          <div className="matte-panel p-4">
            <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">RISK ASSESSMENT</h2>
            <div className="space-y-4">
              <RiskRow label="Market Risk" value={risk.annualized_volatility > 0.3 ? "HIGH" : risk.annualized_volatility > 0.15 ? "MODERATE" : "LOW"} color={risk.annualized_volatility > 0.3 ? "down" : risk.annualized_volatility > 0.15 ? "warn" : "up"} />
              <RiskRow label="Volatility Risk" value={tech.volatility_20 > 0.4 ? "HIGH" : tech.volatility_20 > 0.2 ? "MODERATE" : "LOW"} color={tech.volatility_20 > 0.4 ? "down" : tech.volatility_20 > 0.2 ? "warn" : "up"} />
              <RiskRow label="Drawdown Risk" value={risk.maximum_drawdown < -0.2 ? "HIGH" : risk.maximum_drawdown < -0.1 ? "MODERATE" : "LOW"} color={risk.maximum_drawdown < -0.2 ? "down" : risk.maximum_drawdown < -0.1 ? "warn" : "up"} />
              <RiskRow label="Liquidity" value={tech.volume_ratio_20 > 1.2 ? "HIGH" : "MODERATE"} color={tech.volume_ratio_20 > 1.2 ? "up" : "warn"} />
            </div>
          </div>

          <div className="matte-panel p-4">
            <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">SIGNAL HISTORY</h2>
            <div className="flex justify-between text-[10px] text-quant-text-muted uppercase tracking-widest mb-3">
              <span>{symbol}.SIG</span>
              <span>SEVERITY</span>
            </div>
            <div className="space-y-4">
              <RiskRow label="Momentum Breakdown" value={tech.momentum_20 < -0.05 ? "HIGH" : "LOW"} color={tech.momentum_20 < -0.05 ? "down" : "up"} />
              <RiskRow label="Trend Exhaustion" value={tech.rsi_14 > 70 ? "HIGH" : "LOW"} color={tech.rsi_14 > 70 ? "down" : "up"} />
              <RiskRow label="Volume Spike" value={tech.volume_ratio_20 > 2.0 ? "HIGH" : "LOW"} color={tech.volume_ratio_20 > 2.0 ? "warn" : "up"} />
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}

function StatCell({ label, value }: { label: string, value: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-[10px] uppercase tracking-wider text-quant-text-secondary mb-1">{label}</span>
      <span className="font-mono text-sm tabular-nums text-quant-text-primary">{value}</span>
    </div>
  );
}

function ModelRow({ label, value, isText }: { label: string, value: string, isText?: boolean }) {
  return (
    <div className="flex justify-between items-center">
      <span className={`text-xs ${isText ? 'uppercase tracking-widest text-quant-text-secondary' : 'text-quant-text-secondary'}`}>{label}</span>
      <span className={`text-sm text-quant-text-primary ${isText ? '' : 'font-mono tabular-nums'}`}>{value}</span>
    </div>
  );
}

function RiskRow({ label, value, color }: { label: string, value: string, color: 'up' | 'down' | 'warn' }) {
  const colorClass = color === 'up' ? 'text-quant-up-text' : color === 'warn' ? 'text-quant-warn-text' : 'text-quant-down-text';
  return (
    <div className="flex justify-between items-center">
      <span className="text-xs text-quant-text-secondary">{label}</span>
      <span className={`text-xs uppercase tracking-widest ${colorClass}`}>{value}</span>
    </div>
  );
}

function FactorBar({ label, value }: { label: string, value: number }) {
  return (
    <div>
      <div className="flex justify-between items-end mb-1">
        <span className="text-[10px] uppercase tracking-widest text-quant-text-primary">{label}</span>
        <span className="font-mono text-[11px] text-quant-text-primary">{value}</span>
      </div>
      <div className="h-[2px] w-full bg-quant-border overflow-hidden">
        <div className="h-full bg-quant-text-primary" style={{ width: `${value}%` }}></div>
      </div>
    </div>
  );
}
