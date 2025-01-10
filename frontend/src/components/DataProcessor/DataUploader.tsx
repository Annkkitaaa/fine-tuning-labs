import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card, Progress } from '@/components/ui';

export const DataUploader: React.FC = () => {
    const [uploadProgress, setUploadProgress] = useState(0);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/v1/upload', {
                method: 'POST',
                body: formData,
                onUploadProgress: (progressEvent) => {
                    const progress = (progressEvent.loaded / progressEvent.total) * 100;
                    setUploadProgress(progress);
                },
            });
            if (!response.ok) throw new Error('Upload failed');
        } catch (error) {
            console.error('Upload error:', error);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    return (
        <Card className="p-6">
            <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
                    ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
            >
                <input {...getInputProps()} />
                <p className="text-gray-600">
                    {isDragActive
                        ? "Drop the files here..."
                        : "Drag 'n' drop files here, or click to select files"}
                </p>
            </div>
            {uploadProgress > 0 && (
                <Progress value={uploadProgress} className="mt-4" />
            )}
        </Card>
    );
};