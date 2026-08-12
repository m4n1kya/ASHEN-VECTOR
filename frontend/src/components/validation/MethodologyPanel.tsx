export default function MethodologyPanel({ data }: { data: any }) {
  if (!data) return null;
  
  return (
    <div className="matte-panel p-4 h-full flex flex-col justify-between">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Methodology</h2>
      <div className="space-y-3">
        <Row label="Model" value={data.model} />
        <Row label="Target Horizon" value={`${data.horizon} Days`} />
        <Row label="Training Period" value={data.train_period} />
        <Row label="Test Period" value={data.test_period} />
        <Row label="Target Variable" value={data.target} />
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string, value: string }) {
  return (
    <div className="flex justify-between items-center py-1">
      <span className="text-xs text-quant-text-secondary">{label}</span>
      <span className="font-mono text-xs tabular-nums text-quant-text-primary">{value}</span>
    </div>
  );
}
