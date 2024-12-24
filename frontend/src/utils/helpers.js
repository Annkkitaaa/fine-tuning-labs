export const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
  };
  
  export const validateConfig = (config) => {
    const errors = {};
    if (!config.framework) errors.framework = 'Framework is required';
    if (!config.hyperparameters?.learning_rate) errors.learning_rate = 'Learning rate is required';
    return errors;
  };