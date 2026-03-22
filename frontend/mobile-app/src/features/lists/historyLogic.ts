export const formatRestoreFeedback = (snapshotId: string, restoredItemsCount: number): string =>
  `Restored snapshot ${snapshotId} with ${restoredItemsCount} items.`;
