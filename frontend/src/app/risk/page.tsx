import { Metadata } from "next";
import { ShieldAlert, AlertTriangle } from "lucide-react";

export const metadata: Metadata = {
  title: "Risk Analysis | ASHEN-VECTOR",
};

export default function RiskPage() {
  return (
    <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full gap-8 py-8 animate-in fade-in duration-500">
      
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-quant-border">
        <div>
          <h1 className="text-3xl font-normal tracking-wider text-quant-text-primary mb-2 flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-quant-text-muted" />
            RISK ANALYSIS
          </h1>
          <p className="text-xs tracking-widest text-quant-text-secondary uppercase">Portfolio Risk & Drawdown Management</p>
        </div>
      </div>

      <div className="matte-panel p-16 flex flex-col items-center justify-center text-center">
        <AlertTriangle className="w-12 h-12 text-quant-warn-text mb-6 opacity-80" />
        <h2 className="text-lg font-mono tracking-widest text-quant-text-primary mb-2">NOT IMPLEMENTED</h2>
        <p className="text-xs text-quant-text-muted max-w-md mx-auto leading-relaxed">
          The global portfolio risk engine (VaR, CVaR, Correlation, Stress Testing) is currently under development. Risk metrics for individual instruments can be found on their respective stock analysis pages.
        </p>
      </div>

    </div>
  );
}
