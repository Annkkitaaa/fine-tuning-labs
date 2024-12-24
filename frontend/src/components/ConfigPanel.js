import React from 'react';

export const ConfigPanel = ({ config, onChange }) => {
  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Training Configuration</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Framework</label>
          <select
            value={config.framework}
            onChange={(e) => onChange({ ...config, framework: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          >
            <option value="pytorch">PyTorch</option>
            <option value="tensorflow">TensorFlow</option>
            <option value="sklearn">Scikit-learn</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Learning Rate</label>
          <input
            type="number"
            value={config.hyperparameters.learning_rate}
            onChange={(e) => onChange({
              ...config,
              hyperparameters: {
                ...config.hyperparameters,
                learning_rate: parseFloat(e.target.value)
              }
            })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
      </div>
    </div>
  );
};