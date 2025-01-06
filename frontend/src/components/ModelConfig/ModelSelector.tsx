import React, { useState } from 'react';
import { Card, Select, Input } from '@/components/ui';

export const ModelSelector = () => {
  const [config, setConfig] = useState({
    framework: 'pytorch',
    modelType: 'bert-base',
    customPath: ''
  });

  return (
    <Card className="p-4 space-y-4">
      <Select
        label="Framework"
        value={config.framework}
        options={[
          { value: 'pytorch', label: 'PyTorch' },
          { value: 'tensorflow', label: 'TensorFlow' },
          { value: 'sklearn', label: 'Scikit-learn' }
        ]}
        onChange={(value) => setConfig({...config, framework: value})}
      />
      <Select
        label="Model Type"
        value={config.modelType}
        options={[
          { value: 'bert-base', label: 'BERT Base' },
          { value: 'roberta-base', label: 'RoBERTa Base' }
        ]}
        onChange={(value) => setConfig({...config, modelType: value})}
      />
      <Input
        label="Custom Model Path"
        value={config.customPath}
        onChange={(e) => setConfig({...config, customPath: e.target.value})}
      />
    </Card>
  );
};
