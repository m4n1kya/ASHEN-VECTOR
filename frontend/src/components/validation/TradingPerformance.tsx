import { TooltipIcon } from "./TooltipIcon";

export default function TradingPerformance({ data }: { data: any }) {
  if (!data) return null;

  return (
    <div className="matte-panel p-4 h-full">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Trading Performance</h2>
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <Metric 
          label="Total Return" 
          value={`${(data.total_return * 100).toFixed(2)}%`} 
          color={data.total_return > 0 ? "text-quant-up-text" : "text-quant-down-text"} 
          tooltip="Cumulative return over test period"
        />
        <Metric 
          label="Ann. Return" 
          value={`${(data.annualized_return * 100).toFixed(2)}%`} 
          color={data.annualized_return > 0 ? "text-quant-up-text" : "text-quant-down-text"} 
          tooltip="Annualized return (CAGR)"
        />
        <Metric 
          label="Sharpe Ratio" 
          value={data.sharpe_ratio.toFixed(2)} 
          color={data.sharpe_ratio > 1 ? "text-quant-up-text" : "text-quant-text-primary"} 
          tooltip="Risk-adjusted return. > 1 is good, > 2 excellent"
        />
        <Metric 
          label="Sortino Ratio" 
          value={data.sortino_ratio.toFixed(2)} 
          color={data.sortino_ratio > 1 ? "text-quant-up-text" : "text-quant-text-primary"} 
          tooltip="Return relative to downside risk only"
        />
        <Metric 
          label="Win Rate" 
          value={`${(data.win_rate * 100).toFixed(1)}%`} 
          color={data.win_rate > 0.5 ? "text-quant-up-text" : "text-quant-text-primary"} 
          tooltip="Percentage of profitable trades/periods"
        />
      </div>
    </div>
  );
}

function Metric({ label, value, color, tooltip }: { label: string, value: string, color: string, tooltip: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-[10px] tracking-widest uppercase text-quant-text-muted flex items-center mb-1">
        {label} <TooltipIcon tooltip={tooltip} />
      </span>
      <span className={`text-xl font-mono tabular-nums ${color}`}>
        {value}
      </span>
    </div>
  );
}
