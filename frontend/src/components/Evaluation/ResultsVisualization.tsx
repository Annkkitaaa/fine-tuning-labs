import React from 'react';
import { Card } from '@/components/ui';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Metrics } from '@/types';

interface Props {
    data: Metrics[];
}

export const ResultsVisualization: React.FC<Props> = ({ data }) => {
    return (
        <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Training Progress</h2>
            <div className="h-64">
                <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="epoch" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="loss" stroke="#8884d8" />
                    <Line type="monotone" dataKey="accuracy" stroke="#82ca9d" />
                </LineChart>
            </div>
        </Card>
    );
};
