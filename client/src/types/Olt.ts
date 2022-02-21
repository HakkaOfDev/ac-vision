import { ElementId } from 'react-flow-renderer';

export type Olt = {
  id: ElementId;
  displayName: string;
  macAddress: string;
  ipAddress: string;
  uptime: string;
  temperature: number;
  model: string;
  status: string;
};
