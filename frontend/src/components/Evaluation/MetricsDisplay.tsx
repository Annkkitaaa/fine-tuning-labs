import React from 'react';
import { Card } from '@/components/ui';

interface Metric {
  name: string;
  value: number;
}

interface MetricsDisplayProps {
  metrics: Metric[];
}

export const MetricsDisplay: React.FC<MetricsDisplayProps> = ({ metrics }) => {
  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Model Metrics</h2>
      {metrics.length === 0 ? (
        <p className="text-gray-500">No metrics available yet</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {metrics.map((metric, index) => (
            <div key={index} className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">{metric.name}</p>
              <p className="text-lg font-semibold">{metric.value}</p>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
};