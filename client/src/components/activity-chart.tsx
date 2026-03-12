import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card } from "@/components/ui/card";

// Dummy data for visualization
const data = [
  { time: '09:00', value: 4000, signals: 2 },
  { time: '10:00', value: 3000, signals: 1 },
  { time: '11:00', value: 2000, signals: 4 },
  { time: '12:00', value: 2780, signals: 3 },
  { time: '13:00', value: 1890, signals: 5 },
  { time: '14:00', value: 2390, signals: 2 },
  { time: '15:00', value: 3490, signals: 6 },
  { time: '16:00', value: 4200, signals: 8 },
  { time: '17:00', value: 3800, signals: 4 },
];

export function ActivityChart() {
  return (
    <div className="glass-panel rounded-2xl p-6 h-full flex flex-col">
      <div className="mb-6">
        <h2 className="text-lg font-semibold tracking-tight">Market Activity</h2>
        <p className="text-sm text-muted-foreground mt-1">Signal generation volume over time</p>
      </div>
      
      <div className="flex-1 w-full min-h-[250px]">
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
            <XAxis 
              dataKey="time" 
              stroke="hsl(var(--muted-foreground))" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="hsl(var(--muted-foreground))" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `${value}`}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                borderColor: 'hsl(var(--border))',
                borderRadius: '8px',
                color: 'hsl(var(--foreground))'
              }}
              itemStyle={{ color: 'hsl(var(--primary))' }}
            />
            <Area 
              type="monotone" 
              dataKey="value" 
              stroke="hsl(var(--primary))" 
              strokeWidth={2}
              fillOpacity={1} 
              fill="url(#colorValue)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
