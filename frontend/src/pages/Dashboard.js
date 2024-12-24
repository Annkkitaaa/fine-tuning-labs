// frontend/src/pages/Dashboard.js
import React, { useState, useEffect } from 'react';
import { ModelUpload } from '../components/ModelUpload';
import { ConfigPanel } from '../components/ConfigPanel';
import { TrainingProgress } from '../components/TrainingProgress';
import { AdvancedTraining } from '../components/AdvancedTraining'; 
import { getModels, startTraining } from '../utils/api';

export const Dashboard = () => {
 const [models, setModels] = useState([]);
 const [selectedModel, setSelectedModel] = useState(null);
 const [config, setConfig] = useState({
   framework: 'pytorch',
   hyperparameters: {
     learning_rate: 0.001,
     batch_size: 32,
     epochs: 10
   }
 });
 const [training, setTraining] = useState(null);

 useEffect(() => {
   const fetchModels = async () => {
     try {
       const data = await getModels();
       setModels(data.models);
     } catch (error) {
       console.error('Failed to fetch models:', error);
     }
   };
   fetchModels();
 }, []);

 const handleModelSelect = (model) => {
   setSelectedModel(model);
 };

 const handleStartTraining = async () => {
   if (!selectedModel) return;
   try {
     const response = await startTraining({
       model_id: selectedModel.id,
       ...config
     });
     setTraining(response);
   } catch (error) {
     console.error('Training failed:', error);
   }
 };

 return (
   <div className="min-h-screen bg-gray-50">
     <nav className="bg-white shadow">
       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
         <div className="flex justify-between h-16">
           <h1 className="flex items-center text-2xl font-bold">Fine-Tuning Labs</h1>
         </div>
       </div>
     </nav>

     <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
       <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
         <div className="space-y-6">
           <ModelUpload onUploadComplete={handleModelSelect} />
           <ConfigPanel 
             config={config} 
             onChange={setConfig}
             selectedModel={selectedModel}
           />
         </div>
         
         <div className="space-y-6">
           <AdvancedTraining 
             config={config}
             onChange={setConfig}
           />
           
           <div className="p-6 bg-white rounded-lg shadow">
             <button
               onClick={handleStartTraining}
               disabled={!selectedModel}
               className="w-full bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:opacity-50"
             >
               Start Training
             </button>
           </div>

           {training && (
             <TrainingProgress 
               trainingId={training.training_id}
               history={training.history}
             />
           )}
         </div>
       </div>

       <div className="mt-6">
         <h2 className="text-xl font-semibold mb-4">Available Models</h2>
         <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
           {models.map(model => (
             <div
               key={model.id}
               className={`p-4 border rounded-lg cursor-pointer ${
                 selectedModel?.id === model.id ? 'border-blue-500' : ''
               }`}
               onClick={() => handleModelSelect(model)}
             >
               <h3 className="font-semibold">{model.name}</h3>
               <p className="text-sm text-gray-600">Framework: {model.framework}</p>
             </div>
           ))}
         </div>
       </div>
     </main>
   </div>
 );
};

export default Dashboard;