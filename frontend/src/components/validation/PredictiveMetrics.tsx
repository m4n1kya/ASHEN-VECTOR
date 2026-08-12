import { TooltipIcon } from "./TooltipIcon";

export default function PredictiveMetrics({ data }: { data: any }) {
  if (!data) return null;

  return (
    <div className="matte-panel p-4 h-full">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Predictive Metrics</h2>
      <div className="grid grid-cols-2 gap-4">
        <Metric label="Accuracy" value={data.accuracy} tooltip="> 55% is good for financial data" />
        <Metric label="Precision" value={data.precision} tooltip="True positive rate. > 55% good" />
        <Metric label="Recall" value={data.recall} tooltip="Ability to find all positive instances" />
        <Metric label="F1 Score" value={data.f1_score} tooltip="Harmonic mean of Precision and Recall" />
        <Metric label="ROC AUC" value={data.roc_auc} tooltip="Area under ROC curve. > 0.55 indicates edge" />
      </div>
    </div>
  );
}

function Metric({ label, value, tooltip }: { label: string, value: number, tooltip: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-[10px] tracking-widest uppercase text-quant-text-muted flex items-center mb-1">
        {label} <TooltipIcon tooltip={tooltip} />
      </span>
      <span className={`text-xl font-mono tabular-nums ${value > 0.55 ? 'text-quant-up-text' : 'text-quant-text-primary'}`}>
        {(value * 100).toFixed(1)}%
      </span>
    </div>
  );
}
