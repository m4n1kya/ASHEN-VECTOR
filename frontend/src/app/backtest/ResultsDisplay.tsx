"use client";

import { CheckCircle2, TrendingUp, TrendingDown, Target } from "lucide-react";

export default function ResultsDisplay({ result }: { result: any }) {
  const pred = result.predictive_performance || {};
  const trade = result.trading_performance || {};
  const risk = result.risk_metrics || {};
  const bench = result.benchmark_comparison || {};
  
  const verdict = bench.verdict || "UNKNOWN";

  return (
    <div className="space-y-6 mt-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-ashen-bone">Backtest Results</h2>
        <div className={`px-4 py-1 rounded-full font-bold text-sm tracking-widest border ${
          verdict === 'OUTPERFORMING' ? 'bg-ashen-up/10 text-ashen-up border-ashen-up' :
          verdict === 'UNDERPERFORMING' ? 'bg-ashen-down/10 text-ashen-down border-ashen-down' :
          'bg-ashen-ash/10 text-ashen-bone border-ashen-ash'
        }`}>
          VERDICT: {verdict}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Predictive Performance */}
        <div className="glass-panel p-6 rounded-xl space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-widest text-ashen-ash-light flex items-center gap-2 mb-4">
            <Target className="w-4 h-4" /> Predictive Skill
          </h3>
          <MetricRow label="Accuracy" value={`${(pred.accuracy * 100).toFixed(2)}%`} />
          <MetricRow label="Precision" value={`${(pred.precision * 100).toFixed(2)}%`} />
          <MetricRow label="ROC-AUC" value={pred.roc_auc?.toFixed(4)} />
          <MetricRow label="Correlation (IC)" value={pred.correlation?.toFixed(4)} />
        </div>

        {/* Trading Performance */}
        <div className="glass-panel p-6 rounded-xl space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-widest text-ashen-ash-light flex items-center gap-2 mb-4">
            <TrendingUp className="w-4 h-4" /> Simulated Trading
          </h3>
          <MetricRow 
            label="Cumulative Return" 
            value={`${(trade.cumulative_return * 100).toFixed(2)}%`} 
            highlight={trade.cumulative_return > 0} 
          />
          <MetricRow label="Annualized Return" value={`${(trade.annualized_return * 100).toFixed(2)}%`} />
          <MetricRow label="Win Rate" value={`${(trade.win_rate * 100).toFixed(2)}%`} />
          <MetricRow label="Total Trades" value={trade.number_of_trades} />
        </div>

        {/* Risk Metrics */}
        <div className="glass-panel p-6 rounded-xl space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-widest text-ashen-ash-light flex items-center gap-2 mb-4">
            <TrendingDown className="w-4 h-4" /> Risk & Drawdown
          </h3>
          <MetricRow label="Sharpe Ratio" value={risk.sharpe_ratio?.toFixed(2)} />
          <MetricRow label="Max Drawdown" value={`${(risk.max_drawdown * 100).toFixed(2)}%`} highlight={false} />
          <MetricRow label="Max DD Duration (days)" value={risk.max_drawdown_duration_days} />
          <MetricRow label="Volatility" value={`${(risk.annualized_volatility * 100).toFixed(2)}%`} />
        </div>
      </div>
      
      {/* Benchmark Comparison */}
      <div className="glass-panel p-6 rounded-xl">
        <h3 className="text-sm font-bold uppercase tracking-widest text-ashen-ash-light mb-6">Benchmark Comparison</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-ashen-charcoal-light">
                <th className="pb-3 text-ashen-ash-light font-normal">Strategy</th>
                <th className="pb-3 text-ashen-ash-light font-normal">Return</th>
                <th className="pb-3 text-ashen-ash-light font-normal">Sharpe</th>
                <th className="pb-3 text-ashen-ash-light font-normal">Max DD</th>
                <th className="pb-3 text-ashen-ash-light font-normal">Win Rate</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ashen-charcoal-light/50">
              <BenchmarkRow name="ASHEN-VECTOR Model" stats={{...trade, ...risk}} isModel={true} />
              <BenchmarkRow name="Buy & Hold" stats={{...bench.buy_and_hold?.trading_performance, ...bench.buy_and_hold?.risk_metrics}} />
              <BenchmarkRow name="Momentum" stats={{...bench.momentum?.trading_performance, ...bench.momentum?.risk_metrics}} />
              <BenchmarkRow name="SMA-20" stats={{...bench.sma20?.trading_performance, ...bench.sma20?.risk_metrics}} />
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function MetricRow({ label, value, highlight }: { label: string, value: any, highlight?: boolean }) {
  if (value === undefined || value === "NaN%" || Number.isNaN(value)) value = "---";
  
  let color = "text-ashen-bone";
  if (highlight === true) color = "text-ashen-up";
  if (highlight === false) color = "text-ashen-down";
  
  return (
    <div className="flex justify-between items-center py-1 border-b border-ashen-charcoal-light/30 last:border-0">
      <span className="text-ashen-ash-light text-sm">{label}</span>
      <span className={`font-mono font-bold ${color}`}>{value}</span>
    </div>
  );
}

function BenchmarkRow({ name, stats, isModel }: { name: string, stats: any, isModel?: boolean }) {
  if (!stats) return null;
  return (
    <tr className={`${isModel ? 'bg-ashen-charcoal/50' : ''}`}>
      <td className={`py-3 ${isModel ? 'font-bold text-ashen-bone' : 'text-ashen-bone-light'}`}>
        {name} {isModel && <CheckCircle2 className="inline w-3 h-3 text-ashen-up ml-1" />}
      </td>
      <td className="py-3 font-mono">{stats.cumulative_return ? (stats.cumulative_return * 100).toFixed(2) + '%' : '---'}</td>
      <td className="py-3 font-mono">{stats.sharpe_ratio ? stats.sharpe_ratio.toFixed(2) : '---'}</td>
      <td className="py-3 font-mono">{stats.max_drawdown ? (stats.max_drawdown * 100).toFixed(2) + '%' : '---'}</td>
      <td className="py-3 font-mono">{stats.win_rate ? (stats.win_rate * 100).toFixed(1) + '%' : '---'}</td>
    </tr>
  );
}
