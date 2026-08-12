"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function FoldStability({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="matte-panel p-4 h-[250px] flex flex-col">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Cross-Validation Stability</h2>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" vertical={false} />
            <XAxis 
              dataKey="fold" 
              stroke="#444444" 
              fontSize={10} 
              tickFormatter={(val) => `Fold ${val}`}
            />
            <YAxis 
              stroke="#444444" 
              fontSize={10} 
            />
            <Tooltip 
              cursor={{ fill: '#111111' }}
              contentStyle={{ backgroundColor: '#0A0A0A', border: '1px solid #1a1a1a', borderRadius: '4px' }}
              itemStyle={{ fontSize: '12px', fontFamily: 'monospace' }}
              formatter={(val: any) => [Number(val).toFixed(2), 'Sharpe Ratio']}
            />
            <Bar dataKey="sharpe" fill="#444444">
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.sharpe > 1 ? '#4caf50' : entry.sharpe > 0 ? '#E8E5DE' : '#f44336'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
