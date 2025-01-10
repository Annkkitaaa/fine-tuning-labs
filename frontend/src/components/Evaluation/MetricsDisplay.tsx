import React from 'react';
import { Card } from '@/components/ui';
import { Metrics } from '@/types';

interface Props {
    metrics: Metrics;
}

export const MetricsDisplay: React.FC<Props> = ({ metrics }) => {
    return (
        <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Training Metrics</h2>
            <div className="grid grid-cols-2 gap-4">
                {Object.entries(metrics).map(([key, value]) => (
                    <div key={key} className="bg-gray-50 p-4 rounded-lg">
                        <div className="text-sm text-gray-500">{key}</div>
                        <div className="text-lg font-semibold">
                            {typeof value === 'number' ? value.toFixed(4) : value}
                        </div>
                    </div>
                ))}
            </div>
        </Card>
    );
};
