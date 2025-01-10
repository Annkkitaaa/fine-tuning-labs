import React, { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Switch } from '@/components/ui/Switch';

export const Preprocessing: React.FC = () => {
  const [settings, setSettings] = useState({
    removeStopwords: true,
    lowercase: true,
    stemming: false,
    removeSpecialChars: true
  });

  const handleSettingChange = (setting: keyof typeof settings) => {
    setSettings(prev => ({
      ...prev,
      [setting]: !prev[setting]
    }));
  };

  return (
    <Card>
      <h2 className="text-lg font-semibold mb-4">Preprocessing Settings</h2>
      <div className="space-y-4">
        <Switch
          checked={settings.removeStopwords}
          onChange={() => handleSettingChange('removeStopwords')}
          label="Remove Stopwords"
        />
        <Switch
          checked={settings.lowercase}
          onChange={() => handleSettingChange('lowercase')}
          label="Convert to Lowercase"
        />
        <Switch
          checked={settings.stemming}
          onChange={() => handleSettingChange('stemming')}
          label="Apply Stemming"
        />
        <Switch
          checked={settings.removeSpecialChars}
          onChange={() => handleSettingChange('removeSpecialChars')}
          label="Remove Special Characters"
        />
      </div>
    </Card>
  );
};