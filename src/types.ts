export interface ModelConfig {
  id: string;
  name: string;
  active: boolean;
  version: string;
  status: 'online' | 'offline' | 'degraded';
  health: number;
  tags: string[];
}

export interface SecurityFinding {
  type: string;
  status: string;
  findings: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  details: string[];
}

export interface ScanResult {
  status: string;
  timestamp: string;
  results: SecurityFinding[];
}

export interface TerminalMessage {
  id: string;
  user: string;
  content: string;
  type: 'input' | 'output' | 'error' | 'system';
  timestamp: string;
}

export interface TrainingMetric {
  epoch: number;
  accuracy: number;
  loss: number;
}
