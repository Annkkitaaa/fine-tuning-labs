import React, { useState } from 'react';
import { Card } from '@/components/ui/Card';

interface ConfigFormProps {
  onSubmit: (config: ModelConfig) => void;
}

interface ModelConfig {
  batchSize: number;
  epochs: number;
  learningRate: number;
  modelType: string;
}

export const ConfigForm: React.FC<ConfigFormProps> = ({ onSubmit }) => {
  const [config, setConfig] = useState<ModelConfig>({
    batchSize: 32,
    epochs: 10,
    learningRate: 0.001,
    modelType: 'bert-base'
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(config);
  };

  return (
    <Card>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Model Type</label>
          <select
            value={config.modelType}
            onChange={(e) => setConfig({ ...config, modelType: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
            <option value="bert-base">BERT Base</option>
            <option value="roberta-base">RoBERTa Base</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Batch Size</label>
          <input
            type="number"
            value={config.batchSize}
            onChange={(e) => setConfig({ ...config, batchSize: Number(e.target.value) })}
            min={1}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Epochs</label>
          <input
            type="number"
            value={config.epochs}
            onChange={(e) => setConfig({ ...config, epochs: Number(e.target.value) })}
            min={1}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Learning Rate</label>
          <input
            type="number"
            value={config.learningRate}
            onChange={(e) => setConfig({ ...config, learningRate: Number(e.target.value) })}
            step="0.0001"
            min={0}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Save Configuration
        </button>
      </form>
    </Card>
  );
};