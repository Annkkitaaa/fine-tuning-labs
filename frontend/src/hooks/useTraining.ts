import { useState, useEffect } from 'react';
import { TrainingStatus } from '../types';

export const useTraining = (jobId: string) => {
  const [status, setStatus] = useState<TrainingStatus>({
    status: 'idle',
    progress: 0
  });

  useEffect(() => {
    const interval = setInterval(async () => {
      const response = await fetch(`/api/v1/training/status/${jobId}`);
      const data = await response.json();
      setStatus(data);
      
      if (data.status === 'completed' || data.status === 'failed') {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [jobId]);

  return status;
};
