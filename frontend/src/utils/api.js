const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000/api';

export const uploadModel = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE}/models/upload`, {
    method: 'POST',
    body: formData
  });
  
  if (!response.ok) throw new Error('Upload failed');
  return response.json();
};

export const getModels = async () => {
  const response = await fetch(`${API_BASE}/models/list`);
  if (!response.ok) throw new Error('Failed to fetch models');
  return response.json();
};

export const startTraining = async (config) => {
  const response = await fetch(`${API_BASE}/training/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config)
  });
  
  if (!response.ok) throw new Error('Training failed to start');
  return response.json();
};
