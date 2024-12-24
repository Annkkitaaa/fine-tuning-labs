import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { Models } from './pages/Models';
import { Training } from './pages/Training';
import Navigation from './components/Navigation';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/models" element={<Models />} />
        <Route path="/training" element={<Training />} />
      </Routes>
    </div>
  );
};

export default App;