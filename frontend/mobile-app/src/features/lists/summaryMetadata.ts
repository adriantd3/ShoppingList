import type { ListSummary } from "./types";

export const getPurchasedProgressPercent = (summary: ListSummary): number => {
  if (summary.totalItems <= 0) {
    return 0;
  }

  return Math.round((summary.purchasedCount / summary.totalItems) * 100);
};

export const getPurchasedProgressLabel = (summary: ListSummary): string =>
  `${summary.purchasedCount}/${summary.totalItems}`;

export const getRelativeUpdatedLabel = (summary: ListSummary, now: Date = new Date()): string => {
  const updatedAt = new Date(summary.updatedAtIso);

  if (Number.isNaN(updatedAt.getTime())) {
    return "Updated recently";
  }

  const diffMs = Math.max(0, now.getTime() - updatedAt.getTime());
  const minuteMs = 60_000;
  const hourMs = 60 * minuteMs;
  const dayMs = 24 * hourMs;

  if (diffMs < hourMs) {
    const minutes = Math.max(1, Math.floor(diffMs / minuteMs));
    return `Updated ${minutes}m ago`;
  }

  if (diffMs < dayMs) {
    const hours = Math.floor(diffMs / hourMs);
    return `Updated ${hours}h ago`;
  }

  const days = Math.floor(diffMs / dayMs);
  return `Updated ${days}d ago`;
};
