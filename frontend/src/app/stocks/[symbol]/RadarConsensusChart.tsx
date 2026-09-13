"use client";

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from "recharts";

export default function RadarConsensusChart({ consensusBreakdown }: { consensusBreakdown: any[] }) {
  if (!consensusBreakdown || consensusBreakdown.length === 0) {
    return <div className="h-full flex items-center justify-center text-xs text-quant-text-muted italic">No consensus data</div>;
  }

  // Format data for Recharts Radar
  const data = consensusBreakdown.map(model => {
    return {
      model: model.name.replace(" (OOS)", "").replace(" (126D)", "").replace(" (5D)", ""), // Simplify labels
      strength: Math.abs(model.strength * 100), // Magnitude of strength
      fullSignal: model.signal,
      rawStrength: model.strength
    };
  });

  return (
    <div className="w-full h-full min-h-[250px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="#333333" />
          <PolarAngleAxis 
            dataKey="model" 
            tick={{ fill: '#888888', fontSize: 10, fontFamily: 'monospace' }}
          />
          <PolarRadiusAxis 
            angle={30} 
            domain={[0, 100]} 
            tick={false} 
            axisLine={false} 
          />
          <Tooltip 
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                const isBull = data.fullSignal.includes('BUY') || data.fullSignal.includes('BULL');
                const isBear = data.fullSignal.includes('SELL') || data.fullSignal.includes('BEAR') || data.fullSignal.includes('RISK') || data.fullSignal.includes('HIGH');
                const color = isBull ? '#4CAF50' : isBear ? '#F44336' : '#FF9800';

                return (
                  <div className="bg-black/90 border border-quant-border p-3 rounded-sm shadow-xl">
                    <p className="text-[11px] font-bold text-white mb-1">{data.model}</p>
                    <p className="text-[10px] font-mono" style={{ color }}>{data.fullSignal}</p>
                    <p className="text-[10px] text-quant-text-muted mt-1">Strength: {(data.rawStrength * 100).toFixed(1)}%</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Radar 
            name="Consensus Strength" 
            dataKey="strength" 
            stroke="#666666" 
            fill="#444444" 
            fillOpacity={0.4} 
            strokeWidth={1.5}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
