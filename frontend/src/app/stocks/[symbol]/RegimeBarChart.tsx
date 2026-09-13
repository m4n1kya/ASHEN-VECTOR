"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

export default function RegimeBarChart({ hmmData }: { hmmData: any }) {
  if (!hmmData) {
    return <div className="h-full flex items-center justify-center text-xs text-quant-text-muted italic">No regime data</div>;
  }

  const data = [
    { name: "BULL", prob: hmmData["BULL"] * 100, color: "#4CAF50" },
    { name: "BEAR", prob: hmmData["BEAR"] * 100, color: "#F44336" },
    { name: "HI VOL", prob: hmmData["HIGH VOL"] * 100, color: "#FF9800" },
    { name: "LO VOL", prob: hmmData["LOW VOL"] * 100, color: "#2196F3" },
  ];

  return (
    <div className="w-full h-full min-h-[160px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <XAxis type="number" hide domain={[0, 100]} />
          <YAxis 
            dataKey="name" 
            type="category" 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#888888', fontSize: 10, fontFamily: 'monospace' }}
            width={55}
          />
          <Tooltip
            cursor={{ fill: '#222222' }}
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="bg-black/90 border border-quant-border p-2 rounded-sm shadow-xl">
                    <p className="text-[10px] font-mono text-white">{data.name}: {data.prob.toFixed(1)}%</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Bar dataKey="prob" radius={[0, 4, 4, 0]} barSize={16}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} fillOpacity={0.8} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
