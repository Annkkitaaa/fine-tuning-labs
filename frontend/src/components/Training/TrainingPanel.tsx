import React, { useState } from 'react';
import { Card, Button, Input, Progress } from '@/components/ui';

export const TrainingPanel = () => {
  const [config, setConfig] = useState({
    epochs: 10,
    batchSize: 32,
    learningRate: 0.001
  });
  const [isTraining, setIsTraining] = useState(false);
  const [progress, setProgress] = useState(0);

  const startTraining = async () => {
    setIsTraining(true);
    try {
      const response = await fetch('/api/v1/training/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });
      // Handle response
    } catch (error) {
      console.error('Training error:', error);
    }
    setIsTraining(false);
  };

  return (
    <Card className="p-6 space-y-4">
      <div className="grid grid-cols-3 gap-4">
        <Input
          label="Epochs"
          type="number"
          value={config.epochs}
          onChange={(e) => setConfig({...config, epochs: parseInt(e.target.value)})}
        />
        <Input
          label="Batch Size"
          type="number"
          value={config.batchSize}
          onChange={(e) => setConfig({...config, batchSize: parseInt(e.target.value)})}
        />
        <Input
          label="Learning Rate"
          type="number"
          value={config.learningRate}
          onChange={(e) => setConfig({...config, learningRate: parseFloat(e.target.value)})}
        />
      </div>
      <Button 
        onClick={startTraining}
        disabled={isTraining}
        className="w-full"
      >
        {isTraining ? 'Training...' : 'Start Training'}
      </Button>
      {isTraining && (
        <Progress value={progress} />
      )}
    </Card>
  );
};