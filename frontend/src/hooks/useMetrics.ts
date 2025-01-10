import { useState, useEffect } from 'react';
import { Metrics } from '../types';
import { api } from '../services/api';

export function useMetrics(modelId: string) {
    const [metrics, setMetrics] = useState<Metrics[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchMetrics = async () => {
        setLoading(true);
        try {
            const response = await api.getMetrics(modelId);
            setMetrics(response.data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch metrics');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (modelId) {
            fetchMetrics();
        }
    }, [modelId]);

    return { metrics, loading, error, refreshMetrics: fetchMetrics };
}