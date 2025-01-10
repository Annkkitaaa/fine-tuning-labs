import React, { useState } from 'react';
import { Card, Input, Button } from '@/components/ui';
import { TrainingConfig } from '@/types';

interface Props {
    onSubmit: (config: TrainingConfig) => void;
    defaultConfig?: TrainingConfig;
}

export const ConfigForm: React.FC<Props> = ({ onSubmit, defaultConfig }) => {
    const [config, setConfig] = useState<TrainingConfig>(defaultConfig || {
        epochs: 10,
        batchSize: 32,
        learningRate: 0.001
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(config);
    };

    return (
        <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Training Configuration</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                    label="Epochs"
                    type="number"
                    value={config.epochs}
                    onChange={(e) => setConfig(prev => ({
                        ...prev,
                        epochs: parseInt(e.target.value)
                    }))}
                    min={1}
                />
                <Input
                    label="Batch Size"
                    type="number"
                    value={config.batchSize}
                    onChange={(e) => setConfig(prev => ({
                        ...prev,
                        batchSize: parseInt(e.target.value)
                    }))}
                    min={1}
                />
                <Input
                    label="Learning Rate"
                    type="number"
                    value={config.learningRate}
                    onChange={(e) => setConfig(prev => ({
                        ...prev,
                        learningRate: parseFloat(e.target.value)
                    }))}
                    step="0.0001"
                />
                <Button type="submit" className="w-full">
                    Apply Configuration
                </Button>
            </form>
        </Card>
    );
};