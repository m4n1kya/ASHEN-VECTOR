import { CheckCircle2, XCircle, AlertCircle } from "lucide-react";

export default function ModelVerdict({ data }: { data: any }) {
  if (!data) return null;

  const isPass = data.status === 'PASS';
  const isFail = data.status === 'FAIL';
  const colorClass = isPass ? 'text-quant-up-text' : isFail ? 'text-quant-down-text' : 'text-quant-warn-text';
  const bgClass = isPass ? 'bg-quant-up/10 border-quant-up/30' : isFail ? 'bg-quant-down/10 border-quant-down/30' : 'bg-quant-warn-text/10 border-quant-warn-text/30';

  return (
    <div className={`matte-panel p-6 border ${bgClass} flex flex-col md:flex-row items-center gap-6`}>
      <div className={`shrink-0 ${colorClass}`}>
        {isPass ? <CheckCircle2 className="w-12 h-12" /> : isFail ? <XCircle className="w-12 h-12" /> : <AlertCircle className="w-12 h-12" />}
      </div>
      <div className="flex-1 text-center md:text-left">
        <h2 className="text-[10px] tracking-widest uppercase text-quant-text-secondary mb-1">Final Validation Verdict</h2>
        <div className={`text-2xl font-bold tracking-widest mb-2 ${colorClass}`}>
          {data.status} ({(data.confidence * 100).toFixed(1)}% Confidence)
        </div>
        <p className="text-sm text-quant-text-primary">
          {data.message}
        </p>
      </div>
    </div>
  );
}
