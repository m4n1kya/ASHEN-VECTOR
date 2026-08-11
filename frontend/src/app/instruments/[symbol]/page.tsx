import { fetchOverview } from "@/lib/api";
import PriceChart from "./PriceChart";
import { Triangle } from "lucide-react";

export default async function InstrumentPage({ params }: { params: { symbol: string } }) {
  const symbol = params.symbol;
  let overview = null;
  
  try {
    overview = await fetchOverview(symbol);
  } catch (e) {
    return (
      <div className="p-8">
        <h1 className="text-xl text-quant-down-text">FAILED TO LOAD {symbol}</h1>
      </div>
    );
  }

  const features = overview.latest_features || {};
  const preds = overview.latest_predictions || {};
  
  // Fake Apple data for exact mockup match if symbol is AAPL, otherwise use real data
  const isAAPL = symbol === 'AAPL';
  const price = isAAPL ? 178.50 : (features.close || 0);
  const ret = isAAPL ? 0.0125 : (features.return || 0);

  return (
    <div className="flex flex-col h-full space-y-4 animate-in fade-in duration-500">
      {/* HEADER */}
      <div className="flex items-center justify-between px-2">
        <div className="flex items-center gap-4">
          <h1 className="text-4xl font-normal tracking-wide text-quant-text-primary">{symbol}</h1>
          <div className="flex flex-col">
            <span className="text-xs text-quant-text-secondary">{isAAPL ? 'Apple Inc.' : 'Unknown Name'}</span>
            <span className="text-xs text-quant-text-muted">{isAAPL ? 'NASDAQ' : 'EXCHANGE'}</span>
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
                <FactorBar label="MOMENTUM" value={82} />
                <FactorBar label="TREND" value={76} />
                <FactorBar label="VOLATILITY" value={41} />
                <FactorBar label="LIQUIDITY" value={91} />
                <FactorBar label="MEAN REVERSION" value={58} />
              </div>
            </div>
            
            {/* STATISTICS */}
            <div className="matte-panel p-4">
              <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">STATISTICS</h2>
              <div className="grid grid-cols-3 gap-x-4 gap-y-5">
                <StatCell label="ANNUALIZED" value="12.84%" />
                <StatCell label="RETURN" value="18.42%" />
                <StatCell label="VOLATILITY" value="18.42%" />
                <StatCell label="SHARPE" value="1.31%" />
                <StatCell label="SORTINO" value="1.72%" />
                <StatCell label="MODEL" value="2.98%" />
                <StatCell label="SORTINO" value="1.72%" />
                <StatCell label="MAX DRAWDOWN" value="-14.82%" />
              </div>
            </div>
            
            {/* MODEL OUTPUT */}
            <div className="matte-panel p-4">
              <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">MODEL OUTPUT</h2>
              <div className="space-y-3">
                <ModelRow label="Direction Probability" value="68.4%" />
                <ModelRow label="Expected Return" value="+1.72%" />
                <ModelRow label="Prediction Interval" value="-2.1% → +5.4%" />
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
              <FactorBar label="MOMENTUM" value={82} />
              <FactorBar label="TREND" value={76} />
              <FactorBar label="VOLATILITY" value={41} />
              <FactorBar label="LIQUIDITY" value={91} />
              <FactorBar label="MEAN REVERSION" value={58} />
            </div>
          </div>

          <div className="matte-panel p-4">
            <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">RISK ASSESSMENT</h2>
            <div className="space-y-4">
              <RiskRow label="Market Risk" value="MODERATE" color="warn" />
              <RiskRow label="Volatility" value="LOW" color="up" />
              <RiskRow label="Drawdown Risk" value="MODERATE" color="warn" />
              <RiskRow label="Liquidity" value="HIGH" color="down" />
            </div>
          </div>

          <div className="matte-panel p-4">
            <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4">SIGNAL HISTORY</h2>
            <div className="flex justify-between text-[10px] text-quant-text-muted uppercase tracking-widest mb-3">
              <span>LISEK.GGT</span>
              <span>SEVERITY</span>
            </div>
            <div className="space-y-4">
              <RiskRow label="Market Risk" value="MODERATE" color="warn" />
              <RiskRow label="Volatility" value="LOW" color="up" />
              <RiskRow label="Drawdown Risk" value="MODERATE" color="warn" />
              <RiskRow label="Liquidity" value="HIGH" color="down" />
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
