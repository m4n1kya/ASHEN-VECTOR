"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function EquityCurveChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="matte-panel p-4 h-[300px] flex flex-col">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Equity Curve (OOS)</h2>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" vertical={false} />
            <XAxis 
              dataKey="date" 
              stroke="#444444" 
              fontSize={10} 
              tickMargin={10}
              minTickGap={30}
            />
            <YAxis 
              stroke="#444444" 
              fontSize={10} 
              tickFormatter={(val) => val.toFixed(2)}
              domain={['auto', 'auto']}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0A0A0A', border: '1px solid #1a1a1a', borderRadius: '4px' }}
              itemStyle={{ fontSize: '12px', fontFamily: 'monospace' }}
              labelStyle={{ color: '#858585', fontSize: '10px', marginBottom: '4px' }}
            />
            <Line type="monotone" dataKey="strategy" stroke="#E8E5DE" strokeWidth={2} dot={false} name="Strategy" />
            <Line type="monotone" dataKey="benchmark" stroke="#444444" strokeWidth={2} dot={false} name="Benchmark" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
