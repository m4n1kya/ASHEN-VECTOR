"use client";

export default function ResultsDisplay({ result }: { result: any }) {
  const pred = result.predictive_performance || {};
  const trade = result.trading_performance || {};
  const risk = result.risk_metrics || {};
  const bench = result.benchmark_comparison || {};
  
  const verdict = bench.verdict || "UNKNOWN";

  return (
    <div className="space-y-6 mt-6">
      <div className="flex items-center justify-between pb-2 border-b border-quant-border">
        <h2 className="text-xs font-bold tracking-widest text-quant-text-secondary">QUANTITATIVE REPORT</h2>
        <div className={`px-2 py-0.5 rounded-sm font-mono text-[10px] tracking-widest border ${
          verdict === 'OUTPERFORMING' ? 'bg-quant-up/10 text-quant-up-text border-quant-up/30' :
          verdict === 'UNDERPERFORMING' ? 'bg-quant-down/10 text-quant-down-text border-quant-down/30' :
          'bg-quant-bg text-quant-text-muted border-quant-border'
        }`}>
          VERDICT: {verdict}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Predictive Performance */}
        <div className="matte-panel p-4 space-y-2">
          <h3 className="text-[10px] font-bold tracking-widest text-quant-text-muted mb-3">PREDICTIVE SKILL</h3>
          <MetricRow label="Accuracy" value={`${(pred.accuracy * 100).toFixed(2)}%`} />
          <MetricRow label="Precision" value={`${(pred.precision * 100).toFixed(2)}%`} />
          <MetricRow label="ROC-AUC" value={pred.roc_auc?.toFixed(4)} />
          <MetricRow label="Correlation (IC)" value={pred.correlation?.toFixed(4)} />
        </div>

        {/* Trading Performance */}
        <div className="matte-panel p-4 space-y-2">
          <h3 className="text-[10px] font-bold tracking-widest text-quant-text-muted mb-3">SIMULATED TRADING</h3>
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
        <div className="matte-panel p-4 space-y-2">
          <h3 className="text-[10px] font-bold tracking-widest text-quant-text-muted mb-3">RISK & DRAWDOWN</h3>
          <MetricRow label="Sharpe Ratio" value={risk.sharpe_ratio?.toFixed(2)} />
          <MetricRow label="Max Drawdown" value={`${(risk.max_drawdown * 100).toFixed(2)}%`} highlight={false} />
          <MetricRow label="Max DD Duration (days)" value={risk.max_drawdown_duration_days} />
          <MetricRow label="Volatility" value={`${(risk.annualized_volatility * 100).toFixed(2)}%`} />
        </div>
      </div>
      
      {/* Benchmark Comparison */}
      <div className="matte-panel p-4">
        <h3 className="text-[10px] font-bold tracking-widest text-quant-text-muted mb-4">BENCHMARK COMPARISON</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-quant-border">
                <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Strategy</th>
                <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Return</th>
                <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Sharpe</th>
                <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Max DD</th>
                <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Win Rate</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-quant-border">
              <BenchmarkRow name="ASHEN-VECTOR" stats={{...trade, ...risk}} isModel={true} />
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
  
  let color = "text-quant-text-primary";
  if (highlight === true) color = "text-quant-up-text";
  if (highlight === false) color = "text-quant-down-text";
  
  return (
    <div className="flex justify-between items-center py-1 border-b border-quant-border/50 last:border-0">
      <span className="text-xs text-quant-text-secondary">{label}</span>
      <span className={`font-mono text-xs tabular-nums ${color}`}>{value}</span>
    </div>
  );
}

function BenchmarkRow({ name, stats, isModel }: { name: string, stats: any, isModel?: boolean }) {
  if (!stats) return null;
  return (
    <tr className={`${isModel ? 'bg-quant-bg/50' : ''} hover:bg-quant-bg transition-colors`}>
      <td className={`py-2 text-[10px] tracking-widest uppercase ${isModel ? 'font-bold text-quant-text-primary' : 'text-quant-text-secondary'}`}>
        {name}
      </td>
      <td className="py-2 font-mono tabular-nums text-quant-text-primary">
        {stats.cumulative_return ? (stats.cumulative_return > 0 ? '+' : '') + (stats.cumulative_return * 100).toFixed(2) + '%' : '---'}
      </td>
      <td className="py-2 font-mono tabular-nums text-quant-text-primary">{stats.sharpe_ratio ? stats.sharpe_ratio.toFixed(2) : '---'}</td>
      <td className="py-2 font-mono tabular-nums text-quant-text-primary">{stats.max_drawdown ? (stats.max_drawdown * 100).toFixed(2) + '%' : '---'}</td>
      <td className="py-2 font-mono tabular-nums text-quant-text-primary">{stats.win_rate ? (stats.win_rate * 100).toFixed(1) + '%' : '---'}</td>
    </tr>
  );
}
