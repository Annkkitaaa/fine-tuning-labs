export interface ModelConfig {
    framework: 'pytorch' | 'tensorflow' | 'sklearn';
    modelType: string;
    customPath?: string;
  }
  
  export interface TrainingConfig {
    epochs: number;
    batchSize: number;
    learningRate: number;
  }
  
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