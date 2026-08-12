import ValidationClient from "./ValidationClient";

export default function ValidationPage() {
  return (
    <div className="h-full flex flex-col p-6 max-w-[1600px] mx-auto w-full">
      <div className="mb-6 flex flex-col">
        <h1 className="text-2xl font-bold tracking-widest text-quant-text-primary uppercase">Model Validation</h1>
        <span className="text-xs text-quant-text-secondary tracking-wider uppercase mt-1">
          Phase 8 • Out-of-Sample Backtesting & Performance Analysis
        </span>
      </div>
      <ValidationClient />
    </div>
  );
}
