import { ElementId } from 'react-flow-renderer';

export type Onu = {
  id: ElementId;
  displayName: string;
  macAddress: string;
  ipAddress: string;
  uptime: string;
  model: string;
  status: string;
  rxPower: number;
  profile: string;
  serialNumber: string;
  distance: number;
  gponPort: number;
};
