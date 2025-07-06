export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR'
}

export interface LogEntry {
  timestamp: number;
  level: LogLevel;
  message: string;
  data?: any;
  context?: string;
}

export class Logger {
  private context: string;
  private minLevel: LogLevel;
  private entries: LogEntry[];
  private maxEntries: number;

  constructor(context: string, minLevel: LogLevel = LogLevel.INFO, maxEntries: number = 1000) {
    this.context = context;
    this.minLevel = minLevel;
    this.maxEntries = maxEntries;
    this.entries = [];
  }

  private log(level: LogLevel, message: string, data?: any): void {
    if (this.shouldLog(level)) {
      const entry: LogEntry = {
        timestamp: Date.now(),
        level,
        message,
        data,
        context: this.context
      };

      this.entries.push(entry);
      
      // Trim old entries if exceeding maxEntries
      if (this.entries.length > this.maxEntries) {
        this.entries = this.entries.slice(-this.maxEntries);
      }

      // Console output with timestamp and context
      const timestamp = new Date(entry.timestamp).toISOString();
      const formattedMessage = `[${timestamp}] [${level}] [${this.context}] ${message}`;
      
      switch (level) {
        case LogLevel.ERROR:
          console.error(formattedMessage, data || '');
          break;
        case LogLevel.WARN:
          console.warn(formattedMessage, data || '');
          break;
        case LogLevel.INFO:
          console.info(formattedMessage, data || '');
          break;
        case LogLevel.DEBUG:
          console.debug(formattedMessage, data || '');
          break;
      }
    }
  }

  private shouldLog(level: LogLevel): boolean {
    const levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARN, LogLevel.ERROR];
    return levels.indexOf(level) >= levels.indexOf(this.minLevel);
  }

  debug(message: string, data?: any): void {
    this.log(LogLevel.DEBUG, message, data);
  }

  info(message: string, data?: any): void {
    this.log(LogLevel.INFO, message, data);
  }

  warn(message: string, data?: any): void {
    this.log(LogLevel.WARN, message, data);
  }

  error(message: string, data?: any): void {
    this.log(LogLevel.ERROR, message, data);
  }

  getEntries(level?: LogLevel, limit?: number): LogEntry[] {
    let filtered = this.entries;
    
    if (level) {
      filtered = filtered.filter(entry => entry.level === level);
    }
    
    if (limit) {
      filtered = filtered.slice(-limit);
    }
    
    return filtered;
  }

  clearEntries(): void {
    this.entries = [];
  }

  setMinLevel(level: LogLevel): void {
    this.minLevel = level;
  }

  getContext(): string {
    return this.context;
  }
} 