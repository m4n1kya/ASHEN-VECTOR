import { fetchInstruments, fetchOverview } from "@/lib/api";
import Link from "next/link";
import { ArrowRight, AlertTriangle, CheckCircle2 } from "lucide-react";

export default async function Home() {
  let instruments = [];
  try {
    const data = await fetchInstruments();
    instruments = data.instruments || [];
  } catch (e) {
    console.error("Failed to fetch instruments", e);
  }

  return (
    <div className="space-y-6">
      <header className="pb-4 border-b border-quant-border">
        <h1 className="text-xl font-medium tracking-wide text-quant-text-primary">SYSTEM OVERVIEW</h1>
        <p className="text-xs text-quant-text-secondary mt-1">Instrument discovery and market state</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {instruments.map((symbol: string) => (
          <InstrumentCard key={symbol} symbol={symbol} />
        ))}
      </div>
    </div>
  );
}

async function InstrumentCard({ symbol }: { symbol: string }) {
  let overview = null;
  try {
    overview = await fetchOverview(symbol);
  } catch (e) {
    return (
      <div className="matte-panel p-4 flex flex-col justify-between opacity-50">
        <h2 className="text-sm font-bold text-quant-text-primary tracking-widest">{symbol}</h2>
        <p className="text-quant-down-text text-xs mt-2 flex items-center gap-1">
          <AlertTriangle className="w-3 h-3" /> API ERROR
        </p>
      </div>
    );
  }

  const isFresh = overview.data_quality?.data_status === "FRESH";
  const modelStatus = overview.model_status || "NOT_AVAILABLE";
  const hasModel = modelStatus === "READY";

  return (
    <Link href={`/instruments/${symbol}`} className="matte-panel p-4 flex flex-col justify-between hover:bg-quant-elevated transition-colors group">
      <div>
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-sm font-bold text-quant-text-primary tracking-widest">{symbol}</h2>
          <div className={`text-[10px] font-mono px-1.5 py-0.5 rounded-sm border ${isFresh ? 'text-quant-up-text border-quant-up/30 bg-quant-up/10' : 'text-quant-down-text border-quant-down/30 bg-quant-down/10'}`}>
            {isFresh ? 'FRESH' : `STALE (${overview.data_quality?.trading_days_stale || '?'}D)`}
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 text-xs mb-4">
          <div>
            <p className="text-quant-text-muted text-[10px] uppercase tracking-wider mb-0.5">Close</p>
            <p className="text-quant-text-primary font-mono tabular-nums">{overview.latest_features?.close?.toFixed(2) || '---'}</p>
          </div>
          <div>
            <p className="text-quant-text-muted text-[10px] uppercase tracking-wider mb-0.5">Vol (20d)</p>
            <p className="text-quant-text-primary font-mono tabular-nums">{overview.latest_features?.volatility_20?.toFixed(4) || '---'}</p>
          </div>
        </div>
      </div>

      <div className="pt-3 border-t border-quant-border flex justify-between items-center">
        <div className="flex items-center gap-1.5">
          <div className={`w-1.5 h-1.5 rounded-full ${hasModel ? 'bg-quant-up-text' : 'bg-quant-text-muted'}`}></div>
          <span className="font-mono text-[10px] text-quant-text-secondary tracking-wider">
            {hasModel ? 'MODEL READY' : 'NO MODEL'}
          </span>
        </div>
        <ArrowRight className="w-3.5 h-3.5 text-quant-text-muted group-hover:text-quant-text-primary transition-colors" />
      </div>
    </Link>
  );
}
