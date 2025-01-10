import React, { useState } from 'react';
import { Card, Checkbox } from '@/components/ui';

interface PreprocessingOptions {
    normalize: boolean;
    removeOutliers: boolean;
    augmentData: boolean;
}

export const Preprocessing: React.FC = () => {
    const [options, setOptions] = useState<PreprocessingOptions>({
        normalize: false,
        removeOutliers: false,
        augmentData: false
    });

    const handleOptionChange = (key: keyof PreprocessingOptions) => {
        setOptions(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    return (
        <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Preprocessing Options</h2>
            <div className="space-y-4">
                <Checkbox
                    label="Normalize Data"
                    checked={options.normalize}
                    onChange={() => handleOptionChange('normalize')}
                />
                <Checkbox
                    label="Remove Outliers"
                    checked={options.removeOutliers}
                    onChange={() => handleOptionChange('removeOutliers')}
                />
                <Checkbox
                    label="Data Augmentation"
                    checked={options.augmentData}
                    onChange={() => handleOptionChange('augmentData')}
                />
            </div>
        </Card>
    );
};