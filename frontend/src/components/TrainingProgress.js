import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export const TrainingProgress = ({ history }) => {
  if (!history) return null;

  const data = Object.entries(history.train_loss).map((entry, index) => ({
    epoch: index + 1,
    training: entry[1],
    validation: history.val_loss[index]
  }));

  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Training Progress</h2>
      <div className="h-96">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="epoch" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="training" stroke="#8884d8" name="Training Loss" />
            <Line type="monotone" dataKey="validation" stroke="#82ca9d" name="Validation Loss" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
