import axios from 'axios';
import { ModelConfig, TrainingConfig } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add auth interceptor
axiosInstance.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const api = {
    // Model endpoints
    async uploadModel(file: File, config: Partial<ModelConfig>) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('config', JSON.stringify(config));
        return axiosInstance.post('/models/upload', formData);
    },

    async updateModelConfig(config: ModelConfig) {
        return axiosInstance.put('/models/config', config);
    },

    // Training endpoints
    async startTraining(config: TrainingConfig) {
        return axiosInstance.post('/training/start', config);
    },

    async getTrainingStatus(jobId: string) {
        return axiosInstance.get(`/training/status/${jobId}`);
    },

    async stopTraining(jobId: string) {
        return axiosInstance.post(`/training/stop/${jobId}`);
    },

    // Metrics endpoints
    async getMetrics(modelId: string) {
        return axiosInstance.get(`/metrics/${modelId}`);
    },
};