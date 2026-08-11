"use client";

import { ResponsiveContainer, ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine } from 'recharts';

// Generate more realistic looking mock data to match the screenshot shape
const generateData = () => {
  const data = [];
  let currentPrice = 135;
  let months = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'];
  let monthIdx = 0;
  
  for (let i = 0; i < 200; i++) {
    // Random walk with upward drift
    const change = (Math.random() - 0.45) * 2;
    currentPrice += change;
    
    // Periodically add month labels
    let label = '';
    if (i % 25 === 0 && monthIdx < months.length) {
      label = months[monthIdx];
      monthIdx++;
    }
    
    // Volume spikes on big price moves
    const volBase = Math.random() * 20 + 10;
    const volume = Math.abs(change) > 1.5 ? volBase * 3 : volBase;

    data.push({
      index: i,
      label,
      price: currentPrice,
      volume: volume,
    });
  }
  
  // Force the last price to 178.50 to match the mockup
  data[data.length - 1].price = 178.50;
  
  return data;
};

const data = generateData();

export default function PriceChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <ComposedChart data={data} margin={{ top: 20, right: 0, left: 10, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#242424" vertical={true} />
        
        {/* PRICE AXIS (Right) */}
        <YAxis 
          yAxisId="price"
          orientation="right"
          domain={['dataMin - 5', 'dataMax + 5']}
          stroke="#555555" 
          fontSize={10} 
          tickLine={false} 
          axisLine={false} 
          tickFormatter={(val) => val.toFixed(2)}
          width={45}
        />
        
        {/* VOLUME AXIS (Hidden) */}
        <YAxis 
          yAxisId="volume"
          orientation="left"
          domain={[0, 'dataMax * 4']} // Keep bars in bottom quarter
          hide
        />

        <XAxis 
          dataKey="label" 
          stroke="#555555" 
          fontSize={10} 
          tickLine={false} 
          axisLine={false} 
          dy={10}
        />
        
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#111111', 
            borderColor: '#242424',
            fontSize: '10px',
            fontFamily: 'monospace',
            color: '#E8E5DE'
          }} 
          itemStyle={{ color: '#E8E5DE' }}
          labelStyle={{ display: 'none' }}
          cursor={{ stroke: '#555555', strokeWidth: 1, strokeDasharray: '3 3' }}
        />
        
        {/* Reference Line for current price */}
        <ReferenceLine 
          yAxisId="price" 
          y={178.50} 
          stroke="#555555" 
          strokeDasharray="2 2" 
          strokeWidth={1} 
        />
        <ReferenceLine 
          yAxisId="price" 
          y={178.50} 
          stroke="#none" 
          label={{ position: 'right', value: '178.50', fill: '#E8E5DE', fontSize: 10, fontWeight: 'bold' }} 
        />

        {/* Volume Bars */}
        <Bar 
          yAxisId="volume"
          dataKey="volume" 
          fill="#242424" 
          isAnimationActive={false}
        />

        {/* Price Line */}
        <Line 
          yAxisId="price"
          type="monotone" 
          dataKey="price" 
          stroke="#E8E5DE" 
          strokeWidth={1.5} 
          dot={false} 
          activeDot={{ r: 3, fill: '#E8E5DE', stroke: '#E8E5DE' }} 
          isAnimationActive={false}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
