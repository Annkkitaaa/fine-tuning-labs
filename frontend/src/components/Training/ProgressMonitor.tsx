import React from 'react';
import { Progress } from '@/components/ui';
import { useTraining } from '@/hooks/useTraining';

interface Props {
    jobId?: string;
}

export const ProgressMonitor: React.FC<Props> = ({ jobId }) => {
    const status = useTraining(jobId || '');

    return (
        <div className="space-y-4">
            <div className="flex justify-between text-sm text-gray-600">
                <span>Progress: {status.progress.toFixed(1)}%</span>
                <span>Status: {status.status}</span>
            </div>
            <Progress value={status.progress} />
            {status.metrics && (
                <div className="grid grid-cols-2 gap-4 mt-4">
                    <div>Loss: {status.metrics.loss.toFixed(4)}</div>
                    <div>Accuracy: {status.metrics.accuracy.toFixed(4)}</div>
                </div>
            )}
        </div>
    );
};