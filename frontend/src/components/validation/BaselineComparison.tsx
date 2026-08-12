export default function BaselineComparison({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="matte-panel p-4 overflow-x-auto">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Baseline Comparison</h2>
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-quant-border">
            <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Strategy</th>
            <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Ann. Return</th>
            <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Sharpe</th>
            <th className="pb-2 text-[10px] tracking-widest uppercase font-normal text-quant-text-muted">Max DD</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-quant-border/50">
          {data.map((row, i) => (
            <tr key={i} className={`hover:bg-quant-elevated/50 transition-colors ${row.baseline === 'ASHEN' ? 'bg-quant-text-primary/5' : ''}`}>
              <td className={`py-3 text-xs font-bold tracking-widest ${row.baseline === 'ASHEN' ? 'text-quant-text-primary' : 'text-quant-text-secondary'}`}>
                {row.baseline}
              </td>
              <td className={`py-3 font-mono text-xs tabular-nums ${row.return > 0 ? 'text-quant-up-text' : 'text-quant-down-text'}`}>
                {(row.return * 100).toFixed(2)}%
              </td>
              <td className={`py-3 font-mono text-xs tabular-nums ${row.sharpe > 1 ? 'text-quant-up-text' : 'text-quant-text-primary'}`}>
                {row.sharpe.toFixed(2)}
              </td>
              <td className="py-3 font-mono text-xs tabular-nums text-quant-down-text">
                {(row.max_dd * 100).toFixed(2)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
