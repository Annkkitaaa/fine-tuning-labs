import React from 'react';
import { Card, Select } from '@/components/ui';
import { ModelConfig } from '@/types';

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

    const models = {
        pytorch: ['bert-base', 'roberta-base'],
        tensorflow: ['bert-base-tf', 'distilbert-tf'],
        sklearn: ['random-forest', 'svm']
    };

    return (
        <Card className="p-6 space-y-4">
            <h2 className="text-xl font-semibold">Model Selection</h2>
            <Select
                label="Framework"
                options={frameworks}
                value={currentConfig?.framework || 'pytorch'}
                onChange={(value) => onSelect({ 
                    ...currentConfig,
                    framework: value as ModelConfig['framework'],
                    modelType: ''
                })}
            />
            <Select
                label="Model Type"
                options={models[currentConfig?.framework || 'pytorch'].map(m => ({ value: m, label: m }))}
                value={currentConfig?.modelType || ''}
                onChange={(value) => onSelect({
                    ...currentConfig,
                    modelType: value
                })}
            />
        </Card>
    );
};