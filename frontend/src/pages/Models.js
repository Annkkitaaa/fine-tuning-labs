import React, { useState, useEffect } from 'react';
import { getModels } from '../utils/api';

export const Models = () => {
  const [models, setModels] = useState([]);

  useEffect(() => {
    const fetchModels = async () => {
      const data = await getModels();
      setModels(data.models);
    };
    fetchModels();
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Model Repository</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {models.map(model => (
          <div key={model.id} className="p-6 bg-white rounded-lg shadow">
            <h3 className="font-semibold">{model.name}</h3>
            <p className="text-gray-600">Framework: {model.framework}</p>
          </div>
        ))}
      </div>
    </div>
  );
};