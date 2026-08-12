import ModelsClient from "./ModelsClient";

export default function ModelsPage() {
  return (
    <div className="space-y-6 h-full flex flex-col">
      <header className="pb-4 border-b border-quant-border shrink-0">
        <h1 className="text-xl font-medium tracking-wide text-quant-text-primary uppercase">Unified Model Inference Engine</h1>
        <p className="text-xs text-quant-text-secondary mt-1">Live market analysis across mathematical & ML techniques</p>
      </header>
      
      <ModelsClient />
    </div>
  );
}
