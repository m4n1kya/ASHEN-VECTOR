import { Metadata } from "next";
import Link from "next/link";
import { BookOpen, AlertTriangle } from "lucide-react";

export const metadata: Metadata = {
  title: "Quantitative Research | ASHEN-VECTOR",
};

export default function ResearchPage() {
  return (
    <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full gap-8 py-8 animate-in fade-in duration-500">
      
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-quant-border">
        <div>
          <h1 className="text-3xl font-normal tracking-wider text-quant-text-primary mb-2 flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-quant-text-muted" />
            QUANTITATIVE RESEARCH
          </h1>
          <p className="text-xs tracking-widest text-quant-text-secondary uppercase">Methodology & Deep Research Modules</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ModuleCard title="Factor Models" status="IMPLEMENTED" link="/research/factors" />
        <ModuleCard title="Technical Signals" status="IMPLEMENTED" link="/research/technical" />
        <ModuleCard title="Statistical Models" status="COMING SOON" />
        <ModuleCard title="Regime Analysis" status="IMPLEMENTED" link="/research/regime" />
        <ModuleCard title="Model Consensus" status="IMPLEMENTED" link="/research/consensus" />
      </div>

    </div>
  );
}

function ModuleCard({ title, status, link }: { title: string, status: string, link?: string }) {
  const isImplemented = status === "IMPLEMENTED";

  const Content = (
    <div className={`matte-panel p-6 flex flex-col h-full border ${isImplemented ? 'hover:border-quant-text-muted cursor-pointer transition-colors' : 'opacity-70 border-quant-border'}`}>
      <h2 className="text-sm font-mono tracking-widest text-quant-text-primary mb-6">{title}</h2>
      
      <div className="mt-auto pt-6 border-t border-quant-border flex items-center justify-between">
        <span className={`text-[10px] font-bold tracking-widest uppercase ${isImplemented ? 'text-quant-up-text' : 'text-quant-warn-text'}`}>
          {status}
        </span>
        {!isImplemented && <AlertTriangle className="w-4 h-4 text-quant-warn-text" />}
      </div>
    </div>
  );

  if (link && isImplemented) {
    return <Link href={link} className="block h-full">{Content}</Link>;
  }

  return Content;
}
