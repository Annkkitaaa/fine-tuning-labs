// src/types/index.ts

// Model Configuration Types
export interface ModelConfig {
    framework: 'pytorch' | 'tensorflow' | 'sklearn';
    modelType: string;
  }

// Training Configuration Types
export interface TrainingConfig {
    epochs: number;
    batchSize: number;
    learningRate: number;
}

// Metrics and Training Status Types
export interface Metrics {
    epoch: number;
    loss: number;
    accuracy: number;
    [key: string]: number;
}

export interface TrainingStatus {
    status: 'idle' | 'running' | 'completed' | 'failed';
    progress: number;
    currentEpoch?: number;
    metrics?: Metrics;
}

// File Upload Types
export interface FileUploadResponse {
    success: boolean;
    filename: string;
    error?: string;
}

// API Response Types
export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
}

// Hyperparameter Types
export interface HyperparameterConfig {
    name: string;
    type: 'number' | 'categorical' | 'boolean';
    range?: [number, number];
    options?: string[] | number[];
    default?: any;
}

// Model Evaluation Types
export interface EvaluationMetrics {
    accuracy: number;
    precision: number;
    recall: number;
    f1Score: number;
    confusionMatrix?: number[][];
}

// Component Props Types
export interface DataUploaderProps {
    onUploadComplete?: (response: FileUploadResponse) => void;
    acceptedFileTypes?: string[];
    maxFileSize?: number;
}

export interface ModelSelectorProps {
    onModelSelect: (config: ModelConfig) => void;
    availableFrameworks?: string[];
}

export interface TrainingPanelProps {
    modelConfig: ModelConfig;
    onTrainingStart: (config: TrainingConfig) => void;
    onTrainingComplete?: (metrics: Metrics) => void;
}

export interface MetricsDisplayProps {
    metrics: Metrics[];
    showChart?: boolean;
}

// UI Component Types
export interface CardProps {
    className?: string;
    children: React.ReactNode;
}

export interface ProgressProps {
    value: number;
    className?: string;
    showLabel?: boolean;
}

export interface ButtonProps {
    onClick?: () => void;
    disabled?: boolean;
    variant?: 'primary' | 'secondary' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    className?: string;
    children: React.ReactNode;
}

// Error Types
export interface ValidationError {
    field: string;
    message: string;
}

export type ApiError = {
    code: string;
    message: string;
    details?: ValidationError[];
}

// Utility Types
export type Framework = 'pytorch' | 'tensorflow' | 'sklearn';
export type TrainingPhase = 'preprocessing' | 'training' | 'evaluation';
export type ModelType = 'classification' | 'regression' | 'clustering';

// State Management Types
export interface AppState {
    modelConfig: ModelConfig | null;
    trainingConfig: TrainingConfig | null;
    trainingStatus: TrainingStatus;
    currentMetrics: Metrics[];
}

export type AppAction = 
    | { type: 'SET_MODEL_CONFIG'; payload: ModelConfig }
    | { type: 'SET_TRAINING_CONFIG'; payload: TrainingConfig }
    | { type: 'UPDATE_TRAINING_STATUS'; payload: TrainingStatus }
    | { type: 'ADD_METRICS'; payload: Metrics };