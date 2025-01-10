import React, { useState } from 'react';
import { Card, Button } from '@/components/ui';
import { ProgressMonitor } from './ProgressMonitor';
import { TrainingConfig } from '@/types';

interface Props {
    onStart: (config: TrainingConfig) => void;
    onStop: () => void;
    isTraining: boolean;
}

export const TrainingPanel: React.FC<Props> = ({ onStart, onStop, isTraining }) => {
    const [config, setConfig] = useState<TrainingConfig>({
        epochs: 10,
        batchSize: 32,
        learningRate: 0.001
    });

    return (
        <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Training Control</h2>
            <div className="space-y-4">
                {isTraining ? (
                    <>
                        <ProgressMonitor />
                        <Button onClick={onStop} variant="danger">
                            Stop Training
                        </Button>
                    </>
                ) : (
                    <Button onClick={() => onStart(config)} variant="primary">
                        Start Training
                    </Button>
                )}
            </div>
        </Card>
    );
};