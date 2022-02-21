import { Olt } from '@/types/Olt';
import { Onu } from '@/types/Onu';
import { CustomEdge } from './CustomEdge';

export type Map = {
  olts: Olt[];
  onus: Onu[];
  edges: CustomEdge[];
};
