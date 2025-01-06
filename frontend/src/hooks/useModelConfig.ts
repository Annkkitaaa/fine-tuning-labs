import { useState } from 'react';
import { ModelConfig } from '../types';

export const useModelConfig = () => {
  const [config, setConfig] = useState<ModelConfig>({
    framework: 'pytorch',
    modelType: 'bert-base'
  });

  const updateConfig = (updates: Partial<ModelConfig>) => {
    setConfig(prev => ({ ...prev, ...updates }));
  };

  return { config, updateConfig };
};
