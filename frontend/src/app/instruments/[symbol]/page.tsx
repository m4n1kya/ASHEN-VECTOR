import { fetchOverview } from "@/lib/api";
import Link from "next/link";
import { ArrowLeft, BrainCircuit, Activity } from "lucide-react";

export default async function InstrumentPage({ params }: { params: { symbol: string } }) {
  const symbol = params.symbol;
  let overview = null;
  
  try {
    overview = await fetchOverview(symbol);
  } catch (e) {
    return (
      <div className="p-8">
        <h1 className="text-2xl text-ashen-down">Failed to load {symbol}</h1>
        <Link href="/" className="text-ashen-ash-light hover:text-ashen-bone mt-4 block">← Back</Link>
      </div>
    );
  }

  const features = overview.latest_features || {};
  const preds = overview.latest_predictions || {};
  const isFresh = overview.data_quality?.data_status === "FRESH";

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/" className="p-2 rounded-full hover:bg-ashen-charcoal transition-colors">
            <ArrowLeft className="w-5 h-5 text-ashen-ash-light hover:text-ashen-bone" />
          </Link>
          <h1 className="text-4xl font-bold text-ashen-bone tracking-wider">{symbol}</h1>
          <div className={`px-2 py-1 rounded text-xs font-semibold border ${isFresh ? 'bg-ashen-up/10 border-ashen-up/20 text-ashen-up' : 'bg-ashen-down/10 border-ashen-down/20 text-ashen-down'}`}>
            {isFresh ? 'FRESH' : 'STALE'}
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm text-ashen-ash-light">Last Updated</p>
          <p className="font-mono text-ashen-bone">{overview.data_quality?.latest_available_date || 'Unknown'}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Features Panel */}
        <div className="glass-panel p-6 rounded-xl col-span-1">
          <h2 className="text-xl font-bold text-ashen-bone mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-ashen-ash-light" /> 
            Latest Market Data
          </h2>
          <div className="space-y-3">
            <FeatureRow label="Close" value={features.close?.toFixed(2)} />
            <FeatureRow label="Volume" value={features.volume?.toExponential(2)} />
            <FeatureRow label="RSI 14" value={features.rsi_14?.toFixed(2)} />
            <FeatureRow label="MACD" value={features.macd?.toFixed(4)} />
            <FeatureRow label="Volatility (20d)" value={features.volatility_20?.toFixed(4)} />
            <FeatureRow label="Momentum (20d)" value={features.momentum_20?.toFixed(4)} />
          </div>
        </div>

        {/* Predictions Panel */}
        <div className="glass-panel p-6 rounded-xl col-span-1 lg:col-span-2">
          <h2 className="text-xl font-bold text-ashen-bone mb-4 flex items-center gap-2">
            <BrainCircuit className="w-5 h-5 text-ashen-ash-light" /> 
            Model Inference
          </h2>
          {overview.model_status === "READY" ? (
            <div className="grid grid-cols-2 gap-8 mt-6">
              <div>
                <p className="text-ashen-ash-light text-sm tracking-wider uppercase mb-2">Direction Probability (5D)</p>
                <div className="flex items-end gap-2">
                  <span className={`text-4xl font-mono font-bold ${(preds.probability_up || 0) > 0.5 ? 'text-ashen-up' : 'text-ashen-down'}`}>
                    {((preds.probability_up || 0) * 100).toFixed(1)}%
                  </span>
                  <span className="text-ashen-ash-light mb-1">UP</span>
                </div>
              </div>
              
              <div>
                <p className="text-ashen-ash-light text-sm tracking-wider uppercase mb-2">Expected Return</p>
                <div className="flex items-end gap-2">
                  <span className={`text-4xl font-mono font-bold ${(preds.expected_return || 0) > 0 ? 'text-ashen-up' : 'text-ashen-down'}`}>
                    {((preds.expected_return || 0) * 100).toFixed(2)}%
                  </span>
                </div>
              </div>
              
              <div className="col-span-2 pt-6 border-t border-ashen-charcoal-light">
                <Link 
                  href={`/backtest?symbol=${symbol}`}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-ashen-bone text-ashen-black font-semibold rounded hover:bg-white transition-colors"
                >
                  Run Full Backtest
                </Link>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-40 text-ashen-ash-light">
              <p className="mb-4">No trained models available in registry.</p>
              <Link 
                  href={`/backtest?symbol=${symbol}`}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-ashen-charcoal border border-ashen-ash text-ashen-bone font-semibold rounded hover:bg-ashen-charcoal-light transition-colors"
                >
                  Run Training/Backtest Pipeline
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function FeatureRow({ label, value }: { label: string, value: any }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-ashen-charcoal-light/50 last:border-0">
      <span className="text-sm text-ashen-ash-light">{label}</span>
      <span className="font-mono text-ashen-bone">{value ?? '---'}</span>
    </div>
  );
}
