export const formatters = {
  number(value: number, decimals = 2): string {
      return Number(value).toFixed(decimals);
  },

  percentage(value: number): string {
      return `${(value * 100).toFixed(1)}%`;
  },

  fileSize(bytes: number): string {
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      if (bytes === 0) return '0 Bytes';
      const i = Math.floor(Math.log(bytes) / Math.log(1024));
      return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
  },

  date(date: Date | string): string {
      return new Date(date).toLocaleString();
  },

  duration(seconds: number): string {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);
      return `${hours}h ${minutes}m ${secs}s`;
  }
};
