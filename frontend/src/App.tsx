import React from 'react';
import { ModelSelector } from './components/ModelConfig/ModelSelector';
import { DataUploader } from './components/DataProcessor/DataUploader';
import { TrainingPanel } from './components/Training/TrainingPanel';
import { MetricsDisplay } from './components/Evaluation/MetricsDisplay';

const App = () => {
  // You can initialize with empty metrics or add some test metrics
  const metrics = [
    // Example metrics if needed:
    // { name: 'Accuracy', value: 0.95 },
    // { name: 'Loss', value: 0.123 }
  ];

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
            <ModelSelector />
            <DataUploader />
            <TrainingPanel />
            <MetricsDisplay metrics={metrics} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;