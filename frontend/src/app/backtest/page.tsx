import BacktestClient from "./BacktestClient";

export default function BacktestPage({
  searchParams,
}: {
  searchParams: { symbol?: string };
}) {
  return (
    <div className="space-y-6">
      <header className="pb-4 border-b border-quant-border">
        <h1 className="text-xl font-medium tracking-wide text-quant-text-primary">BACKTEST ENGINE</h1>
        <p className="text-xs text-quant-text-secondary mt-1">Walk-Forward Out-of-Sample Validation</p>
      </header>
      
      <BacktestClient defaultSymbol={searchParams.symbol || "SH600000"} />
    </div>
  );
}
