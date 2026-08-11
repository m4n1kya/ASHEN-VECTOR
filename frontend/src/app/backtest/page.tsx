import BacktestClient from "./BacktestClient";

export default function BacktestPage({
  searchParams,
}: {
  searchParams: { symbol?: string };
}) {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <section>
        <h1 className="text-3xl font-bold text-ashen-bone mb-2">Backtest Engine</h1>
        <p className="text-ashen-ash-light">Run Walk-Forward Out-of-Sample Backtests</p>
      </section>
      
      <BacktestClient defaultSymbol={searchParams.symbol || "SH600000"} />
    </div>
  );
}
