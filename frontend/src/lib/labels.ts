import type { MillStatus } from './types';

export const millStatusLabel: Record<MillStatus, string> = {
  grinding: '研磨中',
  idle: '待机',
  wash: '清洗',
};
