import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card, Progress } from '@/components/ui';

export const DataUploader = () => {
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach(file => {
      const data = new FormData();
      data.append('file', file);

      fetch('/api/v1/upload', {
        method: 'POST',
        body: data,
      }).then(response => response.json());
    });
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <Card className="p-6">
      <div {...getRootProps()} className="border-2 border-dashed rounded-lg p-4">
        <input {...getInputProps()} />
        <p className="text-center">Drop files here or click to select</p>
      </div>
      {uploadProgress > 0 && (
        <Progress value={uploadProgress} className="mt-4" />
      )}
    </Card>
  );
};