"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function FeatureImportance({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="matte-panel p-4 h-[300px] flex flex-col">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Feature Importance (Top 10)</h2>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data.slice(0, 10)} layout="vertical" margin={{ top: 5, right: 5, left: 30, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" horizontal={false} />
            <XAxis 
              type="number" 
              stroke="#444444" 
              fontSize={10} 
            />
            <YAxis 
              dataKey="feature" 
              type="category" 
              stroke="#858585" 
              fontSize={10} 
              width={80}
            />
            <Tooltip 
              cursor={{ fill: '#111111' }}
              contentStyle={{ backgroundColor: '#0A0A0A', border: '1px solid #1a1a1a', borderRadius: '4px' }}
              itemStyle={{ fontSize: '12px', fontFamily: 'monospace', color: '#E8E5DE' }}
              formatter={(val: any) => [Number(val).toFixed(4), 'Importance']}
            />
            <Bar dataKey="importance" fill="#858585" barSize={12} radius={[0, 2, 2, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
