import { Info } from "lucide-react";
import React from "react";

export function TooltipIcon({ tooltip }: { tooltip: string }) {
  return (
    <div className="group relative inline-flex items-center ml-1.5 cursor-help">
      <Info className="w-3 h-3 text-quant-text-muted hover:text-quant-text-primary transition-colors" />
      <div className="pointer-events-none absolute bottom-full left-1/2 -translate-x-1/2 mb-1 w-48 opacity-0 group-hover:opacity-100 transition-opacity z-50">
        <div className="bg-quant-elevated text-quant-text-primary text-[10px] p-2 rounded border border-quant-border shadow-lg">
          {tooltip}
        </div>
      </div>
    </div>
  );
}
