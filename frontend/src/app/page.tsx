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
    <div className="space-y-8">
      <section>
        <h1 className="text-3xl font-bold text-ashen-bone mb-2">System Overview</h1>
        <p className="text-ashen-ash-light">Quantitative Market Intelligence Dashboard</p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {instruments.map((symbol: string) => (
          <InstrumentCard key={symbol} symbol={symbol} />
        ))}
      </section>
    </div>
  );
}

async function InstrumentCard({ symbol }: { symbol: string }) {
  let overview = null;
  try {
    overview = await fetchOverview(symbol);
  } catch (e) {
    // Return minimal card on failure
    return (
      <div className="glass-panel rounded-xl p-6 flex flex-col justify-between opacity-50">
        <h2 className="text-xl font-bold text-ashen-bone">{symbol}</h2>
        <p className="text-ashen-down text-sm mt-2 flex items-center gap-1">
          <AlertTriangle className="w-4 h-4" /> API Error
        </p>
      </div>
    );
  }

  const isFresh = overview.data_quality?.data_status === "FRESH";
  const modelStatus = overview.model_status || "NOT_AVAILABLE";

  return (
    <Link href={`/instruments/${symbol}`} className="glass-panel rounded-xl p-6 flex flex-col justify-between hover:bg-ashen-charcoal transition-all group">
      <div>
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-2xl font-bold text-ashen-bone tracking-wide">{symbol}</h2>
          {isFresh ? (
            <div className="flex items-center gap-1 text-ashen-up text-xs font-semibold px-2 py-1 rounded bg-ashen-up/10 border border-ashen-up/20">
              <CheckCircle2 className="w-3 h-3" /> FRESH
            </div>
          ) : (
            <div className="flex items-center gap-1 text-ashen-down text-xs font-semibold px-2 py-1 rounded bg-ashen-down/10 border border-ashen-down/20">
              <AlertTriangle className="w-3 h-3" /> STALE ({overview.data_quality?.trading_days_stale || '?'}d)
            </div>
          )}
        </div>
        
        <div className="grid grid-cols-2 gap-4 text-sm mb-6">
          <div>
            <p className="text-ashen-ash-light text-xs uppercase tracking-wider mb-1">Latest Close</p>
            <p className="text-ashen-bone font-mono">{overview.latest_features?.close?.toFixed(2) || '---'}</p>
          </div>
          <div>
            <p className="text-ashen-ash-light text-xs uppercase tracking-wider mb-1">Vol (20d)</p>
            <p className="text-ashen-bone font-mono">{overview.latest_features?.volatility_20?.toFixed(4) || '---'}</p>
          </div>
        </div>
      </div>

      <div className="pt-4 border-t border-ashen-charcoal-light flex justify-between items-center text-sm">
        <span className={`font-mono text-xs ${modelStatus === 'READY' ? 'text-ashen-up-light' : 'text-ashen-ash-light'}`}>
          MODEL: {modelStatus}
        </span>
        <span className="text-ashen-ash-light group-hover:text-ashen-bone transition-colors flex items-center gap-1">
          Analyze <ArrowRight className="w-4 h-4" />
        </span>
      </div>
    </Link>
  );
}
