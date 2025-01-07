import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card, Progress } from '@/components/ui';

export const DataUploader: React.FC = () => {
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setError(null);
    
    for (const file of acceptedFiles) {
      try {
        const data = new FormData();
        data.append('file', file);

        const response = await fetch('/api/v1/upload', {
          method: 'POST',
          body: data,
          headers: {
            // Don't set Content-Type header as it's automatically set with boundary for FormData
          },
          // Add upload progress tracking
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const progress = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              setUploadProgress(progress);
            }
          },
        });

        if (!response.ok) {
          throw new Error(`Upload failed: ${response.statusText}`);
        }

        const result = await response.json();
        setUploadProgress(100);
        
        // Reset progress after a delay
        setTimeout(() => setUploadProgress(0), 1000);

      } catch (err) {
        setError(err instanceof Error ? err.message : 'Upload failed');
        setUploadProgress(0);
      }
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/json': ['.json'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    multiple: false // Allow only single file upload
  });

  return (
    <Card className="p-6">
      <div 
        {...getRootProps()} 
        className={`
          border-2 border-dashed rounded-lg p-4 cursor-pointer
          transition-colors duration-200
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
        `}
      >
        <input {...getInputProps()} />
        <p className="text-center">
          {isDragActive 
            ? 'Drop the file here...' 
            : 'Drop a file here or click to select'}
        </p>
      </div>
      
      {uploadProgress > 0 && (
        <div className="mt-4">
          <Progress 
            value={uploadProgress} 
            className="w-full"
          />
          <p className="text-sm text-gray-600 mt-1">
            Uploading: {uploadProgress}%
          </p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}
    </Card>
  );
};