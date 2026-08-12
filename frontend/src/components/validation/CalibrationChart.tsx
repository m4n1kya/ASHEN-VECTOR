"use client";

import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export default function CalibrationChart({ data }: { data: any }) {
  const chartData = Array.isArray(data) ? data : (data?.curve || []);
  if (!chartData || chartData.length === 0) return null;

  return (
    <div className="matte-panel p-4 h-[300px] flex flex-col">
      <h2 className="text-[11px] font-semibold tracking-widest text-quant-text-secondary mb-4 uppercase">Model Calibration (Pred vs Actual)</h2>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
            <XAxis 
              type="number" 
              dataKey="predicted" 
              name="Predicted" 
              stroke="#444444" 
              fontSize={10} 
              tickFormatter={(val) => val.toFixed(2)}
            />
            <YAxis 
              type="number" 
              dataKey="actual" 
              name="Actual" 
              stroke="#444444" 
              fontSize={10} 
              tickFormatter={(val) => val.toFixed(2)}
            />
            <Tooltip 
              cursor={{ strokeDasharray: '3 3' }} 
              contentStyle={{ backgroundColor: '#0A0A0A', border: '1px solid #1a1a1a', borderRadius: '4px' }}
              itemStyle={{ fontSize: '12px', fontFamily: 'monospace' }}
            />
            <Scatter name="Predictions" data={chartData} fill="#858585" fillOpacity={0.5} />
            <ReferenceLine segment={[{ x: -0.1, y: -0.1 }, { x: 0.1, y: 0.1 }]} stroke="#444444" strokeDasharray="3 3" />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
