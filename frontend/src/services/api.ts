const API_BASE = process.env.REACT_APP_API_BASE || '/api/v1';

export const api = {
  async uploadModel(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE}/models/upload`, {
      method: 'POST',
      body: formData
    });
    return response.json();
  },

  async startTraining(config: any) {
    const response = await fetch(`${API_BASE}/training/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    });
    return response.json();
  },

  async getMetrics(jobId: string) {
    const response = await fetch(`${API_BASE}/metrics/${jobId}`);
    return response.json();
  }
};