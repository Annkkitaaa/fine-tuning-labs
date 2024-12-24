import React, { useState } from 'react';
import { ConfigPanel } from '../components/ConfigPanel';
import { TrainingProgress } from '../components/TrainingProgress';
import { startTraining } from '../utils/api';

export const Training = () => {
  const [config, setConfig] = useState({
    framework: 'pytorch',
    hyperparameters: {
      learning_rate: 0.001,
      batch_size: 32,
      epochs: 10
    }
  });

  const handleStartTraining = async () => {
    try {
      await startTraining(config);
    } catch (error) {
      console.error('Training failed:', error);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Training</h1>
      <ConfigPanel config={config} onChange={setConfig} />
      <button
        onClick={handleStartTraining}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Start Training
      </button>
      <TrainingProgress />
    </div>
  );
};
