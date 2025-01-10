import { useState, useEffect } from 'react';
import { TrainingStatus } from '../types';
import { api } from '../services/api';

export function useTraining(jobId: string) {
    const [status, setStatus] = useState<TrainingStatus>({
        status: 'idle',
        progress: 0
    });

    useEffect(() => {
        if (!jobId) return;

        const pollInterval = setInterval(async () => {
            try {
                const response = await api.getTrainingStatus(jobId);
                setStatus(response.data);
                
                if (['completed', 'failed'].includes(response.data.status)) {
                    clearInterval(pollInterval);
                }
            } catch (error) {
                console.error('Error fetching training status:', error);
            }
        }, 1000);

        return () => clearInterval(pollInterval);
    }, [jobId]);

    return status;
}