import type { ListItem } from "./types";

export type DangerAction = "delete-list" | "reset-list" | { itemId: string } | null;

export type DangerCopy = {
  title: string;
  message: string;
  confirmLabel: string;
};

export const groupItemsByCategory = (items: ListItem[]): [string, ListItem[]][] => {
  const map = new Map<string, ListItem[]>();

  for (const item of items) {
    const existing = map.get(item.category) ?? [];
    existing.push(item);
    map.set(item.category, existing);
  }

  for (const categoryItems of map.values()) {
    categoryItems.sort((a, b) => a.sortIndex - b.sortIndex);
  }

  return Array.from(map.entries()).sort((a, b) => a[0].localeCompare(b[0]));
};

export const getDangerCopy = (dangerAction: DangerAction): DangerCopy => {
  if (dangerAction === "delete-list") {
    return {
      title: "Delete list",
      message: "This action permanently removes this list for you.",
      confirmLabel: "Delete list",
    };
  }

  if (dangerAction === "reset-list") {
    return {
      title: "Reset list",
      message: "All items will be reset and saved as latest snapshot.",
      confirmLabel: "Reset list",
    };
  }

  return {
    title: "Delete item",
    message: "This item will be removed from the active list.",
    confirmLabel: "Delete item",
  };
};
