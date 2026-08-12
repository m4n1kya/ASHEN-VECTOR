"use client";

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DrawdownChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="matte-panel p-4 h-[200px] flex flex-col">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Drawdown Profile</h2>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
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
              tickFormatter={(val) => `${(val * 100).toFixed(0)}%`}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0A0A0A', border: '1px solid #1a1a1a', borderRadius: '4px' }}
              itemStyle={{ fontSize: '12px', fontFamily: 'monospace', color: '#f44336' }}
              labelStyle={{ color: '#858585', fontSize: '10px', marginBottom: '4px' }}
              formatter={(val: any) => [`${(Number(val) * 100).toFixed(2)}%`, 'Drawdown']}
            />
            <Area type="monotone" dataKey="drawdown" stroke="#b71c1c" fill="#b71c1c" fillOpacity={0.2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
