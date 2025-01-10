import React from 'react';
import { Card, Select } from '@/components/ui';

// Define the ModelConfig type if not already defined
interface ModelConfig {
  framework: 'pytorch' | 'tensorflow' | 'sklearn';
  modelType: string;
}

interface Props {
  onSelect: (config: ModelConfig) => void;
  currentConfig?: ModelConfig;
}

export const ModelSelector: React.FC<Props> = ({ onSelect, currentConfig }) => {
  const frameworks = [
    { value: 'pytorch', label: 'PyTorch' },
    { value: 'tensorflow', label: 'TensorFlow' },
    { value: 'sklearn', label: 'Scikit-learn' }
  ];

  const models: Record<ModelConfig['framework'], string[]> = {
    pytorch: ['bert-base', 'roberta-base'],
    tensorflow: ['bert-base-tf', 'distilbert-tf'],
    sklearn: ['random-forest', 'svm']
  };

  // Ensure we have a valid framework
  const currentFramework = currentConfig?.framework || 'pytorch';

  return (
    <Card className="p-6 space-y-4">
      <h2 className="text-xl font-semibold">Model Selection</h2>
      <Select
        label="Framework"
        options={frameworks}
        value={currentFramework}
        onChange={(value) => onSelect({
          framework: value as ModelConfig['framework'],
          modelType: models[value as ModelConfig['framework']][0] // Set first model as default
        })}
      />
      <Select
        label="Model Type"
        options={models[currentFramework].map(m => ({ value: m, label: m }))}
        value={currentConfig?.modelType || models[currentFramework][0]}
        onChange={(value) => onSelect({
          framework: currentFramework,
          modelType: value
        })}
        disabled={!currentFramework}
      />
    </Card>
  );
};