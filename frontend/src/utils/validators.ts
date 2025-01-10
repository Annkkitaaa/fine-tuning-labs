export const validators = {
    isValidModelConfig(config: any): boolean {
        return (
            config &&
            typeof config.framework === 'string' &&
            typeof config.modelType === 'string'
        );
    },

    isValidTrainingConfig(config: any): boolean {
        return (
            config &&
            typeof config.epochs === 'number' &&
            typeof config.batchSize === 'number' &&
            typeof config.learningRate === 'number' &&
            config.epochs > 0 &&
            config.batchSize > 0 &&
            config.learningRate > 0
        );
    },

    isValidFileType(file: File, allowedTypes: string[]): boolean {
        return allowedTypes.includes(file.type);
    },

    isValidFileSize(file: File, maxSizeInBytes: number): boolean {
        return file.size <= maxSizeInBytes;
    },

    isValidEmail(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    isStrongPassword(password: string): boolean {
        return (
            password.length >= 8 &&
            /[A-Z]/.test(password) &&
            /[a-z]/.test(password) &&
            /[0-9]/.test(password) &&
            /[^A-Za-z0-9]/.test(password)
        );
    }
};