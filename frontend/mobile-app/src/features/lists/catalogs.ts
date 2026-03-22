export const ITEM_UNITS = ["pcs", "kg", "g", "L", "ml", "pack"] as const;

export const ITEM_CATEGORIES = [
  "Produce",
  "Dairy",
  "Bakery",
  "Meat",
  "Frozen",
  "Household",
  "Other",
] as const;

export type ItemUnit = (typeof ITEM_UNITS)[number];
export type ItemCategory = (typeof ITEM_CATEGORIES)[number];
