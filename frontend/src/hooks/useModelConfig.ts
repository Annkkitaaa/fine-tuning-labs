import { useState } from 'react';
import { ModelConfig } from '../types';
import { api } from '../services/api';

export function useModelConfig() {
    const [config, setConfig] = useState<ModelConfig>({
        framework: 'pytorch',
        modelType: 'bert-base'
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const updateConfig = async (newConfig: Partial<ModelConfig>) => {
        setLoading(true);
        setError(null);
        
        try {
            const updatedConfig = { ...config, ...newConfig };
            await api.updateModelConfig(updatedConfig);
            setConfig(updatedConfig);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to update config');
        } finally {
            setLoading(false);
        }
    };

    return { config, updateConfig, loading, error };
}