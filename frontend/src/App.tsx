import React, { useState } from 'react';
import { ModelSelector } from './components/ModelConfig/ModelSelector';
import { ConfigForm } from './components/ModelConfig/ConfigForm';
import { DataUploader } from './components/DataProcessor/DataUploader';
import { Preprocessing } from './components/DataProcessor/Preprocessing';
import { TrainingPanel } from './components/Training/TrainingPanel';
import { MetricsDisplay } from './components/Evaluation/MetricsDisplay';
import { ModelConfig } from '@/types';

// Define the Metric interface
interface Metric {
  name: string;
  value: number;
}

const App: React.FC = () => {
  const [isTraining, setIsTraining] = useState(false);
  const [modelConfig, setModelConfig] = useState<ModelConfig>({
    framework: 'pytorch',
    modelType: 'bert-base'
  });
  const [metrics, setMetrics] = useState<Metric[]>([]);

  const handleTrainingStart = () => {
    setIsTraining(true);
    // Reset metrics when training starts
    setMetrics([]);
  };

  const handleTrainingStop = () => {
    setIsTraining(false);
  };

  const handleModelSelect = (config: ModelConfig) => {
    setModelConfig(config);
  };

  const handleConfigSubmit = (config: any) => {
    console.log('Training configuration:', config);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">Fine-Tuning Labs</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 gap-6">
            <ModelSelector 
              onSelect={handleModelSelect}
              currentConfig={modelConfig}
            />
            <ConfigForm onSubmit={handleConfigSubmit} />
            <DataUploader />
            <Preprocessing />
            <TrainingPanel 
              onStart={handleTrainingStart}
              onStop={handleTrainingStop}
              isTraining={isTraining}
            />
            <MetricsDisplay 
              metrics={metrics}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;